# ---- Base image ----
    FROM python:3.11-slim

    # ---- Set working directory ----
    WORKDIR /app
    
    # ---- Install system dependencies ----
    RUN apt-get update && apt-get install -y \
        build-essential \
        libmariadb-dev \
        gcc \
        && rm -rf /var/lib/apt/lists/*
    
    # ---- Install Python dependencies ----
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # ---- Copy application code ----
    COPY . .
    
    # ---- Set environment variables (optional fallback values) ----
    ENV DB_HOST=localhost
    ENV DB_PORT=3306
    ENV DB_NAME=product_db
    ENV DB_USER=user
    ENV DB_PASSWORD=password
    ENV INVENTORY_GRPC_HOST=localhost
    ENV INVENTORY_GRPC_PORT=50051
    
    # ---- Expose port ----
    EXPOSE 8000
    
    # ---- Run the FastAPI app ----
    CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
    