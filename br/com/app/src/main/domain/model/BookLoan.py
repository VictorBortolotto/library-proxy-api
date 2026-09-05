from dataclasses import dataclass

@dataclass
class BookLoan:
  id: str
  book_id: str
  client_id: str
  loan_date: str
  expeted_return_date: str
  return_date: str
  returned_quantity: int
  loan_quantity: int
  is_book_already_returned: str