@echo off
echo ========================================
echo PDF to Podcast Backend Setup
echo ========================================

echo.
echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Downloading spaCy model...
python -m spacy download en_core_web_sm

echo.
echo Creating directories...
if not exist "temp_uploads" mkdir temp_uploads
if not exist "logs" mkdir logs
if not exist "default_voices" mkdir default_voices

echo.
echo Copying environment file...
if not exist ".env" (
    copy .env.example .env
    echo Please edit .env file with your AWS credentials!
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your AWS credentials
echo 2. Create S3 bucket: pdf-podcast-bucket
echo 3. Install FFmpeg and espeak-ng (see documentation)
echo 4. Run: python app.py
echo.
pause