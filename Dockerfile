FROM python:3.8.3

ENV PYTHONUNBUFFERED=1

COPY app /app

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

CMD ["python", "/app/main.py"]
