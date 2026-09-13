import jwt
from datetime import datetime, timedelta, timezone
from domain.exceptions.MissingTokenException import MissingTokenException
from domain.exceptions.UnauthorizedException import UnauthorizedException

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
      raise UnauthorizedException()

    except jwt.InvalidTokenError:
      raise UnauthorizedException()

  def get_token(self, request):
    token = request.headers.get('Authorization')

    if token and token.startswith("Bearer "):
      token = token[7:]

    return token