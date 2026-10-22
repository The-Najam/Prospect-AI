
# Base image
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies first (enables caching)
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt
RUN playwright install --with-deps chromium

# Copy application code
COPY . .

# Create logs directory
RUN mkdir -p /app/logs

# Port
EXPOSE 8000

# Start application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
