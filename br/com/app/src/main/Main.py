from flask import Flask
from controller.BookController import BookController
from controller.UserController import UserController
from controller.ClientController import ClientController
from controller.BookLoanController import BookLoanController
from controller.ZipCodeController import ZipCodeController
from config.SwaggerConfig import SwaggerConfig
from flask_cors import CORS
app = Flask(__name__)

CORS(app, resources={
    r"/note*": {
        "origins": ["null", "http://localhost:8081"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

swagger = SwaggerConfig().config(app)

def main():
  BookController(app)
  UserController(app)
  ClientController(app)
  BookLoanController(app)
  ZipCodeController(app)

main()

if __name__ == "__main__":
  app.run(port=8081)