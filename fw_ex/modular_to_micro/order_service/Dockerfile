FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

LABEL service="order-service"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002", "--reload"] 