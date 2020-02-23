import grpc

import mlflow_pb2
import mlflow_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = mlflow_pb2_grpc.MLflowStub(channel)

message = "HELLO WORLD"
input = mlflow_pb2.Input(value=message)

response = stub.predict(input)

print(response.value)