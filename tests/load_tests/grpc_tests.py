import logging
import time

import grpc
import grpc.experimental.gevent as grpc_gevent
import locust.exception as exceptions
from grpc_interceptor import ClientInterceptor
from locust import User, between, task

from src.generated import service_definitions_pb2 as pb2
from src.generated import service_definitions_pb2_grpc as pb2_grpc

# Initialize gevent for asynchronous gRPC calls
grpc_gevent.init_gevent()

# Configure logging to include debug statements
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LocustInterceptor(ClientInterceptor):
    def __init__(self, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.env = environment  # Access the Locust environment

    def intercept(
        self,
        method,
        request_or_iterator,
        call_details,
    ):
        logger.debug(f"Intercepting method: {call_details.method}")
        start_time = time.time()

        try:
            response = method(request_or_iterator, call_details)
            # Determine if the method is a streaming call based on its name
            if "Stream" in call_details.method:
                # Streaming call
                return self.StreamingResponseWrapper(
                    response, self.env, call_details.method, start_time
                )
            else:
                # Unary call
                response_time = (time.time() - start_time) * 1000  # in ms
                response_length = len(str(response))
                self.env.events.request.fire(
                    request_type="gRPC",
                    name=call_details.method,
                    response_time=response_time,
                    response_length=response_length,
                    exception=None,
                )
                logger.debug(f"Successfully processed method: {call_details.method}")
                return response
        except grpc.RpcError as e:
            response_time = (time.time() - start_time) * 1000  # in ms
            self.env.events.request.fire(
                request_type="gRPC",
                name=call_details.method,
                response_time=response_time,
                response_length=0,
                exception=e,
            )
            logger.exception(f"gRPC request failed for method: {call_details.method}")
            raise e

    class StreamingResponseWrapper:
        def __init__(self, generator, env, method_name, start_time):
            self.generator = generator
            self.env = env
            self.method_name = method_name
            self.start_time = start_time
            self.response_length = 0
            self.count = 0

        def __iter__(self):
            return self

        def __next__(self):
            try:
                response = next(self.generator)
                self.count += 1
                self.response_length += len(str(response))
                return response
            except StopIteration:
                # Calculate the response time once the stream is exhausted
                response_time = (time.time() - self.start_time) * 1000  # in ms
                self.env.events.request.fire(
                    request_type="gRPC",
                    name=self.method_name,
                    response_time=response_time,
                    response_length=self.response_length,
                    exception=None,
                )
                raise


class GrpcUser(User):
    abstract = True
    wait_time = between(0.1, 1)  # Define wait time between tasks
    stub_classes = []  # List of stub classes
    host = None

    def __init__(self, environment):
        super().__init__(environment)
        if not self.host:
            raise exceptions.StopUser("You must specify the host.")
        if not self.stub_classes:
            raise exceptions.StopUser("You must specify the stub_classes.")

        # Create a gRPC channel with the interceptor
        interceptor = LocustInterceptor(environment=environment)
        self.channel = grpc.insecure_channel(self.host)
        self.channel = grpc.intercept_channel(self.channel, interceptor)
        self.stubs = [stub_class(self.channel) for stub_class in self.stub_classes]
        logger.info("Successfully connected to gRPC service.")


class HelloGrpcUser(GrpcUser):
    host = "34.57.71.117:50051"  # cloud deployment
    # host = "localhost:50051" #local deployment
    stub_classes = [
        pb2_grpc.SimpleServiceStub,
        pb2_grpc.StreamingServiceStub,
        pb2_grpc.PayloadServiceStub,
    ]

    @task(3)
    def test_simple_request(self):
        logger.debug("Starting test_simple_request")
        request = pb2.SimpleRequest(message="test", data={"key": "value" * 100})
        try:
            self.stubs[0].ProcessRequest(request)
            logger.debug("Processed simple request successfully.")
        except Exception as e:
            logger.error(f"Error processing simple request: {e}")
        logger.debug("Completed test_simple_request")

    @task(2)
    def test_stream_data(self):
        logger.debug("Starting test_stream_data")
        request = pb2.StreamRequest(number_of_messages=100)
        try:
            responses = self.stubs[1].StreamData(request)
            for i, response in enumerate(responses):
                if i >= request.number_of_messages:
                    logger.warning("Received more messages than expected.")
                    break
                # Example processing (can be customized)
                # logger.debug(f"Received message: {response.message}")
            logger.debug("Streamed data successfully.")
        except Exception as e:
            logger.error(f"Error streaming data: {e}")
        logger.debug("Completed test_stream_data")

    @task(1)
    def test_large_payload(self):
        logger.debug("Starting test_large_payload")
        request = pb2.PayloadRequest(
            data=b"x" * (1024 * 1024), size_kb=1024  # 1MB payload
        )
        try:
            self.stubs[2].ProcessLargePayload(request)
            logger.debug("Processed large payload successfully.")
        except Exception as e:
            logger.error(f"Error processing large payload: {e}")
        logger.debug("Completed test_large_payload")
