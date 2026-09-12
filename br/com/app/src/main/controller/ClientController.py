from client.ClientClient import ClientClient
from domain.dto.client.CreateClientDto import CreateClientDto
from domain.dto.client.UpdateClientDto import UpdateClientDto
from utils.ApiResponse import ApiResponse
from domain.exceptions.ConflictException import ConflictException
from domain.exceptions.NotFoundException import NotFoundException
from domain.exceptions.UnauthorizedException import UnauthorizedException
from domain.exceptions.MissingTokenException import MissingTokenException
from auth.JwtAuth import JwtAuth
from flasgger import swag_from
import os
from flask import request

class ClientController:

  def __init__(self, app):
    self.app = app
    self.client_client = ClientClient()
    self.jwt_auth = JwtAuth()
    self.default_route = "/client"
    self.register_routes()

  def register_routes(self):
  
    @self.app.route(self.default_route, methods=['POST'])
    @swag_from(os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/client/create_client.yaml')))
    def create_client():

      json = request.get_json()
      client_dto = CreateClientDto(
        json.get("user_id"), 
        json.get("name"),
        json.get("phone"),
        json.get("address"),
        json.get("zip_code"),
        json.get("city"),
        json.get("neighborhood"),
        json.get("country")
      )
      
      try:
        token = self.jwt_auth.get_token(request)
        self.jwt_auth.validate_token(token)

        response = self.client_client.create_client(client_dto)

        client = {
          "id": response.data.id,
          "user_id": response.data.user_id,
          "name": response.data.name,
          "phone": response.data.phone,
          "address": response.data.address,
          "zip_code": response.data.zip_code,
          "city": response.data.city,
          "neighborhood": response.data.neighborhood,
          "country": response.data.country,
          "is_active": response.data.is_active
        }

        return ApiResponse.created(
          response.message,
          client
        )

      except ConflictException:
        return ApiResponse.internal_server_error(
          "Client already exists with this user."
        )
      
      except MissingTokenException:
        return ApiResponse.unauthorized(
          "Token not found."
        )
      
      except UnauthorizedException:
        return ApiResponse.unauthorized(
          "Invalid or expired token."
        )

      except Exception:
        return ApiResponse.internal_server_error(
          "Error to create client."
        )

      
    @self.app.route(self.default_route + "/<id>", methods=['PUT'])
    @swag_from(os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/client/update_client.yaml')))
    def update_client(id):

      json = request.get_json()
      client_dto = UpdateClientDto(
        json.get("name"),
        json.get("phone"),
        json.get("address"),
        json.get("zip_code"),
        json.get("city"),
        json.get("neighborhood"),
        json.get("country")
      )
      
      try:
        token = self.jwt_auth.get_token(request)
        self.jwt_auth.validate_token(token)

        response = self.client_client.update_client(id, client_dto)

        client = {
          "id": response.data.id,
          "user_id": response.data.user_id,
          "name": response.data.name,
          "phone": response.data.phone,
          "address": response.data.address,
          "zip_code": response.data.zip_code,
          "city": response.data.city,
          "neighborhood": response.data.neighborhood,
          "country": response.data.country,
          "is_active": response.data.is_active
        }

        return ApiResponse.ok(
          response.message,
          client
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

      except Exception as error:
        return ApiResponse.internal_server_error(
          str(error)
        )
      
    @self.app.route(self.default_route + "/deactivate/<id>", methods=['PATCH'])
    @swag_from(os.path.abspath(os.path.join(os.path.dirname(__file__), '../docs/client/deactivate_client.yaml')))
    def deactivate_client(id):
      
      try:
        token = self.jwt_auth.get_token(request)
        self.jwt_auth.validate_token(token)

        response = self.client_client.deactivate_client(id)

        return ApiResponse.ok(
          response.message
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
      
      except Exception as error:
        return ApiResponse.internal_server_error(
          str(error)
        )
