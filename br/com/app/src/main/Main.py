from flask import Flask
from controller.BookController import BookController
from flask_cors import CORS
app = Flask(__name__)

CORS(app, resources={
    r"/note*": {
        "origins": ["null", "http://localhost:8081"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

def main():
  BookController(app)

main()

if __name__ == "__main__":
  app.run(port=8081)