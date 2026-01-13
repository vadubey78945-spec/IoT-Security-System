import React, { useState, useEffect } from 'react';
import { 
  Container, Grid, Paper, Typography, Card, CardContent, 
  Box, Chip, Button, LinearProgress, Alert, IconButton,
  Table, TableBody, TableCell, TableContainer, TableHead, 
  TableRow, AppBar, Toolbar, Drawer, List, ListItem, 
  ListItemIcon, ListItemText, Avatar, Badge, Fab,
  useMediaQuery, Dialog, DialogTitle, DialogContent,
  DialogActions, TextField, Snackbar
} from '@mui/material';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {
  Security as SecurityIcon,
  Devices as DevicesIcon,
  Warning as WarningIcon,
  Block as BlockIcon,
  Refresh as RefreshIcon,
  Settings as SettingsIcon,
  Dashboard as DashboardIcon,
  Timeline as TimelineIcon,
  NetworkCheck as NetworkIcon,
  Wifi as WifiIcon,
  CameraAlt as CameraIcon,
  Tv as TvIcon,
  Smartphone as PhoneIcon,
  Laptop as LaptopIcon,
  Notifications as NotificationsIcon,
  Menu as MenuIcon,
  DarkMode as DarkModeIcon,
  LightMode as LightModeIcon,
  Add as AddIcon,
  Delete as DeleteIcon
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: { main: '#00ff88' },
    secondary: { main: '#0088ff' },
    error: { main: '#ff4444' },
    warning: { main: '#ffaa44' },
    info: { main: '#44aaff' },
    success: { main: '#00cc88' },
    background: { default: '#0a1929', paper: '#1a252f' }
  }
});

