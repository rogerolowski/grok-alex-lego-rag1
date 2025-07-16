FROM gitpod/workspace-full

# Update and install Python 3.10 and tools
RUN sudo apt-get update && sudo apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    sqlite3 \
    && sudo rm -rf /var/lib/apt/lists/*

# Set Python 3.10 as the default
RUN sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1
RUN sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1