# ============================================================
#  Dockerfile  –  LLM Prompt Router
# ============================================================

FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY prompts.py .
COPY router.py .
COPY main.py .
COPY app.py .
COPY test_router.py .

RUN mkdir -p /app/templates
COPY templates/ /app/templates/

# Create logs directory so route_log.jsonl persists
RUN mkdir -p /app/logs
VOLUME ["/app/logs"]

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]