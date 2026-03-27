FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend_pb2.py backend_pb2_grpc.py main.py ./

# Expose gRPC port
EXPOSE 50051

# Entrypoint
CMD ["python", "main.py"]
