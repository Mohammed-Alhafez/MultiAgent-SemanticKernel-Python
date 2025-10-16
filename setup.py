#!/usr/bin/env python3
"""
Setup script for Multi-Agent Task Management System

This script helps users set up the project by creating necessary directories,
checking dependencies, and providing setup instructions.

Author: MultiAgent-SemanticKernel-Python
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        'semantic-kernel',
        'azure-search-documents',
        'azure-ai-openai',
        'python-dotenv',
        'fastmcp'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True


def create_config_file():
    """Create config.env from example if it doesn't exist."""
    config_file = Path("config.env")
    example_file = Path("config.env.example")
    
    if not config_file.exists():
        if example_file.exists():
            shutil.copy(example_file, config_file)
            print("✅ Created config.env from example")
            print("⚠️  Please update config.env with your actual credentials")
        else:
            print("❌ config.env.example not found")
            return False
    else:
        print("✅ config.env already exists")
    
    return True


def create_directories():
    """Create necessary directories."""
    directories = ['logs', 'data']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")


def main():
    """Main setup function."""
    print("🚀 Multi-Agent Task Management System Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create config file
    if not create_config_file():
        sys.exit(1)
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        print("\n🔧 Setup incomplete. Please install missing dependencies.")
        sys.exit(1)
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update config.env with your Azure OpenAI and Azure Search credentials")
    print("2. Set up Gmail app password for email notifications")
    print("3. Start the MCP server: python MCPServer.py")
    print("4. Run the main application: python main.py")


if __name__ == "__main__":
    main()
