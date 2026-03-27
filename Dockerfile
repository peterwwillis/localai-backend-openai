FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./

EXPOSE 50051

# Entrypoint
CMD ["python", "main.py"]
