# 🔐 ArchSense API Implementation

Complete API implementation for the ArchSense architecture design platform with authentication, design management, furniture catalog, and export functionality.

## 🚀 **API Endpoints Overview**

### **1️⃣ Authentication Routes**
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Authenticate user
- `GET /api/auth/profile` - Get user profile (protected)
- `POST /api/auth/logout` - Logout user

### **2️⃣ Design Routes**
- `POST /api/designs` - Save new design (🔐 JWT required)
- `GET /api/designs` - Get all user designs (🔐 JWT required)
- `GET /api/designs/:id` - Get specific design (🔐 JWT required)
- `PUT /api/designs/:id` - Update design (🔐 JWT required)
- `DELETE /api/designs/:id` - Delete design (🔐 JWT required)

### **3️⃣ Furniture Routes**
- `GET /api/furniture` - Get furniture catalog
- `GET /api/furniture/categories` - Get furniture categories
- `GET /api/furniture/:id` - Get specific furniture item

### **4️⃣ Export Routes**
- `GET /api/export/:id/pdf` - Generate PDF floor plan
- `GET /api/export/:id/pdf/download` - Download PDF
- `GET /api/export/:id/3d` - Export 3D model (GLTF/OBJ)
- `GET /api/export/:id/status` - Check export status

---

## 🔐 **Authentication API**

### **Sign Up**
```http
POST /api/auth/signup
Content-Type: application/json

{
  "name": "Nirav",
  "email": "test@mail.com",
  "password": "123456"
}
```

**Response:**
```json
{
  "message": "User created",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "Nirav"
  }
}
```

