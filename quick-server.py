import http.server
import socketserver
import threading
import time

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            html = """<!DOCTYPE html>
<html><head><title>ArchSense Working</title>
<style>body{font-family:Arial;background:#667eea;color:white;text-align:center;padding:50px;}
.box{background:rgba(255,255,255,0.1);padding:30px;border-radius:10px;display:inline-block;}
</style></head>
<body><div class="box">
<h1>🚀 ArchSense Server Running!</h1>
<p>Port 8080 - Server is working correctly</p>
<p>✅ Connection successful</p>
</div></body></html>"""
            self.wfile.write(html.encode())
        else:
            super().do_GET()

print(f"Starting server on port {PORT}...")
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()
