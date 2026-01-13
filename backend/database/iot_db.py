"""
Simple SQLite Database
"""
import sqlite3
import json
from datetime import datetime
import os

def initialize_database():
    """Initialize the database"""
    try:
        conn = sqlite3.connect('iot_security.db')
        cursor = conn.cursor()
        
        # Create devices table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            id TEXT PRIMARY KEY,
            name TEXT,
            ip TEXT,
            type TEXT,
            risk_score REAL,
            discovered TEXT
        )
        ''')
        
        # Create threats table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS threats (
            id TEXT PRIMARY KEY,
            type TEXT,
            source TEXT,
            target TEXT,
            severity TEXT,
            timestamp TEXT,
            status TEXT
        )
        ''')
        
        # Create actions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            target TEXT,
            timestamp TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"⚠️ Database initialization error: {e}")

# Note: The system will work even without database
# This is a simplified version for hackathon