# Use slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file first for dependency install
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8100

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8100"]
