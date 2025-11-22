"""
Главное окно приложения EquipmentTracker
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QStatusBar, QMessageBox, QMenuBar, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from utils.backup import BackupManager
from utils.logger import app_logger
from utils.styles import ModernStyles
from database import Database
from widgets.equipment_widget import EquipmentWidget
from widgets.maintenance_widget import MaintenanceWidget
from widgets.assignments_widget import AssignmentsWidget
from widgets.reports_widget import ReportsWidget
from widgets.dashboard_widget import DashboardWidget
from widgets.maintenance_scheduler_widget import MaintenanceSchedulerWidget


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle("EquipmentTracker - Система учета оборудования")
        self.setGeometry(100, 100, 1400, 900)
        
        # Применяем современные стили
        self.setStyleSheet(ModernStyles.get_main_stylesheet())
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Главный layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        central_widget.setLayout(main_layout)
        
        # Создаем вкладки
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #E0E0E0;
                border-radius: 10px;
                top: -1px;
                padding: 4px;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,
                    stop:1 #F5F7FA);
                color: #757575;
                padding: 14px 28px;
                margin-right: 4px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border: 2px solid #E0E0E0;
                border-bottom: none;
                font-weight: 600;
                font-size: 14px;
            }
            QTabBar::tab:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ECEFF1,
                    stop:1 #F5F7FA);
                color: #212121;
                border-color: #64B5F6;
            }
            QTabBar::tab:selected {
                background: #FFFFFF;
                color: #2196F3;
                border: 2px solid #2196F3;
                border-bottom: 3px solid #FFFFFF;
                font-weight: 700;
                margin-bottom: -1px;
            }
        """)
        main_layout.addWidget(self.tabs)
        
        # Вкладка "Дашборд"
        self.dashboard_widget = DashboardWidget(self.db)
        self.tabs.addTab(self.dashboard_widget, "📊 Дашборд")
        
        # Вкладка "Оборудование"
        self.equipment_widget = EquipmentWidget(self.db)
        self.tabs.addTab(self.equipment_widget, "📦 Реестр оборудования")
        
        # Вкладка "Техническое обслуживание"
        self.maintenance_widget = MaintenanceWidget(self.db)
        self.tabs.addTab(self.maintenance_widget, "🔧 Техническое обслуживание")
        
        # Вкладка "Планировщик ТО"
        self.scheduler_widget = MaintenanceSchedulerWidget(self.db)
        self.tabs.addTab(self.scheduler_widget, "📅 Планировщик ТО")
        
        # Вкладка "Перемещения"
        self.assignments_widget = AssignmentsWidget(self.db)
        self.tabs.addTab(self.assignments_widget, "👥 История перемещений")
        
        # Вкладка "Отчеты"
        self.reports_widget = ReportsWidget(self.db)
        self.tabs.addTab(self.reports_widget, "📊 Отчеты")
        
        # Меню
        self.create_menu()
        
        # Статусная строка с улучшенным дизайном
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #FFFFFF,
                    stop:1 #F5F7FA);
                border-top: 2px solid #E0E0E0;
                color: #212121;
                font-size: 12px;
                font-weight: 500;
                padding: 6px;
            }
        """)
        self.statusBar().showMessage("✅ Готово к работе")
        
        # Подключаем сигналы для обновления данных между вкладками
        self.equipment_widget.equipment_updated.connect(self.on_equipment_updated)
        self.assignments_widget.assignment_updated.connect(self.on_assignment_updated)
    
    def create_menu(self):
        """Создать меню приложения"""
        menubar = self.menuBar()
        
        # Меню "Файл" с улучшенным дизайном
        file_menu = menubar.addMenu("📁 Файл")
        
        backup_action = QAction("💾 Создать резервную копию", self)
        backup_action.setShortcut("Ctrl+B")
        backup_action.setToolTip("Создать резервную копию базы данных")
        backup_action.triggered.connect(self.create_backup)
        file_menu.addAction(backup_action)
        
        restore_action = QAction("📂 Восстановить из резервной копии", self)
        restore_action.setShortcut("Ctrl+R")
        restore_action.setToolTip("Восстановить базу данных из резервной копии")
        restore_action.triggered.connect(self.restore_backup)
        file_menu.addAction(restore_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("🚪 Выход", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setToolTip("Закрыть приложение")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def create_backup(self):
        """Создать резервную копию базы данных"""
        try:
            backup_path = BackupManager.create_backup(self.db.db_path)
            app_logger.log_backup_action("Создана", backup_path)
            QMessageBox.information(
                self, "Успех",
                f"Резервная копия создана:\n{backup_path}"
            )
            self.statusBar().showMessage(f"Резервная копия создана: {backup_path}", 5000)
        except Exception as e:
            app_logger.log_error("Создание резервной копии", str(e))
            QMessageBox.warning(self, "Ошибка", f"Не удалось создать резервную копию:\n{str(e)}")
    
    def restore_backup(self):
        """Восстановить базу данных из резервной копии"""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Восстановление базы данных заменит все текущие данные.\n'
            'Убедитесь, что у вас есть актуальная резервная копия.\n\n'
            'Продолжить?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            backup_path = BackupManager.get_backup_filename(self)
            if backup_path:
                try:
                    # Создаем резервную копию текущей БД перед восстановлением
                    current_backup = BackupManager.create_backup(self.db.db_path)
                    
                    BackupManager.restore_backup(backup_path, self.db.db_path)
                    app_logger.log_backup_action("Восстановлена", backup_path)
                    
                    QMessageBox.information(
                        self, "Успех",
                        f"База данных восстановлена из резервной копии.\n"
                        f"Текущая БД сохранена в: {current_backup}"
                    )
                    
                    # Перезагружаем все виджеты
                    self.equipment_widget.refresh_data()
                    self.maintenance_widget.refresh_data()
                    self.assignments_widget.refresh_data()
                    self.reports_widget.refresh_data()
                    self.dashboard_widget.refresh_data()
                    self.scheduler_widget.refresh_data()
                    
                    self.statusBar().showMessage("База данных восстановлена", 5000)
                except Exception as e:
                    QMessageBox.warning(self, "Ошибка", f"Не удалось восстановить базу данных:\n{str(e)}")
    
    def on_equipment_updated(self):
        """Обработчик обновления оборудования"""
        self.dashboard_widget.refresh_data()
        self.maintenance_widget.refresh_equipment_list()
        self.assignments_widget.refresh_equipment_list()
        self.reports_widget.refresh_data()
        self.scheduler_widget.refresh_data()
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