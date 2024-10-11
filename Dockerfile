# Stage 1: Build environment
FROM python:3.12.1-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory to /app
WORKDIR /app

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

# Copy necessary files from the builder stage
COPY . /app/