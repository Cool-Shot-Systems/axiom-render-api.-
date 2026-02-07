# Use a slim Python 3.10 image (Standard for 2026 AI)
FROM python:3.10-slim

# 1. Install System Compilers (Required for Llama.cpp)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Set the working directory
WORKDIR /app

# 3. Copy dependencies and install
COPY requirements.txt .
# We use --no-cache-dir to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the application code
COPY . .

# 5. Expose the standard port
EXPOSE 8000

# 6. Start the FastAPI server with high timeout limits
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "300"]
