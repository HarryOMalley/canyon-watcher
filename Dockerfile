# Use an official lightweight Python image.
FROM python:3.12-slim as base

# Prevent Python from writing .pyc files and enable unbuffered logging.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/src

WORKDIR /app

# Install system dependencies if any are needed.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application.
COPY src/ /app/src/
COPY config.toml.example /app/config.toml

# Create a non-root user and switch to it.
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Expose the port the app runs on.
EXPOSE 8080

# Command to run the application.
CMD ["python", "src/main.py"]
