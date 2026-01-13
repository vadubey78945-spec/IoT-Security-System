"""
Network Traffic Simulator
"""
import time
import random
import threading
from datetime import datetime, timedelta
import socket
import struct
from scapy.all import IP, TCP, UDP, ICMP, Ether
import config

class NetworkSimulator:
    def __init__(self):
        self.devices = []
        self.traffic_log = []
        self.simulation_running = False
        self.traffic_thread = None
        
    def add_device(self, device_info):
        """Add a device to the simulation"""
        self.devices.append({
            **device_info,
            'last_activity': datetime.now(),
            'traffic_stats': {
                'sent_packets': 0,
                'received_packets': 0,
                'sent_bytes': 0,
                'received_bytes': 0
            }
        })
    
    def start_simulation(self):
        """Start network traffic simulation"""
        if self.simulation_running:
            return
        
        self.simulation_running = True
        self.traffic_thread = threading.Thread(target=self._simulate_traffic, daemon=True)
        self.traffic_thread.start()
        print(f"[{datetime.now()}] 🌐 Network traffic simulation started")
    
    def stop_simulation(self):
        """Stop network traffic simulation"""
        self.simulation_running = False
        if self.traffic_thread:
            self.traffic_thread.join(timeout=2)
        print(f"[{datetime.now()}] 🌐 Network traffic simulation stopped")
    
    def _simulate_traffic(self):
        """Simulate network traffic between devices"""
        while self.simulation_running:
            if len(self.devices) < 2:
                time.sleep(5)
                continue
            
            # Generate random traffic between devices
            num_transactions = random.randint(1, 5)
            
            for _ in range(num_transactions):
                # Randomly select source and destination devices
                src_device = random.choice(self.devices)
                dst_device = random.choice([d for d in self.devices if d != src_device])
                
                # Generate traffic data
                traffic = self._generate_traffic(src_device, dst_device)
                
                if traffic:
                    self.traffic_log.append(traffic)
                    
                    # Update device stats
                    src_device['traffic_stats']['sent_packets'] += 1
                    src_device['traffic_stats']['sent_bytes'] += traffic.get('bytes', 0)
                    dst_device['traffic_stats']['received_packets'] += 1
                    dst_device['traffic_stats']['received_bytes'] += traffic.get('bytes', 0)
                    
                    # Keep log size manageable
                    if len(self.traffic_log) > 1000:
                        self.traffic_log = self.traffic_log[-500:]
            
            # Sleep before next traffic generation
            time.sleep(random.uniform(0.5, 2.0))
    
    def _generate_traffic(self, src_device, dst_device):
        """Generate simulated network traffic"""
        protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'DNS', 'DHCP']
        protocol = random.choice(protocols)
        
        # Common ports for protocols
        port_mapping = {
            'HTTP': 80,
            'HTTPS': 443,
            'DNS': 53,
            'DHCP': 67,
            'SSH': 22,
            'TELNET': 23
        }
        
        # Generate packet size based on protocol
        if protocol in ['HTTP', 'HTTPS']:
            packet_size = random.randint(500, 1500)
        elif protocol == 'DNS':
            packet_size = random.randint(100, 512)
        else:
            packet_size = random.randint(64, 1500)
        
        # Determine if this is normal or suspicious traffic
        is_suspicious = random.random() < 0.05  # 5% chance
        
        traffic = {
            'timestamp': datetime.now().isoformat(),
            'source_ip': src_device.get('ip', '192.168.1.100'),
            'source_mac': src_device.get('mac', '00:00:00:00:00:00'),
            'destination_ip': dst_device.get('ip', '192.168.1.101'),
            'destination_mac': dst_device.get('mac', '00:00:00:00:00:01'),
            'protocol': protocol,
            'port': port_mapping.get(protocol, random.randint(1024, 65535)),
            'bytes': packet_size,
            'is_suspicious': is_suspicious,
            'src_device_id': src_device.get('id', 'unknown'),
            'dst_device_id': dst_device.get('id', 'unknown')
        }
        
        # Add suspicious characteristics
        if is_suspicious:
            suspicious_types = [
                'Port Scan', 'Brute Force', 'Data Exfiltration',
                'Malware Beacon', 'DDoS', 'Credential Stuffing'
            ]
            traffic['suspicious_type'] = random.choice(suspicious_types)
            traffic['bytes'] = random.randint(10000, 50000)  # Larger packets
            traffic['port'] = random.choice([22, 23, 3389, 445, 8080])  # Suspicious ports
        
        return traffic
    
    def generate_port_scan(self, attacker_ip, target_network):
        """Simulate a port scan attack"""
        print(f"[{datetime.now()}] 🔍 Simulating port scan from {attacker_ip}")
        
        scan_traffic = []
        target_ip = target_network.rstrip('0') + str(random.randint(2, 254))
        
        # Scan common ports
        common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3389, 8080]
        
        for port in common_ports[:random.randint(5, 10)]:  # Scan 5-10 ports
            scan_traffic.append({
                'timestamp': datetime.now().isoformat(),
                'source_ip': attacker_ip,
                'destination_ip': target_ip,
                'protocol': 'TCP',
                'port': port,
                'bytes': 60,  # SYN packet size
                'is_suspicious': True,
                'suspicious_type': 'Port Scan',
                'flags': 'SYN'
            })
        
        self.traffic_log.extend(scan_traffic)
        return scan_traffic
    
    def generate_brute_force(self, attacker_ip, target_ip):
        """Simulate brute force attack"""
        print(f"[{datetime.now()}] 🔑 Simulating brute force attack from {attacker_ip}")
        
        attack_traffic = []
        port = random.choice([22, 23, 3389])  # SSH, Telnet, RDP
        
        for attempt in range(random.randint(10, 30)):
            attack_traffic.append({
                'timestamp': (datetime.now() + timedelta(seconds=attempt*0.1)).isoformat(),
                'source_ip': attacker_ip,
                'destination_ip': target_ip,
                'protocol': 'TCP',
                'port': port,
                'bytes': random.randint(100, 500),
                'is_suspicious': True,
                'suspicious_type': 'Brute Force',
                'credentials_attempt': f"user{attempt}:password{attempt}"
            })
        
        self.traffic_log.extend(attack_traffic)
        return attack_traffic
    
    def get_traffic_summary(self, minutes=5):
        """Get traffic summary for the last N minutes"""
        cutoff = datetime.now() - timedelta(minutes=minutes)
        
        recent_traffic = [
            t for t in self.traffic_log
            if datetime.fromisoformat(t['timestamp']) > cutoff
        ]
        
        if not recent_traffic:
            return {
                'total_packets': 0,
                'total_bytes': 0,
                'suspicious_packets': 0,
                'top_protocols': [],
                'top_sources': [],
                'top_destinations': []
            }
        
        # Calculate statistics
        total_packets = len(recent_traffic)
        total_bytes = sum(t.get('bytes', 0) for t in recent_traffic)
        suspicious_packets = sum(1 for t in recent_traffic if t.get('is_suspicious', False))
        
        # Count protocols
        protocol_counts = {}
        for traffic in recent_traffic:
            proto = traffic.get('protocol', 'Unknown')
            protocol_counts[proto] = protocol_counts.get(proto, 0) + 1
        
        top_protocols = sorted(protocol_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Count source IPs
        source_counts = {}
        for traffic in recent_traffic:
            src = traffic.get('source_ip', 'Unknown')
            source_counts[src] = source_counts.get(src, 0) + 1
        
        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Count destination IPs
        dest_counts = {}
        for traffic in recent_traffic:
            dst = traffic.get('destination_ip', 'Unknown')
            dest_counts[dst] = dest_counts.get(dst, 0) + 1
        
        top_destinations = sorted(dest_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_packets': total_packets,
            'total_bytes': total_bytes,
            'suspicious_packets': suspicious_packets,
            'suspicious_percentage': (suspicious_packets / total_packets * 100) if total_packets > 0 else 0,
            'top_protocols': top_protocols,
            'top_sources': top_sources,
            'top_destinations': top_destinations,
            'sample_traffic': recent_traffic[-10:] if recent_traffic else []
        }
    
    def get_device_traffic_stats(self, device_id):
        """Get traffic statistics for a specific device"""
        device_traffic = [
            t for t in self.traffic_log
            if t.get('src_device_id') == device_id or t.get('dst_device_id') == device_id
        ]
        
        sent = [t for t in device_traffic if t.get('src_device_id') == device_id]
        received = [t for t in device_traffic if t.get('dst_device_id') == device_id]
        
        return {
            'device_id': device_id,
            'total_packets': len(device_traffic),
            'sent_packets': len(sent),
            'received_packets': len(received),
            'total_bytes': sum(t.get('bytes', 0) for t in device_traffic),
            'sent_bytes': sum(t.get('bytes', 0) for t in sent),
            'received_bytes': sum(t.get('bytes', 0) for t in received),
            'suspicious_packets': sum(1 for t in device_traffic if t.get('is_suspicious', False)),
            'recent_traffic': device_traffic[-20:] if device_traffic else []
        }