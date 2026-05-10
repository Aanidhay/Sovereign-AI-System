FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY master_requirements.txt .
RUN pip install --no-cache-dir -r master_requirements.txt

# Copy entire project
COPY . .

# Expose all orchestration ports
EXPOSE 8501 8502 8503 8504 8505 5000

# Run the master orchestrator
CMD ["python", "master_app.py"]