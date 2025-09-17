#!/usr/bin/env python3

print("Testing dependencies...")

try:
    import nicegui
    print("✓ nicegui - OK")
except ImportError as e:
    print(f"✗ nicegui - MISSING: {e}")

try:
    import requests
    print("✓ requests - OK")
except ImportError as e:
    print(f"✗ requests - MISSING: {e}")

try:
    import dotenv
    print("✓ python-dotenv - OK")
except ImportError as e:
    print(f"✗ python-dotenv - MISSING: {e}")

try:
    import pydantic
    print("✓ pydantic - OK")
except ImportError as e:
    print(f"✗ pydantic - MISSING: {e}")

try:
    import uvicorn
    print("✓ uvicorn - OK")
except ImportError as e:
    print(f"✗ uvicorn - MISSING: {e}")

print("\nDependency check complete.")
