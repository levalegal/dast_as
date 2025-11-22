"""
Современные стили для приложения EquipmentTracker
Продвинутая система дизайна с градиентами, тенями и анимациями
"""
from PyQt6.QtGui import QColor, QPalette


class ModernStyles:
    """Класс с современными стилями для приложения"""
    
    # Цветовая палитра - расширенная версия
    PRIMARY_COLOR = "#2196F3"
    PRIMARY_DARK = "#1976D2"
    PRIMARY_LIGHT = "#64B5F6"
    PRIMARY_ULTRA_LIGHT = "#E3F2FD"
    
    SECONDARY_COLOR = "#FF9800"
    SECONDARY_DARK = "#F57C00"
    SECONDARY_LIGHT = "#FFB74D"
    
    SUCCESS_COLOR = "#4CAF50"
    SUCCESS_DARK = "#388E3C"
    SUCCESS_LIGHT = "#81C784"
    
    WARNING_COLOR = "#FFC107"
    WARNING_DARK = "#F9A825"
    
    ERROR_COLOR = "#F44336"
    ERROR_DARK = "#D32F2F"
    ERROR_LIGHT = "#E57373"
    
    INFO_COLOR = "#00BCD4"
    INFO_DARK = "#0097A7"
    
    # Нейтральные цвета - улучшенная палитра
    BACKGROUND_LIGHT = "#F5F7FA"
    BACKGROUND_WHITE = "#FFFFFF"
    BACKGROUND_HOVER = "#ECEFF1"
    
    TEXT_PRIMARY = "#212121"
    TEXT_SECONDARY = "#757575"
    TEXT_DISABLED = "#BDBDBD"
    
    BORDER_COLOR = "#E0E0E0"
    BORDER_LIGHT = "#F5F5F5"
    DIVIDER_COLOR = "#BDBDBD"
    
    # Акцентные цвета для карточек
    CARD_BLUE = "#E3F2FD"
    CARD_GREEN = "#E8F5E9"
    CARD_ORANGE = "#FFF3E0"
    CARD_PURPLE = "#F3E5F5"
    
    # Цвета для статусов
    STATUS_ACTIVE = "#4CAF50"
    STATUS_REPAIR = "#FF9800"
    STATUS_WRITTEN_OFF = "#9E9E9E"
    STATUS_RESERVED = "#2196F3"
    
    @staticmethod
    def get_main_stylesheet():
        """Получить основной стиль приложения с продвинутыми эффектами"""
        return f"""
        /* Главное окно с градиентным фоном */
        QMainWindow {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_LIGHT},
                stop:1 {ModernStyles.BACKGROUND_WHITE});
        }}
        
        /* Вкладки с улучшенным дизайном */
        QTabWidget::pane {{
            border: 2px solid {ModernStyles.BORDER_COLOR};
            background-color: {ModernStyles.BACKGROUND_WHITE};
            border-radius: 8px;
            top: -1px;
            padding: 4px;
        }}
        
        QTabBar::tab {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
            color: {ModernStyles.TEXT_SECONDARY};
            padding: 12px 24px;
            margin-right: 3px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            border: 2px solid {ModernStyles.BORDER_COLOR};
            border-bottom: none;
            font-weight: 500;
            font-size: 13px;
        }}
        
        QTabBar::tab:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_HOVER},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
            color: {ModernStyles.TEXT_PRIMARY};
            border-color: {ModernStyles.PRIMARY_LIGHT};
        }}
        
        QTabBar::tab:selected {{
            background: {ModernStyles.BACKGROUND_WHITE};
            color: {ModernStyles.PRIMARY_COLOR};
            border: 2px solid {ModernStyles.PRIMARY_COLOR};
            border-bottom: 3px solid {ModernStyles.BACKGROUND_WHITE};
            font-weight: 600;
            margin-bottom: -1px;
        }}
        
        /* Кнопки с градиентами и тенями */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.PRIMARY_COLOR},
                stop:1 {ModernStyles.PRIMARY_DARK});
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 13px;
            min-height: 36px;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.PRIMARY_LIGHT},
                stop:1 {ModernStyles.PRIMARY_COLOR});
        }}
        
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.PRIMARY_DARK},
                stop:1 {ModernStyles.PRIMARY_COLOR});
            padding-top: 11px;
            padding-left: 21px;
        }}
        
        QPushButton:disabled {{
            background: {ModernStyles.BACKGROUND_LIGHT};
            color: {ModernStyles.TEXT_DISABLED};
            border: 1px solid {ModernStyles.BORDER_COLOR};
        }}
        
        /* Кнопки действий - успешные операции */
        QPushButton[class="action-button"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.SUCCESS_COLOR},
                stop:1 {ModernStyles.SUCCESS_DARK});
        }}
        
        QPushButton[class="action-button"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.SUCCESS_LIGHT},
                stop:1 {ModernStyles.SUCCESS_COLOR});
        }}
        
        QPushButton[class="action-button"]:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.SUCCESS_DARK},
                stop:1 {ModernStyles.SUCCESS_COLOR});
        }}
        
        /* Опасные кнопки */
        QPushButton[class="danger-button"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.ERROR_COLOR},
                stop:1 {ModernStyles.ERROR_DARK});
        }}
        
        QPushButton[class="danger-button"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.ERROR_LIGHT},
                stop:1 {ModernStyles.ERROR_COLOR});
        }}
        
        QPushButton[class="danger-button"]:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.ERROR_DARK},
                stop:1 {ModernStyles.ERROR_COLOR});
        }}
        
        /* Вторичные кнопки */
        QPushButton[class="secondary-button"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.SECONDARY_COLOR},
                stop:1 {ModernStyles.SECONDARY_DARK});
        }}
        
        QPushButton[class="secondary-button"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.SECONDARY_LIGHT},
                stop:1 {ModernStyles.SECONDARY_COLOR});
        }}
        
        /* Таблицы с улучшенным дизайном */
        QTableWidget {{
            gridline-color: {ModernStyles.BORDER_LIGHT};
            background-color: {ModernStyles.BACKGROUND_WHITE};
            border: 2px solid {ModernStyles.BORDER_COLOR};
            border-radius: 8px;
            selection-background-color: {ModernStyles.PRIMARY_ULTRA_LIGHT};
            selection-color: {ModernStyles.TEXT_PRIMARY};
            alternate-background-color: {ModernStyles.BACKGROUND_LIGHT};
        }}
        
        QTableWidget::item {{
            padding: 8px 12px;
            border: none;
            border-bottom: 1px solid {ModernStyles.BORDER_LIGHT};
        }}
        
        QTableWidget::item:hover {{
            background-color: {ModernStyles.PRIMARY_ULTRA_LIGHT};
        }}
        
        QTableWidget::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.PRIMARY_ULTRA_LIGHT},
                stop:1 {ModernStyles.PRIMARY_LIGHT});
            color: {ModernStyles.TEXT_PRIMARY};
            border-bottom: 2px solid {ModernStyles.PRIMARY_COLOR};
        }}
        
        QTableWidget::item:alternate {{
            background-color: {ModernStyles.BACKGROUND_LIGHT};
        }}
        
        QHeaderView::section {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
            color: {ModernStyles.TEXT_PRIMARY};
            padding: 12px 8px;
            border: none;
            border-right: 1px solid {ModernStyles.BORDER_COLOR};
            border-bottom: 3px solid {ModernStyles.PRIMARY_COLOR};
            font-weight: 700;
            font-size: 12px;
            text-transform: uppercase;
        }}
        
        QHeaderView::section:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_HOVER},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
            color: {ModernStyles.PRIMARY_COLOR};
        }}
        
        QHeaderView::section:first {{
            border-top-left-radius: 8px;
        }}
        
        QHeaderView::section:last {{
            border-top-right-radius: 8px;
            border-right: none;
        }}
        
        /* Группы и карточки с тенями */
        QGroupBox {{
            font-weight: 700;
            font-size: 14px;
            border: 2px solid {ModernStyles.BORDER_COLOR};
            border-radius: 10px;
            margin-top: 16px;
            padding-top: 20px;
            padding-bottom: 12px;
            padding-left: 12px;
            padding-right: 12px;
            background-color: {ModernStyles.BACKGROUND_WHITE};
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 16px;
            padding: 4px 12px;
            color: {ModernStyles.PRIMARY_COLOR};
            font-weight: 700;
        }}
        
        /* Карточки статистики */
        QGroupBox[class="stat-card"] {{
            border: 2px solid {ModernStyles.PRIMARY_LIGHT};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.PRIMARY_ULTRA_LIGHT});
        }}
        
        QGroupBox[class="stat-card-equipment"] {{
            border: 2px solid {ModernStyles.SUCCESS_LIGHT};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.CARD_GREEN});
        }}
        
        QGroupBox[class="stat-card-maintenance"] {{
            border: 2px solid {ModernStyles.INFO_COLOR};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.CARD_BLUE});
        }}
        
        QGroupBox[class="stat-card-assignments"] {{
            border: 2px solid {ModernStyles.SECONDARY_LIGHT};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.CARD_ORANGE});
        }}
        
        QGroupBox[class="stat-card-finance"] {{
            border: 2px solid {ModernStyles.WARNING_COLOR};
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.CARD_PURPLE});
        }}
        
        /* Поля ввода с улучшенными эффектами */
        QLineEdit, QTextEdit, QComboBox, QDateEdit {{
            border: 2px solid {ModernStyles.BORDER_COLOR};
            border-radius: 6px;
            padding: 8px 12px;
            background-color: {ModernStyles.BACKGROUND_WHITE};
            color: {ModernStyles.TEXT_PRIMARY};
            selection-background-color: {ModernStyles.PRIMARY_LIGHT};
            selection-color: white;
            font-size: 13px;
        }}
        
        QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QDateEdit:focus {{
            border: 2px solid {ModernStyles.PRIMARY_COLOR};
            background-color: {ModernStyles.PRIMARY_ULTRA_LIGHT};
        }}
        
        QLineEdit:hover, QTextEdit:hover, QComboBox:hover, QDateEdit:hover {{
            border: 2px solid {ModernStyles.PRIMARY_LIGHT};
            background-color: {ModernStyles.BACKGROUND_LIGHT};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox::down-arrow {{
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 6px solid {ModernStyles.TEXT_SECONDARY};
            margin-right: 10px;
        }}
        
        QComboBox QAbstractItemView {{
            border: 2px solid {ModernStyles.PRIMARY_COLOR};
            border-radius: 6px;
            background-color: {ModernStyles.BACKGROUND_WHITE};
            selection-background-color: {ModernStyles.PRIMARY_LIGHT};
            selection-color: {ModernStyles.TEXT_PRIMARY};
            padding: 4px;
        }}
        
        /* Метки с улучшенной типографикой */
        QLabel {{
            color: {ModernStyles.TEXT_PRIMARY};
        }}
        
        QLabel[class="title"] {{
            font-size: 22px;
            font-weight: 700;
            color: {ModernStyles.TEXT_PRIMARY};
            padding: 8px 0px;
        }}
        
        QLabel[class="subtitle"] {{
            font-size: 15px;
            font-weight: 500;
            color: {ModernStyles.TEXT_SECONDARY};
        }}
        
        QLabel[class="stat-value"] {{
            font-size: 32px;
            font-weight: 800;
            color: {ModernStyles.PRIMARY_COLOR};
            letter-spacing: -1px;
        }}
        
        QLabel[class="stat-label"] {{
            font-size: 13px;
            color: {ModernStyles.TEXT_SECONDARY};
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        QLabel[class="stat-value-equipment"] {{
            font-size: 32px;
            font-weight: 800;
            color: {ModernStyles.SUCCESS_COLOR};
        }}
        
        QLabel[class="stat-value-maintenance"] {{
            font-size: 32px;
            font-weight: 800;
            color: {ModernStyles.INFO_COLOR};
        }}
        
        QLabel[class="stat-value-assignments"] {{
            font-size: 32px;
            font-weight: 800;
            color: {ModernStyles.SECONDARY_COLOR};
        }}
        
        QLabel[class="stat-value-finance"] {{
            font-size: 32px;
            font-weight: 800;
            color: {ModernStyles.WARNING_COLOR};
        }}
        
        /* Статусная строка */
        QStatusBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
            border-top: 2px solid {ModernStyles.BORDER_COLOR};
            color: {ModernStyles.TEXT_PRIMARY};
            font-size: 12px;
            padding: 4px;
        }}
        
        /* Меню с улучшенным дизайном */
        QMenuBar {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
            border-bottom: 2px solid {ModernStyles.BORDER_COLOR};
            color: {ModernStyles.TEXT_PRIMARY};
            font-weight: 500;
            padding: 4px;
        }}
        
        QMenuBar::item {{
            padding: 8px 16px;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {ModernStyles.PRIMARY_ULTRA_LIGHT};
            color: {ModernStyles.PRIMARY_COLOR};
        }}
        
        QMenu {{
            background-color: {ModernStyles.BACKGROUND_WHITE};
            border: 2px solid {ModernStyles.BORDER_COLOR};
            border-radius: 8px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 10px 28px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.PRIMARY_ULTRA_LIGHT},
                stop:1 {ModernStyles.PRIMARY_LIGHT});
            color: {ModernStyles.PRIMARY_COLOR};
        }}
        
        QMenu::separator {{
            height: 1px;
            background: {ModernStyles.BORDER_COLOR};
            margin: 4px 8px;
        }}
        
        /* Спинбоксы */
        QSpinBox {{
            border: 2px solid {ModernStyles.BORDER_COLOR};
            border-radius: 6px;
            padding: 8px;
            background-color: {ModernStyles.BACKGROUND_WHITE};
            font-size: 13px;
        }}
        
        QSpinBox:focus {{
            border: 2px solid {ModernStyles.PRIMARY_COLOR};
            background-color: {ModernStyles.PRIMARY_ULTRA_LIGHT};
        }}
        
        QSpinBox:hover {{
            border: 2px solid {ModernStyles.PRIMARY_LIGHT};
        }}
        
        /* Скроллбары с улучшенным дизайном */
        QScrollBar:vertical {{
            background: {ModernStyles.BACKGROUND_LIGHT};
            width: 14px;
            border: none;
            border-radius: 7px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ModernStyles.DIVIDER_COLOR},
                stop:1 {ModernStyles.BORDER_COLOR});
            min-height: 30px;
            border-radius: 7px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {ModernStyles.PRIMARY_LIGHT},
                stop:1 {ModernStyles.PRIMARY_COLOR});
        }}
        
        QScrollBar::handle:vertical:pressed {{
            background: {ModernStyles.PRIMARY_COLOR};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background: {ModernStyles.BACKGROUND_LIGHT};
            height: 14px;
            border: none;
            border-radius: 7px;
            margin: 2px;
        }}
        
        QScrollBar::handle:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.DIVIDER_COLOR},
                stop:1 {ModernStyles.BORDER_COLOR});
            min-width: 30px;
            border-radius: 7px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.PRIMARY_LIGHT},
                stop:1 {ModernStyles.PRIMARY_COLOR});
        }}
        
        QScrollBar::handle:horizontal:pressed {{
            background: {ModernStyles.PRIMARY_COLOR};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """
    
    @staticmethod
    def get_dialog_stylesheet():
        """Стили для диалогов с улучшенным дизайном"""
        return f"""
        QDialog {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
        }}
        
        QDialogButtonBox {{
            button-layout: 1;
            padding: 12px;
        }}
        
        QDialogButtonBox QPushButton {{
            min-width: 100px;
            min-height: 38px;
        }}
        """
    
    @staticmethod
    def get_message_box_stylesheet():
        """Стили для сообщений с улучшенным дизайном"""
        return f"""
        QMessageBox {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
        }}
        
        QMessageBox QPushButton {{
            min-width: 100px;
            min-height: 38px;
        }}
        """
    
    @staticmethod
    def get_card_stylesheet(accent_color):
        """Получить стиль для карточки с указанным акцентным цветом"""
        return f"""
        QGroupBox {{
            border: 2px solid {accent_color};
            border-radius: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {ModernStyles.BACKGROUND_WHITE},
                stop:1 {ModernStyles.BACKGROUND_LIGHT});
            padding: 16px;
            margin-top: 12px;
        }}
        """