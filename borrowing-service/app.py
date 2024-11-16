from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import requests

app = FastAPI()

# Simulated Book Service API URL (update this to the actual book-service URL)
BOOK_SERVICE_URL = "http://localhost:8000/books"

# In-memory store for borrowed books (with sample data preloaded)
borrowed_books: Dict[int, str] = {
    1: "Alice",
    2: "Bob",
}

# Models
class BorrowRequest(BaseModel):
    book_id: int
    borrower: str

class ReturnRequest(BaseModel):
    book_id: int

# Route to list borrowed books
@app.get("/borrowed", response_model=Dict[int, str])
async def list_borrowed_books():
    """
    List all currently borrowed books with borrower details.
    """
    return borrowed_books

# Route to borrow a book
@app.post("/borrow")
async def borrow_book(request: BorrowRequest):
    """
    Borrow a book if available.
    - Checks the availability from the book-service.
    - Marks the book as borrowed by adding it to the in-memory store.
    """
    # Simulated check-availability endpoint response
    sample_book_service_response = {
        1: {"available": False},  # Book 1 is already borrowed
        2: {"available": False},  # Book 2 is already borrowed
        3: {"available": True},   # Book 3 is available
        4: {"available": True},   # Book 4 is available
    }

    # Check availability using simulated book-service response
    book_status = sample_book_service_response.get(request.book_id, None)
    if book_status is None:
        raise HTTPException(status_code=404, detail="Book not found in book-service")

    if not book_status["available"]:
        raise HTTPException(status_code=400, detail="Book is not available for borrowing")

    # Mark the book as borrowed
    if request.book_id in borrowed_books:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    borrowed_books[request.book_id] = request.borrower
    return {"message": f"Book ID {request.book_id} successfully borrowed by {request.borrower}"}

# Route to return a book
@app.post("/return")
async def return_book(request: ReturnRequest):
    """
    Return a borrowed book.
    - Removes the book from the in-memory borrowed_books store.
    """
    if request.book_id not in borrowed_books:
        raise HTTPException(status_code=400, detail="Book is not borrowed")

    borrower = borrowed_books.pop(request.book_id)
    return {"message": f"Book ID {request.book_id} successfully returned by {borrower}"}

# Route to check if a book is borrowed
@app.get("/borrowed/{book_id}")
async def check_borrowed_status(book_id: int):
    """
    Check if a specific book is currently borrowed.
    """
    if book_id in borrowed_books:
        return {"borrowed": True, "borrower": borrowed_books[book_id]}
    return {"borrowed": False}
