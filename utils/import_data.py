"""
Утилиты для импорта данных из CSV
"""
import csv
from typing import List, Dict
from decimal import Decimal, InvalidOperation
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from database import Database


class ImportManager:
    """Менеджер для импорта данных"""
    
    @staticmethod
    def import_equipment_from_csv(db: Database, parent=None) -> tuple:
        """
        Импорт оборудования из CSV файла
        Возвращает (успешно, ошибки, предупреждения)
        """
        filename, _ = QFileDialog.getOpenFileName(
            parent,
            "Выберите CSV файл для импорта",
            "",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not filename:
            return 0, [], []
        
        imported = 0
        errors = []
        warnings = []
        
        try:
            with open(filename, 'r', encoding='utf-8-sig') as csvfile:
                # Пытаемся определить разделитель
                sample = csvfile.read(1024)
                csvfile.seek(0)
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(sample).delimiter
                
                reader = csv.DictReader(csvfile, delimiter=delimiter)
                
                for row_num, row in enumerate(reader, start=2):  # Начинаем с 2, т.к. 1 - заголовок
                    try:
                        # Очищаем значения от пробелов
                        row = {k.strip(): v.strip() if v else None for k, v in row.items()}
                        
                        # Маппинг полей (поддерживаем разные варианты названий)
                        inventory_number = (row.get('Инвентарный номер') or 
                                          row.get('inventory_number') or 
                                          row.get('Инв. номер') or '').strip()
                        
                        name = (row.get('Наименование') or 
                               row.get('name') or 
                               row.get('Название') or '').strip()
                        
                        if not inventory_number or not name:
                            warnings.append(f"Строка {row_num}: пропущена (нет обязательных полей)")
                            continue
                        
                        category = (row.get('Категория') or 
                                  row.get('category') or None)
                        
                        purchase_date = (row.get('Дата покупки') or 
                                      row.get('purchase_date') or 
                                      row.get('Дата') or None)
                        
                        purchase_price = None
                        price_str = (row.get('Цена покупки') or 
                                    row.get('purchase_price') or 
                                    row.get('Цена') or None)
                        if price_str:
                            try:
                                purchase_price = Decimal(str(price_str).replace(',', '.'))
                            except (InvalidOperation, ValueError):
                                warnings.append(f"Строка {row_num}: неверный формат цены '{price_str}'")
                        
                        current_location = (row.get('Местоположение') or 
                                          row.get('current_location') or 
                                          row.get('Место') or None)
                        
                        status = (row.get('Статус') or 
                                row.get('status') or 
                                'active')
                        
                        # Проверяем валидность статуса
                        valid_statuses = ['active', 'in_repair', 'written_off', 'reserved']
                        if status not in valid_statuses:
                            status = 'active'
                            warnings.append(f"Строка {row_num}: неверный статус, установлен 'active'")
                        
                        # Добавляем оборудование
                        try:
                            db.add_equipment(
                                inventory_number=inventory_number,
                                name=name,
                                category=category,
                                purchase_date=purchase_date,
                                purchase_price=purchase_price,
                                current_location=current_location,
                                status=status
                            )
                            imported += 1
                        except ValueError as e:
                            errors.append(f"Строка {row_num}: {str(e)}")
                        except Exception as e:
                            errors.append(f"Строка {row_num}: неожиданная ошибка - {str(e)}")
                    
                    except Exception as e:
                        errors.append(f"Строка {row_num}: ошибка обработки - {str(e)}")
            
            return imported, errors, warnings
            
        except Exception as e:
            errors.append(f"Ошибка чтения файла: {str(e)}")
            return imported, errors, warnings
    
    @staticmethod
    def show_import_results(parent, imported: int, errors: List[str], warnings: List[str]):
        """Показать результаты импорта"""
        message = f"Импорт завершен!\n\n"
        message += f"Успешно импортировано: {imported}\n"
        
        if warnings:
            message += f"\nПредупреждения ({len(warnings)}):\n"
            message += "\n".join(warnings[:10])  # Показываем первые 10
            if len(warnings) > 10:
                message += f"\n... и еще {len(warnings) - 10} предупреждений"
        
        if errors:
            message += f"\n\nОшибки ({len(errors)}):\n"
            message += "\n".join(errors[:10])  # Показываем первые 10
            if len(errors) > 10:
                message += f"\n... и еще {len(errors) - 10} ошибок"
        
        if errors:
            QMessageBox.warning(parent, "Результаты импорта", message)
        elif warnings:
            QMessageBox.information(parent, "Результаты импорта", message)
        else:
            QMessageBox.information(parent, "Успех", f"Успешно импортировано {imported} записей!")
