import subprocess
import sys
import os

def install_dependencies():
    packages = [
        "nicegui==1.4.21",
        "requests==2.31.0", 
        "python-dotenv==1.0.0",
        "pydantic==2.5.0",
        "uvicorn==0.24.0"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")

def test_imports():
    try:
        import nicegui
        print("✓ NiceGUI imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import NiceGUI: {e}")
        return False

def run_app():
    try:
        os.system("python main.py")
    except Exception as e:
        print(f"✗ Failed to run app: {e}")

if __name__ == "__main__":
    print("Installing dependencies...")
    install_dependencies()
    
    print("\nTesting imports...")
    if test_imports():
        print("\nStarting application...")
        run_app()
    else:
        print("\nDependencies not properly installed. Please install manually.")
