#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
from urllib.parse import urlparse

PORT = 8080

class ReactHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="client", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Parse the URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Handle React routing - serve index.html for all routes
        if path == '/' or path.startswith('/editor') or path.startswith('/app'):
            self.serve_react_app()
            return
        
        # Handle API routes
        if path.startswith('/api/'):
            self.handle_api(path)
            return
        
        # Handle static assets
        if path.startswith('/src/') or path.endswith('.tsx') or path.endswith('.ts') or path.endswith('.css'):
            self.serve_static_file(path)
            return
        
        # Default to serving static files
        super().do_GET()
    
    def serve_react_app(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Read and serve the React index.html
        try:
            with open('client/index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            # Fallback HTML with React setup
            html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArchSense</title>
    <script type="module">
        import { createRoot } from 'https://esm.sh/react-dom@18/client';
        import React from 'https://esm.sh/react@18';
        
        function App() {
            return React.createElement('div', {
                style: {
                    fontFamily: 'Arial, sans-serif',
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    minHeight: '100vh',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    margin: 0
                }
            }, React.createElement('div', {
                style: {
                    textAlign: 'center',
                    background: 'rgba(255,255,255,0.1)',
                    padding: '2rem',
                    borderRadius: '10px',
                    backdropFilter: 'blur(10px)'
                }
            }, [
                React.createElement('h1', { key: 'title' }, '🏗️ ArchSense'),
                React.createElement('p', { key: 'status' }, '✅ Frontend is now loading!'),
                React.createElement('p', { key: 'info' }, 'React application is running'),
                React.createElement('button', {
                    key: 'btn',
                    onClick: () => window.location.href = '/editor',
                    style: {
                        background: '#4CAF50',
                        color: 'white',
                        border: 'none',
                        padding: '10px 20px',
                        borderRadius: '5px',
                        cursor: 'pointer',
                        fontSize: '16px'
                    }
                }, 'Go to Editor')
            ]));
        }
        
        const root = createRoot(document.getElementById('root'));
        root.render(React.createElement(App));
    </script>
</head>
<body style="margin: 0;">
    <div id="root"></div>
</body>
</html>'''
            self.wfile.write(html.encode('utf-8'))
    
    def serve_static_file(self, path):
        # Remove leading slash and serve from client directory
        file_path = os.path.join('client', path.lstrip('/'))
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Determine content type
            if path.endswith('.js') or path.endswith('.tsx') or path.endswith('.ts'):
                content_type = 'application/javascript'
            elif path.endswith('.css'):
                content_type = 'text/css'
            elif path.endswith('.json'):
                content_type = 'application/json'
            else:
                content_type = 'text/plain'
            
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'File not found')
    
    def handle_api(self, path):
        if path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'status': 'OK',
                'message': 'ArchSense API is running',
                'frontend': 'React app loaded',
                'backend': 'Python server active'
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'API endpoint not found'}).encode())

# Change to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), ReactHandler) as httpd:
    print("=" * 60)
    print(f"🚀 ARCHSENSE FRONTEND + BACKEND SERVER RUNNING")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"⚛️  Frontend: React application")
    print(f"🐍 Backend: Python HTTP server")
    print(f"🔗 API: http://localhost:{PORT}/api/health")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()
