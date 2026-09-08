import jwt
from datetime import datetime, timedelta, timezone
from utils.ApiResponse import ApiResponse
from domain.exceptions.MissingTokenException import MissingTokenException

class JwtAuth:

  def __init__(self):
    self.secret = "my-secret"

  def gen_token(self,userId,email):
    payload = {
      "user_id": userId,
      "email": email,
      "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    token = jwt.encode(
      payload,
      self.secret,
      algorithm="HS256"
    )

    return token

  def validate_token(self,token):
    if token is None:
      raise MissingTokenException()

    try:
      payload = jwt.decode(
        token,
        self.secret,
        algorithms=["HS256"]
      )

      return payload

    except jwt.ExpiredSignatureError:
      raise jwt.ExpiredSignatureError

    except jwt.InvalidTokenError:
      raise jwt.InvalidTokenError