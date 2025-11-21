"""
Виджет для работы с реестром оборудования
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                             QDialog, QFormLayout, QDateEdit, QComboBox,
                             QMessageBox, QHeaderView, QGroupBox)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QDoubleValidator
from decimal import Decimal
from datetime import datetime
from utils.export import ExportManager
from utils.import_data import ImportManager
from utils.logger import app_logger


class EquipmentDialog(QDialog):
    """Диалог для добавления/редактирования оборудования"""
    
    def __init__(self, parent=None, equipment_data=None):
        super().__init__(parent)
        self.equipment_data = equipment_data
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса диалога"""
        if self.equipment_data:
            self.setWindowTitle("Редактировать оборудование")
        else:
            self.setWindowTitle("Добавить оборудование")
        
        self.setModal(True)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        form = QFormLayout()
        
        # Инвентарный номер
        self.inventory_number_edit = QLineEdit()
        self.inventory_number_edit.setPlaceholderText("ИНВ-001")
        self.inventory_number_edit.setToolTip("Уникальный инвентарный номер оборудования")
        form.addRow("Инвентарный номер *:", self.inventory_number_edit)
        
        # Наименование
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название оборудования")
        self.name_edit.setToolTip("Полное наименование оборудования")
        form.addRow("Наименование *:", self.name_edit)
        
        # Категория
        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems([
            "Компьютерная техника",
            "Офисная мебель",
            "Оргтехника",
            "Производственное оборудование",
            "Транспорт",
            "Другое"
        ])
        form.addRow("Категория:", self.category_combo)
        
        # Дата покупки
        self.purchase_date_edit = QDateEdit()
        self.purchase_date_edit.setCalendarPopup(True)
        self.purchase_date_edit.setDate(QDate.currentDate())
        form.addRow("Дата покупки:", self.purchase_date_edit)
        
        # Цена покупки
        self.purchase_price_edit = QLineEdit()
        self.purchase_price_edit.setPlaceholderText("0.00")
        self.purchase_price_edit.setToolTip("Стоимость покупки оборудования в рублях")
        validator = QDoubleValidator(0, 999999999, 2)
        self.purchase_price_edit.setValidator(validator)
        form.addRow("Цена покупки:", self.purchase_price_edit)
        
        # Текущее местоположение
        self.location_edit = QLineEdit()
        self.location_edit.setPlaceholderText("Отдел/Сотрудник")
        form.addRow("Текущее местоположение:", self.location_edit)
        
        # Статус
        self.status_combo = QComboBox()
        self.status_combo.addItems(["active", "in_repair", "written_off", "reserved"])
        form.addRow("Статус:", self.status_combo)
        
        layout.addLayout(form)
        
        # Кнопки
        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addLayout(buttons_layout)
        
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        # Заполняем данные, если редактируем
        if self.equipment_data:
            self.inventory_number_edit.setText(self.equipment_data.get('inventory_number', ''))
            self.name_edit.setText(self.equipment_data.get('name', ''))
            category = self.equipment_data.get('category', '')
            if category:
                index = self.category_combo.findText(category)
                if index >= 0:
                    self.category_combo.setCurrentIndex(index)
                else:
                    self.category_combo.setCurrentText(category)
            
            purchase_date = self.equipment_data.get('purchase_date')
            if purchase_date:
                date = QDate.fromString(purchase_date, Qt.DateFormat.ISODate)
                if date.isValid():
                    self.purchase_date_edit.setDate(date)
            
            price = self.equipment_data.get('purchase_price')
            if price:
                self.purchase_price_edit.setText(str(price))
            
            self.location_edit.setText(self.equipment_data.get('current_location', ''))
            
            status = self.equipment_data.get('status', 'active')
            index = self.status_combo.findText(status)
            if index >= 0:
                self.status_combo.setCurrentIndex(index)
    
    def get_data(self):
        """Получить данные из формы"""
        data = {
            'inventory_number': self.inventory_number_edit.text().strip(),
            'name': self.name_edit.text().strip(),
            'category': self.category_combo.currentText().strip() or None,
            'purchase_date': self.purchase_date_edit.date().toString(Qt.DateFormat.ISODate),
            'purchase_price': None,
            'current_location': self.location_edit.text().strip() or None,
            'status': self.status_combo.currentText()
        }
        
        price_text = self.purchase_price_edit.text().strip()
        if price_text:
            try:
                data['purchase_price'] = Decimal(price_text)
            except:
                pass
        
        return data


