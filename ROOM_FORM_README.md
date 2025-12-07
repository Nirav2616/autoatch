# 🏠 Room Input Form + Database Integration

A comprehensive room management system for the ArchSense architecture design platform. This feature allows users to create, edit, and manage rooms within their architectural designs with full CRUD operations and database persistence.

## ✨ Features

### 🎨 **Room Input Form**
- **Interactive Form**: Modern, responsive form with real-time validation
- **Room Types**: Support for 7 different room types (bedroom, bathroom, kitchen, living, dining, office, other)
- **Dimensions**: Width, height, and length inputs with validation (2m-20m range)
- **Positioning**: X and Y coordinates for room placement
- **Color Selection**: Visual color picker with predefined options and custom hex input
- **Description**: Optional text area for room notes
- **Live Preview**: Real-time room preview with area calculation

### 🔧 **Form Validation**
- **Zod Schema**: Type-safe validation with detailed error messages
- **Real-time Feedback**: Instant validation feedback on form inputs
- **Required Fields**: Name, type, and dimensions are mandatory
- **Range Validation**: Dimensions must be between 2m and 20m
- **Color Validation**: Hex color format validation

### 💾 **Database Integration**
- **MongoDB Storage**: Rooms stored as embedded documents in Design model
- **CRUD Operations**: Full Create, Read, Update, Delete functionality
- **Authentication**: All operations require valid JWT authentication
- **Data Validation**: Server-side validation using Joi schemas
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 **API Endpoints**

### **Room Management**
```http
# Add room to design
POST /api/designs/:id/rooms
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Master Bedroom",
  "type": "bedroom",
  "width": 4000,
  "height": 3000,
  "length": 5000,
  "position": { "x": 0, "y": 0 },
  "color": "#e8f4fd",
  "description": "Main bedroom with ensuite"
}

# Update room
PUT /api/designs/:id/rooms/:roomId
Authorization: Bearer <token>
Content-Type: application/json

# Delete room
DELETE /api/designs/:id/rooms/:roomId
Authorization: Bearer <token>

# Get rooms for design
GET /api/designs/:id/rooms
Authorization: Bearer <token>
```

## 📁 **File Structure**

```
client/src/
├── components/
│   ├── RoomInputForm.tsx          # Main room input form component
│   └── RoomManagementDemo.tsx     # Demo component showcasing functionality
├── pages/
│   └── RoomDemo.tsx               # Demo page
└── lib/
    └── api.ts                     # API client with room management functions

server/
├── routes/
│   └── designs.js                 # Backend routes with room CRUD operations
└── models/
    └── Design.js                  # MongoDB schema with room subdocument
```

## 🛠️ **Usage Examples**

### **Basic Room Creation**
```tsx
import { RoomInputForm } from "@/components/RoomInputForm";

function MyComponent() {
  const handleRoomAdded = (room) => {
    console.log("Room added:", room);
  };

  return (
    <RoomInputForm 
      onRoomAdded={handleRoomAdded}
    />
  );
}
```

### **Adding Room to Existing Design**
```tsx
<RoomInputForm 
  designId="design_123"
  onRoomAdded={handleRoomAdded}
/>
```

### **Editing Existing Room**
```tsx
<RoomInputForm 
  designId="design_123"
  existingRoom={roomData}
  mode="edit"
  onRoomUpdated={handleRoomUpdated}
/>
```

## 🎯 **Component Props**

### **RoomInputForm Props**
```typescript
interface RoomInputFormProps {
  designId?: string;              // Design ID for adding to existing design
  onRoomAdded?: (room: any) => void;    // Callback when room is added
  onRoomUpdated?: (room: any) => void;  // Callback when room is updated
  existingRoom?: any;             // Room data for editing mode
  mode?: "add" | "edit";          // Form mode
}
```

