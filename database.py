"""
Модуль для работы с базой данных SQLite
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from decimal import Decimal


class Database:
    """Класс для работы с базой данных оборудования"""
    
    def __init__(self, db_path: str = "equipment.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Получить соединение с базой данных"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            # Включаем проверку внешних ключей
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            raise ConnectionError(f"Ошибка подключения к базе данных: {e}")
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Таблица оборудования
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventory_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                category TEXT,
                purchase_date DATE,
                purchase_price DECIMAL,
                current_location TEXT,
                status TEXT DEFAULT 'active'
            )
        """)
        
        # Индекс для быстрого поиска по инвентарному номеру
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_inventory_number 
            ON equipment(inventory_number)
        """)
        
        # Таблица технического обслуживания
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS maintenance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER NOT NULL,
                maintenance_date DATE NOT NULL,
                type TEXT NOT NULL,
                cost DECIMAL DEFAULT 0,
                description TEXT,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
            )
        """)
        
        # Индекс для быстрого поиска обслуживания по оборудованию
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_maintenance_equipment 
            ON maintenance(equipment_id)
        """)
        
        # Таблица назначений/перемещений
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                equipment_id INTEGER NOT NULL,
                assigned_to TEXT NOT NULL,
                department TEXT,
                start_date DATE NOT NULL,
                end_date DATE,
                FOREIGN KEY (equipment_id) REFERENCES equipment(id)
            )
        """)
        
        # Индекс для быстрого поиска назначений
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_assignments_equipment 
            ON assignments(equipment_id)
        """)
        
        conn.commit()
        conn.close()
    
    # Методы для работы с оборудованием
    def add_equipment(self, inventory_number: str, name: str, category: str = None,
                     purchase_date: str = None, purchase_price: Decimal = None,
                     current_location: str = None, status: str = 'active') -> int:
        """Добавить новое оборудование"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO equipment 
                (inventory_number, name, category, purchase_date, purchase_price, 
                 current_location, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (inventory_number, name, category, purchase_date, 
                  str(purchase_price) if purchase_price else None,
                  current_location, status))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise ValueError(f"Оборудование с инвентарным номером {inventory_number} уже существует")
        finally:
            conn.close()
    
    def get_equipment_by_inventory(self, inventory_number: str) -> Optional[Dict]:
        """Получить оборудование по инвентарному номеру (оптимизировано для < 1 сек)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM equipment WHERE inventory_number = ?
        """, (inventory_number,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return dict(row)
        return None
    
    def get_all_equipment(self) -> List[Dict]:
        """Получить все оборудование"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM equipment ORDER BY inventory_number")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def update_equipment(self, equipment_id: int, **kwargs):
        """Обновить данные оборудования"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Формируем динамический запрос
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['inventory_number', 'name', 'category', 'purchase_date',
                      'purchase_price', 'current_location', 'status']:
                fields.append(f"{key} = ?")
                if key == 'purchase_price' and value is not None:
                    values.append(str(value))
                else:
                    values.append(value)
        
        if fields:
            values.append(equipment_id)
            query = f"UPDATE equipment SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            conn.commit()
        
        conn.close()
    
    def delete_equipment(self, equipment_id: int):
        """Удалить оборудование"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM equipment WHERE id = ?", (equipment_id,))
        conn.commit()
        conn.close()
    
    # Методы для работы с обслуживанием
    def add_maintenance(self, equipment_id: int, maintenance_date: str, 
                       type: str, cost: Decimal = None, description: str = None) -> int:
        """Добавить запись о техническом обслуживании"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO maintenance 
            (equipment_id, maintenance_date, type, cost, description)
            VALUES (?, ?, ?, ?, ?)
        """, (equipment_id, maintenance_date, type, 
              str(cost) if cost else '0', description))
        conn.commit()
        maintenance_id = cursor.lastrowid
        conn.close()
        return maintenance_id
    
    def get_maintenance_by_equipment(self, equipment_id: int) -> List[Dict]:
        """Получить все обслуживания для оборудования"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM maintenance 
            WHERE equipment_id = ? 
            ORDER BY maintenance_date DESC
        """, (equipment_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_maintenance_report(self, start_date: str = None, 
                              end_date: str = None) -> List[Dict]:
        """Получить отчет по техническому обслуживанию (оптимизировано для < 5 сек)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT m.*, e.inventory_number, e.name, e.category
                FROM maintenance m
                JOIN equipment e ON m.equipment_id = e.id
                WHERE m.maintenance_date BETWEEN ? AND ?
                ORDER BY m.maintenance_date DESC
            """, (start_date, end_date))
        else:
            cursor.execute("""
                SELECT m.*, e.inventory_number, e.name, e.category
                FROM maintenance m
                JOIN equipment e ON m.equipment_id = e.id
                ORDER BY m.maintenance_date DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Методы для работы с назначениями
    def add_assignment(self, equipment_id: int, assigned_to: str, 
                      department: str = None, start_date: str = None,
                      end_date: str = None) -> int:
        """Добавить назначение оборудования"""
        if not start_date:
            start_date = datetime.now().strftime('%Y-%m-%d')
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Закрываем предыдущее назначение, если оно есть
        if end_date is None:
            cursor.execute("""
                UPDATE assignments 
                SET end_date = ? 
                WHERE equipment_id = ? AND end_date IS NULL
            """, (start_date, equipment_id))
        
        cursor.execute("""
            INSERT INTO assignments 
            (equipment_id, assigned_to, department, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        """, (equipment_id, assigned_to, department, start_date, end_date))
        
        # Обновляем текущее местоположение оборудования
        location = f"{assigned_to}" + (f" ({department})" if department else "")
        cursor.execute("""
            UPDATE equipment 
            SET current_location = ? 
            WHERE id = ?
        """, (location, equipment_id))
        
        conn.commit()
        assignment_id = cursor.lastrowid
        conn.close()
        return assignment_id
    
    def get_assignments_by_equipment(self, equipment_id: int) -> List[Dict]:
        """Получить историю назначений для оборудования"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM assignments 
            WHERE equipment_id = ? 
            ORDER BY start_date DESC
        """, (equipment_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    # Методы для отчетов
    def get_depreciation_report(self) -> List[Dict]:
        """Отчет по амортизации оборудования"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                e.id,
                e.inventory_number,
                e.name,
                e.category,
                e.purchase_date,
                e.purchase_price,
                e.status,
                COALESCE(SUM(CAST(m.cost AS DECIMAL)), 0) as total_maintenance_cost,
                CASE 
                    WHEN e.purchase_date IS NOT NULL 
                    THEN CAST(julianday('now') - julianday(e.purchase_date) AS INTEGER)
                    ELSE 0
                END as days_in_use
            FROM equipment e
            LEFT JOIN maintenance m ON e.id = m.equipment_id
            GROUP BY e.id
            ORDER BY e.inventory_number
        """)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    
    def get_maintenance_cost_report(self, start_date: str = None, 
                                    end_date: str = None) -> Dict:
        """Отчет по стоимости содержания оборудования"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if start_date and end_date:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_maintenances,
                    SUM(CAST(cost AS DECIMAL)) as total_cost,
                    AVG(CAST(cost AS DECIMAL)) as avg_cost
                FROM maintenance
                WHERE maintenance_date BETWEEN ? AND ?
            """, (start_date, end_date))
        else:
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_maintenances,
                    SUM(CAST(cost AS DECIMAL)) as total_cost,
                    AVG(CAST(cost AS DECIMAL)) as avg_cost
                FROM maintenance
            """)
        
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {}

