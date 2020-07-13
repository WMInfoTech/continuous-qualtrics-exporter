FROM python:3.8.3

ENV PYTHONUNBUFFERED=1

COPY app /app

WORKDIR /app

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir git+https://github.com/WMInfoTech/python-msgraph.git

CMD ["python", "/app/main.py"]
