#!/usr/bin/env python3
"""
MCP bridge for robot_control.v1 using fastmcp.

Run:  python robot_mcp_server.py --http-port 8000 --grpc-port 50051
"""

from __future__ import annotations

import asyncio.exceptions
import functools
import os
import sys
from typing import Callable, Dict, Any, Literal

import grpc
from google.protobuf.json_format import MessageToDict

from fastmcp import FastMCP

import proto.robot_control_pb2 as pb
import proto.robot_control_pb2_grpc as pb_grpc

import logging

# ────────────────────────────────────────────────────────────────────────────
# Logger configuration
# ────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("robot_mcp_server.log")
    ]
)
logger = logging.getLogger("RobotMCP")

# ────────────────────────────────────────────────────────────────────────────
#  Environment / CLI configuration
# ────────────────────────────────────────────────────────────────────────────

GRPC_HOST_DEFAULT = "localhost"
GRPC_PORT_DEFAULT = 50051
GRPC_CHANNEL: grpc.aio.Channel | None = None

MIN_DIST_TOLERANCE = 0.01
MIN_ORIENT_TOLERANCE = 0.05
MIN_SPEED = 0.5


def get_channel() -> grpc.aio.Channel:
    global GRPC_CHANNEL
    """Creates an *async* insecure channel each call (cheap in aio)."""
    if GRPC_CHANNEL is None:
        grpc_host = os.getenv("ROBOT_GRPC_HOST", GRPC_HOST_DEFAULT)
        grpc_port = int(os.getenv("ROBOT_GRPC_PORT", str(GRPC_PORT_DEFAULT)))
        channel_target = f"{grpc_host}:{grpc_port}"
        logger.info(f"Creating gRPC channel to {channel_target}")
        GRPC_CHANNEL = grpc.aio.insecure_channel(channel_target)
    return GRPC_CHANNEL


def get_grpc_stub() -> pb_grpc.RobotControlServiceStub:
    ch = get_channel()
    return pb_grpc.RobotControlServiceStub(ch)


def pb_to_dict(msg) -> Dict[str, Any]:
    return MessageToDict(
        msg,
        preserving_proto_field_name=True,
        # including_default_value_fields 更名
        always_print_fields_with_no_presence=True,
        use_integers_for_enums=True,
    )


# ────────────────────────────────────────────────────────────────────────────
#  fastmcp application instance
# ────────────────────────────────────────────────────────────────────────────
mcp = FastMCP(
    name="The MCP server providing robot control service",
    instructions="""This server will help you control a real robot."""
)


# ────────────────────────────────────────────────────────────────────────────
#  fastmcp “tools”
# ────────────────────────────────────────────────────────────────────────────

def common_svr_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Install exception catch common body for server handlers"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except grpc.aio.AioRpcError as e:
            logger.error(f"gRPC error in {func.__name__}: {e}")
            return {
                "error": f"gRPC error: {e.code()}",
                "message": e.details()
            }
        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}")
            return {"error": "Internal server error", "details": str(e)}

    return wrapper


# TIPS
# - Uses the function name (add) as the tool name.
# - Uses the function’s docstring (Adds two integer numbers...) as the tool description.
# - Generates an input schema based on the function’s parameters and type annotations.
# - Handles parameter validation and error reporting.

# @mcp.tool
# async def move_to_position(
#         x: Annotated[float, Field(description="x-coordinate of target position (meters)")],
#         y: Annotated[float, Field(description="y-coordinate of target position (meters)")],
#         z: Annotated[float, Field(description="z-coordinate of target position (meters)")],
#         roll: Annotated[float, Field(description="Target roll angle (radians)")],
#         pitch: Annotated[float, Field(description="Target pitch angle (radians)")],
#         yaw: Annotated[float, Field(description="Target yaw angle (radians)")],
#         max_speed: Annotated[float, Field(description="Maximum speed limit during movement (m/s)")] = 0.0,
#         tolerance: Annotated[float, Field(description="Position tolerance (meters)")] = 0.0,
#         orientation_tolerance: Annotated[float, Field(description="Orientation tolerance (radians)")] = 0.0
# ) -> dict:

