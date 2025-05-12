#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Searching for processes using port 8000..."

# Find process using port 8000
PORT_PID=$(lsof -ti:8000)

# If a process is using the port, terminate it
if [ ! -z "$PORT_PID" ]; then
    echo "Found process using port 8000 (PID: $PORT_PID). Terminating..."
    kill -9 $PORT_PID
    echo "Process terminated successfully."
else
    echo "No processes are using port 8000."
fi

# Wait a moment to ensure the port is released
sleep 1

echo "Starting Django server on port 8000..."

# Run Django server
python manage.py runserver 0.0.0.0:8000
