from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import asyncio
import json
import uvicorn
import random
import time
import threading

from contextlib import asynccontextmanager
from fastapi import FastAPI

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    asyncio.create_task(simulate_background_activity())
    print("=" * 60)
    print("🚀 Guardian AI IoT Security System STARTED!")
    print("📊 API: http://localhost:8000")
    print("🔧 Test: http://localhost:8000/api/test")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("=" * 60)
    yield
    # Shutdown
    print("🛑 System shutting down...")

# Create app with lifespan
app = FastAPI(title="Guardian AI IoT Security", version="1.0.0", lifespan=lifespan)

# 🔧 FIXED CORS - Allow Vite port 5173
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (no MongoDB needed)
devices_db = []
threats_db = []
actions_db = []
websocket_connections = []

# Data Models
class Device(BaseModel):
    id: str
    name: str
    ip: str
    mac: str
    type: str
    vendor: str = "Unknown"
    firmware: str = "1.0.0"
    risk_score: float = 0.0
    ports: List[int] = []
    last_seen: str
    status: str = "online"

class Threat(BaseModel):
    id: str
    type: str
    severity: str
    device_id: str
    description: str
    confidence: float
    timestamp: str
    status: str = "active"

class Action(BaseModel):
    id: str
    action_type: str
    target: str
    description: str
    timestamp: str
    status: str = "completed"

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo for testing
            await websocket.send_text(f"Message received: {data}")
    except:
        websocket_connections.remove(websocket)

# 🔧 API Routes
@app.get("/")
async def root():
    return {
        "message": "Guardian AI IoT Security System",
        "status": "running",
        "version": "1.0.0",
        "endpoints": ["/api/devices", "/api/threats", "/api/actions", "/api/stats", "/api/test"]
    }

# 🔧 TEST ENDPOINT - ADDED HERE
@app.get("/api/test")
async def test_connection():
    return {
        "status": "connected", 
        "message": "Backend is working!",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/devices")
async def get_devices():
    return devices_db

@app.get("/api/threats")
async def get_threats():
    return threats_db

@app.get("/api/actions")
async def get_actions():
    return actions_db

@app.get("/api/stats")
async def get_stats():
    high_risk = len([d for d in devices_db if d.get("risk_score", 0) > 0.7])
    active_threats = len([t for t in threats_db if t.get("status") == "active"])
    
    return {
        "total_devices": len(devices_db),
        "protected_devices": len(devices_db) - high_risk,
        "active_threats": active_threats,
        "threats_blocked": len(actions_db),
        "system_health": 95.5,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/scan")
async def trigger_scan():
    # Generate simulated devices
    device_types = ["Smart TV", "Security Camera", "Smart Bulb", "Thermostat", 
                    "Smart Speaker", "Router", "Phone", "Laptop", "IoT Hub"]
    vendors = ["Philips", "Nest", "Ring", "Samsung", "Apple", "Google", "Amazon"]
    
    devices_db.clear()
    for i in range(random.randint(5, 12)):
        device = {
            "id": f"device_{i}",
            "name": f"{random.choice(device_types)} {i}",
            "ip": f"192.168.1.{100 + i}",
            "mac": f"00:1A:2B:3C:4D:{i:02X}",
            "type": random.choice(device_types),
            "vendor": random.choice(vendors),
            "firmware": f"v{random.randint(1, 5)}.{random.randint(0, 9)}",
            "risk_score": random.uniform(0.1, 0.95),
            "ports": random.sample([80, 443, 8080, 22, 23], random.randint(1, 3)),
            "last_seen": datetime.now().isoformat(),
            "status": random.choice(["online", "online", "online", "offline"])
        }
        devices_db.append(device)
    
    # Generate random threats
    if random.random() > 0.5:
        threat = {
            "id": f"threat_{int(time.time())}",
            "type": random.choice(["Port Scan", "Brute Force", "Malware", "Data Exfiltration", "DDoS"]),
            "severity": random.choice(["high", "critical", "medium"]),
            "device_id": random.choice(devices_db)["id"] if devices_db else "unknown",
            "description": f"Suspicious activity detected on port {random.choice([80, 443, 22, 8080])}",
            "confidence": random.uniform(0.7, 0.99),
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        threats_db.append(threat)
        
        # Auto-generate action
        action = {
            "id": f"action_{int(time.time())}",
            "action_type": "block",
            "target": threat["device_id"],
            "description": f"Automatically blocked {threat['device_id']} due to {threat['type']}",
            "timestamp": datetime.now().isoformat(),
            "status": "completed"
        }
        actions_db.append(action)
    
    # Notify WebSocket clients
    for conn in websocket_connections:
        try:
            await conn.send_json({
                "type": "scan_complete",
                "devices_found": len(devices_db),
                "threats_found": len(threats_db)
            })
        except:
            pass
    
    return {
        "message": "Network scan completed",
        "devices_found": len(devices_db),
        "threats_detected": len(threats_db)
    }

@app.post("/api/block/{device_id}")
async def block_device(device_id: str):
    # Find and update device
    for device in devices_db:
        if device["id"] == device_id:
            device["status"] = "blocked"
            device["risk_score"] = 1.0
            break
    
    # Create action
    action = {
        "id": f"action_{int(time.time())}",
        "action_type": "manual_block",
        "target": device_id,
        "description": f"Manually blocked device {device_id}",
        "timestamp": datetime.now().isoformat(),
        "status": "completed"
    }
    actions_db.append(action)
    
    return {"message": f"Device {device_id} blocked successfully"}

@app.post("/api/threats/{threat_id}/resolve")
async def resolve_threat(threat_id: str):
    for threat in threats_db:
        if threat["id"] == threat_id:
            threat["status"] = "resolved"
            break
    
    return {"message": f"Threat {threat_id} resolved"}

# Background threat simulation
async def simulate_background_activity():
    """Simulate real-time updates"""
    while True:
        # Occasionally add new threat
        if random.random() > 0.8 and devices_db:
            threat = {
                "id": f"threat_bg_{int(time.time())}",
                "type": random.choice(["Port Scan", "Suspicious Traffic", "Unauthorized Access"]),
                "severity": random.choice(["low", "medium"]),
                "device_id": random.choice(devices_db)["id"],
                "description": f"Background security event detected",
                "confidence": random.uniform(0.4, 0.7),
                "timestamp": datetime.now().isoformat(),
                "status": "active"
            }
            threats_db.append(threat)
            
            # Notify WebSocket
            for conn in websocket_connections:
                try:
                    await conn.send_json({
                        "type": "threat_alert",
                        "data": threat
                    })
                except:
                    pass
        
        # Update device status occasionally
        if devices_db and random.random() > 0.9:
            device = random.choice(devices_db)
            old_score = device["risk_score"]
            device["risk_score"] = min(1.0, old_score + random.uniform(-0.1, 0.2))
            device["last_seen"] = datetime.now().isoformat()
        
        await asyncio.sleep(10)  # Update every 10 seconds

@app.on_event("startup")
async def startup_event():
    # Start background simulation
    asyncio.create_task(simulate_background_activity())
    print("=" * 60)
    print("🚀 Guardian AI IoT Security System STARTED!")
    print("📊 API: http://localhost:8000")
    print("🔧 Test: http://localhost:8000/api/test")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("=" * 60)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)