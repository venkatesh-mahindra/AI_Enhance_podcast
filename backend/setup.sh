#!/bin/bash

echo "========================================"
echo "PDF to Podcast Backend Setup"
echo "========================================"

echo ""
echo "Creating virtual environment..."
python3 -m venv venv

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Downloading spaCy model..."
python -m spacy download en_core_web_sm

echo ""
echo "Creating directories..."
mkdir -p temp_uploads logs default_voices

echo ""
echo "Copying environment file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Please edit .env file with your AWS credentials!"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your AWS credentials"
echo "2. Create S3 bucket: pdf-podcast-bucket"
echo "3. Install FFmpeg and espeak-ng"
echo "4. Run: python app.py"
echo ""