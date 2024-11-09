import time

import grpc

from src.generated import service_definitions_pb2 as pb2
from src.generated import service_definitions_pb2_grpc as pb2_grpc


class SimpleServicer(pb2_grpc.SimpleServiceServicer):
    def ProcessRequest(self, request, context):
        try:
            time.sleep(0.01)
            response = pb2.SimpleResponse(status="success", data=request.data)
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pb2.SimpleResponse()
