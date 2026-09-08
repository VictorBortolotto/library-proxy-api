from dataclasses import dataclass

@dataclass
class UserLoginResponse:
  id: int
  is_valid_login: bool