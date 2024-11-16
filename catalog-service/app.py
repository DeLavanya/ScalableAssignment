from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
books = [
    {"id": 1, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "year": 1960, "available": True, 
     "description": "A novel about the serious issues of rape and racial inequality narrated by young Scout Finch."},
    {"id": 2, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "year": 1949, "available": False, 
     "description": "A dystopian social science fiction novel and cautionary tale about the dangers of totalitarianism."},
    {"id": 3, "title": "Moby Dick", "author": "Herman Melville", "genre": "Adventure", "year": 1851, "available": True, 
     "description": "The story of Captain Ahab's obsessive quest to kill the white whale Moby Dick."},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "year": 1813, "available": True, 
     "description": "A romantic novel that charts the emotional development of protagonist Elizabeth Bennet."},
    {"id": 5, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Tragedy", "year": 1925, "available": False, 
     "description": "A critique of the American Dream set in the Jazz Age, focusing on Jay Gatsby and his unrequited love for Daisy."},
    {"id": 6, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "year": 1951, "available": True, 
     "description": "A story about teenage angst and alienation narrated by the disillusioned Holden Caulfield."},
    {"id": 7, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1937, "available": True, 
     "description": "The prelude to 'The Lord of the Rings,' following Bilbo Baggins' adventurous journey to win treasure guarded by Smaug."},
    {"id": 8, "title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical", "year": 1869, "available": False, 
     "description": "A historical novel that intertwines themes of war, love, and societal change during Napoleon's invasion of Russia."},
    {"id": 9, "title": "The Alchemist", "author": "Paulo Coelho", "genre": "Adventure", "year": 1988, "available": True, 
     "description": "A philosophical tale about a shepherd's journey in search of treasure and his own destiny."},
    {"id": 10, "title": "Crime and Punishment", "author": "Fyodor Dostoevsky", "genre": "Psychological Fiction", "year": 1866, "available": True, 
     "description": "An intense psychological drama about a man wrestling with guilt and redemption after committing murder."},
]


# Route to list all books
@app.route('/books', methods=['GET'])
def list_books():
    """
    List all books in the catalog.
    """
    return jsonify({"books": books}), 200

# Route to search for a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Search for a book by its ID.
    """
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Book not found"}), 404

# Route to search for books by title
@app.route('/books/search', methods=['GET'])
def search_books():
    """
    Search for books by title (case-insensitive).
    """
    query = request.args.get('title', '').lower()
    matching_books = [b for b in books if query in b["title"].lower()]
    if matching_books:
        return jsonify({"books": matching_books}), 200
    return jsonify({"error": "No books found matching the title"}), 404

# Route to check book availability
@app.route('/books/check-availability/<int:book_id>', methods=['GET'])
def check_availability(book_id):
    """
    Check if a book is available.
    """
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify({"available": book["available"]}), 200
    return jsonify({"error": "Book not found"}), 404

# Route to add a new book
@app.route('/books', methods=['POST'])
def add_book():
    """
    Add a new book to the catalog.
    """
    new_book = request.json

    # Validate data
    if not all(key in new_book for key in ("id", "title", "available")):
        return jsonify({"error": "Invalid data. Required fields: id, title, available"}), 400

    # Check for duplicate ID
    if any(b["id"] == new_book["id"] for b in books):
        return jsonify({"error": f"Book with ID {new_book['id']} already exists"}), 409

    books.append(new_book)
    return jsonify(new_book), 201

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
