from client.BookLoanClient import BookLoanClient
from domain.dto.bookLoan.CreateBookLoanDto import CreateBookLoanDto
from domain.dto.bookLoan.UpdateBookLoanRequest import UpdateBookLoanRequest
from domain.model.BookLoan import BookLoan
from domain.dto.bookLoan.BookLoanResponseDto import BookLoanResponseDto
from utils.ApiResponse import ApiResponse
from domain.exceptions.ConflictException import ConflictException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.InsufficientQuantityException import InsufficientQuantityException
from domain.exceptions.UnauthorizedException import UnauthorizedException
from domain.exceptions.MissingTokenException import MissingTokenException
from auth.JwtAuth import JwtAuth
from flasgger import swag_from
import os
from flask import request

class BookLoanController:

  def __init__(self, app):
    self.app = app
    self.jwt_auth = JwtAuth()
    self.book_client = BookLoanClient()
    self.default_route = "/loan"
    self.register_routes()

  def register_routes(self):

    @self.app.route(self.default_route, methods=['POST'])
    @swag_from(os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/bookLoan/create_book_loan.yaml')))
    def create_book_loan():

      json = request.get_json()

      book_loan_dto = CreateBookLoanDto(
        json.get("book_id"),
        json.get("client_id"),
        json.get("loan_date"),
        json.get("loan_quantity"),
        json.get("expeted_return_date"),
      )

      try:
        token = self.jwt_auth.get_token(request)
        self.jwt_auth.validate_token(token)

        response = self.book_client.create_book_loan(book_loan_dto)

        book_loan = BookLoanResponseDto( 
          response.data.id,
          response.data.book_id,
          response.data.client_id,
          response.data.loan_date,
          response.data.loan_quantity,
          response.data.expeted_return_date
        )

        return ApiResponse.created(
          response.message,
          book_loan
        )

      except NotFoundException as error:
        return ApiResponse.not_found(
          str(error)
        )
      
      except InsufficientQuantityException as error:
        return ApiResponse.conflict(
          str(error)
        )
      
      except MissingTokenException:
        return ApiResponse.unauthorized(
          "Token not found."
        )
      
      except UnauthorizedException:
        return ApiResponse.unauthorized(
          "Invalid or expired token."
        )

      except Exception as error:
        return ApiResponse.conflict(
          str(error)
        )
      
    @self.app.route(self.default_route + "/<id>", methods=['PUT'])
    @swag_from(os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/bookLoan/update_book_loan.yaml')))
    def update_book_loan(id):

      json = request.get_json()

      book_loan_dto = UpdateBookLoanRequest(
        json.get("book_id"),
        json.get("return_date"),
        json.get("is_book_already_returned"),
        json.get("returned_quantity"),
      )

      try:
        token = self.jwt_auth.get_token(request)
        self.jwt_auth.validate_token(token)

        response = self.book_client.update_book_loan(id, book_loan_dto)

        return ApiResponse.ok(
          response.message
        )

      except NotFoundException as error:
        return ApiResponse.not_found(
          str(error)
        )
      
      except ConflictException as error:
        return ApiResponse.conflict(
          str(error)
        )
      
      except MissingTokenException:
        return ApiResponse.unauthorized(
          "Token not found."
        )
      
      except UnauthorizedException:
        return ApiResponse.unauthorized(
          "Invalid or expired token."
        )

      except Exception as error:
        return ApiResponse.conflict(
          str(error)
        )
      
    @self.app.route(self.default_route + "/<id>", methods=['GET'])
    @swag_from(os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/bookLoan/find_book_loan_by_id.yaml')))
    def find_book_loan_by_id(id):

      try:
        token = self.jwt_auth.get_token(request)
        self.jwt_auth.validate_token(token)

        response = self.book_client.find_book_by_id(id)

        book_loan = BookLoan(
          id=response.data.id,
          book_id=response.data.book_id,
          client_id=response.data.client_id,
          loan_date=response.data.loan_date,
          expeted_return_date=response.data.expeted_return_date,
          return_date=response.data.return_date,
          returned_quantity=response.data.returned_quantity,
          loan_quantity=response.data.loan_quantity,
          is_book_already_returned=response.data.is_book_already_returned
        )

        return ApiResponse.ok(
          response.message,
          book_loan
        )

      except NotFoundException as error:
        return ApiResponse.not_found(
          str(error)
        )
      
      except MissingTokenException:
        return ApiResponse.unauthorized(
          "Token not found."
        )
      
      except UnauthorizedException:
        return ApiResponse.unauthorized(
          "Invalid or expired token."
        )
      
    @self.app.route(self.default_route + "/all/<idClient>", methods=['GET'])
    @swag_from(os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/bookLoan/find_all_book_loan_by_id.yaml')))
    def find_all_book_loan(idClient):

      try:
        token = self.jwt_auth.get_token(request)
        self.jwt_auth.validate_token(token)

        response = self.book_client.find_all_book_loan(idClient)

        book_loan_list = [
          BookLoan(
            id=bookLoan.id,
            book_id=bookLoan.book_id,
            client_id=bookLoan.client_id,
            loan_date=bookLoan.loan_date,
            expeted_return_date=bookLoan.expeted_return_date,
            return_date=bookLoan.return_date,
            returned_quantity=bookLoan.returned_quantity,
            loan_quantity=bookLoan.loan_quantity,
            is_book_already_returned=bookLoan.is_book_already_returned
          )
          for bookLoan in response.data
        ]
        return ApiResponse.ok(
          response.message,
          book_loan_list
        )

      except NotFoundException as error:
        return ApiResponse.not_found(
          str(error)
        )
      
      except MissingTokenException:
        return ApiResponse.unauthorized(
          "Token not found."
        )
      
      except UnauthorizedException:
        return ApiResponse.unauthorized(
          "Invalid or expired token."
        )