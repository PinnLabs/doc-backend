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
    rm pdf2htmlEX-0.18.8.rc1-master-20200630-Ubuntu-bionic-x86_64.deb

# Instala o gerenciador de pacotes uv

# Baixa e instala o uv
RUN curl -L https://github.com/astral-sh/uv/releases/latest/download/uv-x86_64-unknown-linux-gnu.tar.gz | tar -xz && \
    mv uv-x86_64-unknown-linux-gnu/uv /usr/local/bin/ && \
    chmod +x /usr/local/bin/uv && \
    rm -rf uv-x86_64-unknown-linux-gnu*


ENV PATH="/root/.cargo/bin:$PATH"

COPY pyproject.toml requirements.txt ./
RUN uv run pip install --requirements pyproject.toml 

COPY . /app

EXPOSE 8005
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8005", "--forwarded-allow-ips", "*", "--proxy-headers"]
