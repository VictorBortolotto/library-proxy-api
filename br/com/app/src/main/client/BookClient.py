import grpc

from generated import book_pb2
from generated import book_pb2_grpc
from google.protobuf.empty_pb2 import Empty

from domain.exceptions.ConflictException import ConflictException
from domain.exceptions.NotFoundException import NotFoundException

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
          raise ConflictException(
            error.details()
          )

        raise error
      
    def update_book(self, id, bookDto):

      book = book_pb2.BookDto(
        title=bookDto.title,
        description=bookDto.description,
        quantity=bookDto.quantity
      )

      request = book_pb2.BookRequest(
        id=int(id),
        book=book
      )

      try:

        return self.stub.UpdateBook(request)

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
      
    def find_book_by_id(self, id):
      request = book_pb2.BookIdRequest(
        id=int(id)
      )

      try:

        return self.stub.FindBookById(request)

      except grpc.RpcError as error:

        if error.code() == grpc.StatusCode.NOT_FOUND:
          raise NotFoundException(
            error.details()
          )
        
        raise error
      
    def find_all_book(self):
      try:

        return self.stub.FindAllBook(Empty())

      except grpc.RpcError as error:

        if error.code() == grpc.StatusCode.NOT_FOUND:
          raise NotFoundException(
            error.details()
          )
        
        raise error

    def delete_book(self, id):
      request = book_pb2.BookIdRequest(
        id=int(id)
      )

      try:

        return self.stub.DeleteBook(request)

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