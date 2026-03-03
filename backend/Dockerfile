FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/huggingface
ENV NLTK_DATA=/app/.cache/nltk

WORKDIR /app


RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY backend ./backend

RUN mkdir -p /app/.cache/huggingface

RUN python - <<EOF
import nltk
nltk.download("punkt", download_dir="/app/.cache/nltk")
nltk.download("punkt_tab", download_dir="/app/.cache/nltk")
EOF

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
