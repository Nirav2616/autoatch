@echo off
echo ========================================
echo    ArchSense MERN Stack Setup
echo ========================================
echo.

REM Check if Node.js is installed
echo 🔍 Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed!
    echo.
    echo Please install Node.js 18+ from: https://nodejs.org/
    echo After installation, restart this script.
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js is installed
node --version

REM Check if npm is installed
echo.
echo 🔍 Checking npm installation...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed!
    pause
    exit /b 1
)

echo ✅ npm is installed
npm --version

REM Check if Git is installed
echo.
echo 🔍 Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/
    echo After installation, restart this script.
    echo.
    pause
    exit /b 1
)

echo ✅ Git is installed
git --version

REM Create necessary directories
echo.
echo 📁 Creating project structure...
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs
if not exist "ssl" mkdir ssl

REM Copy environment files
echo.
echo 📝 Setting up environment files...
if not exist "server\.env" (
    copy "server\env.example" "server\.env"
    echo ✅ Server environment file created
) else (
    echo ℹ️  Server environment file already exists
)

if not exist "client\.env" (
    copy "client\env.example" "client\.env"
    echo ✅ Client environment file created
) else (
    echo ℹ️  Client environment file already exists
)

REM Install dependencies
echo.
echo 📦 Installing dependencies...
echo Installing root dependencies...
call npm install

echo.
echo Installing server dependencies...
cd server
call npm install
cd ..

echo.
echo Installing client dependencies...
cd client
call npm install
cd ..

REM Check if MongoDB is available
echo.
echo 🔍 Checking MongoDB availability...
curl -s http://localhost:27017 >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ MongoDB is running locally
) else (
    echo ⚠️  MongoDB is not running locally
    echo.
    echo You have several options:
    echo 1. Install MongoDB locally
    echo 2. Use MongoDB Atlas (cloud)
    echo 3. Use Docker (recommended)
    echo.
    echo For Docker setup, run: docker-compose up -d
    echo.
)

REM Create startup scripts
echo.
echo 🚀 Creating startup scripts...
echo @echo off > start-dev.bat
echo echo Starting ArchSense in development mode... >> start-dev.bat
echo npm run dev >> start-dev.bat
echo pause >> start-dev.bat

echo @echo off > start-prod.bat
echo echo Starting ArchSense in production mode... >> start-prod.bat
echo npm run build >> start-prod.bat
echo npm start >> start-prod.bat
echo pause >> start-prod.bat

echo ✅ Startup scripts created

REM Display next steps
echo.
echo ========================================
echo    Setup Complete! 🎉
echo ========================================
echo.
echo 📋 Next Steps:
echo.
echo 1. Configure your environment:
echo    - Edit server\.env with your MongoDB connection
echo    - Edit client\.env with your API URL
echo.
echo 2. Start the application:
echo    - Development: run start-dev.bat
echo    - Production: run start-prod.bat
echo    - Docker: docker-compose up -d
echo.
echo 3. Access your application:
echo    - Frontend: http://localhost:3000
echo    - Backend API: http://localhost:5000/api
echo    - Health Check: http://localhost:5000/api/health
echo.
echo 📚 Documentation: README.md
echo 🐳 Docker: docker-compose.yml
echo.
echo Happy coding! 🚀
echo.
pause
