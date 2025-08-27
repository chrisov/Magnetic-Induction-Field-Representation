FROM python:3.11-slim

WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    qtbase5-dev \
    qttools5-dev-tools \
    libfreetype6-dev \
    libpng-dev \
    gcc \
    g++ \
    make && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies in one step
RUN pip install --upgrade pip && \
    pip install --no-cache-dir numpy matplotlib PyQt6

# Copy application files
COPY . .

# Set the default command
CMD ["python3", "main.py"]