
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip \
    && pip install fastapi uvicorn python-multipart aiofiles

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