@mcp.tool
@common_svr_handler
async def move_to_position(
        x: float, y: float, z: float,
        roll: float, pitch: float, yaw: float,
        max_speed: float = 0.0,
        tolerance: float = 0.0,
        orientation_tolerance: float = 0.0
) -> dict:
    """Controls the robot to move to the specified position and orientation. \
where the length unit defaults to meters (parameters x, y, z) \
and the angle unit defaults to degrees (parameters roll, pitch, yaw).
    It returns a dictionary containing code, message, actual distance traveled, and the final state of the machine."""
    logger.info(f"Received move_to_position request: "
                f"x={x}, y={y}, z={z}, "
                f"yaw={yaw}, pitch={pitch}, roll={roll}, "
                f"max_speed={max_speed}, tolerance={tolerance}, "
                f"orientation_tolerance={orientation_tolerance}")
    if tolerance < MIN_DIST_TOLERANCE:
        tolerance = MIN_DIST_TOLERANCE
    if orientation_tolerance < MIN_ORIENT_TOLERANCE:
        orientation_tolerance = MIN_ORIENT_TOLERANCE
    if max_speed < MIN_SPEED:
        max_speed = MIN_SPEED

    req = pb.TargetPosition(
        position=pb.Position(x=x, y=y, z=z),
        orientation=pb.Orientation(yaw=yaw, pitch=pitch, roll=roll),
        max_speed=max_speed,
        tolerance=tolerance,
        orientation_tolerance=orientation_tolerance,
    )
    stub = get_grpc_stub()
    logger.info("Calling MoveToPosition gRPC method")

    # stream move states
    last_state = pb.RobotState()
    async for state in stub.StreamMoveToPosition(req):
        logger.debug(
            "Robot movement checks: \n"
            f"\tPosition: x={state.position.x}, y={state.position.y}, z={state.position.z}\n"
            f"\tIs Moving: {state.state_code == pb.RobotState.MOVING}\n"
            f"\tBattery: {state.battery_level:.1%}"
        )

        if state.warnings:
            logger.warning(f"Robot current warnings: {', '.join(state.warnings)}")

        last_state = state
        if state.state_code != pb.RobotState.MOVING:
            # stream ended
            break

    # resp: pb.ControlResponse = await stub.MoveToPosition(req, timeout=30)

    # Get current position
    resp: pb.ControlResponse = await stub.GetCurrentPosition(pb.Empty())
    # override code & message for move_to_position
    if last_state.state_code != pb.RobotState.IDLE:
        logger.warning(f"Invalid robot state after move_to_position: {last_state.state_code}")
        resp.code = pb.ControlResponse.EMERGENCY_STOP
        resp.message = "Warning:" + (";".join(last_state.warnings))
    else:
        resp.message = "Finish moving process."
    logger.info(f"Received MoveToPosition response: code={resp.code}, message={resp.message}")

    return pb_to_dict(resp)


@mcp.tool
@common_svr_handler
async def get_current_position() -> dict:
    """Get the coordinates of the current position of the robot.
    Return a dictionary consisting of the coordinates of the current world coordinate system where the robot is located, \
the robot's pose, power level, warning messages, and other data."""
    logger.info("Received get_current_position request")
    stub = get_grpc_stub()
    logger.info("Calling GetCurrentPosition gRPC method")
    resp: pb.ControlResponse = await stub.GetCurrentPosition(pb.Empty())
    state: pb.RobotState = resp.current_state
    logger.info(f"Received GetCurrentPosition response: "
                f"code={resp.code}, message={resp.message}, "
                f"position=({state.position.x}, {state.position.y}, {state.position.z}), "
                f"battery={state.battery_level}")

    return pb_to_dict(state)


@mcp.tool
@common_svr_handler
async def emergency_stop() -> dict:
    """Immediately halt all robot motion. Return error status (code, message, suggested actions, etc.)"""
    logger.info("Received emergency_stop request")
    stub = get_grpc_stub()
    logger.info("Calling EmergencyStop gRPC method")
    resp: pb.ControlResponse = await stub.EmergencyStop(pb.Empty())
    logger.info(f"EmergencyStop executed: {resp.message} (code: {resp.code})")
    return pb_to_dict(resp)


@mcp.tool
@common_svr_handler
async def pick_up_object(object_name_hint: str) -> dict:
    """Pick up the specific object in front of the robot. e.g., pick_up_object("banana").\
    Return action result (code, message, etc.)"""
    logger.info("Received pick_up_object request")
    stub = get_grpc_stub()
    logger.info("Calling PickUpObject gRPC method")
    req = pb.PickOrPlaceCmd(cmd=object_name_hint)

    # stream pick-up
    async for state in stub.StreamPickUpObject(req):
        logger.debug(
            "Robot gripper checks: \n"
            f"\tIs Arm Moving: {state.is_moving_arm}\n"
            f"\tTarget Gripper Holding: {state.is_using_gripper}"
        )

        if state.warnings:
            logger.warning(f"Robot current warnings: {', '.join(state.warnings)}")

        if not state.is_moving_arm:
            # stream ended
            break

    # Get current position
    resp: pb.ControlResponse = await stub.GetCurrentPosition(pb.Empty())
    resp.message += "\nFinish gripper pick-up operation."
    logger.info(f"Received PickUpObject response: code={resp.code}, message={resp.message}")
    return pb_to_dict(resp)


