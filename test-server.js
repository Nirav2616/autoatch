const express = require('express');
const path = require('path');

const app = express();
const port = 5000;

// Add CORS headers
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

// Serve static files from client directory
app.use(express.static(path.join(__dirname, 'client')));

// API health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Server is running' });
});

// Serve test.html for testing
app.get('/test', (req, res) => {
  res.sendFile(path.join(__dirname, 'client', 'test.html'));
});

// Serve the main HTML file for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'client', 'index.html'));
});

app.listen(port, '0.0.0.0', () => {
  console.log(`🚀 Server running at http://localhost:${port}`);
  console.log(`📋 Test page at http://localhost:${port}/test`);
  console.log(`❤️  Health check at http://localhost:${port}/api/health`);
});
