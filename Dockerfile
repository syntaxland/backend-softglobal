# Use a small, stable base image
FROM python:3.11-slim

# Prevents Python from buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system deps (for psycopg2, Pillow, SSL, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc build-essential netcat-traditional \
    ca-certificates curl \
    && rm -rf /var/lib/apt/lists/*

# Add this line to ensure certificates are trusted
RUN update-ca-certificates

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && pip install -r requirements.txt

# Copy project code
COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 8000
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
