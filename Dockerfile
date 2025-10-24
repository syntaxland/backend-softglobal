# Use a small, stable base image
FROM python:3.11-slim

# Prevents Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set working directory
WORKDIR /app

# Install system deps (for psycopg2 and Pillow)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . .

# Create a non-root user (for security)
RUN useradd -m appuser
USER appuser

# Expose port 8000 (Django default)
EXPOSE 8000

# Entry point for Docker Compose (runs Django via gunicorn)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
