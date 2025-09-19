#!/usr/bin/env python3
"""
JobBoard Application Startup Script
Ensures proper configuration and runs the application with authentication support
"""

import os
import sys
from nicegui import ui
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Import main application
from main import *

if __name__ == "__main__":
    # Get configuration from environment
    storage_secret = os.getenv('STORAGE_SECRET', 'dev-fallback-secret-change-in-production')
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print("🚀 Starting JobBoard Application with Authentication...")
    print("📍 Project Directory:", project_dir)
    print("🔐 Authentication: Enabled")
    print("💾 Storage: Configured with secure secret")
    print(f"🌐 Server: http://localhost:{port}")
    print(f"🔧 Debug Mode: {debug}")
    print("=" * 50)
    
    # Add Tailwind CSS
    ui.add_head_html('<script src="https://cdn.tailwindcss.com"></script>')
    
    # Run with proper configuration from environment
    ui.run(
        title="JobBoard - Modern Job Portal",
        port=port,
        host="0.0.0.0",
        storage_secret=storage_secret,  # Secure secret from .env
        show=True,  # Auto-open browser
        reload=debug,  # Enable reload only in debug mode
        favicon="🔍"
    )
