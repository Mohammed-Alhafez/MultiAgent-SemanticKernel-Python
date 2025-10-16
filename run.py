#!/usr/bin/env python3
"""
Run script for Multi-Agent Task Management System

This script provides an easy way to start the system with proper checks
and error handling.

Author: MultiAgent-SemanticKernel-Python
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path


def check_config():
    """Check if config.env exists and has required variables."""
    config_file = Path("config.env")
    
    if not config_file.exists():
        print("❌ config.env not found!")
        print("Please copy config.env.example to config.env and update with your credentials.")
        return False
    
    # Check for required environment variables
    required_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_CHAT_DEPLOYMENT',
        'SENDER_EMAIL',
        'APP_PASSWORD'
    ]
    
    missing_vars = []
    with open(config_file, 'r') as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=your_" in content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or incomplete configuration: {', '.join(missing_vars)}")
        print("Please update config.env with your actual credentials.")
        return False
    
    print("✅ Configuration file is valid")
    return True


def start_mcp_server():
    """Start the MCP server in a separate process."""
    try:
        print("🚀 Starting MCP server...")
        process = subprocess.Popen([sys.executable, "MCPServer.py"])
        print("✅ MCP server started")
        return process
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return None


def start_main_app():
    """Start the main application."""
    try:
        print("🚀 Starting main application...")
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error running main application: {e}")


def main():
    """Main function to run the system."""
    print("🤖 Multi-Agent Task Management System")
    print("=" * 40)
    
    # Check configuration
    if not check_config():
        sys.exit(1)
    
    # Start MCP server
    mcp_process = start_mcp_server()
    if not mcp_process:
        sys.exit(1)
    
    # Wait a moment for MCP server to start
    print("⏳ Waiting for MCP server to initialize...")
    time.sleep(3)
    
    try:
        # Start main application
        start_main_app()
    finally:
        # Clean up MCP server process
        if mcp_process:
            print("🛑 Stopping MCP server...")
            mcp_process.terminate()
            mcp_process.wait()
            print("✅ MCP server stopped")


if __name__ == "__main__":
    main()
