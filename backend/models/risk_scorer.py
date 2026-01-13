"""
Risk Scoring Model
"""
import random

class RiskScorer:
    def __init__(self):
        self.device_risks = {}
    
    def calculate_risk(self, device_info):
        """Calculate risk score for device"""
        risk = 0.0
        
        # Device type risk
        device_type = device_info.get('type', '')
        if 'Camera' in device_type or 'Lock' in device_type:
            risk += 0.3
        elif 'Thermostat' in device_type or 'Speaker' in device_type:
            risk += 0.2
        else:
            risk += 0.1
        
        # Firmware risk
        firmware = device_info.get('firmware', 'v1.0')
        if firmware < 'v3.0':
            risk += 0.2
        
        # Vulnerabilities
        vulns = device_info.get('vulnerabilities', [])
        risk += len(vulns) * 0.15
        
        # Add some randomness
        risk += random.uniform(-0.1, 0.1)
        
        # Ensure between 0 and 1
        risk = max(0.0, min(1.0, risk))
        
        # Determine level
        if risk >= 0.7:
            level = "CRITICAL"
        elif risk >= 0.5:
            level = "HIGH"
        elif risk >= 0.3:
            level = "MEDIUM"
        else:
            level = "LOW"
        
        return {
            'score': round(risk, 2),
            'level': level,
            'factors': {
                'device_type': device_type,
                'firmware': firmware,
                'vulnerabilities': len(vulns)
            }
        }