### **Room Data Structure**
```typescript
interface Room {
  _id: string;
  name: string;
  type: "bedroom" | "bathroom" | "kitchen" | "living" | "dining" | "office" | "other";
  width: number;      // in millimeters
  height: number;     // in millimeters
  length: number;     // in millimeters
  position: {
    x: number;
    y: number;
  };
  color: string;      // hex color code
  description?: string;
}
```

## 🔒 **Security Features**

- **JWT Authentication**: All room operations require valid authentication
- **User Ownership**: Users can only modify their own designs
- **Input Validation**: Both client and server-side validation
- **Rate Limiting**: API endpoints protected against abuse
- **CORS Protection**: Configured for specific origins

## 🎨 **UI Features**

### **Color Selection**
- **Predefined Colors**: 7 default color options
- **Custom Colors**: Hex color input for custom colors
- **Visual Preview**: Color swatches with selection indicator

### **Room Preview**
- **Live Preview**: Real-time room visualization
- **Area Calculation**: Automatic area calculation in m²
- **Proportional Scaling**: Preview scales based on room dimensions

### **Form States**
- **Loading States**: Spinner during form submission
- **Error States**: Clear error messages for validation failures
- **Success Feedback**: Toast notifications for successful operations

## 📊 **Database Schema**

### **Design Model (MongoDB)**
```javascript
const designSchema = new mongoose.Schema({
  userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  name: { type: String, required: true },
  description: String,
  rooms: [{
    name: { type: String, required: true },
    type: { type: String, enum: ['bedroom', 'bathroom', 'kitchen', 'living', 'dining', 'office', 'other'] },
    width: { type: Number, required: true, min: 2000, max: 20000 },
    height: { type: Number, required: true, min: 2000, max: 20000 },
    length: { type: Number, required: true, min: 2000, max: 20000 },
    position: {
      x: { type: Number, default: 0 },
      y: { type: Number, default: 0 }
    },
    color: { type: String, default: '#e8f4fd' },
    description: String
  }],
  siteDimensions: {
    width: { type: Number, required: true },
    height: { type: Number, required: true }
  },
  isPublic: { type: Boolean, default: false },
  tags: [String],
  timestamps: true
});
```

## 🚀 **Getting Started**

### **1. Install Dependencies**
```bash
npm install
```

### **2. Set up Environment**
```bash
# Copy environment files
cp server/env.example server/.env
cp client/env.example client/.env

# Configure MongoDB connection and JWT secret
```

### **3. Start Development Servers**
```bash
# Start both frontend and backend
npm run dev
```

### **4. Access Demo Page**
Navigate to `/room-demo` to see the room management demo in action.

## 🧪 **Testing**

### **API Testing**
```bash
# Test room creation
curl -X POST http://localhost:5000/api/designs/:id/rooms \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Room",
    "type": "bedroom",
    "width": 4000,
    "height": 3000,
    "length": 5000,
    "color": "#e8f4fd"
  }'
```

### **Component Testing**
```bash
# Run frontend tests
npm run test

# Run linting
npm run lint
```

## 🔧 **Customization**

### **Adding New Room Types**
1. Update the `roomTypes` array in `RoomInputForm.tsx`
2. Update the validation schema in both frontend and backend
3. Add corresponding color mappings in the demo component

### **Modifying Validation Rules**
1. Update the `roomSchema` in `RoomInputForm.tsx`
2. Update the `roomSchema` in `server/routes/designs.js`
3. Test with various input scenarios

### **Styling Customization**
The form uses Tailwind CSS classes and can be customized by:
- Modifying the className props
- Updating the color palette
- Adjusting the layout grid system

## 📈 **Performance Considerations**

- **Lazy Loading**: Forms load only when needed
- **Debounced Validation**: Real-time validation with debouncing
- **Optimistic Updates**: UI updates immediately, syncs with server
- **Error Boundaries**: Graceful error handling
- **Memory Management**: Proper cleanup of event listeners

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 **License**

This project is licensed under the MIT License.

---

**Built with ❤️ for the ArchSense Team**
