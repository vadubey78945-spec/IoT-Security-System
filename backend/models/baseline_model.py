"""
Behavioral Baseline Model
"""
import random

class BaselineModel:
    def __init__(self):
        self.device_baselines = {}
    
    def create_baseline(self, device_id, metrics):
        """Create baseline for device"""
        baseline = {
            'packet_rate': random.uniform(10, 100),
            'bytes_per_min': random.uniform(1000, 10000),
            'active_hours': list(range(8, 22)),  # 8 AM to 10 PM
            'normal_ports': [80, 443, 53],
            'created': '2024-01-01'
        }
        self.device_baselines[device_id] = baseline
        return baseline
    
    def check_anomaly(self, device_id, current_metrics):
        """Check for anomalies"""
        if device_id not in self.device_baselines:
            return 0.0, "No baseline"
        
        # Simulate anomaly detection
        anomaly_score = random.random()
        if anomaly_score > 0.7:
            return anomaly_score, "High anomaly detected"
        elif anomaly_score > 0.4:
            return anomaly_score, "Medium anomaly"
        else:
            return anomaly_score, "Normal"