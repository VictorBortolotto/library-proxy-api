from dataclasses import dataclass

@dataclass
class UpdateClientDto:
  name: str
  phone: str
  address: str
  zip_code: str
  city: str
  neighborhood: str
  country: str