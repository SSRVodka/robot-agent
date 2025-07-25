# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from proto import robot_control_pb2 as proto_dot_robot__control__pb2

GRPC_GENERATED_VERSION = '1.73.0'
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
        + f' but the generated code in proto/robot_control_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RobotControlServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.MoveToPosition = channel.unary_unary(
                '/robot_control.v1.RobotControlService/MoveToPosition',
                request_serializer=proto_dot_robot__control__pb2.TargetPosition.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.ControlResponse.FromString,
                _registered_method=True)
        self.StreamMove = channel.unary_stream(
                '/robot_control.v1.RobotControlService/StreamMove',
                request_serializer=proto_dot_robot__control__pb2.RobotDirection.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.RobotState.FromString,
                _registered_method=True)
        self.StreamMoveToPosition = channel.unary_stream(
                '/robot_control.v1.RobotControlService/StreamMoveToPosition',
                request_serializer=proto_dot_robot__control__pb2.TargetPosition.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.RobotState.FromString,
                _registered_method=True)
        self.GetCurrentPosition = channel.unary_unary(
                '/robot_control.v1.RobotControlService/GetCurrentPosition',
                request_serializer=proto_dot_robot__control__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.ControlResponse.FromString,
                _registered_method=True)
        self.EmergencyStop = channel.unary_unary(
                '/robot_control.v1.RobotControlService/EmergencyStop',
                request_serializer=proto_dot_robot__control__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.ControlResponse.FromString,
                _registered_method=True)
        self.StreamPickUpObject = channel.unary_stream(
                '/robot_control.v1.RobotControlService/StreamPickUpObject',
                request_serializer=proto_dot_robot__control__pb2.PickOrPlaceCmd.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.RobotState.FromString,
                _registered_method=True)
        self.StreamPlaceObject = channel.unary_stream(
                '/robot_control.v1.RobotControlService/StreamPlaceObject',
                request_serializer=proto_dot_robot__control__pb2.PickOrPlaceCmd.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.RobotState.FromString,
                _registered_method=True)


class RobotControlServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def MoveToPosition(self, request, context):
        """简单移动接口 (请求-响应模式)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamMove(self, request, context):
        """简单小位移移动接口
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamMoveToPosition(self, request, context):
        """带实时反馈的移动 (服务器流模式)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCurrentPosition(self, request, context):
        """获取当前状态
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def EmergencyStop(self, request, context):
        """紧急停止
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamPickUpObject(self, request, context):
        """夹起物体
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StreamPlaceObject(self, request, context):
        """放下物体
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RobotControlServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'MoveToPosition': grpc.unary_unary_rpc_method_handler(
                    servicer.MoveToPosition,
                    request_deserializer=proto_dot_robot__control__pb2.TargetPosition.FromString,
                    response_serializer=proto_dot_robot__control__pb2.ControlResponse.SerializeToString,
            ),
            'StreamMove': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamMove,
                    request_deserializer=proto_dot_robot__control__pb2.RobotDirection.FromString,
                    response_serializer=proto_dot_robot__control__pb2.RobotState.SerializeToString,
            ),
            'StreamMoveToPosition': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamMoveToPosition,
                    request_deserializer=proto_dot_robot__control__pb2.TargetPosition.FromString,
                    response_serializer=proto_dot_robot__control__pb2.RobotState.SerializeToString,
            ),
            'GetCurrentPosition': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCurrentPosition,
                    request_deserializer=proto_dot_robot__control__pb2.Empty.FromString,
                    response_serializer=proto_dot_robot__control__pb2.ControlResponse.SerializeToString,
            ),
            'EmergencyStop': grpc.unary_unary_rpc_method_handler(
                    servicer.EmergencyStop,
                    request_deserializer=proto_dot_robot__control__pb2.Empty.FromString,
                    response_serializer=proto_dot_robot__control__pb2.ControlResponse.SerializeToString,
            ),
            'StreamPickUpObject': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamPickUpObject,
                    request_deserializer=proto_dot_robot__control__pb2.PickOrPlaceCmd.FromString,
                    response_serializer=proto_dot_robot__control__pb2.RobotState.SerializeToString,
            ),
            'StreamPlaceObject': grpc.unary_stream_rpc_method_handler(
                    servicer.StreamPlaceObject,
                    request_deserializer=proto_dot_robot__control__pb2.PickOrPlaceCmd.FromString,
                    response_serializer=proto_dot_robot__control__pb2.RobotState.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'robot_control.v1.RobotControlService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('robot_control.v1.RobotControlService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class RobotControlService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def MoveToPosition(request,
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
            '/robot_control.v1.RobotControlService/MoveToPosition',
            proto_dot_robot__control__pb2.TargetPosition.SerializeToString,
            proto_dot_robot__control__pb2.ControlResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StreamMove(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/robot_control.v1.RobotControlService/StreamMove',
            proto_dot_robot__control__pb2.RobotDirection.SerializeToString,
            proto_dot_robot__control__pb2.RobotState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StreamMoveToPosition(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/robot_control.v1.RobotControlService/StreamMoveToPosition',
            proto_dot_robot__control__pb2.TargetPosition.SerializeToString,
            proto_dot_robot__control__pb2.RobotState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetCurrentPosition(request,
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
            '/robot_control.v1.RobotControlService/GetCurrentPosition',
            proto_dot_robot__control__pb2.Empty.SerializeToString,
            proto_dot_robot__control__pb2.ControlResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def EmergencyStop(request,
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
            '/robot_control.v1.RobotControlService/EmergencyStop',
            proto_dot_robot__control__pb2.Empty.SerializeToString,
            proto_dot_robot__control__pb2.ControlResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StreamPickUpObject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/robot_control.v1.RobotControlService/StreamPickUpObject',
            proto_dot_robot__control__pb2.PickOrPlaceCmd.SerializeToString,
            proto_dot_robot__control__pb2.RobotState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StreamPlaceObject(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/robot_control.v1.RobotControlService/StreamPlaceObject',
            proto_dot_robot__control__pb2.PickOrPlaceCmd.SerializeToString,
            proto_dot_robot__control__pb2.RobotState.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class CameraServiceStub(object):
    """相机服务
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetImage = channel.unary_unary(
                '/robot_control.v1.CameraService/GetImage',
                request_serializer=proto_dot_robot__control__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.ImageResponse.FromString,
                _registered_method=True)
        self.GetCameraConfig = channel.unary_unary(
                '/robot_control.v1.CameraService/GetCameraConfig',
                request_serializer=proto_dot_robot__control__pb2.Empty.SerializeToString,
                response_deserializer=proto_dot_robot__control__pb2.CameraConfig.FromString,
                _registered_method=True)


class CameraServiceServicer(object):
    """相机服务
    """

    def GetImage(self, request, context):
        """获取单张图像
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetCameraConfig(self, request, context):
        """获取相机配置
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_CameraServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetImage': grpc.unary_unary_rpc_method_handler(
                    servicer.GetImage,
                    request_deserializer=proto_dot_robot__control__pb2.Empty.FromString,
                    response_serializer=proto_dot_robot__control__pb2.ImageResponse.SerializeToString,
            ),
            'GetCameraConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.GetCameraConfig,
                    request_deserializer=proto_dot_robot__control__pb2.Empty.FromString,
                    response_serializer=proto_dot_robot__control__pb2.CameraConfig.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'robot_control.v1.CameraService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('robot_control.v1.CameraService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class CameraService(object):
    """相机服务
    """

    @staticmethod
    def GetImage(request,
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
            '/robot_control.v1.CameraService/GetImage',
            proto_dot_robot__control__pb2.Empty.SerializeToString,
            proto_dot_robot__control__pb2.ImageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetCameraConfig(request,
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
            '/robot_control.v1.CameraService/GetCameraConfig',
            proto_dot_robot__control__pb2.Empty.SerializeToString,
            proto_dot_robot__control__pb2.CameraConfig.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
