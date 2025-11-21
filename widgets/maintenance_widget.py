"""
Виджет для работы с техническим обслуживанием
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QComboBox, QLabel,
                             QDialog, QFormLayout, QDateEdit, QLineEdit,
                             QMessageBox, QHeaderView, QGroupBox, QTextEdit)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QDoubleValidator
from decimal import Decimal
from database import Database
from utils.logger import app_logger


class MaintenanceDialog(QDialog):
    """Диалог для добавления записи о техническом обслуживании"""
    
    def __init__(self, parent=None, db=None, maintenance_data=None):
        super().__init__(parent)
        self.db = db
        self.maintenance_data = maintenance_data
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса диалога"""
        if self.maintenance_data:
            self.setWindowTitle("Редактировать обслуживание")
        else:
            self.setWindowTitle("Добавить обслуживание")
        
        self.setModal(True)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        form = QFormLayout()
        
        # Оборудование
        self.equipment_combo = QComboBox()
        equipment_list = self.db.get_all_equipment()
        if not equipment_list:
            QMessageBox.warning(self, "Предупреждение", 
                              "Нет доступного оборудования. Сначала добавьте оборудование в реестр.")
        else:
            for eq in equipment_list:
                self.equipment_combo.addItem(
                    f"{eq['inventory_number']} - {eq['name']}",
                    eq['id']
                )
        form.addRow("Оборудование *:", self.equipment_combo)
        
        # Дата обслуживания
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDate(QDate.currentDate())
        form.addRow("Дата обслуживания *:", self.date_edit)
        
        # Тип обслуживания
        self.type_combo = QComboBox()
        self.type_combo.setEditable(True)
        self.type_combo.addItems([
            "Плановое ТО",
            "Внеплановое ТО",
            "Ремонт",
            "Калибровка",
            "Проверка",
            "Замена расходных материалов",
            "Другое"
        ])
        form.addRow("Тип обслуживания *:", self.type_combo)
        
        # Стоимость
        self.cost_edit = QLineEdit()
        self.cost_edit.setPlaceholderText("0.00")
        validator = QDoubleValidator(0, 999999999, 2)
        self.cost_edit.setValidator(validator)
        form.addRow("Стоимость:", self.cost_edit)
        
        # Описание
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        form.addRow("Описание:", self.description_edit)
        
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
        if self.maintenance_data:
            equipment_id = self.maintenance_data.get('equipment_id')
            for i in range(self.equipment_combo.count()):
                if self.equipment_combo.itemData(i) == equipment_id:
                    self.equipment_combo.setCurrentIndex(i)
                    break
            
            date = self.maintenance_data.get('maintenance_date')
            if date:
                qdate = QDate.fromString(date, Qt.DateFormat.ISODate)
                if qdate.isValid():
                    self.date_edit.setDate(qdate)
            
            type_text = self.maintenance_data.get('type', '')
            index = self.type_combo.findText(type_text)
            if index >= 0:
                self.type_combo.setCurrentIndex(index)
            else:
                self.type_combo.setCurrentText(type_text)
            
            cost = self.maintenance_data.get('cost')
            if cost:
                self.cost_edit.setText(str(cost))
            
            self.description_edit.setPlainText(self.maintenance_data.get('description', ''))
    
    def get_data(self):
        """Получить данные из формы"""
        data = {
            'equipment_id': self.equipment_combo.currentData(),
            'maintenance_date': self.date_edit.date().toString(Qt.DateFormat.ISODate),
            'type': self.type_combo.currentText().strip(),
            'cost': None,
            'description': self.description_edit.toPlainText().strip() or None
        }
        
        cost_text = self.cost_edit.text().strip()
        if cost_text:
            try:
                data['cost'] = Decimal(cost_text)
            except:
                pass
        
        return data


