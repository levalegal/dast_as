"""
Модуль логирования действий пользователя
"""
import logging
from datetime import datetime
from pathlib import Path


class AppLogger:
    """Класс для логирования действий в приложении"""
    
    def __init__(self, log_file: str = "equipment_tracker.log"):
        self.log_file = log_file
        self.setup_logger()
    
    def setup_logger(self):
        """Настройка логгера"""
        # Создаем директорию для логов, если её нет
        log_path = Path(self.log_file)
        log_path.parent.mkdir(exist_ok=True)
        
        # Настраиваем формат логирования
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(self.log_file, encoding='utf-8'),
                logging.StreamHandler()  # Также выводим в консоль
            ]
        )
        
        self.logger = logging.getLogger('EquipmentTracker')
    
    def log_equipment_action(self, action: str, equipment_id: int = None, 
                            inventory_number: str = None, details: str = None):
        """Логирование действий с оборудованием"""
        message = f"Оборудование - {action}"
        if inventory_number:
            message += f": {inventory_number}"
        if equipment_id:
            message += f" (ID: {equipment_id})"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_maintenance_action(self, action: str, maintenance_id: int = None,
                              equipment_id: int = None, details: str = None):
        """Логирование действий с обслуживанием"""
        message = f"Обслуживание - {action}"
        if maintenance_id:
            message += f" (ID: {maintenance_id})"
        if equipment_id:
            message += f" для оборудования ID: {equipment_id}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_assignment_action(self, action: str, assignment_id: int = None,
                             equipment_id: int = None, details: str = None):
        """Логирование действий с назначениями"""
        message = f"Назначение - {action}"
        if assignment_id:
            message += f" (ID: {assignment_id})"
        if equipment_id:
            message += f" для оборудования ID: {equipment_id}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_report_action(self, report_type: str, details: str = None):
        """Логирование генерации отчетов"""
        message = f"Отчет - {report_type}"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_error(self, error_type: str, error_message: str, details: str = None):
        """Логирование ошибок"""
        message = f"ОШИБКА - {error_type}: {error_message}"
        if details:
            message += f" - {details}"
        self.logger.error(message)
    
    def log_backup_action(self, action: str, file_path: str = None):
        """Логирование действий с резервными копиями"""
        message = f"Резервное копирование - {action}"
        if file_path:
            message += f": {file_path}"
        self.logger.info(message)


# Глобальный экземпляр логгера
app_logger = AppLogger()
