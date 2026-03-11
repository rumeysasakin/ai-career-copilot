FROM python:3.11-slim

WORKDIR /app

# uv kurulumu
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Bağımlılık dosyalarını kopyala (cache katmanı)
COPY pyproject.toml uv.lock ./

# Bağımlılıkları yükle
RUN uv sync --no-dev --frozen

# Uygulama kodunu kopyala
COPY . .

EXPOSE 8501

ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

CMD ["uv", "run", "streamlit", "run", "streamlit_app.py"]
