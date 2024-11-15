import logging
from concurrent import futures

import grpc
from prometheus_client import start_http_server

from src.generated import service_definitions_pb2_grpc as pb2_grpc
from src.grpc_services.services.payload_service import PayloadServicer
from src.grpc_services.services.simple_service import SimpleServicer
from src.grpc_services.services.stream_service import StreamingServicer
from src.grpc_services.utils.metrics import REQUEST_COUNT, REQUEST_LATENCY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PrometheusInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        handler = continuation(handler_call_details)
        if handler is None:
            return None

        method = handler_call_details.method
        service_name = method.split("/")[1]
        method_name = method.split("/")[2]

        if isinstance(handler, grpc.RpcMethodHandler):
            if handler.unary_unary:
                original_handler = handler.unary_unary

                def new_unary_unary(request, context):
                    with REQUEST_LATENCY.labels(
                        service=service_name, method=method_name
                    ).time():
                        try:
                            response = original_handler(request, context)
                            REQUEST_COUNT.labels(
                                service=service_name,
                                method=method_name,
                                grpc_status="OK",
                            ).inc()
                            return response
                        except grpc.RpcError as e:
                            REQUEST_COUNT.labels(
                                service=service_name,
                                method=method_name,
                                grpc_status=e.code().name,
                            ).inc()
                            raise

                return grpc.unary_unary_rpc_method_handler(
                    new_unary_unary,
                    request_deserializer=handler.request_deserializer,
                    response_serializer=handler.response_serializer,
                )

            elif handler.unary_stream:
                original_handler = handler.unary_stream

                def new_unary_stream(request, context):
                    with REQUEST_LATENCY.labels(
                        service=service_name, method=method_name
                    ).time():
                        try:
                            responses = original_handler(request, context)
                            REQUEST_COUNT.labels(
                                service=service_name,
                                method=method_name,
                                grpc_status="OK",
                            ).inc()
                            for response in responses:
                                yield response
                        except grpc.RpcError as e:
                            REQUEST_COUNT.labels(
                                service=service_name,
                                method=method_name,
                                grpc_status=e.code().name,
                            ).inc()
                            raise

                return grpc.unary_stream_rpc_method_handler(
                    new_unary_stream,
                    request_deserializer=handler.request_deserializer,
                    response_serializer=handler.response_serializer,
                )

            elif handler.stream_unary:
                original_handler = handler.stream_unary

                def new_stream_unary(request_iterator, context):
                    with REQUEST_LATENCY.labels(
                        service=service_name, method=method_name
                    ).time():
                        try:
                            response = original_handler(
                                request_iterator,
                                context,
                            )
                            REQUEST_COUNT.labels(
                                service=service_name,
                                method=method_name,
                                grpc_status="OK",
                            ).inc()
                            return response
                        except grpc.RpcError as e:
                            REQUEST_COUNT.labels(
                                service=service_name,
                                method=method_name,
                                grpc_status=e.code().name,
                            ).inc()
                            raise

                return grpc.stream_unary_rpc_method_handler(
                    new_stream_unary,
                    request_deserializer=handler.request_deserializer,
                    response_serializer=handler.response_serializer,
                )

            elif handler.stream_stream:
                original_handler = handler.stream_stream

                def new_stream_stream(request_iterator, context):
                    with REQUEST_LATENCY.labels(
                        service=service_name, method=method_name
                    ).time():
                        try:
                            responses = original_handler(
                                request_iterator,
                                context,
                            )
                            REQUEST_COUNT.labels(
                                service=service_name,
                                method=method_name,
                                grpc_status="OK",
                            ).inc()
                            for response in responses:
                                yield response
                        except grpc.RpcError as e:
                            REQUEST_COUNT.labels(
                                service=service_name,
                                method=method_name,
                                grpc_status=e.code().name,
                            ).inc()
                            raise

                return grpc.stream_stream_rpc_method_handler(
                    new_stream_stream,
                    request_deserializer=handler.request_deserializer,
                    response_serializer=handler.response_serializer,
                )

        return handler


def serve():
    # Start Prometheus metrics server on port 8002
    start_http_server(8002)
    logger.info("Prometheus metrics server started on port 8002")

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=5000),
        interceptors=[PrometheusInterceptor()],
    )

    # Register your servicers here
    pb2_grpc.add_PayloadServiceServicer_to_server(PayloadServicer(), server)
    pb2_grpc.add_SimpleServiceServicer_to_server(SimpleServicer(), server)
    pb2_grpc.add_StreamingServiceServicer_to_server(
        StreamingServicer(),
        server,
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info("gRPC server started on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
