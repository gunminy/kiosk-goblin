#!/bin/bash

# Kiosk Goblin - Linux Startup Script
# This script runs the Streamlit visualization framework in headless mode and
# automatically opens Chromium in fullscreen Kiosk Mode on the secondary/primary display.

# Get current script directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
PROJECT_DIR="$(dirname "$DIR")"

echo "👺 Starting Kiosk Goblin MVP..."

# Check if chromium-browser or google-chrome is installed
if command -v google-chrome &> /dev/null; then
    CHROME_BIN="google-chrome"
elif command -v chromium-browser &> /dev/null; then
    CHROME_BIN="chromium-browser"
elif command -v chromium &> /dev/null; then
    CHROME_BIN="chromium"
else
    echo "⚠️ Warning: Neither Google Chrome nor Chromium browser was found in PATH."
    echo "You must install Chrome or Chromium to utilize Kiosk mode."
    CHROME_BIN=""
fi

# Run Streamlit server in the background
cd "$PROJECT_DIR"
echo "🚀 Initializing Streamlit Server..."
streamlit run app.py --server.port=8501 --server.headless=true &
STREAMLIT_PID=$!

# Wait for 3 seconds to let Streamlit server bootstrap
sleep 3

if [ -n "$CHROME_BIN" ]; then
    echo "📺 Bootstrapping Chrome in Kiosk Mode at http://localhost:8501..."
    # Disable restore bubble prompts, start in kiosk fullscreen mode
    $CHROME_BIN \
        --start-fullscreen \
        --no-first-run \
        --disable-restore-session-state \
        --user-data-dir="/tmp/kiosk-chrome-profile" \
        "http://localhost:8501"
else
    echo "💡 To view your Kiosk Dashboard, open your web browser and navigate to:"
    echo "   👉 http://localhost:8501"
    # Wait for the backend process
    wait $STREAMLIT_PID
fi

# Cleanup background processes on exit
cleanup() {
    echo "🛑 Shutting down Kiosk Goblin..."
    kill $STREAMLIT_PID 2>/dev/null
    exit
}

trap cleanup INT TERM EXIT
