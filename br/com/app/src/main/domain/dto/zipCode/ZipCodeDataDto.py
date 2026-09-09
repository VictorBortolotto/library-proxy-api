from dataclasses import dataclass

@dataclass
class ZipCodeDataDto:
  address: str
  zip_code: str
  city: str
  neighborhood: str