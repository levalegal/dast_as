"""
Утилиты для резервного копирования базы данных
"""
import shutil
from datetime import datetime
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog, QMessageBox


class BackupManager:
    """Менеджер для резервного копирования БД"""
    
    @staticmethod
    def create_backup(db_path: str, backup_dir: str = None) -> str:
        """Создать резервную копию базы данных"""
        if backup_dir is None:
            backup_dir = "backups"
        
        # Создаем директорию для бэкапов, если её нет
        Path(backup_dir).mkdir(exist_ok=True)
        
        # Генерируем имя файла с timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"equipment_backup_{timestamp}.db"
        backup_path = Path(backup_dir) / backup_filename
        
        try:
            shutil.copy2(db_path, str(backup_path))
            return str(backup_path)
        except Exception as e:
            raise Exception(f"Ошибка создания резервной копии: {e}")
    
    @staticmethod
    def restore_backup(backup_path: str, db_path: str) -> bool:
        """Восстановить базу данных из резервной копии"""
        try:
            shutil.copy2(backup_path, db_path)
            return True
        except Exception as e:
            raise Exception(f"Ошибка восстановления из резервной копии: {e}")
    
    @staticmethod
    def get_backup_filename(parent, default_dir: str = "backups") -> str:
        """Получить путь к файлу резервной копии через диалог"""
        filename, _ = QFileDialog.getOpenFileName(
            parent,
            "Выберите файл резервной копии",
            default_dir,
            "Database Files (*.db);;All Files (*)"
        )
        return filename if filename else None
