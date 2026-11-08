
# Base image
FROM python:3.12-slim

# Working directory
WORKDIR /app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 1. Copy dependencies first
COPY requirement.txt .

# 2. Install Python dependencies
RUN pip install --no-cache-dir -r requirement.txt

# 3. Install Playwright Chromium and its system dependencies
RUN playwright install --with-deps chromium

# 4. Copy application code last
COPY . .

# 5. Create logs directory
RUN mkdir -p /app/logs

# Port
EXPOSE 8000

# Start application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