### **Login**
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "test@mail.com",
  "password": "123456"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "Nirav"
  }
}
```

### **Get Profile**
```http
GET /api/auth/profile
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "user": {
    "id": "507f1f77bcf86cd799439011",
    "name": "Nirav",
    "email": "test@mail.com",
    "profileImageUrl": "https://...",
    "lastLogin": "2024-01-15T10:30:00.000Z"
  }
}
```

---

## 🏗️ **Design API**

### **Save New Design**
```http
POST /api/designs
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "rooms": [
    {
      "type": "bedroom",
      "width": 12,
      "height": 14,
      "position": { "x": 0, "y": 0 }
    },
    {
      "type": "kitchen",
      "width": 10,
      "height": 12,
      "position": { "x": 12, "y": 0 }
    }
  ],
  "furniture": [
    {
      "name": "Sofa",
      "position": { "x": 2, "y": 1 }
    }
  ],
  "name": "My House Design",
  "description": "Modern family home"
}
```

**Response:**
```json
{
  "message": "Design saved",
  "designId": "507f1f77bcf86cd799439012"
}
```

### **Get All Designs**
```http
GET /api/designs?page=1&limit=10
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "designs": [
    {
      "_id": "507f1f77bcf86cd799439012",
      "name": "My House Design",
      "description": "Modern family home",
      "rooms": [...],
      "interior": {
        "furniture": [...]
      },
      "createdAt": "2024-01-15T10:30:00.000Z",
      "updatedAt": "2024-01-15T10:30:00.000Z"
    }
  ],
  "totalPages": 1,
  "currentPage": 1,
  "totalDesigns": 1
}
```

### **Get Single Design**
```http
GET /api/designs/507f1f77bcf86cd799439012
Authorization: Bearer <JWT_TOKEN>
```

### **Update Design**
```http
PUT /api/designs/507f1f77bcf86cd799439012
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "name": "Updated House Design",
  "rooms": [...],
  "furniture": [...]
}
```

### **Delete Design**
```http
DELETE /api/designs/507f1f77bcf86cd799439012
Authorization: Bearer <JWT_TOKEN>
```

---

## 🪑 **Furniture API**

### **Get Furniture Catalog**
```http
GET /api/furniture
```

**Response:**
```json
[
  {
    "id": "1",
    "name": "Bed",
    "category": "Bedroom",
    "modelUrl": "/models/bed.gltf",
    "thumbnailUrl": "/thumbnails/bed.jpg",
    "dimensions": {
      "width": 1600,
      "height": 600,
      "depth": 2000
    }
  },
  {
    "id": "2",
    "name": "Sofa",
    "category": "Living Room",
    "modelUrl": "/models/sofa.gltf",
    "thumbnailUrl": "/thumbnails/sofa.jpg",
    "dimensions": {
      "width": 2000,
      "height": 800,
      "depth": 900
    }
  }
]
```

### **Get Furniture Categories**
```http
GET /api/furniture/categories
```

**Response:**
```json
[
  "Bedroom",
  "Living Room",
  "Dining Room",
  "Kitchen",
  "Bathroom",
  "Office"
]
```

### **Filter by Category**
```http
GET /api/furniture?category=Bedroom
```

### **Get Specific Furniture Item**
```http
GET /api/furniture/1
```

**Response:**
```json
{
  "id": "1",
  "name": "Bed",
  "category": "Bedroom",
  "modelUrl": "/models/bed.gltf",
  "thumbnailUrl": "/thumbnails/bed.jpg",
  "dimensions": {
    "width": 1600,
    "height": 600,
    "depth": 2000
  },
  "description": "Comfortable double bed with wooden frame",
  "price": 299.99
}
```

---

## 📄 **Export API**

### **Generate PDF**
```http
GET /api/export/507f1f77bcf86cd799439012/pdf
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "message": "PDF generated successfully",
  "downloadUrl": "/api/export/507f1f77bcf86cd799439012/pdf/download",
  "data": {
    "designId": "507f1f77bcf86cd799439012",
    "designName": "My House Design",
    "rooms": [...],
    "generatedAt": "2024-01-15T10:30:00.000Z",
    "format": "PDF"
  }
}
```

### **Download PDF**
```http
GET /api/export/507f1f77bcf86cd799439012/pdf/download
Authorization: Bearer <JWT_TOKEN>
```

**Response:** Binary PDF file

### **Export 3D Model**
```http
GET /api/export/507f1f77bcf86cd799439012/3d?format=gltf
Authorization: Bearer <JWT_TOKEN>
```

**Response:** GLTF file or OBJ file

### **Check Export Status**
```http
GET /api/export/507f1f77bcf86cd799439012/status
Authorization: Bearer <JWT_TOKEN>
```

**Response:**
```json
{
  "designId": "507f1f77bcf86cd799439012",
  "status": "completed",
  "progress": 100,
  "downloadUrl": "/api/export/507f1f77bcf86cd799439012/pdf/download",
  "createdAt": "2024-01-15T10:30:00.000Z",
  "completedAt": "2024-01-15T10:30:00.000Z"
}
```

---

## 🔧 **Frontend Integration**

### **React/Axios Example**

```typescript
import axios from "axios";

// Login
const login = async (email: string, password: string) => {
  const res = await axios.post("/api/auth/login", { email, password });
  localStorage.setItem("token", res.data.token);
  return res.data;
};

