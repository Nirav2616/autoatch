#!/usr/bin/env python3
import http.server
import socketserver
import os
import json
import uuid
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs
import base64

PORT = 8080

# Mock data storage
mock_users = {
    'dev-user-1': {
        'id': 'dev-user-1',
        'email': 'dev@example.com',
        'firstName': 'Development',
        'lastName': 'User',
        'profileImageUrl': '',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
}

mock_projects = []
mock_plans = []
mock_exports = []

class CompleteHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="dist/public", **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # Handle API routes
        if path.startswith('/api/'):
            self.handle_api(path, parsed_path.query)
            return
        
        # Handle React routing - serve index.html for all routes
        if path == '/' or path.startswith('/editor') or path.startswith('/app'):
            self.serve_react_app()
            return
        
        # Default to serving static files from dist/public
        super().do_GET()
    
    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/'):
            self.handle_api_post(path)
            return
        
        self.send_response(404)
        self.end_headers()
    
    def serve_react_app(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        try:
            with open('dist/public/index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ArchSense</title>
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
        .error { color: #ff6b6b; font-size: 2rem; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="error">⚠️ Error</div>
        <h1>🏗️ ArchSense</h1>
        <p>Built files not found. Please run 'npm run build' first.</p>
    </div>
</body>
</html>'''
            self.wfile.write(html.encode('utf-8'))
    
    def handle_api(self, path, query):
        if path == '/api/auth/user':
            self.handle_auth_user()
        elif path == '/api/auth/login':
            self.handle_auth_login()
        elif path == '/api/auth/register':
            self.handle_auth_register()
        elif path == '/api/auth/logout':
            self.handle_auth_logout()
        elif path == '/api/login':
            self.handle_auth_login()
        elif path == '/api/logout':
            self.handle_auth_logout()
        elif path == '/api/health':
            self.handle_health()
        elif path == '/api/projects':
            self.handle_projects()
        elif path.startswith('/api/projects/') and '/plans/latest' in path:
            project_id = path.split('/')[3]
            self.handle_project_latest_plan(project_id)
        elif path.startswith('/api/projects/'):
            project_id = path.split('/')[-1]
            self.handle_project_detail(project_id)
        elif path == '/api/exports':
            self.handle_exports()
        elif path.startswith('/api/exports/'):
            export_id = path.split('/')[-1]
            self.handle_export_detail(export_id)
        elif path.startswith('/api/furniture/category/'):
            category = path.split('/')[-1]
            self.handle_furniture_category(category)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'API endpoint not found'}).encode())
    
    def handle_api_post(self, path):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            data = {}
        
        if path == '/api/auth/login':
            self.handle_auth_login()
        elif path == '/api/auth/register':
            self.handle_auth_register()
        elif path == '/api/login':
            self.handle_auth_login()
        elif path == '/api/register':
            self.handle_auth_register()
        elif path == '/api/projects':
            self.handle_create_project(data)
        elif path == '/api/exports':
            self.handle_create_export(data)
        elif path == '/api/layout/generate':
            self.handle_generate_layout(data)
        elif path.startswith('/api/projects/') and '/plans' in path:
            project_id = path.split('/')[3]
            self.handle_create_plan(project_id, data)
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'API endpoint not found'}).encode())
    
    def handle_auth_user(self):
        # Mock authentication - always return a development user
        user = mock_users['dev-user-1']
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(user).encode())
    
    def handle_auth_logout(self):
        # Mock logout - just return a success message
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Logout successful'}).encode())
    
    def handle_auth_login(self):
        # Mock login - always return success for development
        response = {
            'message': 'Login successful',
            'user': mock_users['dev-user-1'],
            'token': 'dev-token-123'
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def handle_auth_register(self):
        # Mock registration - always return success for development
        response = {
            'message': 'Registration successful',
            'user': mock_users['dev-user-1'],
            'token': 'dev-token-123'
        }
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def handle_health(self):
        response = {
            'status': 'OK',
            'message': 'ArchSense Complete API is running',
            'frontend': 'Built React app loaded',
            'backend': 'Python server active',
            'auth': 'Development mode enabled'
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def handle_projects(self):
        # Return mock projects for the development user
        user_projects = [p for p in mock_projects if p.get('userId') == 'dev-user-1']
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(user_projects).encode())
    
    def handle_project_detail(self, project_id):
        project = next((p for p in mock_projects if p.get('id') == project_id), None)
        if project:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(project).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Project not found'}).encode())
    
    def handle_project_latest_plan(self, project_id):
        # Find the latest plan for the project
        project_plans = [p for p in mock_plans if p.get('projectId') == project_id]
        if project_plans:
            latest_plan = max(project_plans, key=lambda p: p.get('version', 0))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(latest_plan).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'No plans found'}).encode())
    
    def handle_create_project(self, data):
        project_id = str(uuid.uuid4())
        project = {
            'id': project_id,
            'userId': 'dev-user-1',
            'name': data.get('name', 'New Project'),
            'siteWidthMm': data.get('siteWidthMm', 10000),
            'siteDepthMm': data.get('siteDepthMm', 15000),
            'floors': data.get('floors', 1),
            'stylePreset': data.get('stylePreset', 'modern'),
            'createdAt': datetime.now().isoformat(),
            'updatedAt': datetime.now().isoformat(),
            'isPublic': False,
            'shareSlug': None
        }
        mock_projects.append(project)
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(project).encode())
    
    def handle_create_plan(self, project_id, data):
        plan_id = str(uuid.uuid4())
        plan = {
            'id': plan_id,
            'projectId': project_id,
            'version': data.get('version', 1),
            'planJson': data.get('planJson', {}),
            'constraintsJson': data.get('constraintsJson', {}),
            'cameraStateJson': data.get('cameraStateJson', {}),
            'createdAt': datetime.now().isoformat()
        }
        mock_plans.append(plan)
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(plan).encode())
    
    def handle_generate_layout(self, requirements):
        # Enhanced layout generation with 3D visualization support
        rooms = requirements.get('rooms', [])
        site_width = requirements.get('siteWidthMm', 10000)
        site_depth = requirements.get('siteDepthMm', 15000)
        
        # Generate comprehensive floor plan with 3D data
        plan_data = {
            'rooms': [],
            'walls': [],
            'doors': [],
            'windows': [],
            'furniture': [],
            '3d_data': {
                'camera': {
                    'position': {'x': 5000, 'y': 7500, 'z': 3000},
                    'target': {'x': 5000, 'y': 7500, 'z': 0},
                    'fov': 60
                },
                'lights': [
                    {'type': 'ambient', 'intensity': 0.4, 'color': 0xffffff},
                    {'type': 'directional', 'position': {'x': 5000, 'y': 0, 'z': 5000}, 'intensity': 0.8, 'color': 0xffffff}
                ],
                'materials': {
                    'floor': {'color': 0xf5f5dc, 'roughness': 0.8},
                    'wall': {'color': 0xf0f0f0, 'roughness': 0.9},
                    'ceiling': {'color': 0xffffff, 'roughness': 0.7}
                }
            },
            'react_planner_data': {
                'version': '1.0',
                'scale': 1,
                'layers': {
                    'layer-1': {
                        'id': 'layer-1',
                        'name': 'Floor Plan',
                        'visible': True,
                        'opacity': 1,
                        'selected': True,
                        'elements': {}
                    }
                },
                'scene': {
                    'width': site_width,
                    'height': site_depth,
                    'rotation': 0,
                    'scale': 1
                }
            }
        }
        
        # Define room dimensions and 3D properties
        room_specs = {
            'bedroom': {
                'min_area': 10, 'width': 3500, 'depth': 3000, 'height': 2800,
                'color': 0xe8f4fd, 'floor_color': 0xf0f8ff
            },
            'bathroom': {
                'min_area': 3, 'width': 2000, 'depth': 2000, 'height': 2600,
                'color': 0xf0f8ff, 'floor_color': 0xe6f3ff
            },
            'kitchen': {
                'min_area': 7, 'width': 4000, 'depth': 2500, 'height': 2800,
                'color': 0xfff8dc, 'floor_color': 0xfff5e6
            },
            'living': {
                'min_area': 14, 'width': 5000, 'depth': 3500, 'height': 3000,
                'color': 0xf5f5dc, 'floor_color': 0xf0f0e6
            }
        }
        
        # Create enhanced layout for 10m x 15m site
        # Layout: Living room at front, kitchen adjacent, bedrooms grouped at back, bathrooms strategically placed
        
        # 1. Living Room (Front left - 5m x 3.5m)
        living_room = {
            'id': 'living_1',
            'type': 'living',
            'x': 0,
            'y': 0,
            'width': 5000,
            'depth': 3500,
            'height': 3000,
            'area': 17.5,
            'color': 0xf5f5dc,
            'floor_color': 0xf0f0e6,
            'furniture': [
                {'type': 'sofa', 'x': 500, 'y': 500, 'z': 0, 'width': 2000, 'depth': 800, 'height': 850, 'name': '3-Seater Sofa', 'rotation': 0},
                {'type': 'tv', 'x': 3000, 'y': 300, 'z': 0, 'width': 1200, 'depth': 100, 'height': 500, 'name': 'TV Stand', 'rotation': 0},
                {'type': 'table', 'x': 1000, 'y': 1500, 'z': 0, 'width': 1200, 'depth': 600, 'height': 450, 'name': 'Coffee Table', 'rotation': 0},
                {'type': 'table', 'x': 500, 'y': 2500, 'z': 0, 'width': 1800, 'depth': 900, 'height': 750, 'name': 'Dining Table', 'rotation': 0}
            ],
            '3d_properties': {
                'ceiling_height': 3000,
                'wall_thickness': 200,
                'window_height': 1200,
                'door_height': 2100
            }
        }
        plan_data['rooms'].append(living_room)
        
        # 2. Kitchen (Front right - 4m x 2.5m)
        kitchen = {
            'id': 'kitchen_1',
            'type': 'kitchen',
            'x': 5000,
            'y': 0,
            'width': 4000,
            'depth': 2500,
            'height': 2800,
            'area': 10.0,
            'color': 0xfff8dc,
            'floor_color': 0xfff5e6,
            'furniture': [
                {'type': 'counter', 'x': 500, 'y': 500, 'z': 0, 'width': 2000, 'depth': 600, 'height': 900, 'name': 'Kitchen Counter', 'rotation': 0},
                {'type': 'stove', 'x': 1000, 'y': 1200, 'z': 0, 'width': 600, 'depth': 600, 'height': 900, 'name': 'Stove', 'rotation': 0},
                {'type': 'sink', 'x': 1800, 'y': 1200, 'z': 0, 'width': 500, 'depth': 500, 'height': 900, 'name': 'Kitchen Sink', 'rotation': 0},
                {'type': 'appliance', 'x': 2800, 'y': 500, 'z': 0, 'width': 700, 'depth': 700, 'height': 1800, 'name': 'Refrigerator', 'rotation': 0}
            ],
            '3d_properties': {
                'ceiling_height': 2800,
                'wall_thickness': 200,
                'window_height': 1200,
                'door_height': 2100
            }
        }
        plan_data['rooms'].append(kitchen)
        
        # 3. Bathroom 1 (Near living room - 2m x 2m)
        bathroom1 = {
            'id': 'bathroom_1',
            'type': 'bathroom',
            'x': 5000,
            'y': 2500,
            'width': 2000,
            'depth': 2000,
            'height': 2600,
            'area': 4.0,
            'color': 0xf0f8ff,
            'floor_color': 0xe6f3ff,
            'furniture': [
                {'type': 'toilet', 'x': 300, 'y': 300, 'z': 0, 'width': 400, 'depth': 700, 'height': 750, 'name': 'Toilet', 'rotation': 0},
                {'type': 'sink', 'x': 1000, 'y': 300, 'z': 0, 'width': 500, 'depth': 400, 'height': 850, 'name': 'Bathroom Sink', 'rotation': 0},
                {'type': 'shower', 'x': 300, 'y': 1200, 'z': 0, 'width': 900, 'depth': 900, 'height': 2000, 'name': 'Shower', 'rotation': 0}
            ],
            '3d_properties': {
                'ceiling_height': 2600,
                'wall_thickness': 200,
                'window_height': 800,
                'door_height': 2100
            }
        }
        plan_data['rooms'].append(bathroom1)
        
        # 4. Bedroom 1 (Back left - 3.5m x 3m)
        bedroom1 = {
            'id': 'bedroom_1',
            'type': 'bedroom',
            'x': 0,
            'y': 3500,
            'width': 3500,
            'depth': 3000,
            'height': 2800,
            'area': 10.5,
            'color': 0xe8f4fd,
            'floor_color': 0xf0f8ff,
            'furniture': [
                {'type': 'bed', 'x': 500, 'y': 500, 'z': 0, 'width': 1500, 'depth': 2000, 'height': 600, 'name': 'Queen Bed', 'rotation': 0},
                {'type': 'storage', 'x': 2200, 'y': 500, 'z': 0, 'width': 800, 'depth': 600, 'height': 2000, 'name': 'Wardrobe', 'rotation': 0},
                {'type': 'table', 'x': 500, 'y': 2600, 'z': 0, 'width': 400, 'depth': 400, 'height': 600, 'name': 'Nightstand', 'rotation': 0}
            ],
            '3d_properties': {
                'ceiling_height': 2800,
                'wall_thickness': 200,
                'window_height': 1200,
                'door_height': 2100
            }
        }
        plan_data['rooms'].append(bedroom1)
        
        # 5. Bedroom 2 (Back center - 3.5m x 3m)
        bedroom2 = {
            'id': 'bedroom_2',
            'type': 'bedroom',
            'x': 3500,
            'y': 3500,
            'width': 3500,
            'depth': 3000,
            'height': 2800,
            'area': 10.5,
            'color': 0xe8f4fd,
            'floor_color': 0xf0f8ff,
            'furniture': [
                {'type': 'bed', 'x': 500, 'y': 500, 'z': 0, 'width': 1500, 'depth': 2000, 'height': 600, 'name': 'Queen Bed', 'rotation': 0},
                {'type': 'storage', 'x': 2200, 'y': 500, 'z': 0, 'width': 800, 'depth': 600, 'height': 2000, 'name': 'Wardrobe', 'rotation': 0},
                {'type': 'table', 'x': 500, 'y': 2600, 'z': 0, 'width': 400, 'depth': 400, 'height': 600, 'name': 'Nightstand', 'rotation': 0}
            ],
            '3d_properties': {
                'ceiling_height': 2800,
                'wall_thickness': 200,
                'window_height': 1200,
                'door_height': 2100
            }
        }
        plan_data['rooms'].append(bedroom2)
        
        # 6. Bedroom 3 (Back right - 3m x 3m)
        bedroom3 = {
            'id': 'bedroom_3',
            'type': 'bedroom',
            'x': 7000,
            'y': 3500,
            'width': 3000,
            'depth': 3000,
            'height': 2800,
            'area': 9.0,
            'color': 0xe8f4fd,
            'floor_color': 0xf0f8ff,
            'furniture': [
                {'type': 'bed', 'x': 500, 'y': 500, 'z': 0, 'width': 1350, 'depth': 1900, 'height': 600, 'name': 'Double Bed', 'rotation': 0},
                {'type': 'storage', 'x': 2000, 'y': 500, 'z': 0, 'width': 800, 'depth': 600, 'height': 2000, 'name': 'Wardrobe', 'rotation': 0},
                {'type': 'table', 'x': 500, 'y': 2500, 'z': 0, 'width': 400, 'depth': 400, 'height': 600, 'name': 'Nightstand', 'rotation': 0}
            ],
            '3d_properties': {
                'ceiling_height': 2800,
                'wall_thickness': 200,
                'window_height': 1200,
                'door_height': 2100
            }
        }
        plan_data['rooms'].append(bedroom3)
        
        # 7. Bathroom 2 (Near bedrooms - 2m x 2m)
        bathroom2 = {
            'id': 'bathroom_2',
            'type': 'bathroom',
            'x': 7000,
            'y': 2500,
            'width': 2000,
            'depth': 2000,
            'height': 2600,
            'area': 4.0,
            'color': 0xf0f8ff,
            'floor_color': 0xe6f3ff,
            'furniture': [
                {'type': 'toilet', 'x': 300, 'y': 300, 'z': 0, 'width': 400, 'depth': 700, 'height': 750, 'name': 'Toilet', 'rotation': 0},
                {'type': 'sink', 'x': 1000, 'y': 300, 'z': 0, 'width': 500, 'depth': 400, 'height': 850, 'name': 'Bathroom Sink', 'rotation': 0},
                {'type': 'bathtub', 'x': 300, 'y': 1200, 'z': 0, 'width': 1700, 'depth': 700, 'height': 600, 'name': 'Bathtub', 'rotation': 0}
            ],
            '3d_properties': {
                'ceiling_height': 2600,
                'wall_thickness': 200,
                'window_height': 800,
                'door_height': 2100
            }
        }
        plan_data['rooms'].append(bathroom2)
        
        # Add walls with 3D properties
        plan_data['walls'] = [
            {'x1': 0, 'y1': 0, 'x2': site_width, 'y2': 0, 'height': 3000, 'thickness': 200},  # Top
            {'x1': site_width, 'y1': 0, 'x2': site_width, 'y2': site_depth, 'height': 3000, 'thickness': 200},  # Right
            {'x1': site_width, 'y1': site_depth, 'x2': 0, 'y2': site_depth, 'height': 3000, 'thickness': 200},  # Bottom
            {'x1': 0, 'y1': site_depth, 'x2': 0, 'y2': 0, 'height': 3000, 'thickness': 200},  # Left
        ]
        
        # Add internal walls for room separation
        plan_data['walls'].extend([
            {'x1': 5000, 'y1': 0, 'x2': 5000, 'y2': 2500, 'height': 3000, 'thickness': 200},  # Kitchen wall
            {'x1': 0, 'y1': 3500, 'x2': 10000, 'y2': 3500, 'height': 3000, 'thickness': 200},  # Bedroom area wall
            {'x1': 3500, 'y1': 3500, 'x2': 3500, 'y2': 6500, 'height': 3000, 'thickness': 200},  # Bedroom 1-2 wall
            {'x1': 7000, 'y1': 2500, 'x2': 7000, 'y2': 6500, 'height': 3000, 'thickness': 200},  # Bedroom 3 wall
        ])
        
        # Add doors with 3D properties
        plan_data['doors'] = [
            {'x': 2500, 'y': 0, 'width': 900, 'height': 2100, 'room1': 'entrance', 'room2': 'living', 'type': 'entrance'},  # Main entrance
            {'x': 4500, 'y': 0, 'width': 900, 'height': 2100, 'room1': 'living', 'room2': 'kitchen', 'type': 'interior'},  # Living to kitchen
            {'x': 6000, 'y': 2500, 'width': 900, 'height': 2100, 'room1': 'kitchen', 'room2': 'bathroom1', 'type': 'interior'},  # Kitchen to bathroom
            {'x': 1750, 'y': 3500, 'width': 900, 'height': 2100, 'room1': 'living', 'room2': 'bedroom1', 'type': 'interior'},  # Living to bedroom 1
            {'x': 5250, 'y': 3500, 'width': 900, 'height': 2100, 'room1': 'bathroom1', 'room2': 'bedroom2', 'type': 'interior'},  # Bathroom to bedroom 2
            {'x': 8500, 'y': 3500, 'width': 900, 'height': 2100, 'room1': 'bedroom2', 'room2': 'bedroom3', 'type': 'interior'},  # Bedroom 2 to 3
            {'x': 8000, 'y': 2500, 'width': 900, 'height': 2100, 'room1': 'bedroom3', 'room2': 'bathroom2', 'type': 'interior'},  # Bedroom 3 to bathroom
        ]
        
        # Add windows with 3D properties
        plan_data['windows'] = [
            {'x': 1000, 'y': 0, 'width': 1500, 'height': 1200, 'room': 'living', 'type': 'window', 'depth': 100},  # Living room window
            {'x': 6000, 'y': 0, 'width': 1500, 'height': 1200, 'room': 'kitchen', 'type': 'window', 'depth': 100},  # Kitchen window
            {'x': 500, 'y': 3500, 'width': 1200, 'height': 1200, 'room': 'bedroom1', 'type': 'window', 'depth': 100},  # Bedroom 1 window
            {'x': 4000, 'y': 3500, 'width': 1200, 'height': 1200, 'room': 'bedroom2', 'type': 'window', 'depth': 100},  # Bedroom 2 window
            {'x': 7500, 'y': 3500, 'width': 1200, 'height': 1200, 'room': 'bedroom3', 'type': 'window', 'depth': 100},  # Bedroom 3 window
        ]
        
        # Generate React-Planner compatible data
        element_id = 1
        for room in plan_data['rooms']:
            # Add room as React-Planner element
            plan_data['react_planner_data']['layers']['layer-1']['elements'][f'element-{element_id}'] = {
                'id': f'element-{element_id}',
                'type': 'room',
                'x': room['x'],
                'y': room['y'],
                'width': room['width'],
                'height': room['depth'],
                'properties': {
                    'name': room['type'].title(),
                    'height': room['height'],
                    'color': room['color']
                }
            }
            element_id += 1
        
        response = {
            'plan': plan_data,
            'message': 'Enhanced floor plan with 3D visualization generated successfully',
            'rooms': len(plan_data['rooms']),
            'totalArea': site_width * site_depth / 1000000,  # Convert to m²
            'layout': {
                'description': 'Family-friendly layout with living room at front, kitchen adjacent, bedrooms grouped at back',
                'features': [
                    'Living room near entrance for easy access',
                    'Kitchen connects to living room for family flow',
                    'Bedrooms grouped together for privacy',
                    'Bathrooms strategically placed near bedrooms and living area',
                    'Balanced layout optimized for family use',
                    '3D visualization ready with Three.js',
                    'React-Planner compatible format'
                ]
            },
            'visualization': {
                '2d_editor': 'React-Planner compatible',
                '3d_engine': 'Three.js ready',
                'furniture_library': 'Complete furniture catalog',
                'export_formats': ['2D PDF', '3D GLTF', 'VR Ready']
            }
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())
    
    def handle_exports(self):
        user_exports = [e for e in mock_exports if e.get('userId') == 'dev-user-1']
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(user_exports).encode())
    
    def handle_export_detail(self, export_id):
        export = next((e for e in mock_exports if e.get('id') == export_id), None)
        if export:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(export).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Export not found'}).encode())
    
    def handle_create_export(self, data):
        export_id = str(uuid.uuid4())
        export = {
            'id': export_id,
            'projectId': data.get('projectId'),
            'userId': 'dev-user-1',
            'type': data.get('type', 'pdf'),
            'status': 'pending',
            'fileUri': None,
            'createdAt': datetime.now().isoformat()
        }
        mock_exports.append(export)
        
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(export).encode())
    
    def handle_furniture_category(self, category):
        # Mock furniture data for different categories
        furniture_data = {
            'living-room': [
                {'id': 'sofa_1', 'name': '3-Seater Sofa', 'type': 'sofa', 'width': 2000, 'depth': 800, 'height': 850},
                {'id': 'sofa_2', 'name': '2-Seater Sofa', 'type': 'sofa', 'width': 1500, 'depth': 800, 'height': 850},
                {'id': 'tv_stand', 'name': 'TV Stand', 'type': 'tv', 'width': 1200, 'depth': 400, 'height': 500},
                {'id': 'coffee_table', 'name': 'Coffee Table', 'type': 'table', 'width': 1200, 'depth': 600, 'height': 450},
                {'id': 'dining_table', 'name': 'Dining Table', 'type': 'table', 'width': 1800, 'depth': 900, 'height': 750},
                {'id': 'dining_chairs', 'name': 'Dining Chairs', 'type': 'chair', 'width': 450, 'depth': 450, 'height': 900}
            ],
            'bedroom': [
                {'id': 'bed_single', 'name': 'Single Bed', 'type': 'bed', 'width': 900, 'depth': 1900, 'height': 600},
                {'id': 'bed_double', 'name': 'Double Bed', 'type': 'bed', 'width': 1350, 'depth': 1900, 'height': 600},
                {'id': 'bed_queen', 'name': 'Queen Bed', 'type': 'bed', 'width': 1500, 'depth': 2000, 'height': 600},
                {'id': 'wardrobe', 'name': 'Wardrobe', 'type': 'storage', 'width': 800, 'depth': 600, 'height': 2000},
                {'id': 'nightstand', 'name': 'Nightstand', 'type': 'table', 'width': 400, 'depth': 400, 'height': 600},
                {'id': 'dresser', 'name': 'Dresser', 'type': 'storage', 'width': 1200, 'depth': 450, 'height': 800}
            ],
            'kitchen': [
                {'id': 'kitchen_counter', 'name': 'Kitchen Counter', 'type': 'counter', 'width': 2000, 'depth': 600, 'height': 900},
                {'id': 'stove', 'name': 'Stove', 'type': 'appliance', 'width': 600, 'depth': 600, 'height': 900},
                {'id': 'refrigerator', 'name': 'Refrigerator', 'type': 'appliance', 'width': 700, 'depth': 700, 'height': 1800},
                {'id': 'sink', 'name': 'Kitchen Sink', 'type': 'sink', 'width': 500, 'depth': 500, 'height': 900},
                {'id': 'dishwasher', 'name': 'Dishwasher', 'type': 'appliance', 'width': 600, 'depth': 600, 'height': 850},
                {'id': 'microwave', 'name': 'Microwave', 'type': 'appliance', 'width': 500, 'depth': 400, 'height': 300}
            ],
            'bathroom': [
                {'id': 'toilet', 'name': 'Toilet', 'type': 'toilet', 'width': 400, 'depth': 700, 'height': 750},
                {'id': 'sink', 'name': 'Bathroom Sink', 'type': 'sink', 'width': 500, 'depth': 400, 'height': 850},
                {'id': 'shower', 'name': 'Shower', 'type': 'shower', 'width': 900, 'depth': 900, 'height': 2000},
                {'id': 'bathtub', 'name': 'Bathtub', 'type': 'bathtub', 'width': 1700, 'depth': 700, 'height': 600},
                {'id': 'towel_rack', 'name': 'Towel Rack', 'type': 'accessory', 'width': 400, 'depth': 100, 'height': 1800},
                {'id': 'mirror', 'name': 'Bathroom Mirror', 'type': 'mirror', 'width': 600, 'depth': 50, 'height': 800}
            ]
        }
        
        category_data = furniture_data.get(category, [])
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(category_data).encode())

# Change to the script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), CompleteHandler) as httpd:
    print("=" * 60)
    print(f"🚀 ARCHSENSE COMPLETE SERVER RUNNING")
    print(f"📍 URL: http://localhost:{PORT}")
    print(f"⚛️  Frontend: Built React application")
    print(f"🐍 Backend: Python HTTP server with full API")
    print(f"🔗 API: http://localhost:{PORT}/api/health")
    print(f"👤 Auth: Development mode (auto-authenticated)")
    print(f"📁 Projects: Mock data available")
    print(f"🏗️  Layout Generation: AI-powered floor plans")
    print(f"📋 Plans: Project versioning support")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()