function App() {
  const [devices, setDevices] = useState([]);
  const [threats, setThreats] = useState([]);
  const [actions, setActions] = useState([]);
  const [stats, setStats] = useState({
    total_devices: 0,
    protected_devices: 0,
    active_threats: 0,
    threats_blocked: 0,
    system_health: 100
  });
  const [darkMode, setDarkMode] = useState(true);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [scanning, setScanning] = useState(false);
  const [notification, setNotification] = useState(null);
  const isMobile = useMediaQuery('(max-width:600px)');

  // Fetch all data
  const fetchData = async () => {
    try {
      const [devicesRes, threatsRes, actionsRes, statsRes] = await Promise.all([
        fetch('/api/devices'),
        fetch('/api/threats'),
        fetch('/api/actions'),
        fetch('/api/stats')
      ]);
      
      if (devicesRes.ok) setDevices(await devicesRes.json());
      if (threatsRes.ok) setThreats(await threatsRes.json());
      if (actionsRes.ok) setActions(await actionsRes.json());
      if (statsRes.ok) setStats(await statsRes.json());
    } catch (error) {
      console.error('Error fetching data:', error);
      setNotification({ message: 'Error connecting to backend', severity: 'error' });
    }
  };

  // Initial load
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Update every 5 seconds
    return () => clearInterval(interval);
  }, []);

  // Trigger network scan
  const triggerScan = async () => {
    setScanning(true);
    try {
      const response = await fetch('/api/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      setNotification({ message: data.message, severity: 'success' });
      fetchData(); // Refresh data
    } catch (error) {
      setNotification({ message: 'Scan failed', severity: 'error' });
    } finally {
      setScanning(false);
    }
  };

  // Block device
  const blockDevice = async (deviceId) => {
    try {
      const response = await fetch(`/api/block/${deviceId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      setNotification({ message: data.message, severity: 'warning' });
      fetchData(); // Refresh data
    } catch (error) {
      setNotification({ message: 'Block failed', severity: 'error' });
    }
  };

  // Resolve threat
  const resolveThreat = async (threatId) => {
    try {
      const response = await fetch(`/api/threats/${threatId}/resolve`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      setNotification({ message: data.message, severity: 'info' });
      fetchData(); // Refresh data
    } catch (error) {
      setNotification({ message: 'Failed to resolve threat', severity: 'error' });
    }
  };

  // Get device icon
  const getDeviceIcon = (type) => {
    const typeLower = type.toLowerCase();
    if (typeLower.includes('camera')) return <CameraIcon />;
    if (typeLower.includes('tv')) return <TvIcon />;
    if (typeLower.includes('phone')) return <PhoneIcon />;
    if (typeLower.includes('laptop')) return <LaptopIcon />;
    if (typeLower.includes('router')) return <WifiIcon />;
    if (typeLower.includes('speaker')) return <SettingsIcon />;
    if (typeLower.includes('bulb')) return <LightModeIcon />;
    return <DevicesIcon />;
  };

  // Get severity color
  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'critical': return '#ff4444';
      case 'high': return '#ff8844';
      case 'medium': return '#ffaa44';
      default: return '#44aa44';
    }
  };

  // Mock chart data
  const threatTimelineData = [
    { hour: '00:00', threats: 2 },
    { hour: '04:00', threats: 1 },
    { hour: '08:00', threats: 3 },
    { hour: '12:00', threats: 4 },
    { hour: '16:00', threats: 2 },
    { hour: '20:00', threats: 5 }
  ];

  const deviceTypeData = devices.length > 0 ? [
    { name: 'Cameras', value: devices.filter(d => d.type.toLowerCase().includes('camera')).length },
    { name: 'Computers', value: devices.filter(d => d.type.toLowerCase().includes('laptop') || d.type.toLowerCase().includes('computer')).length },
    { name: 'Smart Home', value: devices.filter(d => d.type.toLowerCase().includes('bulb') || d.type.toLowerCase().includes('thermostat')).length },
    { name: 'Phones', value: devices.filter(d => d.type.toLowerCase().includes('phone')).length },
    { name: 'Others', value: devices.filter(d => !['camera', 'laptop', 'phone', 'bulb', 'thermostat'].some(t => d.type.toLowerCase().includes(t))).length }
  ] : [];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  return (
    <ThemeProvider theme={darkMode ? theme : createTheme({ palette: { mode: 'light' } })}>
      <CssBaseline />
      
      {/* Notification Snackbar */}
      <Snackbar
        open={!!notification}
        autoHideDuration={4000}
        onClose={() => setNotification(null)}
        message={notification?.message}
      />
      
      <Box sx={{ display: 'flex', minHeight: '100vh' }}>
        {/* App Bar */}
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <IconButton color="inherit" onClick={() => setMobileOpen(!mobileOpen)} sx={{ mr: 2 }}>
              <MenuIcon />
            </IconButton>
            <SecurityIcon sx={{ mr: 2 }} />
            <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
              Guardian AI - IoT Security
            </Typography>
            <IconButton color="inherit" onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? <LightModeIcon /> : <DarkModeIcon />}
            </IconButton>
            <IconButton color="inherit">
              <Badge badgeContent={threats.filter(t => t.status === 'active').length} color="error">
                <NotificationsIcon />
              </Badge>
            </IconButton>
          </Toolbar>
        </AppBar>

        {/* Sidebar Drawer */}
        <Drawer
          variant={isMobile ? "temporary" : "permanent"}
          open={isMobile ? mobileOpen : true}
          onClose={() => setMobileOpen(false)}
          sx={{
            width: 240,
            flexShrink: 0,
            '& .MuiDrawer-paper': { width: 240, boxSizing: 'border-box', mt: 8 }
          }}
        >
          <Box sx={{ overflow: 'auto', pt: 2 }}>
            <List>
              <ListItem button selected>
                <ListItemIcon><DashboardIcon /></ListItemIcon>
                <ListItemText primary="Dashboard" />
              </ListItem>
              <ListItem button onClick={triggerScan}>
                <ListItemIcon><NetworkIcon /></ListItemIcon>
                <ListItemText primary="Scan Network" />
              </ListItem>
              <ListItem button>
                <ListItemIcon><DevicesIcon /></ListItemIcon>
                <ListItemText primary="Devices" />
                <Chip label={stats.total_devices} size="small" color="primary" />
              </ListItem>
              <ListItem button>
                <ListItemIcon><WarningIcon /></ListItemIcon>
                <ListItemText primary="Threats" />
                <Chip label={stats.active_threats} size="small" color="error" />
              </ListItem>
              <ListItem button>
                <ListItemIcon><BlockIcon /></ListItemIcon>
                <ListItemText primary="Firewall" />
              </ListItem>
              <ListItem button>
                <ListItemIcon><SettingsIcon /></ListItemIcon>
                <ListItemText primary="Settings" />
              </ListItem>
            </List>
          </Box>
        </Drawer>

        {/* Main Content */}
        <Box component="main" sx={{ flexGrow: 1, p: 3, mt: 8 }}>
          {/* Stats Cards */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <DevicesIcon color="primary" sx={{ fontSize: 30, mr: 1 }} />
                    <Typography variant="h6">Total Devices</Typography>
                  </Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>{stats.total_devices}</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={100} 
                    color="primary"
                    sx={{ mt: 1, height: 6, borderRadius: 3 }}
                  />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <SecurityIcon color="success" sx={{ fontSize: 30, mr: 1 }} />
                    <Typography variant="h6">Protected</Typography>
                  </Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>{stats.protected_devices}</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={(stats.protected_devices / Math.max(stats.total_devices, 1)) * 100} 
                    color="success"
                    sx={{ mt: 1, height: 6, borderRadius: 3 }}
                  />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <WarningIcon color="error" sx={{ fontSize: 30, mr: 1 }} />
                    <Typography variant="h6">Active Threats</Typography>
                  </Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>{stats.active_threats}</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={Math.min(stats.active_threats * 20, 100)} 
                    color="error"
                    sx={{ mt: 1, height: 6, borderRadius: 3 }}
                  />
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <Card elevation={3}>
                <CardContent>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <BlockIcon color="warning" sx={{ fontSize: 30, mr: 1 }} />
                    <Typography variant="h6">Threats Blocked</Typography>
                  </Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold' }}>{stats.threats_blocked}</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={Math.min(stats.threats_blocked * 10, 100)} 
                    color="warning"
                    sx={{ mt: 1, height: 6, borderRadius: 3 }}
                  />
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Charts Row */}
          <Grid container spacing={3} sx={{ mb: 4 }}>
            <Grid item xs={12} md={8}>
              <Card elevation={3}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                    <TimelineIcon sx={{ mr: 1 }} /> Threat Activity Timeline
                  </Typography>
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={threatTimelineData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                      <XAxis dataKey="hour" stroke="#888" />
                      <YAxis stroke="#888" />
                      <Tooltip 
                        contentStyle={{ backgroundColor: '#1a252f', borderColor: '#444' }}
                        labelStyle={{ color: '#fff' }}
                      />
                      <Line 
                        type="monotone" 
                        dataKey="threats" 
                        stroke="#00ff88" 
                        strokeWidth={2}
                        dot={{ r: 4 }}
                        activeDot={{ r: 6 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={4}>
              <Card elevation={3}>
                <CardContent>
                  <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                    <DevicesIcon sx={{ mr: 1 }} /> Device Distribution
                  </Typography>
                  {deviceTypeData.length > 0 ? (
                    <ResponsiveContainer width="100%" height={250}>
                      <PieChart>
                        <Pie
                          data={deviceTypeData}
                          cx="50%"
                          cy="50%"
                          labelLine={false}
                          label={(entry) => `${entry.name}: ${entry.value}`}
                          outerRadius={80}
                          fill="#8884d8"
                          dataKey="value"
                        >
                          {deviceTypeData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <Tooltip 
                          contentStyle={{ backgroundColor: '#1a252f', borderColor: '#444' }}
                        />
                      </PieChart>
                    </ResponsiveContainer>
                  ) : (
                    <Box sx={{ height: 250, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <Typography color="textSecondary">No devices found. Run a scan!</Typography>
                    </Box>
                  )}
                </CardContent>
              </Card>
            </Grid>
          </Grid>

          {/* Devices Table */}
          <Card elevation={3} sx={{ mb: 4 }}>
            <CardContent>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
                  <DevicesIcon sx={{ mr: 1 }} /> Connected Devices ({devices.length})
                </Typography>
                <Button 
                  variant="contained" 
                  startIcon={<RefreshIcon />} 
                  onClick={triggerScan}
                  disabled={scanning}
                  sx={{ bgcolor: 'primary.main', '&:hover': { bgcolor: 'primary.dark' } }}
                >
                  {scanning ? 'Scanning...' : 'Scan Network'}
                </Button>
              </Box>
              
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Device</TableCell>
                      <TableCell>IP Address</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Risk Score</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {devices.slice(0, 8).map((device) => (
                      <TableRow key={device.id} hover>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Avatar sx={{ bgcolor: 'primary.dark', mr: 2, width: 40, height: 40 }}>
                              {getDeviceIcon(device.type)}
                            </Avatar>
                            <Box>
                              <Typography variant="subtitle2">{device.name}</Typography>
                              <Typography variant="caption" color="textSecondary">
                                {device.vendor} • {device.mac}
                              </Typography>
                            </Box>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip label={device.ip} size="small" variant="outlined" />
                        </TableCell>
                        <TableCell>
                          <Chip 
                            label={device.type} 
                            size="small" 
                            sx={{ textTransform: 'capitalize' }}
                          />
                        </TableCell>
                        <TableCell>
                          <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <Box sx={{ width: '100%', mr: 1 }}>
                              <LinearProgress 
                                variant="determinate" 
                                value={device.risk_score * 100}
                                color={
                                  device.risk_score > 0.7 ? "error" : 
                                  device.risk_score > 0.4 ? "warning" : "success"
                                }
                                sx={{ height: 8, borderRadius: 4 }}
                              />
                            </Box>
                            <Typography variant="body2" sx={{ minWidth: 45 }}>
                              {(device.risk_score * 100).toFixed(0)}%
                            </Typography>
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip 
                            label={device.status} 
                            size="small"
                            color={device.status === 'online' ? 'success' : device.status === 'blocked' ? 'error' : 'warning'}
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell>
                          <Button
                            size="small"
                            variant="contained"
                            color="error"
                            startIcon={<BlockIcon />}
                            onClick={() => blockDevice(device.id)}
                            disabled={device.status === 'blocked'}
                            sx={{ textTransform: 'none' }}
                          >
                            {device.status === 'blocked' ? 'Blocked' : 'Block'}
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
              
              {devices.length === 0 && (
                <Box sx={{ textAlign: 'center', py: 4 }}>
                  <DevicesIcon sx={{ fontSize: 60, color: 'text.secondary', mb: 2 }} />
                  <Typography variant="h6" color="textSecondary">No devices found</Typography>
                  <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                    Click "Scan Network" to discover devices
                  </Typography>
                  <Button variant="outlined" onClick={triggerScan}>
                    Start First Scan
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>

          {/* Threats Section */}
          <Card elevation={3}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <WarningIcon sx={{ mr: 1 }} /> Recent Security Threats
              </Typography>
              
              {threats.length === 0 ? (
                <Alert severity="success" icon={<SecurityIcon />}>
                  No active threats detected. Your network is secure!
                </Alert>
              ) : (
                threats.slice(0, 5).map((threat) => (
                  <Alert 
                    key={threat.id}
                    severity={threat.severity === 'critical' ? 'error' : threat.severity}
                    sx={{ mb: 2 }}
                    action={
                      <Box>
                        <Button 
                          color="inherit" 
                          size="small" 
                          onClick={() => resolveThreat(threat.id)}
                          sx={{ mr: 1 }}
                        >
                          Resolve
                        </Button>
                        <Button color="inherit" size="small">
                          Details
                        </Button>
                      </Box>
                    }
                  >
                    <Typography variant="subtitle2">
                      <strong>{threat.type}</strong> • Device: {threat.device_id}
                    </Typography>
                    <Typography variant="body2">
                      {threat.description}
                    </Typography>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 1 }}>
                      <Typography variant="caption">
                        Confidence: <strong>{(threat.confidence * 100).toFixed(0)}%</strong>
                      </Typography>
                      <Typography variant="caption">
                        {new Date(threat.timestamp).toLocaleTimeString()}
                      </Typography>
                    </Box>
                  </Alert>
                ))
              )}
            </CardContent>
          </Card>
        </Box>

        {/* Floating Action Button for Mobile */}
        {isMobile && (
          <Fab
            color="primary"
            sx={{ position: 'fixed', bottom: 16, right: 16 }}
            onClick={triggerScan}
          >
            {scanning ? <RefreshIcon className="spin" /> : <NetworkIcon />}
          </Fab>
        )}
      </Box>
      
      {/* Custom CSS for spinning icon */}
      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        .spin {
          animation: spin 1s linear infinite;
        }
      `}</style>
    </ThemeProvider>
  );
}

export default App;