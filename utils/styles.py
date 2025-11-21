"""
Современные стили для приложения EquipmentTracker
"""
from PyQt6.QtGui import QColor, QPalette


class ModernStyles:
    """Класс с современными стилями для приложения"""
    
    # Цветовая палитра
    PRIMARY_COLOR = "#2196F3"
    PRIMARY_DARK = "#1976D2"
    PRIMARY_LIGHT = "#64B5F6"
    SECONDARY_COLOR = "#FF9800"
    SUCCESS_COLOR = "#4CAF50"
    WARNING_COLOR = "#FFC107"
    ERROR_COLOR = "#F44336"
    INFO_COLOR = "#00BCD4"
    
    # Нейтральные цвета
    BACKGROUND_LIGHT = "#F5F5F5"
    BACKGROUND_WHITE = "#FFFFFF"
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    BORDER_COLOR = "#E0E0E0"
    DIVIDER_COLOR = "#BDBDBD"
    
    @staticmethod
    def get_main_stylesheet():
        """Получить основной стиль приложения"""
        return f"""
        /* Главное окно */
        QMainWindow {{
            background-color: {ModernStyles.BACKGROUND_LIGHT};
        }}
        
        /* Вкладки */
        QTabWidget::pane {{
            border: 1px solid {ModernStyles.BORDER_COLOR};
            background-color: {ModernStyles.BACKGROUND_WHITE};
            border-radius: 4px;
            top: -1px;
        }}
        
        QTabBar::tab {{
            background-color: {ModernStyles.BACKGROUND_WHITE};
            color: {ModernStyles.TEXT_SECONDARY};
            padding: 10px 20px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            border: 1px solid {ModernStyles.BORDER_COLOR};
            border-bottom: none;
            font-weight: 500;
        }}
        
        QTabBar::tab:hover {{
            background-color: {ModernStyles.BACKGROUND_LIGHT};
            color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        QTabBar::tab:selected {{
            background-color: {ModernStyles.BACKGROUND_WHITE};
            color: {ModernStyles.PRIMARY_COLOR};
            border-bottom: 2px solid {ModernStyles.PRIMARY_COLOR};
            font-weight: 600;
        }}
        
        /* Кнопки */
        QPushButton {{
            background-color: {ModernStyles.PRIMARY_COLOR};
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: 500;
            min-height: 32px;
        }}
        
        QPushButton:hover {{
            background-color: {ModernStyles.PRIMARY_DARK};
        }}
        
        QPushButton:pressed {{
            background-color: {ModernStyles.PRIMARY_DARK};
            padding-top: 9px;
            padding-left: 17px;
        }}
        
        QPushButton:disabled {{
            background-color: {ModernStyles.BORDER_COLOR};
            color: {ModernStyles.TEXT_SECONDARY};
        }}
        
        /* Кнопки действий */
        QPushButton[class="action-button"] {{
            background-color: {ModernStyles.SUCCESS_COLOR};
        }}
        
        QPushButton[class="action-button"]:hover {{
            background-color: #45a049;
        }}
        
        QPushButton[class="danger-button"] {{
            background-color: {ModernStyles.ERROR_COLOR};
        }}
        
        QPushButton[class="danger-button"]:hover {{
            background-color: #da190b;
        }}
        
        QPushButton[class="secondary-button"] {{
            background-color: {ModernStyles.SECONDARY_COLOR};
        }}
        
        QPushButton[class="secondary-button"]:hover {{
            background-color: #f57c00;
        }}
        
        /* Таблицы */
        QTableWidget {{
            gridline-color: {ModernStyles.BORDER_COLOR};
            background-color: {ModernStyles.BACKGROUND_WHITE};
            border: 1px solid {ModernStyles.BORDER_COLOR};
            border-radius: 4px;
            selection-background-color: {ModernStyles.PRIMARY_LIGHT};
            selection-color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        QTableWidget::item {{
            padding: 4px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {ModernStyles.PRIMARY_LIGHT};
            color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        QTableWidget::item:alternate {{
            background-color: {ModernStyles.BACKGROUND_LIGHT};
        }}
        
        QHeaderView::section {{
            background-color: {ModernStyles.BACKGROUND_LIGHT};
            color: {ModernStyles.TEXT_PRIMARY};
            padding: 8px;
            border: none;
            border-bottom: 2px solid {ModernStyles.BORDER_COLOR};
            font-weight: 600;
        }}
        
        QHeaderView::section:hover {{
            background-color: {ModernStyles.BORDER_COLOR};
        }}
        
        /* Группы */
        QGroupBox {{
            font-weight: 600;
            font-size: 13px;
            border: 2px solid {ModernStyles.BORDER_COLOR};
            border-radius: 6px;
            margin-top: 12px;
            padding-top: 12px;
            background-color: {ModernStyles.BACKGROUND_WHITE};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 12px;
            padding: 0 8px;
            color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        /* Поля ввода */
        QLineEdit, QTextEdit, QComboBox, QDateEdit {{
            border: 1px solid {ModernStyles.BORDER_COLOR};
            border-radius: 4px;
            padding: 6px 10px;
            background-color: {ModernStyles.BACKGROUND_WHITE};
            color: {ModernStyles.TEXT_PRIMARY};
            selection-background-color: {ModernStyles.PRIMARY_LIGHT};
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {{
            border: 2px solid {ModernStyles.PRIMARY_COLOR};
            padding: 5px 9px;
        }}
        
        QLineEdit:hover, QTextEdit:hover, QComboBox:hover, QDateEdit:hover {{
            border: 1px solid {ModernStyles.PRIMARY_LIGHT};
        }}
        
        /* Метки */
        QLabel {{
            color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        QLabel[class="title"] {{
            font-size: 18px;
            font-weight: 600;
            color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        QLabel[class="subtitle"] {{
            font-size: 14px;
            font-weight: 500;
            color: {ModernStyles.TEXT_SECONDARY};
        }}
        
        QLabel[class="stat-value"] {{
            font-size: 24px;
            font-weight: 700;
            color: {ModernStyles.PRIMARY_COLOR};
        }}
        
        QLabel[class="stat-label"] {{
            font-size: 12px;
            color: {ModernStyles.TEXT_SECONDARY};
            font-weight: 500;
        }}
        
        /* Статусная строка */
        QStatusBar {{
            background-color: {ModernStyles.BACKGROUND_WHITE};
            border-top: 1px solid {ModernStyles.BORDER_COLOR};
            color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        /* Меню */
        QMenuBar {{
            background-color: {ModernStyles.BACKGROUND_WHITE};
            border-bottom: 1px solid {ModernStyles.BORDER_COLOR};
            color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        QMenuBar::item {{
            padding: 6px 12px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {ModernStyles.BACKGROUND_LIGHT};
        }}
        
        QMenu {{
            background-color: {ModernStyles.BACKGROUND_WHITE};
            border: 1px solid {ModernStyles.BORDER_COLOR};
            border-radius: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 24px;
        }}
        
        QMenu::item:selected {{
            background-color: {ModernStyles.PRIMARY_LIGHT};
        }}
        
        /* Спинбоксы */
        QSpinBox {{
            border: 1px solid {ModernStyles.BORDER_COLOR};
            border-radius: 4px;
            padding: 6px;
            background-color: {ModernStyles.BACKGROUND_WHITE};
        }}
        
        QSpinBox:focus {{
            border: 2px solid {ModernStyles.PRIMARY_COLOR};
        }}
        
        /* Скроллбары */
        QScrollBar:vertical {{
            background: {ModernStyles.BACKGROUND_LIGHT};
            width: 12px;
            border: none;
        }}
        
        QScrollBar::handle:vertical {{
            background: {ModernStyles.BORDER_COLOR};
            min-height: 20px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: {ModernStyles.DIVIDER_COLOR};
        }}
        
        QScrollBar:horizontal {{
            background: {ModernStyles.BACKGROUND_LIGHT};
            height: 12px;
            border: none;
        }}
        
        QScrollBar::handle:horizontal {{
            background: {ModernStyles.BORDER_COLOR};
            min-width: 20px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: {ModernStyles.DIVIDER_COLOR};
        }}
        """
    
    @staticmethod
    def get_dialog_stylesheet():
        """Стили для диалогов"""
        return f"""
        QDialog {{
            background-color: {ModernStyles.BACKGROUND_WHITE};
        }}
        
        QDialogButtonBox {{
            button-layout: 1;
        }}
        
        QDialogButtonBox QPushButton {{
            min-width: 80px;
        }}
        """
    
    @staticmethod
    def get_message_box_stylesheet():
        """Стили для сообщений"""
        return f"""
        QMessageBox {{
            background-color: {ModernStyles.BACKGROUND_WHITE};
        }}
        
        QMessageBox QPushButton {{
            min-width: 80px;
        }}
        """
