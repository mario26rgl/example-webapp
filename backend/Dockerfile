# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Copy Flake8 configuration
COPY .flake8 .

# Expose the Flask application port
EXPOSE 80

# Run the application
CMD ["python", "app.py"]