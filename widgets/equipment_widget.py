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
        form.addRow("Инвентарный номер *:", self.inventory_number_edit)
        
        # Наименование
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Название оборудования")
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
        
        # Группа поиска
        search_group = QGroupBox("Поиск оборудования")
        search_layout = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Введите инвентарный номер...")
        self.search_edit.returnPressed.connect(self.search_equipment)
        search_layout.addWidget(QLabel("Инвентарный номер:"))
        search_layout.addWidget(self.search_edit)
        
        self.search_btn = QPushButton("Найти")
        self.search_btn.clicked.connect(self.search_equipment)
        search_layout.addWidget(self.search_btn)
        
        self.clear_search_btn = QPushButton("Очистить")
        self.clear_search_btn.clicked.connect(self.clear_search)
        search_layout.addWidget(self.clear_search_btn)
        
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
        self.table.setRowCount(len(equipment_list))
        
        for row, equipment in enumerate(equipment_list):
            self.table.setItem(row, 0, QTableWidgetItem(str(equipment['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(equipment['inventory_number']))
            self.table.setItem(row, 2, QTableWidgetItem(equipment['name']))
            self.table.setItem(row, 3, QTableWidgetItem(equipment['category'] or ''))
            self.table.setItem(row, 4, QTableWidgetItem(equipment['purchase_date'] or ''))
            price = equipment['purchase_price'] or '0'
            self.table.setItem(row, 5, QTableWidgetItem(str(price)))
            self.table.setItem(row, 6, QTableWidgetItem(equipment['status']))
        
        self.equipment_updated.emit()
    
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
        """Очистить поиск"""
        self.search_edit.clear()
        self.refresh_data()
    
    def add_equipment(self):
        """Добавить новое оборудование"""
        dialog = EquipmentDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            if not data['inventory_number'] or not data['name']:
                QMessageBox.warning(self, "Ошибка", "Заполните обязательные поля")
                return
            
            try:
                self.db.add_equipment(**data)
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Оборудование добавлено")
            except ValueError as e:
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
                    self.refresh_data()
                    QMessageBox.information(self, "Успех", "Оборудование обновлено")
                except Exception as e:
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
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Оборудование удалено")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Ошибка удаления: {str(e)}")
