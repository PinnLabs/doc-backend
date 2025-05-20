# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    git \
    libpng-dev \
    ca-certificates \
    libjpeg-dev \
    libpoppler-cpp-dev \
    zlib1g-dev \
    libglib2.0-0 \
    libxml2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libjpeg-dev \
    libxml2 \
    libxslt1.1 \
    libpq-dev \
    libssl-dev \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

# Install pdf2htmlEX
RUN wget https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb \
    && dpkg -i pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb || apt-get install -f -y \
    && rm pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb

# Install uv (dependency manager)
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Copy project files
COPY . /app

# Sync dependencies (assumes `uv.lock` is present)
RUN uv sync --locked

# Expose the desired port
EXPOSE 8005

# Default command to run the app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005", "--forwarded-allow-ips", "*", "--proxy-headers"]
