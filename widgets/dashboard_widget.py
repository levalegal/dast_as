"""
Виджет дашборда со статистикой
Современный дизайн с карточками статистики
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
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(layout)
        
        # Заголовок с улучшенным дизайном
        header_layout = QHBoxLayout()
        title = QLabel("📊 Общая статистика")
        title.setProperty("class", "title")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2196F3; padding: 10px 0px;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Сетка со статистикой - улучшенная компоновка
        stats_grid = QGridLayout()
        stats_grid.setSpacing(20)
        
        # Карточка "Оборудование"
        equipment_group = QGroupBox("📦 Оборудование")
        equipment_group.setProperty("class", "stat-card-equipment")
        equipment_layout = QVBoxLayout()
        equipment_layout.setSpacing(12)
        equipment_layout.setContentsMargins(20, 30, 20, 20)
        
        self.total_equipment_label = QLabel("0")
        self.total_equipment_label.setProperty("class", "stat-value-equipment")
        equipment_layout.addWidget(self.total_equipment_label)
        
        total_label = QLabel("Всего единиц оборудования")
        total_label.setProperty("class", "stat-label")
        equipment_layout.addWidget(total_label)
        
        equipment_layout.addSpacing(16)
        
        # Детали по статусам
        status_container = QVBoxLayout()
        status_container.setSpacing(8)
        
        self.active_equipment_label = QLabel("✓ Активное: 0")
        self.active_equipment_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #4CAF50; padding: 4px;")
        status_container.addWidget(self.active_equipment_label)
        
        self.in_repair_label = QLabel("🔧 В ремонте: 0")
        self.in_repair_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #FF9800; padding: 4px;")
        status_container.addWidget(self.in_repair_label)
        
        self.written_off_label = QLabel("✗ Списано: 0")
        self.written_off_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #757575; padding: 4px;")
        status_container.addWidget(self.written_off_label)
        
        equipment_layout.addLayout(status_container)
        equipment_group.setLayout(equipment_layout)
        stats_grid.addWidget(equipment_group, 0, 0)
        
        # Карточка "Обслуживание"
        maintenance_group = QGroupBox("🔧 Техническое обслуживание")
        maintenance_group.setProperty("class", "stat-card-maintenance")
        maintenance_layout = QVBoxLayout()
        maintenance_layout.setSpacing(12)
        maintenance_layout.setContentsMargins(20, 30, 20, 20)
        
        self.total_maintenance_label = QLabel("0")
        self.total_maintenance_label.setProperty("class", "stat-value-maintenance")
        maintenance_layout.addWidget(self.total_maintenance_label)
        
        maintenance_count_label = QLabel("Всего обслуживаний")
        maintenance_count_label.setProperty("class", "stat-label")
        maintenance_layout.addWidget(maintenance_count_label)
        
        maintenance_layout.addSpacing(16)
        
        self.total_maintenance_cost_label = QLabel("💰 Общая стоимость: 0.00 ₽")
        self.total_maintenance_cost_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #00BCD4; padding: 4px;")
        maintenance_layout.addWidget(self.total_maintenance_cost_label)
        
        self.avg_maintenance_cost_label = QLabel("📊 Средняя стоимость: 0.00 ₽")
        self.avg_maintenance_cost_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #00BCD4; padding: 4px;")
        maintenance_layout.addWidget(self.avg_maintenance_cost_label)
        
        maintenance_group.setLayout(maintenance_layout)
        stats_grid.addWidget(maintenance_group, 0, 1)
        
        # Карточка "Назначения"
        assignments_group = QGroupBox("👥 Назначения")
        assignments_group.setProperty("class", "stat-card-assignments")
        assignments_layout = QVBoxLayout()
        assignments_layout.setSpacing(12)
        assignments_layout.setContentsMargins(20, 30, 20, 20)
        
        self.total_assignments_label = QLabel("0")
        self.total_assignments_label.setProperty("class", "stat-value-assignments")
        assignments_layout.addWidget(self.total_assignments_label)
        
        assignments_count_label = QLabel("Всего назначений")
        assignments_count_label.setProperty("class", "stat-label")
        assignments_layout.addWidget(assignments_count_label)
        
        assignments_layout.addSpacing(16)
        
        self.active_assignments_label = QLabel("✓ Активных: 0")
        self.active_assignments_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #FF9800; padding: 4px;")
        assignments_layout.addWidget(self.active_assignments_label)
        
        assignments_group.setLayout(assignments_layout)
        stats_grid.addWidget(assignments_group, 1, 0)
        
        # Карточка "Финансы"
        finance_group = QGroupBox("💵 Финансы")
        finance_group.setProperty("class", "stat-card-finance")
        finance_layout = QVBoxLayout()
        finance_layout.setSpacing(12)
        finance_layout.setContentsMargins(20, 30, 20, 20)
        
        self.total_purchase_cost_label = QLabel("0.00 ₽")
        self.total_purchase_cost_label.setProperty("class", "stat-value-finance")
        finance_layout.addWidget(self.total_purchase_cost_label)
        
        purchase_label = QLabel("Общая стоимость покупок")
        purchase_label.setProperty("class", "stat-label")
        finance_layout.addWidget(purchase_label)
        
        finance_layout.addSpacing(16)
        
        self.total_maintenance_finance_label = QLabel("🔧 Стоимость ТО: 0.00 ₽")
        self.total_maintenance_finance_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #FFC107; padding: 4px;")
        finance_layout.addWidget(self.total_maintenance_finance_label)
        
        finance_group.setLayout(finance_layout)
        stats_grid.addWidget(finance_group, 1, 1)
        
        layout.addLayout(stats_grid)
        
        # Кнопка обновления с улучшенным дизайном
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        refresh_btn = QPushButton("🔄 Обновить статистику")
        refresh_btn.setProperty("class", "secondary-button")
        refresh_btn.setStyleSheet("padding: 12px 32px; font-size: 14px; font-weight: 600;")
        refresh_btn.clicked.connect(self.refresh_data)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
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
        
        self.total_equipment_label.setText(str(total_equipment))
        self.active_equipment_label.setText(f"✓ Активное: {status_counts['active']}")
        self.in_repair_label.setText(f"🔧 В ремонте: {status_counts['in_repair']}")
        self.written_off_label.setText(f"✗ Списано: {status_counts['written_off']}")
        
        # Статистика по обслуживанию
        maintenance_summary = self.db.get_maintenance_cost_report()
        total_maintenance = maintenance_summary.get('total_maintenances', 0) or 0
        total_maintenance_cost = Decimal(maintenance_summary.get('total_cost', 0) or 0)
        avg_maintenance_cost = Decimal(maintenance_summary.get('avg_cost', 0) or 0)
        
        self.total_maintenance_label.setText(str(total_maintenance))
        self.total_maintenance_cost_label.setText(f"💰 Общая стоимость: {total_maintenance_cost:,.2f} ₽".replace(',', ' '))
        self.avg_maintenance_cost_label.setText(f"📊 Средняя стоимость: {avg_maintenance_cost:,.2f} ₽".replace(',', ' '))
        
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
        
        self.total_assignments_label.setText(str(total_assignments))
        self.active_assignments_label.setText(f"✓ Активных: {active_assignments}")
        
        # Финансы
        self.total_purchase_cost_label.setText(f"{total_purchase_cost:,.2f} ₽".replace(',', ' '))
        self.total_maintenance_finance_label.setText(f"🔧 Стоимость ТО: {total_maintenance_cost:,.2f} ₽".replace(',', ' '))