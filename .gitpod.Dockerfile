# syntax=docker/dockerfile:1.4
FROM gitpod/workspace-full

# Install system dependencies in one layer
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    curl \
 && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 \
 && update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Install uv and make it available
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/home/gitpod/.cargo/bin:/root/.cargo/bin:$PATH"

# Set working directory early
WORKDIR /workspace

# Copy dependency files first (for better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies with cache mount
RUN --mount=type=cache,target=/home/gitpod/.cache/uv \
    --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# Copy application code (this layer changes most often)
COPY . .

# Set up persistent cache directories
RUN mkdir -p /workspace/.cache/pip /workspace/.cache/uv

# Set environment variables for caching
ENV PIP_CACHE_DIR=/workspace/.cache/pip
ENV UV_CACHE_DIR=/workspace/.cache/uv
ENV PYTHONPATH=/workspace