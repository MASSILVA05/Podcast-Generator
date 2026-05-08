FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libcairo2 libcairo2-dev pkg-config gcc g++ git \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY back/ ./back/
COPY voix.json ./
EXPOSE 8000
CMD ["uvicorn", "back.api:app", "--host", "0.0.0.0", "--port", "8000"]