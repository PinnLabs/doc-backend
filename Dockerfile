FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    wget \ 
    libpng-dev \
    libjpeg-dev \
    libpoppler-cpp-dev \
    zlib1g-dev \
    libglib2.0-0 \
    libxml2 \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/pdf2htmlEX/pdf2htmlEX/releases/download/v0.18.8.rc1/pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb && \
    dpkg -i pdf2htmlex_0.18.8.rc2-1_amd64.deb || apt-get install -f -y && \
    rm pdf2htmlex_0.18.8.rc2-1_amd64.deb

# Instala o gerenciador de pacotes uv
RUN apt-get update && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    apt-get remove -y curl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="/root/.cargo/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv pip install -r uv.lock --system

COPY . /app

EXPOSE 8005
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005", "--forwarded-allow-ips", "*", "--proxy-headers"]
