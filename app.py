from flask import Flask, jsonify, render_template, request
import sqlite3
import os
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)

# Define the path to your SQLite database file
DATABASE = 'db/books.db'

# Configure upload folder
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Books.book_id, Books.title, Books.publication_year, Authors.name, Books.image_url
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
                'author': book[3] if book[3] else 'Unknown',
                'image_url': book[4]
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

@app.route('/api/add_book', methods=['POST'])
def add_book():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # Get book details from the request
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_name = request.form.get('author')
        
        # Handle file upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add timestamp to avoid filename conflicts
                timestamp = str(int(time.time()))
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_url = f'/static/images/{filename}'

        # Insert or get the author
        cursor.execute("INSERT OR IGNORE INTO Authors (name) VALUES (?)", (author_name,))
        cursor.execute("SELECT author_id FROM Authors WHERE name = ?", (author_name,))
        author_id = cursor.fetchone()[0]

        # Insert the book with image_url
        cursor.execute("INSERT INTO Books (title, publication_year, image_url) VALUES (?, ?, ?)", 
                       (title, publication_year, image_url))
        book_id = cursor.lastrowid

        # Create the relationship in book_author table
        cursor.execute("INSERT INTO book_author (book_id, author_id) VALUES (?, ?)", 
                       (book_id, author_id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Book added successfully', 'image_url': image_url})
    except Exception as e:
        return jsonify({'error': str(e)})

# Route to render the index.html page
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")