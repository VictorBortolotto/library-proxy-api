from dataclasses import dataclass

@dataclass
class BookDto:
  title: str
  description: str
  quantity: int