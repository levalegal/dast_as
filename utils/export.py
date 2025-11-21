"""
Утилиты для экспорта данных
"""
import csv
from datetime import datetime
from typing import List, Dict
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import QObject


class ExportManager(QObject):
    """Менеджер для экспорта данных в различные форматы"""
    
    @staticmethod
    def export_to_csv(data: List[Dict], headers: List[str], filename: str = None) -> bool:
        """Экспорт данных в CSV файл"""
        if not data:
            return False
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception as e:
            print(f"Ошибка экспорта в CSV: {e}")
            return False
    
    @staticmethod
    def export_table_to_csv(table, filename: str = None) -> bool:
        """Экспорт таблицы QTableWidget в CSV"""
        if table.rowCount() == 0:
            return False
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"export_{timestamp}.csv"
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                
                # Заголовки
                headers = []
                for col in range(table.columnCount()):
                    headers.append(table.horizontalHeaderItem(col).text())
                writer.writerow(headers)
                
                # Данные
                for row in range(table.rowCount()):
                    row_data = []
                    for col in range(table.columnCount()):
                        item = table.item(row, col)
                        row_data.append(item.text() if item else '')
                    writer.writerow(row_data)
            
            return True
        except Exception as e:
            print(f"Ошибка экспорта таблицы в CSV: {e}")
            return False
    
    @staticmethod
    def get_export_filename(parent, default_name: str = "export") -> str:
        """Получить имя файла для экспорта через диалог"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{default_name}_{timestamp}.csv"
        
        filename, _ = QFileDialog.getSaveFileName(
            parent,
            "Сохранить как CSV",
            default_filename,
            "CSV Files (*.csv);;All Files (*)"
        )
        
        return filename if filename else None
