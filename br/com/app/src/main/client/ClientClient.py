import grpc

from generated import client_pb2
from generated import client_pb2_grpc
from google.protobuf.empty_pb2 import Empty

from domain.exceptions.ConflictException import ConflictException
from domain.exceptions.NotFoundException import NotFoundException

class ClientClient:

  def __init__(self):
    channel = grpc.insecure_channel("library-api:50051")
    self.stub = client_pb2_grpc.ClientServiceStub(channel)

  
  def create_client(self, clientDto):

    request = client_pb2.CreateClientRequest(
      user_id=clientDto.user_id,
      name=clientDto.name,
      phone=clientDto.phone,
      address=clientDto.address,
      zip_code=clientDto.zip_code,
      city=clientDto.city,
      neighborhood=clientDto.neighborhood,
      country=clientDto.country
    )

    try:

      return self.stub.CreateClient(request)

    except grpc.RpcError as error:

      if error.code() == grpc.StatusCode.ALREADY_EXISTS:
        raise ConflictException(
          error.details()
        )
      
      if error.code() == grpc.StatusCode.INTERNAL:
        raise Exception(
          error.details()
        )

      raise error
    
  def update_client(self, id, clientDto):

    client = client_pb2.UpdateClientData(
      name=clientDto.name,
      phone=clientDto.phone,
      address=clientDto.address,
      zip_code=clientDto.zip_code,
      city=clientDto.city,
      neighborhood=clientDto.neighborhood,
      country=clientDto.country
    )

    request = client_pb2.UpdateClientRequest(
      id=int(id),
      client=client
    )

    try:

      return self.stub.UpdateClient(request)

    except grpc.RpcError as error:

      if error.code() == grpc.StatusCode.NOT_FOUND:
        raise NotFoundException(
          error.details()
        )

      if error.code() == grpc.StatusCode.INTERNAL:
        raise Exception(
          error.details()
        )

      raise error
    
  def deactivate_client(self, id):

    request = client_pb2.ClientIdRequest(
      id=int(id)
    )

    try:

      return self.stub.DeactivateClient(request)

    except grpc.RpcError as error:

      if error.code() == grpc.StatusCode.NOT_FOUND:
        raise NotFoundException(
          error.details()
        )

      if error.code() == grpc.StatusCode.INTERNAL:
        raise Exception(
          error.details()
        )

      raise error