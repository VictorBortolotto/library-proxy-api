from client.BookClient import BookClient
from domain.dto.book.BookDto import BookDto
from utils.ApiResponse import ApiResponse
from domain.exceptions.BookAlreadyExistsException import BookAlreadyExistsException
from flask import request


class BookController:

    def __init__(self, app):
      self.app = app
      self.book_client = BookClient()
      self.default_route = "/book"
      self.register_routes()

    def register_routes(self):

      @self.app.route(self.default_route, methods=['POST'])
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

        except BookAlreadyExistsException as error:

          return ApiResponse.conflict(
            str(error)
          )