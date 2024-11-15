# Stage 1: Export requirements using Poetry
FROM python:3.11-slim AS poetry
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Build Dependencies and Compile Protobufs
FROM python:3.11-slim AS build

WORKDIR /app

# Environment variables
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY --from=poetry /app/requirements.txt .
RUN pip install -r requirements.txt

# Copy source code and proto files
COPY src/ ./src/
COPY proto/ ./proto/

# Compile protocol buffers
RUN python -m grpc_tools.protoc -I./proto \
    --python_out=./src/generated \
    --grpc_python_out=./src/generated \
    ./proto/service_definitions.proto

# Stage 3: Final Image
FROM python:3.11-slim AS final

WORKDIR /app

ENV PYTHONPATH=/app

# Copy installed packages and application code from the build stage
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /app /app

EXPOSE 8000 8001

# Start the FastAPI application with auto-reload
CMD ["python", "-m", "uvicorn", "src.rest_services.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "./src"]
