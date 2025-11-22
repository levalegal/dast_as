"""
Виджет для генерации отчетов
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QGroupBox,
                             QDateEdit, QHeaderView, QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt, QDate
from database import Database
from decimal import Decimal
from utils.export import ExportManager


class ReportsWidget(QWidget):
    """Виджет для генерации отчетов"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Вкладки для разных отчетов
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Вкладка "Амортизация"
        depreciation_widget = QWidget()
        depreciation_layout = QVBoxLayout()
        depreciation_widget.setLayout(depreciation_layout)
        
        buttons_layout = QHBoxLayout()
        self.depreciation_refresh_btn = QPushButton("🔄 Обновить отчет")
        self.depreciation_refresh_btn.setProperty("class", "secondary-button")
        self.depreciation_refresh_btn.clicked.connect(self.refresh_depreciation)
        buttons_layout.addWidget(self.depreciation_refresh_btn)
        
        self.depreciation_export_btn = QPushButton("📤 Экспорт в CSV")
        self.depreciation_export_btn.setProperty("class", "secondary-button")
        self.depreciation_export_btn.clicked.connect(self.export_depreciation)
        buttons_layout.addWidget(self.depreciation_export_btn)
        
        buttons_layout.addStretch()
        depreciation_layout.addLayout(buttons_layout)
        
        self.depreciation_table = QTableWidget()
        self.depreciation_table.setColumnCount(8)
        self.depreciation_table.setHorizontalHeaderLabels([
            "ID", "Инвентарный номер", "Наименование", "Категория",
            "Дата покупки", "Цена покупки", "Дней в эксплуатации", "Стоимость ТО"
        ])
        self.depreciation_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.depreciation_table.setAlternatingRowColors(True)
        self.depreciation_table.setSortingEnabled(True)
        depreciation_layout.addWidget(self.depreciation_table)
        
        self.tabs.addTab(depreciation_widget, "Амортизация")
        
        # Вкладка "Стоимость содержания"
        maintenance_cost_widget = QWidget()
        maintenance_cost_layout = QVBoxLayout()
        maintenance_cost_widget.setLayout(maintenance_cost_layout)
        
        # Фильтры по датам
        filter_group = QGroupBox("Период")
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("С:"))
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        filter_layout.addWidget(self.start_date_edit)
        
        filter_layout.addWidget(QLabel("По:"))
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate.currentDate())
        filter_layout.addWidget(self.end_date_edit)
        
        self.cost_refresh_btn = QPushButton("🔄 Обновить")
        self.cost_refresh_btn.setProperty("class", "secondary-button")
        self.cost_refresh_btn.clicked.connect(self.refresh_maintenance_cost)
        filter_layout.addWidget(self.cost_refresh_btn)
        
        self.cost_export_btn = QPushButton("📤 Экспорт")
        self.cost_export_btn.setProperty("class", "secondary-button")
        self.cost_export_btn.clicked.connect(self.export_maintenance_cost)
        filter_layout.addWidget(self.cost_export_btn)
        
        filter_group.setLayout(filter_layout)
        maintenance_cost_layout.addWidget(filter_group)
        
        # Сводная информация
        summary_group = QGroupBox("Сводная информация")
        summary_layout = QVBoxLayout()
        self.summary_label = QLabel()
        self.summary_label.setProperty("class", "stat-label")
        self.summary_label.setStyleSheet("font-size: 14px; font-weight: 600; padding: 8px; color: #2196F3;")
        summary_layout.addWidget(self.summary_label)
        summary_group.setLayout(summary_layout)
        maintenance_cost_layout.addWidget(summary_group)
        
        self.maintenance_cost_table = QTableWidget()
        self.maintenance_cost_table.setColumnCount(6)
        self.maintenance_cost_table.setHorizontalHeaderLabels([
            "ID", "Оборудование", "Дата", "Тип", "Стоимость", "Описание"
        ])
        self.maintenance_cost_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.maintenance_cost_table.setAlternatingRowColors(True)
        self.maintenance_cost_table.setSortingEnabled(True)
        maintenance_cost_layout.addWidget(self.maintenance_cost_table)
        
        self.tabs.addTab(maintenance_cost_widget, "Стоимость содержания")
        
        # Вкладка "Отчет по ТО"
        maintenance_report_widget = QWidget()
        maintenance_report_layout = QVBoxLayout()
        maintenance_report_widget.setLayout(maintenance_report_layout)
        
        # Фильтры
        report_filter_group = QGroupBox("Период")
        report_filter_layout = QHBoxLayout()
        
        report_filter_layout.addWidget(QLabel("С:"))
        self.report_start_date_edit = QDateEdit()
        self.report_start_date_edit.setCalendarPopup(True)
        self.report_start_date_edit.setDate(QDate.currentDate().addMonths(-1))
        report_filter_layout.addWidget(self.report_start_date_edit)
        
        report_filter_layout.addWidget(QLabel("По:"))
        self.report_end_date_edit = QDateEdit()
        self.report_end_date_edit.setCalendarPopup(True)
        self.report_end_date_edit.setDate(QDate.currentDate())
        report_filter_layout.addWidget(self.report_end_date_edit)
        
        self.maintenance_report_refresh_btn = QPushButton("📊 Сформировать отчет")
        self.maintenance_report_refresh_btn.setProperty("class", "action-button")
        self.maintenance_report_refresh_btn.clicked.connect(self.refresh_maintenance_report)
        report_filter_layout.addWidget(self.maintenance_report_refresh_btn)
        
        self.maintenance_report_export_btn = QPushButton("📤 Экспорт в CSV")
        self.maintenance_report_export_btn.setProperty("class", "secondary-button")
        self.maintenance_report_export_btn.clicked.connect(self.export_maintenance_report)
        report_filter_layout.addWidget(self.maintenance_report_export_btn)
        
        report_filter_group.setLayout(report_filter_layout)
        maintenance_report_layout.addWidget(report_filter_group)
        
        self.maintenance_report_table = QTableWidget()
        self.maintenance_report_table.setColumnCount(6)
        self.maintenance_report_table.setHorizontalHeaderLabels([
            "ID", "Оборудование", "Дата", "Тип", "Стоимость", "Описание"
        ])
        self.maintenance_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.maintenance_report_table.setAlternatingRowColors(True)
        self.maintenance_report_table.setSortingEnabled(True)
        maintenance_report_layout.addWidget(self.maintenance_report_table)
        
        self.tabs.addTab(maintenance_report_widget, "Отчет по ТО")
    
    def refresh_data(self):
        """Обновить все отчеты"""
        self.refresh_depreciation()
        self.refresh_maintenance_cost()
        self.refresh_maintenance_report()
    
    def refresh_depreciation(self):
        """Обновить отчет по амортизации"""
        report_data = self.db.get_depreciation_report()
        self.depreciation_table.setRowCount(len(report_data))
        
        for row, item in enumerate(report_data):
            self.depreciation_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            self.depreciation_table.setItem(row, 1, QTableWidgetItem(item['inventory_number']))
            self.depreciation_table.setItem(row, 2, QTableWidgetItem(item['name']))
            self.depreciation_table.setItem(row, 3, QTableWidgetItem(item['category'] or ''))
            self.depreciation_table.setItem(row, 4, QTableWidgetItem(item['purchase_date'] or ''))
            # Форматирование цены покупки
            price = item['purchase_price'] or '0'
            try:
                price_decimal = Decimal(str(price))
                price_text = f"{price_decimal:,.2f} ₽".replace(',', ' ')
            except:
                price_text = f"{price} ₽" if price != '0' else "0.00 ₽"
            price_item = QTableWidgetItem(price_text)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.depreciation_table.setItem(row, 5, price_item)
            
            days = item.get('days_in_use', 0) or 0
            self.depreciation_table.setItem(row, 6, QTableWidgetItem(str(days)))
            
            # Форматирование стоимости ТО
            maintenance_cost = item.get('total_maintenance_cost', '0') or '0'
            try:
                cost_decimal = Decimal(str(maintenance_cost))
                cost_text = f"{cost_decimal:,.2f} ₽".replace(',', ' ')
            except:
                cost_text = f"{maintenance_cost} ₽" if maintenance_cost != '0' else "0.00 ₽"
            cost_item = QTableWidgetItem(cost_text)
            cost_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.depreciation_table.setItem(row, 7, cost_item)
    
    def refresh_maintenance_cost(self):
        """Обновить отчет по стоимости содержания"""
        start_date = self.start_date_edit.date().toString(Qt.DateFormat.ISODate)
        end_date = self.end_date_edit.date().toString(Qt.DateFormat.ISODate)
        
        # Получаем сводную информацию
        summary = self.db.get_maintenance_cost_report(start_date, end_date)
        
        total_cost = Decimal(summary.get('total_cost', 0) or 0)
        avg_cost = Decimal(summary.get('avg_cost', 0) or 0)
        total_count = summary.get('total_maintenances', 0) or 0
        
        self.summary_label.setText(
            f"📊 Всего обслуживаний: <b>{total_count}</b> | "
            f"💰 Общая стоимость: <b>{total_cost:,.2f} ₽</b> | "
            f"📈 Средняя стоимость: <b>{avg_cost:,.2f} ₽</b>".replace(',', ' ')
        )
        
        # Получаем детальный отчет
        report_data = self.db.get_maintenance_report(start_date, end_date)
        self.maintenance_cost_table.setRowCount(len(report_data))
        
        for row, item in enumerate(report_data):
            self.maintenance_cost_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            equipment_text = f"{item.get('inventory_number', '')} - {item.get('name', '')}"
            self.maintenance_cost_table.setItem(row, 1, QTableWidgetItem(equipment_text))
            self.maintenance_cost_table.setItem(row, 2, QTableWidgetItem(item['maintenance_date']))
            self.maintenance_cost_table.setItem(row, 3, QTableWidgetItem(item['type']))
            
            # Форматирование стоимости
            cost = item.get('cost', '0') or '0'
            try:
                cost_decimal = Decimal(str(cost))
                cost_text = f"{cost_decimal:,.2f} ₽".replace(',', ' ')
            except:
                cost_text = f"{cost} ₽" if cost != '0' else "0.00 ₽"
            cost_item = QTableWidgetItem(cost_text)
            cost_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.maintenance_cost_table.setItem(row, 4, cost_item)
            description = item.get('description', '') or ''
            self.maintenance_cost_table.setItem(row, 5, QTableWidgetItem(description[:50] + '...' if len(description) > 50 else description))
    
    def refresh_maintenance_report(self):
        """Обновить отчет по техническому обслуживанию (оптимизировано для < 5 сек)"""
        start_date = self.report_start_date_edit.date().toString(Qt.DateFormat.ISODate)
        end_date = self.report_end_date_edit.date().toString(Qt.DateFormat.ISODate)
        
        report_data = self.db.get_maintenance_report(start_date, end_date)
        self.maintenance_report_table.setRowCount(len(report_data))
        
        for row, item in enumerate(report_data):
            self.maintenance_report_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            equipment_text = f"{item.get('inventory_number', '')} - {item.get('name', '')}"
            self.maintenance_report_table.setItem(row, 1, QTableWidgetItem(equipment_text))
            self.maintenance_report_table.setItem(row, 2, QTableWidgetItem(item['maintenance_date']))
            self.maintenance_report_table.setItem(row, 3, QTableWidgetItem(item['type']))
            
            # Форматирование стоимости
            cost = item.get('cost', '0') or '0'
            try:
                cost_decimal = Decimal(str(cost))
                cost_text = f"{cost_decimal:,.2f} ₽".replace(',', ' ')
            except:
                cost_text = f"{cost} ₽" if cost != '0' else "0.00 ₽"
            cost_item = QTableWidgetItem(cost_text)
            cost_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.maintenance_report_table.setItem(row, 4, cost_item)
            description = item.get('description', '') or ''
            self.maintenance_report_table.setItem(row, 5, QTableWidgetItem(description[:50] + '...' if len(description) > 50 else description))
    
    def export_depreciation(self):
        """Экспорт отчета по амортизации в CSV"""
        filename = ExportManager.get_export_filename(self, "depreciation_report")
        if filename:
            if ExportManager.export_table_to_csv(self.depreciation_table, filename):
                QMessageBox.information(self, "Успех", f"Отчет экспортирован в {filename}")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось экспортировать отчет")
    
    def export_maintenance_cost(self):
        """Экспорт отчета по стоимости содержания в CSV"""
        filename = ExportManager.get_export_filename(self, "maintenance_cost_report")
        if filename:
            if ExportManager.export_table_to_csv(self.maintenance_cost_table, filename):
                QMessageBox.information(self, "Успех", f"Отчет экспортирован в {filename}")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось экспортировать отчет")
    
    def export_maintenance_report(self):
        """Экспорт отчета по ТО в CSV"""
        filename = ExportManager.get_export_filename(self, "maintenance_report")
        if filename:
            if ExportManager.export_table_to_csv(self.maintenance_report_table, filename):
                QMessageBox.information(self, "Успех", f"Отчет экспортирован в {filename}")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось экспортировать отчет")
