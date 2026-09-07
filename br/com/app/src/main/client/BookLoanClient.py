import grpc

from generated import book_loan_pb2
from generated import book_loan_pb2_grpc

from domain.exceptions.ConflictException import ConflictException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.InsufficientQuantityException import InsufficientQuantityException

class BookLoanClient:

  def __init__(self):
    channel = grpc.insecure_channel("localhost:50051")
    self.stub = book_loan_pb2_grpc.BookLoanServiceStub(channel)

  def create_book_loan(self, bookLoanDto):

    request = book_loan_pb2.BookLoanCreateRequest(
      book_id=bookLoanDto.book_id,
      client_id=bookLoanDto.client_id,
      loan_date=bookLoanDto.loan_date,
      loan_quantity=bookLoanDto.loan_quantity,
      expeted_return_date=bookLoanDto.expeted_return_date
    )

    try:

      return self.stub.CreateBookLoan(request)

    except grpc.RpcError as error:
      
      if error.code() == grpc.StatusCode.NOT_FOUND:
        raise NotFoundException(
          error.details()
        )
      if error.code() == grpc.StatusCode.OUT_OF_RANGE:
        raise InsufficientQuantityException(
          error.details()
        )
      if error.code() == grpc.StatusCode.INTERNAL:
        raise ConflictException(
          error.details()
        )

      raise error
    
  def update_book_loan(self, id, bookLoanDto):

    book_loan_update_data = book_loan_pb2.BookLoanUpdateData(
      book_id=bookLoanDto.book_id,
      return_date=bookLoanDto.return_date,
      is_book_already_returned=bookLoanDto.is_book_already_returned,
      returned_quantity=bookLoanDto.returned_quantity
    )

    request = book_loan_pb2.BookLoanUpdateRequest(
      data=book_loan_update_data,
      id=int(id)
    )

    try:

      return self.stub.UpdateBookLoan(request)

    except grpc.RpcError as error:
      
      if error.code() == grpc.StatusCode.NOT_FOUND:
        raise NotFoundException(
          error.details()
        )
      if error.code() == grpc.StatusCode.INVALID_ARGUMENT:
        raise ConflictException(
          error.details()
        )
      if error.code() == grpc.StatusCode.INTERNAL:
        raise Exception(
          error.details()
        )

      raise error

  def find_all_book_loan(self, idClient):
    request = book_loan_pb2.BookLoanIdRequest(
      id=int(idClient)
    )

    try:

      return self.stub.FindAllBookLoan(request)

    except grpc.RpcError as error:

      if error.code() == grpc.StatusCode.NOT_FOUND:
        raise NotFoundException(
          error.details()
        )
      
      raise error

  def find_book_by_id(self, id):
    request = book_loan_pb2.BookLoanIdRequest(
      id=int(id)
    )

    try:

      return self.stub.FindBookLoanById(request)

    except grpc.RpcError as error:

      if error.code() == grpc.StatusCode.NOT_FOUND:
        raise NotFoundException(
          error.details()
        )
      
      raise error