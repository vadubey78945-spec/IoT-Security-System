"""
Configuration for IoT Security System
"""
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
DB_PATH = os.path.join(BASE_DIR, 'iot_security.db')

# Simulation Settings
SIMULATED_NETWORK = "192.168.1.0/24"
MAX_DEVICES = 50
SCAN_INTERVAL = 30

# Risk Thresholds
RISK_HIGH = 0.7
RISK_MEDIUM = 0.4
RISK_LOW = 0.1

# Device Types
DEVICE_TYPES = [
    "Smart TV", "Security Camera", "Smart Bulb", "Thermostat",
    "Smart Speaker", "Refrigerator", "Smart Lock", "Robot Vacuum",
    "Fitness Tracker", "Smart Plug"
]

# Attack Types
ATTACK_TYPES = [
    "Port Scan", "Brute Force", "DDoS", "Malware",
    "Data Theft", "Credential Attack", "Botnet"
]

# Honeypot Settings
HONEYPOT_PORTS = [8080, 8443, 2323]
HONEYTOKEN_FILES = ["config_backup.zip", "admin_passwords.txt"]

# AI Model Settings
ANOMALY_THRESHOLD = 0.8
MODEL_UPDATE_INTERVAL = 300  # 5 minutes