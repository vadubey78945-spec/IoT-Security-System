"""
AI Threat Detection Agent
"""
import random
from datetime import datetime

from config import RISK_HIGH, RISK_MEDIUM, ANOMALY_THRESHOLD, ATTACK_TYPES


class ThreatDetector:
    def __init__(self):
        self.threats = []
        self.threat_count = 0
        print("⚠️ Threat Detector initialized")
    
    def analyze_traffic(self, traffic_data=None):
        """Analyze traffic for threats"""
        self.threat_count += 1
        
        # Simulate threat detection (30% chance)
        if random.random() < 0.3:
            threat_types = config.ATTACK_TYPES
            threat = {
                'id': f"THR{self.threat_count:04d}",
                'type': random.choice(threat_types),
                'source': f"10.0.0.{random.randint(1, 255)}",
                'target': f"192.168.1.{random.randint(10, 250)}",
                'severity': random.choice(['Low', 'Medium', 'High', 'Critical']),
                'timestamp': datetime.now().strftime("%H:%M:%S"),
                'status': 'Detected'
            }
            self.threats.append(threat)
            
            # Log threat
            self._log_threat(threat)
            return threat
        
        return None
    
    def _log_threat(self, threat):
        """Log threat to file"""
        log_msg = f"[{threat['timestamp']}] {threat['type']} from {threat['source']} to {threat['target']}\n"
        try:
            with open('logs/threats.log', 'a') as f:
                f.write(log_msg)
        except:
            pass
    
    def get_recent_threats(self, count=10):
        """Get recent threats"""
        return self.threats[-count:] if self.threats else []
    
    def get_threat_stats(self):
        """Get threat statistics"""
        severities = {}
        for threat in self.threats:
            sev = threat['severity']
            severities[sev] = severities.get(sev, 0) + 1
        
        return {
            'total': len(self.threats),
            'today': len([t for t in self.threats if 'timestamp' in t and 
                         datetime.now().strftime("%H:%M") in t['timestamp']]),
            'severities': severities,
            'active_threats': len([t for t in self.threats if t.get('status') == 'Detected'])
        }