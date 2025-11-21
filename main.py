"""
Главный файл приложения EquipmentTracker
"""
import sys
from PyQt6.QtWidgets import QApplication
from main_window import MainWindow


def main():
    """Точка входа в приложение"""
    app = QApplication(sys.argv)
    app.setApplicationName("EquipmentTracker")
    app.setOrganizationName("EquipmentTracker")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