// Save Design
const saveDesign = async (design: any) => {
  const token = localStorage.getItem("token");
  const res = await axios.post("/api/designs", design, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};

// Fetch Furniture
const getFurniture = async () => {
  const res = await axios.get("/api/furniture");
  return res.data;
};

// Export PDF
const exportPDF = async (designId: string) => {
  const token = localStorage.getItem("token");
  const res = await axios.get(`/api/export/${designId}/pdf`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return res.data;
};
```

### **API Client Usage**

```typescript
import { authAPI, designsAPI, furnitureAPI, exportAPI } from "@/lib/api";

// Authentication
const user = await authAPI.signup({
  name: "Nirav",
  email: "test@mail.com",
  password: "123456"
});

// Design Management
const design = await designsAPI.create({
  rooms: [
    { type: "bedroom", width: 12, height: 14, position: { x: 0, y: 0 } }
  ],
  furniture: [
    { name: "Sofa", position: { x: 2, y: 1 } }
  ]
});

// Furniture Catalog
const furniture = await furnitureAPI.getAll("Bedroom");

// Export
const pdfData = await exportAPI.generatePDF(designId);
const pdfBlob = await exportAPI.downloadPDF(designId);
```

---

## 🛡️ **Security Features**

### **JWT Authentication**
- All protected routes require valid JWT token
- Tokens expire after 7 days
- Automatic token validation middleware

### **Input Validation**
- Server-side validation using Joi schemas
- Type-safe validation with detailed error messages
- Sanitization of user inputs

### **Rate Limiting**
- 100 requests per 15 minutes per IP
- Protection against abuse and DDoS attacks

### **CORS Protection**
- Configured for specific origins
- Credentials support for authenticated requests

---

## 📁 **File Structure**

```
server/
├── routes/
│   ├── auth.js          # Authentication endpoints
│   ├── designs.js        # Design CRUD operations
│   ├── furniture.js      # Furniture catalog
│   └── exports.js        # Export functionality
├── models/
│   ├── User.js          # User schema
│   └── Design.js        # Design schema
├── middleware/
│   └── auth.js          # JWT authentication middleware
└── index.js             # Main server file

client/src/
├── lib/
│   └── api.ts           # API client functions
├── components/
│   └── APIDemo.tsx      # API demo component
└── pages/
    └── APIDemo.tsx      # Demo page
```

---

## 🚀 **Getting Started**

### **1. Install Dependencies**
```bash
# Backend
cd server
npm install

# Frontend
cd client
npm install
```

### **2. Environment Setup**
```bash
# Copy environment files
cp server/env.example server/.env
cp client/env.example client/.env

# Configure MongoDB and JWT secret
```

### **3. Start Development Servers**
```bash
# Backend
cd server
npm run dev

# Frontend
cd client
npm run dev
```

### **4. Test API**
- Navigate to `/api-demo` to test all endpoints
- Use the interactive demo to create designs and test exports

---

## 🧪 **Testing**

### **API Testing with curl**

```bash
# Sign up
curl -X POST http://localhost:5000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","password":"123456"}'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"123456"}'

# Create design
curl -X POST http://localhost:5000/api/designs \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"rooms":[{"type":"bedroom","width":12,"height":14,"position":{"x":0,"y":0}}]}'

# Get furniture
curl -X GET http://localhost:5000/api/furniture

# Export PDF
curl -X GET http://localhost:5000/api/export/<DESIGN_ID>/pdf \
  -H "Authorization: Bearer <TOKEN>"
```

---

## 📊 **Database Schema**

### **User Model**
```javascript
{
  _id: ObjectId,
  firstName: String,
  email: String,
  password: String (hashed),
  profileImageUrl: String,
  lastLogin: Date,
  createdAt: Date,
  updatedAt: Date
}
```

### **Design Model**
```javascript
{
  _id: ObjectId,
  userId: ObjectId (ref: User),
  name: String,
  description: String,
  rooms: [{
    name: String,
    type: String,
    width: Number,
    height: Number,
    length: Number,
    position: { x: Number, y: Number },
    color: String,
    description: String
  }],
  interior: {
    furniture: [{
      type: String,
      name: String,
      position: { x: Number, y: Number, z: Number },
      dimensions: { width: Number, height: Number, depth: Number },
      rotation: Number,
      roomId: String
    }]
  },
  siteDimensions: { width: Number, height: Number },
  isPublic: Boolean,
  version: Number,
  createdAt: Date,
  updatedAt: Date
}
```

---

## 🔄 **Error Handling**

### **Standard Error Response**
```json
{
  "error": "Error message description"
}
```

### **Common HTTP Status Codes**
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation error)
- `401` - Unauthorized (invalid/missing token)
- `404` - Not Found
- `500` - Internal Server Error

---

## 📈 **Performance Considerations**

- **Database Indexing**: Proper indexes on frequently queried fields
- **Pagination**: All list endpoints support pagination
- **Caching**: Furniture catalog can be cached
- **Compression**: Response compression enabled
- **Rate Limiting**: Protection against abuse

---

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📄 **License**

This project is licensed under the MIT License.

---

**Built with ❤️ for the ArchSense Team**
