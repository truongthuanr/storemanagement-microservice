# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install netcat to run wait-for-it.sh 
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Copy entire project (including alembic.ini and alembic folder)
COPY . .



# Set PYTHONPATH
ENV PYTHONPATH=/app

# Expose FastAPI port
EXPOSE 8000

# Run migrations and start the app
CMD alembic -c alembic.ini upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
