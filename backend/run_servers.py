#!/usr/bin/env python3
"""
Script to run both the main API server and the MCP server
"""

import subprocess
import sys
import threading
import time
import signal
import os

def run_main_server():
    """Run the main FastAPI server"""
    os.chdir(os.path.dirname(__file__))
    cmd = [sys.executable, "start_server.py"]
    process = subprocess.Popen(cmd)
    return process

def run_mcp_server():
    """Run the MCP server"""
    os.chdir(os.path.dirname(__file__))
    cmd = [sys.executable, "-m", "app.mcp.server"]
    process = subprocess.Popen(cmd)
    return process

def main():
    print("Starting AI To-Do App servers...")
    print("Starting main API server...")

    # Start main server
    main_process = run_main_server()

    print("Starting MCP server...")
    # Start MCP server
    mcp_process = run_mcp_server()

    def signal_handler(signum, frame):
        print("\nShutting down servers...")
        main_process.terminate()
        mcp_process.terminate()
        main_process.wait()
        mcp_process.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Wait for either process to finish
        while True:
            if main_process.poll() is not None:
                print("Main server exited")
                break
            if mcp_process.poll() is not None:
                print("MCP server exited")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        main_process.terminate()
        mcp_process.terminate()
        main_process.wait()
        mcp_process.wait()

if __name__ == "__main__":
    main()