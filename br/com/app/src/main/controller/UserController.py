from client.UserClient import UserClient
from domain.dto.user.UserDto import UserDto
from utils.ApiResponse import ApiResponse
from domain.exceptions.ConflictException import ConflictException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.UnauthorizedException import UnauthorizedException
from auth.JwtAuth import JwtAuth
from flask import request

class UserController:

  def __init__(self, app):
    self.app = app
    self.user_client = UserClient()
    self.jwt = JwtAuth()
    self.default_route = "/user"
    self.register_routes()

  def register_routes(self):

    @self.app.route(self.default_route, methods=['POST'])
    def create_user():

      json = request.get_json()

      userDto = UserDto(
        json.get("email"),
        json.get("password")
      )

      try:

        response = self.user_client.create_user(userDto)

        token = self.jwt.gen_token(response.user_id, userDto.email)

        return ApiResponse.created(
          response.message,
          {"token": token}
        )

      except ConflictException as error:

        return ApiResponse.conflict(
          str(error)
        )

      except Exception as error:

        return ApiResponse.internal_server_error(
          str(error)
        )
      
    @self.app.route(self.default_route + "/login", methods=['POST'])
    def login():

      json = request.get_json()

      userDto = UserDto(
        json.get("email"),
        json.get("password")
      )

      try:

        response = self.user_client.login(userDto)

        token = self.jwt.gen_token(response.user_id, userDto.email)

        return ApiResponse.created(
          "Authenticated with success",
          {"token": token}
        )

      except NotFoundException as error:

        return ApiResponse.not_found(
          str(error)
        )

      except UnauthorizedException as error:

        return ApiResponse.unauthorized(
          str(error)
        )
      