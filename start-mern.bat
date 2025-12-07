@echo off
echo ========================================
echo    ArchSense MERN Stack Startup
echo ========================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if MongoDB is running (optional)
echo 🔍 Checking MongoDB connection...
curl -s http://localhost:27017 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ MongoDB is running
) else (
    echo ⚠️  MongoDB is not running on localhost:27017
    echo    Make sure MongoDB is started or update your .env file
    echo.
)

REM Check if environment files exist
if not exist "server\.env" (
    echo ⚠️  Server environment file not found!
    echo    Copying from example...
    copy "server\env.example" "server\.env"
    echo    Please edit server\.env with your configuration
    echo.
)

if not exist "client\.env" (
    echo ⚠️  Client environment file not found!
    echo    Copying from example...
    copy "client\env.example" "client\.env"
    echo.
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo 📦 Installing root dependencies...
    npm install
)

if not exist "server\node_modules" (
    echo 📦 Installing server dependencies...
    cd server
    npm install
    cd ..
)

if not exist "client\node_modules" (
    echo 📦 Installing client dependencies...
    cd client
    npm install
    cd ..
)

echo.
echo 🚀 Starting ArchSense MERN Stack...
echo.
echo 📱 Frontend will be available at: http://localhost:3000
echo 🔗 Backend API will be available at: http://localhost:5000/api
echo.
echo Press Ctrl+C to stop all services
echo.

REM Start the development servers
npm run dev

pause
