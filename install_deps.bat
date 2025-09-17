@echo off
echo Installing dependencies...
python -m pip install --upgrade pip
python -m pip install nicegui==1.4.21
python -m pip install requests==2.31.0
python -m pip install python-dotenv==1.0.0
python -m pip install pydantic==2.5.0
python -m pip install uvicorn==0.24.0
echo.
echo Testing imports...
python -c "import nicegui; print('NiceGUI: OK')"
python -c "import requests; print('Requests: OK')"
python -c "import dotenv; print('Python-dotenv: OK')"
python -c "import pydantic; print('Pydantic: OK')"
python -c "import uvicorn; print('Uvicorn: OK')"
echo.
echo Dependencies installed successfully!
echo Starting application...
python main.py
