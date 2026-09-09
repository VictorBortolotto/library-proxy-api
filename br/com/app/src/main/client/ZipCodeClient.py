import grpc

from generated import zip_code_pb2
from generated import zip_code_pb2_grpc
from domain.exceptions.NotFoundException import NotFoundException

class ZipCodeClient:

  def __init__(self):
    channel = grpc.insecure_channel("localhost:50051")
    self.stub = zip_code_pb2_grpc.ZipCodeServiceStub(channel)

  def find_zip_code_data(self, cep):
    request = zip_code_pb2.ZipCodeRequest(
      zip_code=cep
    )

    try:

      return self.stub.FindDataByZipCode(request)

    except grpc.RpcError as error:

      if error.code() == grpc.StatusCode.NOT_FOUND:
        raise NotFoundException(
          error.details()
        )
      
      raise error