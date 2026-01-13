"""
IoT Device Discovery Agent
"""
import random
from datetime import datetime
import config

class DiscoveryAgent:
    def __init__(self):
        self.devices = []
        print("🔍 Discovery Agent initialized")
    
    def scan_network(self):
        """Simulate network scan"""
        new_devices = []
        
        # Simulate finding 1-3 new devices
        for i in range(random.randint(1, 3)):
            device = self._create_device()
            self.devices.append(device)
            new_devices.append(device)
        
        return new_devices
    
    def _create_device(self):
        """Create simulated IoT device"""
        device_types = config.DEVICE_TYPES
        vendors = ["Philips", "Samsung", "Google", "Amazon", "Xiaomi"]
        
        return {
            'id': f"DEV{random.randint(1000, 9999)}",
            'name': f"{random.choice(vendors)} {random.choice(device_types)}",
            'ip': f"192.168.1.{random.randint(10, 250)}",
            'mac': ':'.join(f"{random.randint(0,255):02x}" for _ in range(6)),
            'type': random.choice(device_types),
            'vendor': random.choice(vendors),
            'firmware': f"v{random.randint(1,4)}.{random.randint(0,9)}",
            'risk_score': random.uniform(0.1, 0.9),
            'vulnerabilities': random.sample(["Old Firmware", "Open Port", "Weak Auth"], 
                                           random.randint(0, 2)),
            'discovered': datetime.now().strftime("%H:%M:%S")
        }
    
    def get_devices(self):
        """Get all discovered devices"""
        return self.devices
    
    def get_risk_summary(self):
        """Get risk summary"""
        high = len([d for d in self.devices if d['risk_score'] > 0.7])
        medium = len([d for d in self.devices if 0.4 <= d['risk_score'] <= 0.7])
        low = len([d for d in self.devices if d['risk_score'] < 0.4])
        
        return {
            'total': len(self.devices),
            'high_risk': high,
            'medium_risk': medium,
            'low_risk': low,
            'devices': self.devices[-10:]  # Last 10 devices
        }