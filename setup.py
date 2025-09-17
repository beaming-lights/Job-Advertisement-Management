import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError:
        print(f"Failed to install {package}")

packages = ["nicegui", "requests", "python-dotenv", "pydantic", "uvicorn"]

for package in packages:
    install_package(package)

print("All packages installation attempted.")
