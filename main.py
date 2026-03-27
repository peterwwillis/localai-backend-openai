import os
import grpc
from concurrent import futures
import backend_pb2
import backend_pb2_grpc
from openai import OpenAI

# Initialize the real OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class OpenAIProxyServicer(backend_pb2_grpc.BackendServicer):
    def Health(self, request, context):
        return backend_pb2.Reply(message="OK")

    def LoadModel(self, request, context):
        # LocalAI calls this first. You can use request.Model to decide 
        # which OpenAI model to target later.
        print(f"Loading proxy for model: {request.Model}")
        return backend_pb2.Reply(message="Model logic initialized")

    def Predict(self, request, context):
        # Map LocalAI's PredictRequest to OpenAI's Chat Completion
        # LocalAI often sends the full prompt in request.Prompt
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": request.Prompt}],
            temperature=request.Temperature or 0.7,
        )
        
        text_result = response.choices[0].message.content
        return backend_pb2.Reply(message=text_result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    backend_pb2_grpc.add_BackendServicer_to_server(OpenAIProxyServicer(), server)
    server.add_insecure_port('[::]:50051')
    print("Proxy Backend running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
