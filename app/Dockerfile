# Use Python 3.13.5 slim image
FROM python:3.13.5-slim

# Set working directory
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY app.py .
COPY package/ ./package/
COPY config.yaml .

# Run your app
CMD ["python", "app.py"]