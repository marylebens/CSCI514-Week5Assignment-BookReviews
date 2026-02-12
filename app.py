from flask import Flask, jsonify, render_template, request
import sqlite3

app = Flask(__name__)

# Define the path to the SQLite database file
DATABASE = 'db/books.db'

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Books.book_id, Books.title, Books.publication_year, Authors.name
            FROM Books
            LEFT JOIN book_author ON Books.book_id = book_author.book_id
            LEFT JOIN Authors ON book_author.author_id = Authors.author_id
        """)
        books = cursor.fetchall()
        conn.close()

        # Convert the list of tuples into a list of dictionaries
        book_list = []
        for book in books:
            book_dict = {
                'book_id': book[0],
                'title': book[1],
                'publication_year': book[2],
                'author': book[3] if book[3] else 'Unknown'
            }
            book_list.append(book_dict)

        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)})


# API to get all authors
@app.route('/api/authors', methods=['GET'])
def get_all_authors():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Authors")
        authors = cursor.fetchall()
        conn.close()
        return jsonify(authors)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to get all reviews
@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reviews")
        reviews = cursor.fetchall()
        conn.close()
        return jsonify(reviews)
    except Exception as e:
        return jsonify({'error': str(e)})

# API to add a book to the database
@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get book details from the request
        data = request.get_json()
        title = data.get('title')
        publication_year = data.get('publication_year')
        author_name = data.get('author')

        # Insert or get the author
        cursor.execute("INSERT OR IGNORE INTO Authors (name) VALUES (?)", (author_name,))
        cursor.execute("SELECT author_id FROM Authors WHERE name = ?", (author_name,))
        author_id = cursor.fetchone()[0]

        # Insert the book
        cursor.execute("INSERT INTO Books (title, publication_year) VALUES (?, ?)", 
                       (title, publication_year))
        book_id = cursor.lastrowid

        # Create the relationship in book_author table
        cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES (?, ?)", 
                       (book_id, author_id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Book added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")