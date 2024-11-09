import time

import grpc

from src.generated import service_definitions_pb2 as pb2
from src.generated import service_definitions_pb2_grpc as pb2_grpc


class PayloadServicer(pb2_grpc.PayloadServiceServicer):
    def ProcessLargePayload(self, request, context):
        try:
            time.sleep(0.02 * (request.size_kb / 1024))

            response = pb2.PayloadResponse(
                success=True, processed_size_kb=request.size_kb
            )
            return response
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pb2.PayloadResponse(success=False)
