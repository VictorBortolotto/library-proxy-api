from client.BookClient import BookClient
from domain.dto.book.BookDto import BookDto
from domain.model.Book import Book
from utils.ApiResponse import ApiResponse
from domain.exceptions.ConflictException import ConflictException
from domain.exceptions.NotFoundException import NotFoundException
from flask import request

from flasgger import swag_from
import os

class BookController:

  def __init__(self, app):
    self.app = app
    self.book_client = BookClient()
    self.default_route = "/book"
    self.register_routes()

  def register_routes(self):

    @self.app.route(self.default_route, methods=['POST'])
    @swag_from(os.path.join(os.getcwd(), 'docs/book/create_book.yaml'))
    def create_book():

      json = request.get_json()

      bookDto = BookDto(
        json.get("title"),
        json.get("description"),
        json.get("quantity")
      )

      try:

        response = self.book_client.create_book(bookDto)

        book = {
          "id": response.data.id,
          "title": response.data.title,
          "description": response.data.description,
          "quantity": response.data.quantity
        }

        return ApiResponse.created(
          response.message,
          book
        )

      except ConflictException as error:

        return ApiResponse.conflict(
          str(error)
        )
      
    @self.app.route(self.default_route + "/<id>", methods=['PUT'])
    @swag_from(os.path.join(os.getcwd(), 'docs/book/update_book.yaml'))
    def update_book(id):

      json = request.get_json()

      bookDto = BookDto(
        json.get("title"),
        json.get("description"),
        json.get("quantity")
      )

      try:

        response = self.book_client.update_book(id, bookDto)

        book = Book(
          response.data.id,
          response.data.title,
          response.data.description,
          response.data.quantity
        )

        return ApiResponse.created(
          response.message,
          book
        )

      except NotFoundException as error:

        return ApiResponse.not_found(
          str(error)
        )
      
      except Exception as error:

        return ApiResponse.internal_server_error(
          str(error)
        )
      
    @self.app.route(self.default_route, methods=['GET'])
    @swag_from(os.path.join(os.getcwd(), 'docs/book/find_all_book.yaml'))
    def find_all_book():
      try:

        response = self.book_client.find_all_book()

        book_list = [
          Book(
            id=book.id,
            title=book.title,
            description=book.description,
            quantity=book.quantity
          )
          for book in response.data
        ]

        return ApiResponse.ok(
          response.message,
          book_list
        )

      except NotFoundException as error:

        return ApiResponse.not_found(
          str(error)
        )
      
    @self.app.route(self.default_route + "/<id>", methods=['GET'])
    @swag_from(os.path.join(os.getcwd(), 'docs/book/find_book_by_id.yaml'))
    def find_book_by_id(id):
      try:

        response = self.book_client.find_book_by_id(id)

        book = Book(
          response.data.id,
          response.data.title,
          response.data.description,
          response.data.quantity
        )

        return ApiResponse.ok(
          response.message,
          book
        )

      except NotFoundException as error:

        return ApiResponse.not_found(
          str(error)
        )

    @self.app.route(self.default_route + "/<id>", methods=['DELETE'])
    @swag_from(os.path.join(os.getcwd(), 'docs/book/delete_book.yaml'))
    def delete_book(id):
      try:

        response = self.book_client.delete_book(id)

        return ApiResponse.ok(
          response.message,
        )

      except NotFoundException as error:

        return ApiResponse.not_found(
          str(error)
        )
      
      except Exception as error:

        return ApiResponse.internal_server_error(
          str(error)
        )