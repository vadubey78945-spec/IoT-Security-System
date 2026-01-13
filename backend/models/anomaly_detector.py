"""
Anomaly Detection Model
"""
import random

class AnomalyDetector:
    def __init__(self):
        print("🤖 Anomaly Detector initialized")
    
    def detect(self, traffic_data):
        """Detect anomalies in traffic"""
        # Simulate AI detection
        if random.random() < 0.25:  # 25% chance of anomaly
            return {
                'is_anomaly': True,
                'confidence': random.uniform(0.7, 0.95),
                'type': random.choice(['Traffic Spike', 'Unusual Port', 'Suspicious Pattern']),
                'details': 'AI detected unusual network behavior'
            }
        
        return {
            'is_anomaly': False,
            'confidence': random.uniform(0.1, 0.3),
            'type': 'Normal',
            'details': 'Traffic patterns normal'
        }