import grpc

from generated import book_pb2
from generated import book_pb2_grpc

from domain.exceptions.BookAlreadyExistsException import BookAlreadyExistsException


class BookClient:

    def __init__(self):
      channel = grpc.insecure_channel("localhost:50051")
      self.stub = book_pb2_grpc.BookServiceStub(channel)

    def create_book(self, bookDto):

      request = book_pb2.BookDto(
        title=bookDto.title,
        description=bookDto.description,
        quantity=bookDto.quantity
      )

      try:

        return self.stub.CreateBook(request)

      except grpc.RpcError as error:

        if error.code() == grpc.StatusCode.ALREADY_EXISTS:
          raise BookAlreadyExistsException(
            error.details()
          )

        raise error