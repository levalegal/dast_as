"""
Виджет планировщика технического обслуживания
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QGroupBox,
                             QDateEdit, QHeaderView, QMessageBox, QSpinBox, QComboBox)
from PyQt6.QtCore import Qt, QDate
from database import Database
from datetime import datetime, timedelta
from decimal import Decimal


class MaintenanceSchedulerWidget(QWidget):
    """Виджет для планирования и отслеживания предстоящего ТО"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Группа настроек
        settings_group = QGroupBox("Настройки напоминаний")
        settings_layout = QVBoxLayout()
        
        # Первая строка настроек
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Показывать обслуживания за:"))
        self.days_spinbox = QSpinBox()
        self.days_spinbox.setMinimum(1)
        self.days_spinbox.setMaximum(365)
        self.days_spinbox.setValue(30)
        self.days_spinbox.setSuffix(" дней")
        self.days_spinbox.valueChanged.connect(self.refresh_data)
        row1.addWidget(self.days_spinbox)
        
        row1.addWidget(QLabel("Интервал ТО по умолчанию:"))
        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setMinimum(1)
        self.interval_spinbox.setMaximum(365)
        self.interval_spinbox.setValue(90)
        self.interval_spinbox.setSuffix(" дней")
        self.interval_spinbox.valueChanged.connect(self.refresh_data)
        row1.addWidget(self.interval_spinbox)
        
        row1.addStretch()
        settings_layout.addLayout(row1)
        
        # Вторая строка - фильтр по категории
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Категория:"))
        self.category_filter = QComboBox()
        self.category_filter.addItem("Все категории", None)
        self.category_filter.currentIndexChanged.connect(self.refresh_data)
        row2.addWidget(self.category_filter)
        
        row2.addStretch()
        settings_layout.addLayout(row2)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.refresh_data)
        buttons_layout.addWidget(self.refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Таблица предстоящего обслуживания
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Оборудование", "Последнее ТО", "Дней назад", "Тип", "Следующее ТО", "Статус"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
    
    def refresh_data(self):
        """Обновить данные о предстоящем обслуживании"""
        days_ahead = self.days_spinbox.value()
        default_interval = self.interval_spinbox.value()
        today = datetime.now().date()
        end_date = today + timedelta(days=days_ahead)
        
        # Обновляем список категорий
        equipment_list = self.db.get_all_equipment()
        categories = set()
        for eq in equipment_list:
            if eq.get('category'):
                categories.add(eq['category'])
        
        current_category = self.category_filter.currentData()
        self.category_filter.clear()
        self.category_filter.addItem("Все категории", None)
        for cat in sorted(categories):
            self.category_filter.addItem(cat, cat)
        
        # Восстанавливаем выбор
        if current_category:
            for i in range(self.category_filter.count()):
                if self.category_filter.itemData(i) == current_category:
                    self.category_filter.setCurrentIndex(i)
                    break
        
        selected_category = self.category_filter.currentData()
        upcoming_maintenance = []
        
        # Интервалы ТО по категориям (можно расширить)
        category_intervals = {
            'Компьютерная техника': 180,
            'Офисная мебель': 365,
            'Оргтехника': 90,
            'Производственное оборудование': 30,
            'Транспорт': 60
        }
        
        for eq in equipment_list:
            # Фильтр по категории
            if selected_category and eq.get('category') != selected_category:
                continue
            # Получаем последнее обслуживание
            maintenance_list = self.db.get_maintenance_by_equipment(eq['id'])
            
            if maintenance_list:
                # Берем последнее обслуживание
                last_maintenance = maintenance_list[0]  # Уже отсортировано по дате DESC
                last_date_str = last_maintenance['maintenance_date']
                
                try:
                    last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
                    days_since = (today - last_date).days
                    
                    # Определяем интервал ТО для категории
                    category = eq.get('category', '')
                    interval = category_intervals.get(category, default_interval)
                    
                    # Следующее ТО через интервал после последнего
                    next_maintenance_date = last_date + timedelta(days=interval)
                    
                    # Проверяем, попадает ли в диапазон
                    if next_maintenance_date <= end_date:
                        status = "Требуется ТО" if next_maintenance_date <= today else "Запланировано"
                        upcoming_maintenance.append({
                            'equipment': eq,
                            'last_maintenance': last_maintenance,
                            'last_date': last_date,
                            'days_since': days_since,
                            'next_date': next_maintenance_date,
                            'status': status
                        })
                except:
                    pass
            else:
                # Если обслуживания не было, считаем что нужно провести первое
                purchase_date_str = eq.get('purchase_date')
                if purchase_date_str:
                    try:
                        purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date()
                        days_since = (today - purchase_date).days
                        
                        # Определяем интервал для категории
                        category = eq.get('category', '')
                        interval = category_intervals.get(category, default_interval)
                        
                        # Если прошло больше интервала с покупки, требуется первое ТО
                        if days_since >= interval:
                            upcoming_maintenance.append({
                                'equipment': eq,
                                'last_maintenance': None,
                                'last_date': None,
                                'days_since': days_since,
                                'next_date': today,
                                'status': "Требуется первое ТО"
                            })
                    except:
                        pass
        
        # Сортируем по дате следующего ТО
        upcoming_maintenance.sort(key=lambda x: x['next_date'])
        
        self.table.setRowCount(len(upcoming_maintenance))
        
        for row, item in enumerate(upcoming_maintenance):
            eq = item['equipment']
            equipment_text = f"{eq['inventory_number']} - {eq['name']}"
            self.table.setItem(row, 0, QTableWidgetItem(equipment_text))
            
            if item['last_maintenance']:
                self.table.setItem(row, 1, QTableWidgetItem(item['last_maintenance']['maintenance_date']))
                self.table.setItem(row, 2, QTableWidgetItem(str(item['days_since'])))
                self.table.setItem(row, 3, QTableWidgetItem(item['last_maintenance']['type']))
            else:
                self.table.setItem(row, 1, QTableWidgetItem("Не проводилось"))
                self.table.setItem(row, 2, QTableWidgetItem(str(item['days_since'])))
                self.table.setItem(row, 3, QTableWidgetItem("-"))
            
            next_date_text = item['next_date'].strftime('%Y-%m-%d')
            self.table.setItem(row, 4, QTableWidgetItem(next_date_text))
            
            status_item = QTableWidgetItem(item['status'])
            if "Требуется" in item['status']:
                status_item.setForeground(Qt.GlobalColor.red)
            else:
                status_item.setForeground(Qt.GlobalColor.blue)
            self.table.setItem(row, 5, status_item)
