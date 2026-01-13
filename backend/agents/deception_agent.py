"""
Deception Agent - Honeypots & Honeytokens
"""
import random
from datetime import datetime
import config

class DeceptionAgent:
    def __init__(self):
        self.honeypots = []
        self.honeytokens = []
        self.deploy_honeypots()
        print("🎣 Deception Agent initialized")
    
    def deploy_honeypots(self):
        """Deploy honeypot devices"""
        honeypot_names = [
            "Fake Security Camera", "Fake Smart Lock", 
            "Fake Thermostat", "Fake IoT Hub"
        ]
        
        for i in range(3):
            self.honeypots.append({
                'id': f"HONEYPOT{i+1:03d}",
                'name': random.choice(honeypot_names),
                'ip': f"192.168.1.{150 + i}",
                'ports': random.sample(config.HONEYPOT_PORTS, 2),
                'deployed': datetime.now().strftime("%H:%M:%S"),
                'interactions': 0
            })
        
        # Deploy honeytokens
        self.honeytokens = config.HONEYTOKEN_FILES.copy()
        
        return self.honeypots
    
    def check_interactions(self):
        """Check honeypot interactions"""
        alerts = []
        
        for honeypot in self.honeypots:
            # 20% chance of interaction
            if random.random() < 0.2:
                honeypot['interactions'] += 1
                alert = {
                    'honeypot': honeypot['name'],
                    'attacker': f"10.0.0.{random.randint(1, 255)}",
                    'time': datetime.now().strftime("%H:%M:%S"),
                    'action': random.choice(['Port Scan', 'Login Attempt', 'Exploit Try'])
                }
                alerts.append(alert)
        
        return alerts
    
    def get_status(self):
        """Get deception status"""
        return {
            'honeypots': self.honeypots,
            'honeytokens': self.honeytokens,
            'total_interactions': sum(h['interactions'] for h in self.honeypots)
        }