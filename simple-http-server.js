const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
  console.log(`Request: ${req.method} ${req.url}`);
  
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  // Simple test response
  if (req.url === '/test' || req.url === '/') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>ArchSense - Server Working</title>
        <style>
          body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
          }
          .container {
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 2rem;
            border-radius: 10px;
            backdrop-filter: blur(10px);
          }
          .success { color: #4CAF50; font-size: 2rem; margin-bottom: 1rem; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="success">✅ SUCCESS!</div>
          <h1>🏗️ ArchSense Server is Running</h1>
          <p>Server is working correctly on port 5000</p>
          <p>Time: ${new Date().toLocaleString()}</p>
          <p><strong>Next:</strong> The React application will be loaded here</p>
        </div>
      </body>
      </html>
    `);
    return;
  }
  
  // Health check
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'OK', port: 5000, time: new Date().toISOString() }));
    return;
  }
  
  // 404 for other routes
  res.writeHead(404, { 'Content-Type': 'text/html' });
  res.end('<h1>404 - Not Found</h1><p><a href="/">Go to Home</a></p>');
});

const PORT = 5000;
server.listen(PORT, '0.0.0.0', () => {
  console.log('='.repeat(50));
  console.log(`🚀 SERVER STARTED SUCCESSFULLY`);
  console.log(`📍 URL: http://localhost:${PORT}`);
  console.log(`🕒 Time: ${new Date().toLocaleString()}`);
  console.log('='.repeat(50));
});

server.on('error', (err) => {
  console.error('Server error:', err);
});
