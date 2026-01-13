"""
Web Dashboard Server
"""
from flask import Flask, render_template, jsonify
import json
from datetime import datetime
import random

app = Flask(__name__)

# Initialize agents
from agents.discovery_agent import DiscoveryAgent
from agents.threat_detector import ThreatDetector
from agents.deception_agent import DeceptionAgent
from agents.defense_agent import DefenseAgent
from simulation.iot_simulator import IoTDeviceSimulator
from models.risk_scorer import RiskScorer

discovery = DiscoveryAgent()
threat_detector = ThreatDetector()
deception = DeceptionAgent()
defense = DefenseAgent()
iot_sim = IoTDeviceSimulator(num_devices=8)
risk_scorer = RiskScorer()

# Global stats
system_stats = {
    'start_time': datetime.now().strftime("%H:%M:%S"),
    'total_scans': 0,
    'total_threats': 0
}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/dashboard')
def get_dashboard():
    """Get dashboard data"""
    # Update stats
    system_stats['total_scans'] += 1
    
    # Get device data
    devices = iot_sim.get_devices()
    
    # Calculate risks for devices
    for device in devices:
        risk = risk_scorer.calculate_risk(device)
        device['risk_score'] = risk['score']
        device['risk_level'] = risk['level']
    
    # Get threats
    threats = threat_detector.get_recent_threats(5)
    system_stats['total_threats'] = len(threats)
    
    # Get deception status
    deception_status = deception.get_status()
    
    # Get defense status
    defense_status = defense.get_defense_status()
    
    # Calculate summary
    high_risk = len([d for d in devices if d.get('risk_score', 0) > 0.7])
    medium_risk = len([d for d in devices if 0.4 <= d.get('risk_score', 0) <= 0.7])
    low_risk = len([d for d in devices if d.get('risk_score', 0) < 0.4])
    
    # Simulate a threat detection occasionally
    if random.random() < 0.3:  # 30% chance
        threat_detector.analyze_traffic()
    
    # Simulate defense action occasionally
    if random.random() < 0.2:  # 20% chance
        defense.simulate_defense()
    
    # Check honeypots
    honeypot_alerts = deception.check_interactions()
    
    return jsonify({
        'status': 'active',
        'system': system_stats,
        'devices': {
            'total': len(devices),
            'online': len([d for d in devices if d.get('status') == 'Online']),
            'high_risk': high_risk,
            'medium_risk': medium_risk,
            'low_risk': low_risk,
            'list': devices[-10:]  # Last 10 devices
        },
        'threats': {
            'total': system_stats['total_threats'],
            'recent': threats,
            'active': len([t for t in threats if t.get('status') == 'Detected'])
        },
        'deception': deception_status,
        'defense': defense_status,
        'honeypot_alerts': honeypot_alerts[-5:] if honeypot_alerts else [],
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })

@app.route('/api/scan')
def trigger_scan():
    """Trigger manual scan"""
    new_devices = discovery.scan_network()
    return jsonify({
        'status': 'success',
        'new_devices': len(new_devices),
        'message': f'Found {len(new_devices)} new devices'
    })

@app.route('/api/devices')
def get_all_devices():
    """Get all devices"""
    devices = iot_sim.get_devices()
    return jsonify(devices)

@app.route('/api/threats')
def get_all_threats():
    """Get all threats"""
    threats = threat_detector.get_recent_threats(20)
    return jsonify(threats)

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'discovery': 'active',
            'threat_detector': 'active',
            'deception': 'active',
            'defense': 'active',
            'dashboard': 'active'
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)