FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Start command
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=10000"]
