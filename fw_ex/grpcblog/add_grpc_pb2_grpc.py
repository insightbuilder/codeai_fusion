# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import add_grpc_pb2 as add__grpc__pb2

GRPC_GENERATED_VERSION = '1.68.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in add_grpc_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class AddNumberStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddTwoNumber = channel.unary_unary(
                '/add_grpc.AddNumber/AddTwoNumber',
                request_serializer=add__grpc__pb2.AddRequest.SerializeToString,
                response_deserializer=add__grpc__pb2.AddResponse.FromString,
                _registered_method=True)


class AddNumberServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AddTwoNumber(self, request, context):
        """Adds two numbers
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_AddNumberServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddTwoNumber': grpc.unary_unary_rpc_method_handler(
                    servicer.AddTwoNumber,
                    request_deserializer=add__grpc__pb2.AddRequest.FromString,
                    response_serializer=add__grpc__pb2.AddResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'add_grpc.AddNumber', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('add_grpc.AddNumber', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class AddNumber(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AddTwoNumber(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/add_grpc.AddNumber/AddTwoNumber',
            add__grpc__pb2.AddRequest.SerializeToString,
            add__grpc__pb2.AddResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
