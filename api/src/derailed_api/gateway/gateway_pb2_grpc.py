# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import gateway_pb2 as gateway__pb2
import grpc
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class GatewayStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.dispatch_guild = channel.unary_unary(
            "/derailed.gateway.Gateway/dispatch_guild",
            request_serializer=gateway__pb2.Interchange.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
        self.dispatch_user = channel.unary_unary(
            "/derailed.gateway.Gateway/dispatch_user",
            request_serializer=gateway__pb2.Interchange.SerializeToString,
            response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )


class GatewayServicer(object):
    """Missing associated documentation comment in .proto file."""

    def dispatch_guild(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def dispatch_user(self, request, context):
        """rpc dispatch_bulk (BulkInterchange) returns (google.protobuf.Empty);
        rpc get_metadata (GuildInfo) returns (GuildMetadata);
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_GatewayServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "dispatch_guild": grpc.unary_unary_rpc_method_handler(
            servicer.dispatch_guild,
            request_deserializer=gateway__pb2.Interchange.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
        "dispatch_user": grpc.unary_unary_rpc_method_handler(
            servicer.dispatch_user,
            request_deserializer=gateway__pb2.Interchange.FromString,
            response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "derailed.gateway.Gateway", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class Gateway(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def dispatch_guild(
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
            "/derailed.gateway.Gateway/dispatch_guild",
            gateway__pb2.Interchange.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def dispatch_user(
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
            "/derailed.gateway.Gateway/dispatch_user",
            gateway__pb2.Interchange.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
