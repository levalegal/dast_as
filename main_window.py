"""
Главное окно приложения EquipmentTracker
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QStatusBar, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from database import Database
from widgets.equipment_widget import EquipmentWidget
from widgets.maintenance_widget import MaintenanceWidget
from widgets.assignments_widget import AssignmentsWidget
from widgets.reports_widget import ReportsWidget
from widgets.dashboard_widget import DashboardWidget


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("EquipmentTracker - Учет оборудования")
        self.setGeometry(100, 100, 1200, 800)
        
        # Применяем стили
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #2196F3;
            }
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Вкладка "Дашборд"
        self.dashboard_widget = DashboardWidget(self.db)
        self.tabs.addTab(self.dashboard_widget, "📊 Дашборд")
        
        # Вкладка "Оборудование"
        self.equipment_widget = EquipmentWidget(self.db)
        self.tabs.addTab(self.equipment_widget, "Реестр оборудования")
        
        # Вкладка "Техническое обслуживание"
        self.maintenance_widget = MaintenanceWidget(self.db)
        self.tabs.addTab(self.maintenance_widget, "Техническое обслуживание")
        
        # Вкладка "Перемещения"
        self.assignments_widget = AssignmentsWidget(self.db)
        self.tabs.addTab(self.assignments_widget, "История перемещений")
        
        # Вкладка "Отчеты"
        self.reports_widget = ReportsWidget(self.db)
        self.tabs.addTab(self.reports_widget, "Отчеты")
        
        # Статусная строка
        self.statusBar().showMessage("Готово к работе")
        
        # Подключаем сигналы для обновления данных между вкладками
        self.equipment_widget.equipment_updated.connect(self.on_equipment_updated)
        self.assignments_widget.assignment_updated.connect(self.on_assignment_updated)
    
    def on_equipment_updated(self):
        """Обработчик обновления оборудования"""
        self.dashboard_widget.refresh_data()
        self.maintenance_widget.refresh_equipment_list()
        self.assignments_widget.refresh_equipment_list()
        self.reports_widget.refresh_data()
        self.statusBar().showMessage("Данные обновлены", 2000)
    
    def on_assignment_updated(self):
        """Обработчик обновления назначений"""
        self.dashboard_widget.refresh_data()
        self.equipment_widget.refresh_data()
        self.reports_widget.refresh_data()
        self.statusBar().showMessage("Данные обновлены", 2000)
    
    def closeEvent(self, event):
        """Обработка закрытия приложения"""
        reply = QMessageBox.question(
            self, 'Выход',
            'Вы уверены, что хотите выйти?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()