import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [devices, setDevices] = useState([]);
  const [threats, setThreats] = useState([]);
  const [stats, setStats] = useState({
    total_devices: 0,
    active_threats: 0,
    system_health: 100
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch initial data
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      const [devicesRes, threatsRes, statsRes] = await Promise.all([
        fetch('/api/devices'),
        fetch('/api/threats'),
        fetch('/api/stats')
      ]);
      
      if (devicesRes.ok) setDevices(await devicesRes.json());
      if (threatsRes.ok) setThreats(await threatsRes.json());
      if (statsRes.ok) setStats(await statsRes.json());
      
      setError('');
    } catch (err) {
      setError('Cannot connect to backend. Make sure it\'s running on port 8000');
      console.error(err);
    }
  };

  const triggerScan = async () => {
    setIsLoading(true);
    try {
      const response = await fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      alert(`Scan completed! Found ${data.devices_found} devices and ${data.threats_detected} threats.`);
      fetchData();
    } catch (err) {
      alert('Scan failed: ' + err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const blockDevice = async (deviceId) => {
    if (window.confirm('Are you sure you want to block this device?')) {
      try {
        await fetch(`/api/block/${deviceId}`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        alert('Device blocked successfully!');
        fetchData();
      } catch (err) {
        alert('Failed to block device');
      }
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <h1>🛡️ Guardian AI IoT Security</h1>
          <div className="status-indicator">
            <span className="status-dot active"></span>
            <span>System Active</span>
          </div>
        </div>
        <button 
          className="scan-btn" 
          onClick={triggerScan}
          disabled={isLoading}
        >
          {isLoading ? '🔍 Scanning...' : '🔍 Scan Network'}
        </button>
      </header>

      {error && (
        <div className="error-alert">
          ⚠️ {error}
          <br />
          <small>Make sure to run: <code>python main.py</code> in the backend folder</small>
        </div>
      )}

      {/* Stats Cards */}
      <div className="stats-container">
        <div className="stat-card">
          <h3>Total Devices</h3>
          <p className="stat-value">{stats.total_devices}</p>
          <div className="stat-bar">
            <div className="stat-fill" style={{width: '100%'}}></div>
          </div>
        </div>
        
        <div className="stat-card">
          <h3>Protected</h3>
          <p className="stat-value">{stats.total_devices - threats.length}</p>
          <div className="stat-bar">
            <div 
              className="stat-fill green" 
              style={{width: `${((stats.total_devices - threats.length) / Math.max(stats.total_devices, 1)) * 100}%`}}
            ></div>
          </div>
        </div>
        
        <div className="stat-card">
          <h3>Active Threats</h3>
          <p className="stat-value red">{stats.active_threats}</p>
          <div className="stat-bar">
            <div 
              className="stat-fill red" 
              style={{width: `${Math.min(stats.active_threats * 20, 100)}%`}}
            ></div>
          </div>
        </div>
        
        <div className="stat-card">
          <h3>System Health</h3>
          <p className="stat-value">{stats.system_health}%</p>
          <div className="stat-bar">
            <div 
              className="stat-fill blue" 
              style={{width: `${stats.system_health}%`}}
            ></div>
          </div>
        </div>
      </div>

      {/* Devices Section */}
      <div className="section">
        <div className="section-header">
          <h2>📱 Connected Devices ({devices.length})</h2>
          <button className="refresh-btn" onClick={fetchData}>🔄 Refresh</button>
        </div>
        
        {devices.length === 0 ? (
          <div className="empty-state">
            <p>No devices found. Click "Scan Network" to discover devices.</p>
          </div>
        ) : (
          <div className="devices-grid">
            {devices.map((device) => (
              <div key={device.id} className="device-card">
                <div className="device-header">
                  <div className="device-icon">
                    {device.type?.includes('Camera') ? '📷' : 
                     device.type?.includes('TV') ? '📺' : 
                     device.type?.includes('Phone') ? '📱' : 
                     device.type?.includes('Laptop') ? '💻' : '🔌'}
                  </div>
                  <div className="device-info">
                    <h4>{device.name}</h4>
                    <p className="device-ip">{device.ip}</p>
                  </div>
                  <span className={`device-status ${device.status}`}>
                    {device.status}
                  </span>
                </div>
                
                <div className="device-details">
                  <div className="detail">
                    <span>Type:</span>
                    <span>{device.type}</span>
                  </div>
                  <div className="detail">
                    <span>Vendor:</span>
                    <span>{device.vendor}</span>
                  </div>
                  <div className="detail">
                    <span>Firmware:</span>
                    <span>{device.firmware}</span>
                  </div>
                </div>
                
                <div className="risk-section">
                  <div className="risk-label">
                    <span>Risk Score:</span>
                    <span className="risk-value">{(device.risk_score * 100).toFixed(0)}%</span>
                  </div>
                  <div className="risk-bar">
                    <div 
                      className={`risk-fill ${device.risk_score > 0.7 ? 'high' : device.risk_score > 0.4 ? 'medium' : 'low'}`}
                      style={{width: `${device.risk_score * 100}%`}}
                    ></div>
                  </div>
                </div>
                
                <button 
                  className={`block-btn ${device.status === 'blocked' ? 'blocked' : ''}`}
                  onClick={() => blockDevice(device.id)}
                  disabled={device.status === 'blocked'}
                >
                  {device.status === 'blocked' ? '🚫 Blocked' : '🛑 Block Device'}
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Threats Section */}
      {threats.length > 0 && (
        <div className="section">
          <div className="section-header">
            <h2>⚠️ Security Threats ({threats.length})</h2>
          </div>
          
          <div className="threats-list">
            {threats.slice(0, 5).map((threat) => (
              <div key={threat.id} className={`threat-card ${threat.severity}`}>
                <div className="threat-header">
                  <span className="threat-type">{threat.type}</span>
                  <span className={`threat-severity ${threat.severity}`}>
                    {threat.severity.toUpperCase()}
                  </span>
                </div>
                <p className="threat-desc">{threat.description}</p>
                <div className="threat-footer">
                  <span>Device: {threat.device_id}</span>
                  <span>Confidence: {(threat.confidence * 100).toFixed(0)}%</span>
                  <span>{new Date(threat.timestamp).toLocaleTimeString()}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="footer">
        <p>Guardian AI IoT Security System • Hackathon Edition</p>
        <div className="footer-links">
          <span>Backend: <a href="http://localhost:8000" target="_blank" rel="noreferrer">http://localhost:8000</a></span>
          <span>API Docs: <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">/docs</a></span>
          <span>Ports: Backend(8000) • Frontend(5173)</span>
        </div>
      </footer>
    </div>
  );
}

export default App;