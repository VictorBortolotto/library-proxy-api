from dataclasses import dataclass

@dataclass
class CreateBookLoanDto:
  book_id: int
  client_id: int
  loan_date: str
  loan_quantity: int
  expeted_return_date: str