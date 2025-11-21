"""
Виджет для работы с историей перемещений оборудования
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QComboBox, QLabel,
                             QDialog, QFormLayout, QDateEdit, QLineEdit,
                             QMessageBox, QHeaderView, QGroupBox)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from database import Database
from utils.logger import app_logger


class AssignmentDialog(QDialog):
    """Диалог для добавления назначения оборудования"""
    
    def __init__(self, parent=None, db=None, assignment_data=None):
        super().__init__(parent)
        self.db = db
        self.assignment_data = assignment_data
        self.init_ui()
    
    def init_ui(self):
        """Инициализация интерфейса диалога"""
        if self.assignment_data:
            self.setWindowTitle("Редактировать назначение")
        else:
            self.setWindowTitle("Добавить назначение")
        
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
        
        # Назначено кому
        self.assigned_to_edit = QLineEdit()
        self.assigned_to_edit.setPlaceholderText("ФИО сотрудника")
        form.addRow("Назначено кому *:", self.assigned_to_edit)
        
        # Отдел
        self.department_edit = QLineEdit()
        self.department_edit.setPlaceholderText("Название отдела")
        form.addRow("Отдел:", self.department_edit)
        
        # Дата начала
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setDate(QDate.currentDate())
        form.addRow("Дата начала *:", self.start_date_edit)
        
        # Дата окончания
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setDate(QDate())
        self.end_date_edit.setSpecialValueText("Текущее назначение")
        form.addRow("Дата окончания:", self.end_date_edit)
        
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
        if self.assignment_data:
            equipment_id = self.assignment_data.get('equipment_id')
            for i in range(self.equipment_combo.count()):
                if self.equipment_combo.itemData(i) == equipment_id:
                    self.equipment_combo.setCurrentIndex(i)
                    break
            
            self.assigned_to_edit.setText(self.assignment_data.get('assigned_to', ''))
            self.department_edit.setText(self.assignment_data.get('department', ''))
            
            start_date = self.assignment_data.get('start_date')
            if start_date:
                qdate = QDate.fromString(start_date, Qt.DateFormat.ISODate)
                if qdate.isValid():
                    self.start_date_edit.setDate(qdate)
            
            end_date = self.assignment_data.get('end_date')
            if end_date:
                qdate = QDate.fromString(end_date, Qt.DateFormat.ISODate)
                if qdate.isValid():
                    self.end_date_edit.setDate(qdate)
    
    def get_data(self):
        """Получить данные из формы"""
        end_date = None
        if self.end_date_edit.date().isValid() and not self.end_date_edit.date().isNull():
            end_date = self.end_date_edit.date().toString(Qt.DateFormat.ISODate)
        
        data = {
            'equipment_id': self.equipment_combo.currentData(),
            'assigned_to': self.assigned_to_edit.text().strip(),
            'department': self.department_edit.text().strip() or None,
            'start_date': self.start_date_edit.date().toString(Qt.DateFormat.ISODate),
            'end_date': end_date
        }
        
        return data


class AssignmentsWidget(QWidget):
    """Виджет для управления назначениями оборудования"""
    
    assignment_updated = pyqtSignal()
    
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
        
        self.add_btn = QPushButton("Добавить назначение")
        self.add_btn.clicked.connect(self.add_assignment)
        buttons_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("Редактировать")
        self.edit_btn.clicked.connect(self.edit_assignment)
        buttons_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("Удалить")
        self.delete_btn.clicked.connect(self.delete_assignment)
        buttons_layout.addWidget(self.delete_btn)
        
        self.view_btn = QPushButton("Просмотр истории")
        self.view_btn.clicked.connect(self.view_history)
        buttons_layout.addWidget(self.view_btn)
        
        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.refresh_data)
        buttons_layout.addWidget(self.refresh_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Таблица назначений
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Оборудование", "Назначено", "Отдел", "Дата начала", "Дата окончания"
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setAlternatingRowColors(True)
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
        
        # Получаем все назначения или фильтруем по оборудованию
        all_equipment = self.db.get_all_equipment()
        all_assignments = []
        
        for eq in all_equipment:
            if equipment_id is None or eq['id'] == equipment_id:
                assignments = self.db.get_assignments_by_equipment(eq['id'])
                for assignment in assignments:
                    assignment['equipment_name'] = f"{eq['inventory_number']} - {eq['name']}"
                    all_assignments.append(assignment)
        
        # Сортируем по дате начала
        all_assignments.sort(key=lambda x: x['start_date'] or '', reverse=True)
        
        self.table.setRowCount(len(all_assignments))
        
        for row, assignment in enumerate(all_assignments):
            self.table.setItem(row, 0, QTableWidgetItem(str(assignment['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(assignment.get('equipment_name', '')))
            self.table.setItem(row, 2, QTableWidgetItem(assignment['assigned_to']))
            self.table.setItem(row, 3, QTableWidgetItem(assignment.get('department', '') or ''))
            self.table.setItem(row, 4, QTableWidgetItem(assignment['start_date']))
            end_date = assignment.get('end_date') or 'Текущее'
            self.table.setItem(row, 5, QTableWidgetItem(end_date))
        
        self.assignment_updated.emit()
    
    def add_assignment(self):
        """Добавить новое назначение"""
        equipment_list = self.db.get_all_equipment()
        if not equipment_list:
            QMessageBox.warning(self, "Ошибка", 
                              "Нет доступного оборудования. Сначала добавьте оборудование в реестр.")
            return
        
        dialog = AssignmentDialog(self, self.db)
        if dialog.exec():
            data = dialog.get_data()
            if not data['assigned_to']:
                QMessageBox.warning(self, "Ошибка", "Заполните поле 'Назначено кому'")
                return
            
            if not data['equipment_id']:
                QMessageBox.warning(self, "Ошибка", "Выберите оборудование")
                return
            
            try:
                assignment_id = self.db.add_assignment(**data)
                app_logger.log_assignment_action(
                    "Добавлено",
                    assignment_id=assignment_id,
                    equipment_id=data['equipment_id'],
                    details=f"Назначено: {data['assigned_to']}, Отдел: {data.get('department', 'N/A')}"
                )
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Назначение добавлено")
            except Exception as e:
                app_logger.log_error("Добавление назначения", str(e))
                QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
    
    def edit_assignment(self):
        """Редактировать назначение"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для редактирования")
            return
        
        assignment_id = int(self.table.item(current_row, 0).text())
        assignment_data = self.db.get_assignment_by_id(assignment_id)
        
        if not assignment_data:
            QMessageBox.warning(self, "Ошибка", "Запись не найдена")
            return
        
        dialog = AssignmentDialog(self, self.db, assignment_data)
        if dialog.exec():
            data = dialog.get_data()
            if not data['assigned_to']:
                QMessageBox.warning(self, "Ошибка", "Заполните поле 'Назначено кому'")
                return
            
            try:
                self.db.update_assignment(assignment_id, **data)
                app_logger.log_assignment_action(
                    "Обновлено",
                    assignment_id=assignment_id,
                    equipment_id=data.get('equipment_id')
                )
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Назначение обновлено")
            except Exception as e:
                app_logger.log_error("Обновление назначения", str(e), f"ID: {assignment_id}")
                QMessageBox.warning(self, "Ошибка", f"Ошибка: {str(e)}")
    
    def delete_assignment(self):
        """Удалить назначение"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return
        
        assignment_id = int(self.table.item(current_row, 0).text())
        equipment_text = self.table.item(current_row, 1).text()
        assigned_to = self.table.item(current_row, 2).text()
        
        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить назначение?\n\n'
            f'Оборудование: {equipment_text}\n'
            f'Назначено: {assigned_to}',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_assignment(assignment_id)
                app_logger.log_assignment_action(
                    "Удалено",
                    assignment_id=assignment_id
                )
                self.refresh_data()
                QMessageBox.information(self, "Успех", "Назначение удалено")
            except Exception as e:
                app_logger.log_error("Удаление назначения", str(e), f"ID: {assignment_id}")
                QMessageBox.warning(self, "Ошибка", f"Ошибка удаления: {str(e)}")
    
    def view_history(self):
        """Просмотр истории назначений для выбранного оборудования"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для просмотра")
            return
        
        equipment_name = self.table.item(current_row, 1).text()
        # Получаем ID оборудования из названия
        equipment_id = None
        for eq in self.db.get_all_equipment():
            if f"{eq['inventory_number']} - {eq['name']}" == equipment_name:
                equipment_id = eq['id']
                break
        
        if equipment_id:
            assignments = self.db.get_assignments_by_equipment(equipment_id)
            history_text = f"История назначений для {equipment_name}:\n\n"
            for i, assignment in enumerate(assignments, 1):
                history_text += f"{i}. {assignment['assigned_to']}"
                if assignment.get('department'):
                    history_text += f" ({assignment['department']})"
                history_text += f"\n   С {assignment['start_date']}"
                if assignment.get('end_date'):
                    history_text += f" по {assignment['end_date']}"
                else:
                    history_text += " (текущее)"
                history_text += "\n\n"
            
            QMessageBox.information(self, "История назначений", history_text)
