import grpc

from generated import user_pb2
from generated import user_pb2_grpc

from domain.exceptions.ConflictException import ConflictException

class UserClient:

  def __init__(self):
    channel = grpc.insecure_channel("localhost:50051")
    self.stub = user_pb2_grpc.UserServiceStub(channel)

  def create_user(self, userDto):

    request = user_pb2.UserRequest(
      email=userDto.email,
      password=userDto.password
    )

    try:

      return self.stub.CreateUser(request)

    except grpc.RpcError as error:

      if error.code() == grpc.StatusCode.ALREADY_EXISTS:
        raise ConflictException(
          error.details()
        )

      raise error