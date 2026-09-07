from client.UserClient import UserClient
from domain.dto.user.UserDto import UserDto
from utils.ApiResponse import ApiResponse
from domain.exceptions.ConflictException import ConflictException
from flask import request

class UserController:

  def __init__(self, app):
    self.app = app
    self.user_client = UserClient()
    self.default_route = "/user"
    self.register_routes()

  def register_routes(self):

    @self.app.route(self.default_route, methods=['POST'])
    def create_user():

      json = request.get_json()

      bookDto = UserDto(
        json.get("email"),
        json.get("password")
      )

      try:

        response = self.user_client.create_user(bookDto)

        return ApiResponse.created(
          response.message,
          response.message
        )

      except ConflictException as error:

        return ApiResponse.conflict(
          str(error)
        )

      except Exception as error:

        return ApiResponse.internal_server_error(
          str(error)
        )
      