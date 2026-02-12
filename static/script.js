// Array to store book data
const books = [];

// Function to add a book to the list and send it to the server
function addBook() {
    const bookTitle = document.getElementById('bookTitle').value;
    const publicationYear = document.getElementById('publicationYear').value;
    const author = document.getElementById('author').value;

    // Create a JSON object with book data
    const bookData = {
        title: bookTitle,
        publication_year: publicationYear,
        author: author
    };

    // Send the book data to the server via POST request
    fetch('/api/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
    })
        .then(response => response.json())
        .then(data => {
            // Display a success message or handle errors if needed
            console.log(data.message);

            // Add the new book data to the books array
            books.push(bookData);
            console.log(books)

            // Refresh the book list
            displayBooks();
        })
        .catch(error => {
            console.error('Error adding book:', error);
        });
}

// Function to display books in the list
function displayBooks() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = ''; // Clear existing book list

    books.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.innerHTML = `
        <div class="card-body">
            <h5 class="card-title">${book.title}</h2>
            <p class="card-text"><strong>Publication Year: ${book.publication_year}</strong></p>
            <p class="card-text"><strong>Author: ${book.author}</strong></p>
        `;
        bookList.appendChild(bookElement);
    });
}

// Function to fetch and display all books from the server
function showAllBooks() {
    fetch('/api/books')
        .then(response => response.json())
        .then(data => {
            const bookList = document.getElementById('allbooks');
            bookList.innerHTML = '';
            
            data.books.forEach(book => {
                const bookElement = document.createElement('div');
                bookElement.className = 'col-md-4 mb-3';
                bookElement.innerHTML = `
                    <div class="card h-100">
                        <div class="card-body">
                            <h5 class="card-title">${book.title}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${book.author}</h6>
                            <p class="card-text">
                                <span class="badge bg-info">${book.publication_year}</span>
                            </p>
                        </div>
                    </div>
                `;
                bookList.appendChild(bookElement);
            });
        })
        .catch(error => {
            console.error('Error fetching all books:', error);
        });
}
