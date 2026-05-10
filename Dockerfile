# FROM python:3.10-slim

# WORKDIR /app

# # Install dependencies
# COPY master_requirements.txt .
# RUN pip install --no-cache-dir -r master_requirements.txt

# # Copy entire project
# COPY . .

# # Expose all orchestration ports
# EXPOSE 8501 8502 8503 8504 8505 5000

# # Run the master orchestrator
# CMD ["python", "master_app.py"]


FROM python:3.10-slim

WORKDIR /app

# STEP 1: Force install CPU-only PyTorch to prevent pip from backtracking and downloading Nvidia CUDA drivers
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# STEP 2: Copy your requirements
COPY master_requirements.txt .

# STEP 3: Install the remaining requirements
# Using --prefer-binary prevents pip from trying to build complex packages from scratch
RUN pip install --no-cache-dir --prefer-binary -r master_requirements.txt

# STEP 4: Copy the rest of the project
COPY . .

EXPOSE 8501 8502 8503 8504 8505 5000

CMD ["python", "master_app.py"]