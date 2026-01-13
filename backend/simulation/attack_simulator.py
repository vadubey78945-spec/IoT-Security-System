"""
Attack Simulator
"""
import time
import random
from datetime import datetime
import config

class AttackSimulator:
    def __init__(self):
        self.attack_log = []
        print("⚔️ Attack Simulator initialized")
    
    def generate_attack(self):
        """Generate simulated attack"""
        attack_type = random.choice(config.ATTACK_TYPES)
        attack = {
            'id': f"ATT{len(self.attack_log)+1:04d}",
            'type': attack_type,
            'source': f"10.0.0.{random.randint(1, 255)}",
            'target': f"192.168.1.{random.randint(10, 100)}",
            'time': datetime.now().strftime("%H:%M:%S"),
            'severity': random.choice(['Low', 'Medium', 'High']),
            'status': 'Active'
        }
        
        self.attack_log.append(attack)
        
        # Log attack
        self._log_attack(attack)
        
        return attack
    
    def _log_attack(self, attack):
        """Log attack to file"""
        log_msg = f"[{attack['time']}] {attack['type']} from {attack['source']}\n"
        try:
            with open('logs/attacks.log', 'a') as f:
                f.write(log_msg)
        except:
            pass
    
    def get_recent_attacks(self):
        """Get recent attacks"""
        return self.attack_log[-10:] if self.attack_log else []