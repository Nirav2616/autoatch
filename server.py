#!/usr/bin/env python3
import http.server
import socketserver
import os
import webbrowser
from datetime import datetime

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="client", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/' or self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>ArchSense - Server Working</title>
                <style>
                    body {{ 
                        font-family: Arial, sans-serif; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        margin: 0;
                    }}
                    .container {{
                        text-align: center;
                        background: rgba(255,255,255,0.1);
                        padding: 2rem;
                        border-radius: 10px;
                        backdrop-filter: blur(10px);
                    }}
                    .success {{ color: #4CAF50; font-size: 2rem; margin-bottom: 1rem; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="success">✅ SUCCESS!</div>
                    <h1>🏗️ ArchSense Server is Running</h1>
                    <p>Python HTTP Server is working correctly on port 5000</p>
                    <p>Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p><strong>Server Status:</strong> Active and Responding</p>
                    <p><strong>Next:</strong> The React application will be loaded here</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode())
        else:
            super().do_GET()

PORT = 5000
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print("=" * 50)
    print(f"🚀 PYTHON SERVER STARTED SUCCESSFULLY")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()