@mcp.tool
@common_svr_handler
async def place_object(object_name_hint: str) -> dict:
    """Place the object grabbed by the robot. Return action result (code, message, etc.)"""
    logger.info("Received place_object request")
    stub = get_grpc_stub()
    logger.info("Calling PlaceObject gRPC method")
    req = pb.PickOrPlaceCmd(cmd=object_name_hint)

    # stream pick-up
    async for state in stub.StreamPlaceObject(req):
        logger.debug(
            "Robot gripper checks: \n"
            f"\tIs Arm Moving: {state.is_moving_arm}\n"
            f"\tTarget Gripper Holding: {state.is_using_gripper}"
        )

        if state.warnings:
            logger.warning(f"Robot current warnings: {', '.join(state.warnings)}")

        if not state.is_moving_arm:
            # stream ended
            break

    # Get current position
    resp: pb.ControlResponse = await stub.GetCurrentPosition(pb.Empty())
    resp.message += "\nFinish gripper place operation."
    logger.info(f"Received PlaceObject response: code={resp.code}, message={resp.message}")
    return pb_to_dict(resp)


@mcp.tool
@common_svr_handler
async def move_relative(
        direction: Literal[
            "LEFT_FORWARD", "LEFT_BACKWARD",
            "RIGHT_FORWARD", "RIGHT_BACKWARD",
            "FORWARD", "BACKWARD"
        ], distance: float) -> dict:
    """Do relative moving. `direction` can be 'LEFT_FORWARD', 'LEFT_BACKWARD', 'RIGHT_FORWARD', 'RIGHT_BACKWARD',\
    'FORWARD', or 'BACKWARD'. `distance` is meters. \
    Return action result (code, message, etc.)"""
    logger.info("Received move_relative request")
    stub = get_grpc_stub()
    logger.info("Calling MoveRelative gRPC method")

    # stream move states
    last_state = pb.RobotState()
    direction_ = pb.RobotDirection()
    match direction:
        case "LEFT_FORWARD":
            direction_.direction = pb.RobotDirection.FORWARD_LEFT
        case "LEFT_BACKWARD":
            direction_.direction = pb.RobotDirection.BACKWARD_LEFT
        case "RIGHT_FORWARD":
            direction_.direction = pb.RobotDirection.FORWARD_RIGHT
        case "RIGHT_BACKWARD":
            direction_.direction = pb.RobotDirection.BACKWARD_RIGHT
        case "FORWARD":
            direction_.direction = pb.RobotDirection.FORWARD
        case "BACKWARD":
            direction_.direction = pb.RobotDirection.BACKWARD
    direction_.distance = distance
    async for state in stub.StreamMove(direction_):
        logger.debug(
            "Robot movement checks: \n"
            f"\tPosition: x={state.position.x}, y={state.position.y}, z={state.position.z}\n"
            f"\tIs Moving: {state.state_code == pb.RobotState.MOVING}\n"
            f"\tBattery: {state.battery_level:.1%}"
        )

        if state.warnings:
            logger.warning(f"Robot current warnings: {', '.join(state.warnings)}")

        last_state = state
        if state.state_code != pb.RobotState.MOVING:
            # stream ended
            break

    # Get current position
    resp: pb.ControlResponse = await stub.GetCurrentPosition(pb.Empty())
    # override code & message for move_to_position
    if last_state.state_code != pb.RobotState.IDLE:
        logger.warning(f"Invalid robot state after move_relative: {last_state.state_code}")
        resp.code = pb.ControlResponse.EMERGENCY_STOP
        resp.message = "Warning:" + (";".join(last_state.warnings))
    else:
        resp.message = "Finish moving process."
    logger.info(f"Received MoveRelative response: code={resp.code}, message={resp.message}")

    return pb_to_dict(resp)


# ────────────────────────────────────────────────────────────────────────────
#  CLI entry-point
# ────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--stdio", action="store_true")
    parser.add_argument("--http-host", default="0.0.0.0")
    parser.add_argument("--http-port", type=int, default=8000)
    parser.add_argument("--grpc-host", default=GRPC_HOST_DEFAULT)
    parser.add_argument("--grpc-port", type=int, default=GRPC_PORT_DEFAULT)
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"]),
    p_args = parser.parse_args()

    logger.setLevel(p_args.log_level)

    os.environ["ROBOT_GRPC_HOST"] = p_args.grpc_host
    os.environ["ROBOT_GRPC_PORT"] = str(p_args.grpc_port)

    logger.info(f"Starting MCP server with configuration:")
    logger.info(f"  gRPC target: {p_args.grpc_host}:{p_args.grpc_port}")
    logger.info(f"  HTTP server: {p_args.http_host}:{p_args.http_port}")
    logger.info(f"  Log level: {p_args.log_level}")
    logger.info(f"  Stdio mode: {p_args.stdio}")

    try:
        if p_args.stdio:
            # The transport uses Python standard input/output (stdio) for a local MCP server
            logger.info("Running in stdio mode")
            mcp.run(transport="stdio")
        else:
            logger.info(f"Starting HTTP server on {p_args.http_host}:{p_args.http_port}")
            mcp.run(transport="streamable-http", host=p_args.http_host, port=p_args.http_port)
    except asyncio.exceptions.CancelledError:
        logger.warning("MCP server stopped due to cancellation")
        sys.exit(0)
