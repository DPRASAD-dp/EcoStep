import sqlite3
from datetime import datetime
from typing import Dict, Any, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

DB_PATH = "ocr_results.db"

def init_db():
    """Initialize the database and create tables if they don't exist"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                carbon_footprint REAL,
                quantity INTEGER,
                category TEXT,
                current_date TEXT
            )
            ''')
            conn.commit()
            logging.info("Database initialized successfully")
    except Exception as e:
        logging.error(f"Failed to initialize database: {e}")

def insert_into_db(entry: Dict[str, Any]) -> bool:
    """Insert a record into the database"""
    try:
        # Normalize values and handle potential type errors
        item_name = str(entry.get('item_name', 'N/A'))
        
        # Convert carbon_footprint to float
        try:
            carbon_footprint = float(entry.get('carbon_footprint', 0))
        except (ValueError, TypeError):
            carbon_footprint = 0.0
            logging.warning(f"Invalid carbon_footprint value for '{item_name}', using 0.0")
        
        # Convert quantity to int
        try:
            quantity = int(float(entry.get('quantity', 1)))
        except (ValueError, TypeError):
            quantity = 1
            logging.warning(f"Invalid quantity value for '{item_name}', using 1")
        
        category = str(entry.get('category', 'Unknown'))
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO receipts (item_name, carbon_footprint, quantity, category, current_date)
            VALUES (?, ?, ?, ?, ?)
            ''', (item_name, carbon_footprint, quantity, category, current_date))
            conn.commit()
            
            # Log successful insertion
            logging.info(f"Inserted into database: {item_name}, carbon: {carbon_footprint}, qty: {quantity}")
            return True
    except Exception as e:
        logging.error(f"Failed to insert into database: {e}")
        return False

def get_db_records(limit=50) -> List:
    """Retrieve records from the database"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM receipts ORDER BY id DESC LIMIT ?", (limit,))
            return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error fetching database records: {e}")
        return []