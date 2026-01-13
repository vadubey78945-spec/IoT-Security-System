"""
IoT Device Simulator
"""
import time
import random
from datetime import datetime
import config

class IoTDeviceSimulator:
    def __init__(self, num_devices=8):
        self.devices = []
        self.create_devices(num_devices)
        print(f"📱 Created {num_devices} IoT devices")
    
    def create_devices(self, num_devices):
        """Create simulated IoT devices"""
        for i in range(num_devices):
            device = {
                'id': f"DEV{i+1:03d}",
                'name': f"{random.choice(['Philips', 'Samsung', 'Google'])} {random.choice(config.DEVICE_TYPES)}",
                'ip': f"192.168.1.{i+10}",
                'type': random.choice(config.DEVICE_TYPES),
                'status': 'Online',
                'last_active': datetime.now().strftime("%H:%M:%S"),
                'activity': random.randint(10, 100)
            }
            self.devices.append(device)
    
    def simulate_activity(self):
        """Simulate device activity"""
        while True:
            for device in self.devices:
                # Update activity
                device['activity'] = random.randint(10, 100)
                device['last_active'] = datetime.now().strftime("%H:%M:%S")
                
                # Occasionally change status
                if random.random() < 0.05:  # 5% chance
                    device['status'] = random.choice(['Online', 'Offline', 'Busy'])
            
            time.sleep(10)  # Update every 10 seconds
    
    def get_devices(self):
        """Get current device states"""
        return self.devices