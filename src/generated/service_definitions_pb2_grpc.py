# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import warnings

import grpc

from . import service_definitions_pb2 as service__definitions__pb2

GRPC_GENERATED_VERSION = "1.67.1"
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower

    _version_not_supported = first_version_is_lower(
        GRPC_VERSION, GRPC_GENERATED_VERSION
    )
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f"The grpc package installed is at version {GRPC_VERSION},"
        + f" but the generated code in service_definitions_pb2_grpc.py depends on"
        + f" grpcio>={GRPC_GENERATED_VERSION}."
        + f" Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}"
        + f" or downgrade your generated code using grpcio-tools<={GRPC_VERSION}."
    )


class SimpleServiceStub(object):
    """Simple request-response service"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProcessRequest = channel.unary_unary(
            "/benchmark.SimpleService/ProcessRequest",
            request_serializer=service__definitions__pb2.SimpleRequest.SerializeToString,
            response_deserializer=service__definitions__pb2.SimpleResponse.FromString,
            _registered_method=True,
        )


class SimpleServiceServicer(object):
    """Simple request-response service"""

    def ProcessRequest(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_SimpleServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ProcessRequest": grpc.unary_unary_rpc_method_handler(
            servicer.ProcessRequest,
            request_deserializer=service__definitions__pb2.SimpleRequest.FromString,
            response_serializer=service__definitions__pb2.SimpleResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "benchmark.SimpleService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers(
        "benchmark.SimpleService", rpc_method_handlers
    )


# This class is part of an EXPERIMENTAL API.
class SimpleService(object):
    """Simple request-response service"""

    @staticmethod
    def ProcessRequest(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/benchmark.SimpleService/ProcessRequest",
            service__definitions__pb2.SimpleRequest.SerializeToString,
            service__definitions__pb2.SimpleResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )


class StreamingServiceStub(object):
    """Streaming service"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StreamData = channel.unary_stream(
            "/benchmark.StreamingService/StreamData",
            request_serializer=service__definitions__pb2.StreamRequest.SerializeToString,
            response_deserializer=service__definitions__pb2.StreamResponse.FromString,
            _registered_method=True,
        )


class StreamingServiceServicer(object):
    """Streaming service"""

    def StreamData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_StreamingServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "StreamData": grpc.unary_stream_rpc_method_handler(
            servicer.StreamData,
            request_deserializer=service__definitions__pb2.StreamRequest.FromString,
            response_serializer=service__definitions__pb2.StreamResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "benchmark.StreamingService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers(
        "benchmark.StreamingService", rpc_method_handlers
    )


# This class is part of an EXPERIMENTAL API.
class StreamingService(object):
    """Streaming service"""

    @staticmethod
    def StreamData(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_stream(
            request,
            target,
            "/benchmark.StreamingService/StreamData",
            service__definitions__pb2.StreamRequest.SerializeToString,
            service__definitions__pb2.StreamResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )


class PayloadServiceStub(object):
    """Large payload service"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ProcessLargePayload = channel.unary_unary(
            "/benchmark.PayloadService/ProcessLargePayload",
            request_serializer=service__definitions__pb2.PayloadRequest.SerializeToString,
            response_deserializer=service__definitions__pb2.PayloadResponse.FromString,
            _registered_method=True,
        )


class PayloadServiceServicer(object):
    """Large payload service"""

    def ProcessLargePayload(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_PayloadServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "ProcessLargePayload": grpc.unary_unary_rpc_method_handler(
            servicer.ProcessLargePayload,
            request_deserializer=service__definitions__pb2.PayloadRequest.FromString,
            response_serializer=service__definitions__pb2.PayloadResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "benchmark.PayloadService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers(
        "benchmark.PayloadService", rpc_method_handlers
    )


# This class is part of an EXPERIMENTAL API.
class PayloadService(object):
    """Large payload service"""

    @staticmethod
    def ProcessLargePayload(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/benchmark.PayloadService/ProcessLargePayload",
            service__definitions__pb2.PayloadRequest.SerializeToString,
            service__definitions__pb2.PayloadResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True,
        )