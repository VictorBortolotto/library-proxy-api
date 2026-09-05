from dataclasses import dataclass

@dataclass
class UpdateBookLoanRequest:
  book_id: str
  return_date: str
  is_book_already_returned: bool
  returned_quantity: int