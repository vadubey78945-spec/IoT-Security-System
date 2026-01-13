"""
Simplified Runner - Use if main.py has issues
"""
from dashboard.web_server import app
import webbrowser
import threading
import time

def run_simulations():
    """Run background simulations"""
    from simulation.iot_simulator import IoTDeviceSimulator
    from simulation.attack_simulator import AttackSimulator
    
    iot_sim = IoTDeviceSimulator(num_devices=8)
    attack_sim = AttackSimulator()
    
    # Run in background
    def run_iot():
        while True:
            iot_sim.simulate_activity()
            time.sleep(5)
    
    def run_attack():
        while True:
            attack_sim.generate_attack()
            time.sleep(25)
    
    threading.Thread(target=run_iot, daemon=True).start()
    threading.Thread(target=run_attack, daemon=True).start()

if __name__ == "__main__":
    print("🚀 Starting IoT Security System...")
    print("📊 Dashboard: http://localhost:5000")
    
    # Start simulations
    run_simulations()
    
    # Open browser
    time.sleep(2)
    webbrowser.open("http://localhost:5000")
    
    # Run app
    app.run(host='0.0.0.0', port=5000, debug=True)