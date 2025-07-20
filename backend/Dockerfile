# Use the official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install uv
RUN pip install uv

# Set the working directory
WORKDIR /app

# Copy project files
COPY . .

# Create virtual environment and sync dependencies using uv
RUN uv venv && uv pip sync pyproject.toml

# Expose port (Fly expects 8080)
EXPOSE 8080

# Start FastAPI using uvicorn
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
