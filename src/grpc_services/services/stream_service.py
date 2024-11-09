import time

import grpc

from src.generated import service_definitions_pb2 as pb2
from src.generated import service_definitions_pb2_grpc as pb2_grpc


class StreamingServicer(pb2_grpc.StreamingServiceServicer):
    def StreamData(self, request, context):
        messages_sent = 0
        try:
            for i in range(request.number_of_messages):
                yield pb2.StreamResponse(
                    data=f"Message {i}", timestamp=int(time.time() * 1000)
                )
                messages_sent += 1
                time.sleep(0.01)  # Simulate streaming interval

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
