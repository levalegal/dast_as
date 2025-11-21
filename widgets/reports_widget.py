"""
Виджет для генерации отчетов
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLabel, QGroupBox,
                             QDateEdit, QHeaderView, QMessageBox, QTabWidget)
from PyQt6.QtCore import Qt, QDate
from database import Database
from decimal import Decimal


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
        self.depreciation_refresh_btn = QPushButton("Обновить отчет")
        self.depreciation_refresh_btn.clicked.connect(self.refresh_depreciation)
        buttons_layout.addWidget(self.depreciation_refresh_btn)
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
        
        self.cost_refresh_btn = QPushButton("Обновить отчет")
        self.cost_refresh_btn.clicked.connect(self.refresh_maintenance_cost)
        filter_layout.addWidget(self.cost_refresh_btn)
        
        filter_group.setLayout(filter_layout)
        maintenance_cost_layout.addWidget(filter_group)
        
        # Сводная информация
        self.summary_label = QLabel()
        self.summary_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        maintenance_cost_layout.addWidget(self.summary_label)
        
        self.maintenance_cost_table = QTableWidget()
        self.maintenance_cost_table.setColumnCount(6)
        self.maintenance_cost_table.setHorizontalHeaderLabels([
            "ID", "Оборудование", "Дата", "Тип", "Стоимость", "Описание"
        ])
        self.maintenance_cost_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.maintenance_cost_table.setAlternatingRowColors(True)
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
        
        self.maintenance_report_refresh_btn = QPushButton("Сформировать отчет")
        self.maintenance_report_refresh_btn.clicked.connect(self.refresh_maintenance_report)
        report_filter_layout.addWidget(self.maintenance_report_refresh_btn)
        
        report_filter_group.setLayout(report_filter_layout)
        maintenance_report_layout.addWidget(report_filter_group)
        
        self.maintenance_report_table = QTableWidget()
        self.maintenance_report_table.setColumnCount(6)
        self.maintenance_report_table.setHorizontalHeaderLabels([
            "ID", "Оборудование", "Дата", "Тип", "Стоимость", "Описание"
        ])
        self.maintenance_report_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.maintenance_report_table.setAlternatingRowColors(True)
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
            price = item['purchase_price'] or '0'
            self.depreciation_table.setItem(row, 5, QTableWidgetItem(str(price)))
            days = item.get('days_in_use', 0) or 0
            self.depreciation_table.setItem(row, 6, QTableWidgetItem(str(days)))
            maintenance_cost = item.get('total_maintenance_cost', '0') or '0'
            self.depreciation_table.setItem(row, 7, QTableWidgetItem(str(maintenance_cost)))
    
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
            f"Всего обслуживаний: {total_count} | "
            f"Общая стоимость: {total_cost:.2f} | "
            f"Средняя стоимость: {avg_cost:.2f}"
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
            cost = item.get('cost', '0') or '0'
            self.maintenance_cost_table.setItem(row, 4, QTableWidgetItem(str(cost)))
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
            cost = item.get('cost', '0') or '0'
            self.maintenance_report_table.setItem(row, 4, QTableWidgetItem(str(cost)))
            description = item.get('description', '') or ''
            self.maintenance_report_table.setItem(row, 5, QTableWidgetItem(description[:50] + '...' if len(description) > 50 else description))
