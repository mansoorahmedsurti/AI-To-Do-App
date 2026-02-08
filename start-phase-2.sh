#!/bin/bash
# Script to start both frontend and backend servers

echo "Starting AI To-Do App - Phase 2..."

# Start backend server in the background
echo "Starting backend server..."
cd backend
python start_server.py &
BACKEND_PID=$!

# Give backend a moment to start
sleep 2

# Start frontend server in the background
echo "Starting frontend server..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID
wait $FRONTEND_PID

echo "Servers stopped."