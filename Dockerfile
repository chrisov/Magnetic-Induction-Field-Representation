FROM python:3.11-slim

WORKDIR /app

# This command adds a rule that allows connections from the Docker container to your display
# RUN xhost +local:docker

# Install required system dependencies
RUN apt-get update
RUN apt-get install -y --no-install-recommends qtbase5-dev
RUN apt-get install -y --no-install-recommends qttools5-dev-tools
RUN apt-get install -y --no-install-recommends libfreetype6-dev
RUN apt-get install -y --no-install-recommends libpng-dev
RUN apt-get install -y --no-install-recommends gcc
RUN apt-get install -y --no-install-recommends g++
RUN apt-get install -y --no-install-recommends make

# X11 forwarding dependencies
RUN apt-get install -y --no-install-recommends libgl1
RUN apt-get install -y --no-install-recommends libglx-mesa0
RUN apt-get install -y --no-install-recommends libglx0
RUN apt-get install -y --no-install-recommends libsm6
RUN apt-get install -y --no-install-recommends libxrender1
RUN apt-get install -y --no-install-recommends libfontconfig1
RUN apt-get install -y --no-install-recommends libice6
RUN apt-get install -y --no-install-recommends libxi6
RUN apt-get install -y --no-install-recommends libxkbcommon-x11-0
RUN apt-get install -y --no-install-recommends libxcb-randr0
RUN apt-get install -y --no-install-recommends libxcb-cursor0

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies in one step
RUN pip install --upgrade pip
RUN pip install --no-cache-dir numpy
RUN pip install --no-cache-dir matplotlib
RUN pip install --no-cache-dir python-dotenv
RUN pip install --no-cache-dir PyQt6 
    
# Copy application files
COPY . .

# Set the default command
CMD ["python3", "main.py"]
