# AutoArch - AI-Powered Smart Architecture Designer

AutoArch is a cutting-edge web application designed to revolutionize the way users create and visualize architectural floor plans. By leveraging AI and procedural generation, it allows users to generate optimized floor layouts based on specific requirements and visualize them instantly in 3D.

## 🚀 Features

- **Dynamic Layout Generation**: Automatically generates floor plans based on user-defined room counts and area requirements. Supports multiple layout strategies (Grid, L-Shaped, Courtyard, Open Plan).
- **Interactive 2D & 3D Editor**: Seamlessly switch between a 2D blueprint view and an immersive 3D walkthrough.
- **Smart Room Management**:
  - **Add/Remove Rooms**: Dynamically adjust the floor plan.
  - **Room Functions**: Add doors and windows, duplicate rooms, and delete unwanted spaces.
  - **Customization**: Adjust dimensions, wall colors, and floor materials.
- **Rich Furniture Catalog**:
  - **Live Library**: Browse a categorized catalog of furniture items (Living, Bedroom, Kitchen, etc.).
  - **Search & Filter**: Quickly find items by name or tag.
  - **Drag & Drop**: Place furniture directly into rooms.
- **Real-Time Visualization**: High-performance 3D rendering using Three.js and React Three Fiber.
- **Project Management**: Save and load your designs (Work in Progress).

## 🛠️ Tech Stack

### Frontend
- **Framework**: React (Vite)
- **Language**: TypeScript
- **Styling**: Tailwind CSS, Shadcn UI
- **State Management**: Zustand
- **3D Graphics**: Three.js, @react-three/fiber, @react-three/drei

### Backend
- **Runtime**: Node.js
- **Framework**: Express.js
- **Database**: PostgreSQL (via Drizzle ORM)
- **API**: RESTful endpoints for layout generation and furniture data

## 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd ArchSense
    ```

2.  **Install Dependencies**
    The project includes a convenience script to install dependencies for both client and server.
    ```bash
    npm run setup
    ```
    *Alternatively, you can install them manually:*
    ```bash
    npm install
    cd client && npm install
    cd ../server && npm install
    ```

3.  **Environment Configuration**
    Create a `.env` file in the `server` directory (and `client` if needed) with your configuration variables (Database URL, etc.).

4.  **Start the Application**
    Run the development server (starts both client and backend):
    ```bash
    npm run dev
    ```
    - Frontend: `http://localhost:5173`
    - Backend: `http://localhost:5000`

## 🎮 Usage

1.  **Define Requirements**: Use the left sidebar to set the number of bedrooms, bathrooms, etc., and the total site area.
2.  **Generate Layout**: Click "Regenerate Layout" to create a new floor plan.
3.  **Customize**:
    - Click on a room in 3D view to select it.
    - Use the Right Sidebar to change colors, materials, or add doors/windows.
    - Open the "Catalog" tab to add furniture.
4.  **Explore**: Use the mouse to orbit, pan, and zoom in the 3D view.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.
