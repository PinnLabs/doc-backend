FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl && \
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
