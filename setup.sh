#!/bin/bash

echo "============================================================"
echo "🚀 ARCHSENSE MERN STACK SETUP"
echo "============================================================"
echo

echo "📦 Installing root dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install root dependencies"
    exit 1
fi

echo
echo "📦 Installing backend dependencies..."
cd server
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install backend dependencies"
    exit 1
fi

echo
echo "📦 Installing frontend dependencies..."
cd ../client
npm install
if [ $? -ne 0 ]; then
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

cd ..

echo
echo "🔧 Setting up environment..."
if [ ! -f "server/.env" ]; then
    echo "📝 Creating .env file from template..."
    cp server/env.example server/.env
    echo "✅ Environment file created"
    echo "⚠️  Please edit server/.env with your configuration"
else
    echo "✅ Environment file already exists"
fi

echo
echo "============================================================"
echo "✅ SETUP COMPLETE!"
echo "============================================================"
echo
echo "🚀 To start the application:"
echo "   npm run dev"
echo
echo "📖 For more information, see README.md"
echo
