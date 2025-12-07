@echo off
echo ============================================================
echo 🚀 ARCHSENSE MERN STACK SETUP
echo ============================================================
echo.

echo 📦 Installing root dependencies...
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install root dependencies
    pause
    exit /b 1
)

echo.
echo 📦 Installing backend dependencies...
cd server
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo 📦 Installing frontend dependencies...
cd ../client
call npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

cd ..

echo.
echo 🔧 Setting up environment...
if not exist "server\.env" (
    echo 📝 Creating .env file from template...
    copy "server\env.example" "server\.env"
    echo ✅ Environment file created
    echo ⚠️  Please edit server\.env with your configuration
) else (
    echo ✅ Environment file already exists
)

echo.
echo ============================================================
echo ✅ SETUP COMPLETE!
echo ============================================================
echo.
echo 🚀 To start the application:
echo    npm run dev
echo.
echo 📖 For more information, see README.md
echo.
pause
