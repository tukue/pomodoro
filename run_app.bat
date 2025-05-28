@echo off
:: Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Run the application
echo Starting Pomodoro Timer...
python src\main.py

:: Deactivate virtual environment
deactivate