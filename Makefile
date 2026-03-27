
all: docker-build

docker-build: gen-rpc
	docker build -t localai-backend-openai:latest .

gen-rpc: pip download-backend-proto
	./venv/bin/python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. backend.proto

download-backend-proto:
	curl -fsSL -o backend.proto https://raw.githubusercontent.com/mudler/LocalAI/master/backend/backend.proto

pip: venv
	./venv/bin/pip install -r requirements.txt

venv:
	python3 -m venv venv

