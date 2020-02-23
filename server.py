import grpc
from concurrent import futures

import mlflow.pyfunc

import mlflow_pb2
import mlflow_pb2_grpc

MODEL_PATH = "model/mlruns/0/b185538811854dc19978ae7e8c1356c5/artifacts/model/"
MODEL = mlflow.pyfunc.load_model(MODEL_PATH)

class MlflowModelsServicer(mlflow_pb2_grpc.MLflowServicer):
    def _predict(self, input):
        return MODEL.predict(input)

    def predict(self, request, context):
        print(f"RECEIVED: {request.value}")
        response = mlflow_pb2.Output()
        response.value = self._predict(request.value)
        
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
mlflow_pb2_grpc.add_MLflowServicer_to_server(MlflowModelsServicer(), server)

print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()