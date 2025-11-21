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
    
    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        from PyQt6.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Критическая ошибка")
        msg.setText(f"Произошла ошибка при запуске приложения:\n{str(e)}")
        msg.exec()
        sys.exit(1)


if __name__ == "__main__":
    main()