class MaintenanceWidget(QWidget):
    """Виджет для управления техническим обслуживанием"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Группа фильтров
        filter_group = QGroupBox("Фильтры")
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Оборудование:"))
        self.equipment_filter = QComboBox()
        self.equipment_filter.addItem("Все", None)
        self.equipment_filter.currentIndexChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.equipment_filter)
        
        filter_layout.addStretch()
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("➕ Добавить обслуживание")
        self.add_btn.setProperty("class", "action-button")
        self.add_btn.clicked.connect(self.add_maintenance)
        buttons_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("✏️ Редактировать")
        self.edit_btn.clicked.connect(self.edit_maintenance)
        buttons_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("🗑️ Удалить")
        self.delete_btn.setProperty("class", "danger-button")
        self.delete_btn.clicked.connect(self.delete_maintenance)
        buttons_layout.addWidget(self.delete_btn)
        
        self.refresh_btn = QPushButton("🔄 Обновить")
        self.refresh_btn.setProperty("class", "secondary-button")
        self.refresh_btn.clicked.connect(self.refresh_data)
        buttons_layout.addWidget(self.refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Таблица обслуживания
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Оборудование", "Дата", "Тип", "Стоимость", "Описание"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        layout.addWidget(self.table)
    
    def refresh_equipment_list(self):
        """Обновить список оборудования в фильтре"""
        current_id = self.equipment_filter.currentData()
        self.equipment_filter.clear()
        self.equipment_filter.addItem("Все", None)
        
        equipment_list = self.db.get_all_equipment()
        for eq in equipment_list:
            self.equipment_filter.addItem(
                f"{eq['inventory_number']} - {eq['name']}",
                eq['id']
            )
        
        # Восстанавливаем выбор
        if current_id:
            for i in range(self.equipment_filter.count()):
                if self.equipment_filter.itemData(i) == current_id:
                    self.equipment_filter.setCurrentIndex(i)
                    break
    
    def refresh_data(self):
        """Обновить данные в таблице"""
        self.refresh_equipment_list()
        
        equipment_id = self.equipment_filter.currentData()
        
        if equipment_id:
            maintenance_list = self.db.get_maintenance_by_equipment(equipment_id)
        else:
            # Получаем все обслуживания
            maintenance_list = self.db.get_maintenance_report()
        
        self.table.setRowCount(len(maintenance_list))
        
        for row, maintenance in enumerate(maintenance_list):
            self.table.setItem(row, 0, QTableWidgetItem(str(maintenance['id'])))
            
            # Название оборудования
            if 'name' in maintenance:
                equipment_text = f"{maintenance.get('inventory_number', '')} - {maintenance.get('name', '')}"
            else:
                # Получаем оборудование по ID
                eq = self.db.get_all_equipment()
                eq_dict = {e['id']: e for e in eq}
                if maintenance['equipment_id'] in eq_dict:
                    e = eq_dict[maintenance['equipment_id']]
                    equipment_text = f"{e['inventory_number']} - {e['name']}"
                else:
                    equipment_text = f"ID: {maintenance['equipment_id']}"
            
            self.table.setItem(row, 1, QTableWidgetItem(equipment_text))
            self.table.setItem(row, 2, QTableWidgetItem(maintenance['maintenance_date']))
            self.table.setItem(row, 3, QTableWidgetItem(maintenance['type']))
            cost = maintenance.get('cost', '0') or '0'
            self.table.setItem(row, 4, QTableWidgetItem(str(cost)))
            description = maintenance.get('description', '') or ''
            self.table.setItem(row, 5, QTableWidgetItem(description[:50] + '...' if len(description) > 50 else description))
    
    def add_maintenance(self):
        """Добавить новое обслуживание"""
        equipment_list = self.db.get_all_equipment()
        if not equipment_list:
            QMessageBox.warning(self, "Ошибка", 
                              "Нет доступного оборудования. Сначала добавьте оборудование в реестр.")
            return
        
        dialog = MaintenanceDialog(self, self.db)
        if dialog.exec():
            data = dialog.get_data()
            if not data['type']:
                QMessageBox.warning(self, "Ошибка", "Заполните тип обслуживания")
                return
            
            if not data['equipment_id']:
                QMessageBox.warning(self, "Ошибка", "Выберите оборудование")
                return
            
            try:
                maintenance_id = self.db.add_maintenance(**data)
                app_logger.log_maintenance_action(
                    "Добавлено",
                    maintenance_id=maintenance_id,
                    equipment_id=data['equipment_id'],
                    details=f"Тип: {data['type']}, Дата: {data['maintenance_date']}"
                )
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Обслуживание добавлено")
            except Exception as e:
                app_logger.log_error("Добавление обслуживания", str(e))
                QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
    
    def edit_maintenance(self):
        """Редактировать обслуживание"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")
            return
        
        maintenance_id = int(self.table.item(current_row, 0).text())
        maintenance_data = self.db.get_maintenance_by_id(maintenance_id)
        
        if not maintenance_data:
            QMessageBox.warning(self, "Ошибка", "Запись не найдена")
            return
        
        dialog = MaintenanceDialog(self, self.db, maintenance_data)
        if dialog.exec():
            data = dialog.get_data()
            if not data['type']:
                QMessageBox.warning(self, "Ошибка", "Заполните тип обслуживания")
                return
            
            try:
                self.db.update_maintenance(maintenance_id, **data)
                app_logger.log_maintenance_action(
                    "Обновлено",
                    maintenance_id=maintenance_id,
                    equipment_id=data.get('equipment_id')
                )
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Обслуживание обновлено")
            except Exception as e:
                app_logger.log_error("Обновление обслуживания", str(e), f"ID: {maintenance_id}")
                QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
    
    def delete_maintenance(self):
        """Удалить обслуживание"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return
        
        maintenance_id = int(self.table.item(current_row, 0).text())
        equipment_text = self.table.item(current_row, 1).text()
        date_text = self.table.item(current_row, 2).text()
        
        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить обслуживание?\n\n'
            f'Оборудование: {equipment_text}\n'
            f'Дата: {date_text}',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_maintenance(maintenance_id)
                app_logger.log_maintenance_action(
                    "Удалено",
                    maintenance_id=maintenance_id
                )
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Обслуживание удалено")
            except Exception as e:
                app_logger.log_error("Удаление обслуживания", str(e), f"ID: {maintenance_id}")
                QMessageBox.warning(self, "Ошибка", f"Ошибка удаления: {str(e)}")
