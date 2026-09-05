from dataclasses import dataclass
from datetime import datetime

@dataclass
class Client:
  id: int | None
  user_id: str
  name: str
  phone: str
  address: str
  zip_code: str
  city: str
  neighborhood: str
  country: str
  is_active: bool