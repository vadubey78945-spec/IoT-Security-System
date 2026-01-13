"""
Autonomous Defense Agent
"""
import random
from datetime import datetime

class DefenseAgent:
    def __init__(self):
        self.blocked_ips = []
        self.firewall_rules = []
        self.actions = []
        print("🛡️ Defense Agent initialized")
    
    def respond_to_threat(self, threat):
        """Respond to detected threat"""
        actions = []
        
        # Block source IP
        if threat['source'].startswith('10.0.0.'):
            self.blocked_ips.append(threat['source'])
            actions.append(f"Blocked IP {threat['source']}")
        
        # Create firewall rule
        rule = {
            'id': f"RULE{len(self.firewall_rules)+1:04d}",
            'action': 'BLOCK',
            'source': threat['source'],
            'target': threat['target'],
            'reason': threat['type'],
            'time': datetime.now().strftime("%H:%M:%S")
        }
        self.firewall_rules.append(rule)
        
        # Log action
        action_log = {
            'time': datetime.now().strftime("%H:%M:%S"),
            'threat': threat['type'],
            'actions': actions,
            'status': 'Mitigated'
        }
        self.actions.append(action_log)
        
        # Update threat status
        threat['status'] = 'Mitigated'
        threat['mitigated_at'] = datetime.now().strftime("%H:%M:%S")
        
        return actions
    
    def get_defense_status(self):
        """Get current defense status"""
        return {
            'blocked_ips': self.blocked_ips[-10:],  # Last 10 blocked IPs
            'total_rules': len(self.firewall_rules),
            'recent_actions': self.actions[-5:] if self.actions else [],
            'active_defenses': len(self.blocked_ips)
        }
    
    def simulate_defense(self):
        """Simulate defense action"""
        if random.random() < 0.4:  # 40% chance of defense action
            threat = {
                'type': 'Simulated Attack',
                'source': f"10.0.0.{random.randint(1, 255)}",
                'target': f"192.168.1.{random.randint(10, 250)}",
                'severity': random.choice(['Medium', 'High'])
            }
            return self.respond_to_threat(threat)
        return []