from client.ZipCodeClient import ZipCodeClient
from utils.ApiResponse import ApiResponse
from domain.dto.zipCode.ZipCodeDataDto import ZipCodeDataDto
from domain.exceptions.NotFoundException import NotFoundException
from flask import request

class ZipCodeController:

  def __init__(self, app):
    self.app = app
    self.zip_code_client = ZipCodeClient()
    self.default_route = "/zip_code"
    self.register_routes()

  def register_routes(self):
    @self.app.route(self.default_route + "/<cep>", methods=['GET'])
    def find_zip_code_data(cep):
      try:

        response = self.zip_code_client.find_zip_code_data(cep)

        zip_code_data = ZipCodeDataDto(
          response.data.address,
          response.data.zip_code,
          response.data.city,
          response.data.neighborhood
        )

        return ApiResponse.ok(
          response.message,
          zip_code_data
        )

      except NotFoundException as error:

        return ApiResponse.not_found(
          str(error)
        )