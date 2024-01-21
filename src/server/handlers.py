import logging
from concurrent import futures as cf

from grpclib import GRPCError, Status
from grpclib.server import Stream

from core.enums import Direction
from core.exceptions import PathfinderError
from server.lib import pathfinder_pb2 as grpc_models
from server.lib.pathfinder_grpc import PathFinderBase
from services import field_state
from state.state import State


class Pathfinder(PathFinderBase):
    """
    This class handles the gRPC requests for setting fields and moving.
    It uses a process pool executor (for computing path) and a state object (to persist results) to perform these operations.
    """

    def __init__(self, executor: cf.ProcessPoolExecutor, state: State):
        """
        Initialize the Pathfinder with a process pool executor and a state object.

        Parameters:
        executor (cf.ProcessPoolExecutor): The process pool executor.
        state (State): The state object.
        """
        self._executor = executor
        self._state = state

    async def SetField(self, stream: Stream[grpc_models.Field, grpc_models.Empty]):
        """
        Handle the SetField gRPC request: start new step sequence.

        Parameters:
        stream (Stream[grpc_models.Field, grpc_models.Empty]): The gRPC stream.
        """
        request = await stream.recv_message()

        if request is None:
            logging.error("No field provided")
            raise GRPCError(Status.INVALID_ARGUMENT, 'No Field for SetField provided')
        logging.debug(f"SetField request: {request}")
        try:
            result = await field_state.set_field(self._state, request)
            logging.debug(f"SetField answered: {result}")
            await stream.send_message(result)
        except PathfinderError as e:
            logging.error('Houston, we have a problem!')
            logging.error(e)
            return

    async def Moving(
        self, stream: Stream[grpc_models.MoveRequest, grpc_models.MoveResponse]
    ):
        """
        Handle the Moving gRPC request: retrieve direction for list of targets.

        Parameters:
        stream (Stream[grpc_models.MoveRequest, grpc_models.MoveResponse]): The gRPC stream.
        """
        request = await stream.recv_message()

        if request is None:
            logging.error("No MoveRequest provided")
            raise GRPCError(Status.INVALID_ARGUMENT, 'No MoveRequest provided')

        logging.debug(f"Moving request: {request}")
        try:
            result = await field_state.moving(self._state, self._executor, request)
            await stream.send_message(result)
            logging.debug(f"Moving answered: {result}")
        except PathfinderError as e:
            logging.error('Houston, we have a problem!')
            logging.error(e)
            response = grpc_models.MoveResponse()
            response.direction = Direction.ERROR  # type: ignore
            await stream.send_message(response)