class EquipmentWidget(QWidget):
    """Виджет для управления реестром оборудования"""
    
    equipment_updated = pyqtSignal()
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Группа поиска и фильтров
        search_group = QGroupBox("Поиск и фильтры")
        search_layout = QVBoxLayout()
        
        # Строка поиска
        search_row = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск по инвентарному номеру или названию...")
        self.search_edit.textChanged.connect(self.apply_filters)
        search_row.addWidget(QLabel("Поиск:"))
        search_row.addWidget(self.search_edit)
        self.search_btn = QPushButton("Найти")
        self.search_btn.clicked.connect(self.search_equipment)
        search_row.addWidget(self.search_btn)
        self.clear_search_btn = QPushButton("Очистить")
        self.clear_search_btn.clicked.connect(self.clear_search)
        search_row.addWidget(self.clear_search_btn)
        search_layout.addLayout(search_row)
        
        # Фильтры
        filters_row = QHBoxLayout()
        filters_row.addWidget(QLabel("Категория:"))
        self.category_filter = QComboBox()
        self.category_filter.addItem("Все категории", None)
        self.category_filter.currentIndexChanged.connect(self.apply_filters)
        filters_row.addWidget(self.category_filter)
        
        filters_row.addWidget(QLabel("Статус:"))
        self.status_filter = QComboBox()
        self.status_filter.addItem("Все статусы", None)
        self.status_filter.addItems(["active", "in_repair", "written_off", "reserved"])
        self.status_filter.currentIndexChanged.connect(self.apply_filters)
        filters_row.addWidget(self.status_filter)
        
        filters_row.addStretch()
        search_layout.addLayout(filters_row)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить оборудование")
        self.add_btn.clicked.connect(self.add_equipment)
        buttons_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_equipment)
        buttons_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_equipment)
        buttons_layout.addWidget(self.delete_btn)
        
        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.refresh_data)
        buttons_layout.addWidget(self.refresh_btn)
        
        self.export_btn = QPushButton("Экспорт в CSV")
        self.export_btn.clicked.connect(self.export_data)
        buttons_layout.addWidget(self.export_btn)
        
        self.import_btn = QPushButton("Импорт из CSV")
        self.import_btn.clicked.connect(self.import_data)
        buttons_layout.addWidget(self.import_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Таблица оборудования
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Инвентарный номер", "Наименование", "Категория",
            "Дата покупки", "Цена", "Статус"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)
    
    def refresh_data(self):
        """Обновить данные в таблице"""
        equipment_list = self.db.get_all_equipment()
        
        # Обновляем список категорий в фильтре
        categories = set()
        for eq in equipment_list:
            if eq.get('category'):
                categories.add(eq['category'])
        
        current_category = self.category_filter.currentData()
        self.category_filter.clear()
        self.category_filter.addItem("Все категории", None)
        for cat in sorted(categories):
            self.category_filter.addItem(cat, cat)
        
        # Восстанавливаем выбор категории
        if current_category:
            for i in range(self.category_filter.count()):
                if self.category_filter.itemData(i) == current_category:
                    self.category_filter.setCurrentIndex(i)
                    break
        
        self.apply_filters()
        self.equipment_updated.emit()
    
    def apply_filters(self):
        """Применить фильтры к таблице"""
        equipment_list = self.db.get_all_equipment()
        
        # Фильтрация
        search_text = self.search_edit.text().strip().lower()
        category_filter = self.category_filter.currentData()
        status_filter = self.status_filter.currentData()
        
        filtered_list = []
        for equipment in equipment_list:
            # Поиск по тексту
            if search_text:
                if (search_text not in equipment['inventory_number'].lower() and
                    search_text not in equipment['name'].lower()):
                    continue
            
            # Фильтр по категории
            if category_filter and equipment.get('category') != category_filter:
                continue
            
            # Фильтр по статусу
            if status_filter and equipment.get('status') != status_filter:
                continue
            
            filtered_list.append(equipment)
        
        # Отображаем отфильтрованные данные
        self.table.setRowCount(len(filtered_list))
        
        for row, equipment in enumerate(filtered_list):
            self.table.setItem(row, 0, QTableWidgetItem(str(equipment['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(equipment['inventory_number']))
            self.table.setItem(row, 2, QTableWidgetItem(equipment['name']))
            self.table.setItem(row, 3, QTableWidgetItem(equipment['category'] or ''))
            
            # Форматирование даты
            date_text = equipment['purchase_date'] or ''
            self.table.setItem(row, 4, QTableWidgetItem(date_text))
            
            # Форматирование цены
            price = equipment['purchase_price'] or '0'
            try:
                price_decimal = Decimal(str(price))
                price_text = f"{price_decimal:,.2f}".replace(',', ' ')
            except:
                price_text = str(price)
            price_item = QTableWidgetItem(price_text)
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.table.setItem(row, 5, price_item)
            
            # Форматирование статуса
            status = equipment['status']
            status_text = {
                'active': 'Активное',
                'in_repair': 'В ремонте',
                'written_off': 'Списано',
                'reserved': 'Резерв'
            }.get(status, status)
            self.table.setItem(row, 6, QTableWidgetItem(status_text))
    
    def search_equipment(self):
        """Поиск оборудования по инвентарному номеру"""
        inventory_number = self.search_edit.text().strip()
        if not inventory_number:
            QMessageBox.warning(self, "Ошибка", "Введите инвентарный номер для поиска")
            return
        
        equipment = self.db.get_equipment_by_inventory(inventory_number)
        if equipment:
            # Находим строку в таблице
            for row in range(self.table.rowCount()):
                if self.table.item(row, 1).text() == inventory_number:
                    self.table.selectRow(row)
                    self.table.scrollToItem(self.table.item(row, 0))
                    break
        else:
            QMessageBox.information(self, "Результат поиска", 
                                  f"Оборудование с инвентарным номером '{inventory_number}' не найдено")
    
    def clear_search(self):
        """Очистить поиск и фильтры"""
        self.search_edit.clear()
        self.category_filter.setCurrentIndex(0)
        self.status_filter.setCurrentIndex(0)
        self.apply_filters()
    
    def add_equipment(self):
        """Добавить новое оборудование"""
        dialog = EquipmentDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data['inventory_number'] or not data['name']:
                QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
                return
            
            try:
                equipment_id = self.db.add_equipment(**data)
                app_logger.log_equipment_action(
                    "Добавлено",
                    equipment_id=equipment_id,
                    inventory_number=data['inventory_number'],
                    details=f"Категория: {data.get('category', 'N/A')}"
                )
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Оборудование добавлено")
            except ValueError as e:
                app_logger.log_error("Добавление оборудования", str(e))
                QMessageBox.warning(self, "Ошибка", str(e))
    
    def edit_equipment(self):
        """Редактировать оборудование"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите оборудование для редактирования")
            return
        
        equipment_id = int(self.table.item(current_row, 0).text())
        equipment = self.db.get_equipment_by_inventory(
            self.table.item(current_row, 1).text()
        )
        
        if equipment:
            dialog = EquipmentDialog(self, equipment)
            if dialog.exec():
                data = dialog.get_data()
                if not data['inventory_number'] or not data['name']:
                    QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
                    return
                
                try:
                    self.db.update_equipment(equipment_id, **data)
                    app_logger.log_equipment_action(
                        "Обновлено",
                        equipment_id=equipment_id,
                        inventory_number=data.get('inventory_number', 'N/A')
                    )
                    self.refresh_data()
                    QMessageBox.information(self, "Успех", "Оборудование обновлено")
                except Exception as e:
                    app_logger.log_error("Обновление оборудования", str(e), f"ID: {equipment_id}")
                    QMessageBox.warning(self, "Ошибка", f"Ошибка обновления: {str(e)}")
    
    def delete_equipment(self):
        """Удалить оборудование"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите оборудование для удаления")
            return
        
        equipment_id = int(self.table.item(current_row, 0).text())
        inventory_number = self.table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить оборудование "{inventory_number}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_equipment(equipment_id)
                app_logger.log_equipment_action(
                    "Удалено",
                    equipment_id=equipment_id,
                    inventory_number=inventory_number
                )
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Оборудование удалено")
            except Exception as e:
                app_logger.log_error("Удаление оборудования", str(e), f"ID: {equipment_id}")
                QMessageBox.warning(self, "Ошибка", f"Ошибка удаления: {str(e)}")
    
    def export_data(self):
        """Экспорт данных оборудования в CSV"""
        if self.table.rowCount() == 0:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для экспорта")
            return
        
        filename = ExportManager.get_export_filename(self, "equipment")
        if filename:
            if ExportManager.export_table_to_csv(self.table, filename):
                app_logger.log_report_action("Экспорт оборудования", f"Файл: {filename}")
                QMessageBox.information(self, "Успех", f"Данные экспортированы в {filename}")
            else:
                app_logger.log_error("Экспорт оборудования", "Не удалось экспортировать данные")
                QMessageBox.warning(self, "Ошибка", "Не удалось экспортировать данные")
    
    def import_data(self):
        """Импорт данных оборудования из CSV"""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Импорт данных добавит новое оборудование в базу.\n'
            'Оборудование с существующими инвентарными номерами будет пропущено.\n\n'
            'Продолжить?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            imported, errors, warnings = ImportManager.import_equipment_from_csv(self.db, self)
            ImportManager.show_import_results(self, imported, errors, warnings)
            
            if imported > 0:
                app_logger.log_equipment_action(
                    "Импорт",
                    details=f"Импортировано {imported} записей"
                )
                self.refresh_data()
