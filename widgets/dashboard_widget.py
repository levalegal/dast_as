"""
Виджет дашборда со статистикой
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QGroupBox, QGridLayout, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from database import Database
from decimal import Decimal


class DashboardWidget(QWidget):
    """Виджет дашборда с общей статистикой"""
    
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()
        self.refresh_data()
    
    def init_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Заголовок
        title = QLabel("Общая статистика")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Сетка со статистикой
        stats_grid = QGridLayout()
        
        # Группа "Оборудование"
        equipment_group = QGroupBox("Оборудование")
        equipment_layout = QVBoxLayout()
        
        self.total_equipment_label = QLabel("Всего: 0")
        self.total_equipment_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        equipment_layout.addWidget(self.total_equipment_label)
        
        self.active_equipment_label = QLabel("Активное: 0")
        equipment_layout.addWidget(self.active_equipment_label)
        
        self.in_repair_label = QLabel("В ремонте: 0")
        equipment_layout.addWidget(self.in_repair_label)
        
        self.written_off_label = QLabel("Списано: 0")
        equipment_layout.addWidget(self.written_off_label)
        
        equipment_group.setLayout(equipment_layout)
        stats_grid.addWidget(equipment_group, 0, 0)
        
        # Группа "Обслуживание"
        maintenance_group = QGroupBox("Техническое обслуживание")
        maintenance_layout = QVBoxLayout()
        
        self.total_maintenance_label = QLabel("Всего обслуживаний: 0")
        self.total_maintenance_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        maintenance_layout.addWidget(self.total_maintenance_label)
        
        self.total_maintenance_cost_label = QLabel("Общая стоимость: 0.00")
        maintenance_layout.addWidget(self.total_maintenance_cost_label)
        
        self.avg_maintenance_cost_label = QLabel("Средняя стоимость: 0.00")
        maintenance_layout.addWidget(self.avg_maintenance_cost_label)
        
        maintenance_group.setLayout(maintenance_layout)
        stats_grid.addWidget(maintenance_group, 0, 1)
        
        # Группа "Назначения"
        assignments_group = QGroupBox("Назначения")
        assignments_layout = QVBoxLayout()
        
        self.total_assignments_label = QLabel("Всего назначений: 0")
        self.total_assignments_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        assignments_layout.addWidget(self.total_assignments_label)
        
        self.active_assignments_label = QLabel("Активных: 0")
        assignments_layout.addWidget(self.active_assignments_label)
        
        assignments_group.setLayout(assignments_layout)
        stats_grid.addWidget(assignments_group, 1, 0)
        
        # Группа "Финансы"
        finance_group = QGroupBox("Финансы")
        finance_layout = QVBoxLayout()
        
        self.total_purchase_cost_label = QLabel("Общая стоимость покупок: 0.00")
        self.total_purchase_cost_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        finance_layout.addWidget(self.total_purchase_cost_label)
        
        self.total_maintenance_finance_label = QLabel("Общая стоимость ТО: 0.00")
        finance_layout.addWidget(self.total_maintenance_finance_label)
        
        finance_group.setLayout(finance_layout)
        stats_grid.addWidget(finance_group, 1, 1)
        
        layout.addLayout(stats_grid)
        
        # Кнопка обновления
        refresh_btn = QPushButton("Обновить статистику")
        refresh_btn.clicked.connect(self.refresh_data)
        layout.addWidget(refresh_btn)
        
        layout.addStretch()
    
    def refresh_data(self):
        """Обновить статистику"""
        # Статистика по оборудованию
        equipment_list = self.db.get_all_equipment()
        total_equipment = len(equipment_list)
        
        status_counts = {'active': 0, 'in_repair': 0, 'written_off': 0, 'reserved': 0}
        total_purchase_cost = Decimal(0)
        
        for eq in equipment_list:
            status = eq.get('status', 'active')
            if status in status_counts:
                status_counts[status] += 1
            
            price = eq.get('purchase_price')
            if price:
                try:
                    total_purchase_cost += Decimal(str(price))
                except:
                    pass
        
        self.total_equipment_label.setText(f"Всего: {total_equipment}")
        self.active_equipment_label.setText(f"Активное: {status_counts['active']}")
        self.in_repair_label.setText(f"В ремонте: {status_counts['in_repair']}")
        self.written_off_label.setText(f"Списано: {status_counts['written_off']}")
        
        # Статистика по обслуживанию
        maintenance_summary = self.db.get_maintenance_cost_report()
        total_maintenance = maintenance_summary.get('total_maintenances', 0) or 0
        total_maintenance_cost = Decimal(maintenance_summary.get('total_cost', 0) or 0)
        avg_maintenance_cost = Decimal(maintenance_summary.get('avg_cost', 0) or 0)
        
        self.total_maintenance_label.setText(f"Всего обслуживаний: {total_maintenance}")
        self.total_maintenance_cost_label.setText(f"Общая стоимость: {total_maintenance_cost:.2f}")
        self.avg_maintenance_cost_label.setText(f"Средняя стоимость: {avg_maintenance_cost:.2f}")
        
        # Статистика по назначениям
        all_equipment = self.db.get_all_equipment()
        total_assignments = 0
        active_assignments = 0
        
        for eq in all_equipment:
            assignments = self.db.get_assignments_by_equipment(eq['id'])
            total_assignments += len(assignments)
            for assignment in assignments:
                if not assignment.get('end_date'):
                    active_assignments += 1
        
        self.total_assignments_label.setText(f"Всего назначений: {total_assignments}")
        self.active_assignments_label.setText(f"Активных: {active_assignments}")
        
        # Финансы
        self.total_purchase_cost_label.setText(f"Общая стоимость покупок: {total_purchase_cost:.2f}")
        self.total_maintenance_finance_label.setText(f"Общая стоимость ТО: {total_maintenance_cost:.2f}")
