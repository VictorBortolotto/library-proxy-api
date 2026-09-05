from dataclasses import dataclass

@dataclass
class BookLoanResponseDto:
  id: int
  book_id: str
  client_id: str
  loan_date: str
  loan_quantity: int
  expeted_return_date: str