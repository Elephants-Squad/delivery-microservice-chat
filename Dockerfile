# Stage 1: Build environment
FROM python:3.12.1-bullseye AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Set the working directory to /app
WORKDIR /app

# Stage 2: Dependency installation
FROM python-base AS builder

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    libc6-dev \
    curl \
    wget \
    && \
    pip install --upgrade pip && \
    pip install poetry

# Copy pyproject.toml file to the container
COPY pyproject.toml /app

# Install dependencies using Poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Stage 3: Production environment
FROM python-base AS production

# Copy necessary files from the builder stage
COPY --from=builder . /app/

# Expose the port that the application will listen on
EXPOSE 8000