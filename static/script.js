// Array to store book data
const books = [];

// Function to add a book to the list and send it to the server
function addBook() {
    const bookTitle = document.getElementById('bookTitle').value;
    const publicationYear = document.getElementById('publicationYear').value;
    const author = document.getElementById('author').value;
    const imageFile = document.getElementById('imageFile').files[0];

    // Create FormData to send both text and file data
    const formData = new FormData();
    formData.append('title', bookTitle);
    formData.append('publication_year', publicationYear);
    formData.append('author', author);
    if (imageFile) {
        formData.append('image', imageFile);
    }

    // Send the book data to the server via POST request
    fetch('/api/add_book', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            console.log(data.message);
            
            // Add book to local array with the returned image URL
            const bookData = {
                title: bookTitle,
                publication_year: publicationYear,
                author: author,
                image_url: data.image_url
            };
            books.push(bookData);
            displayBooks();
            
            // Clear form
            document.getElementById('bookTitle').value = '';
            document.getElementById('author').value = '';
            document.getElementById('publicationYear').value = '';
            document.getElementById('imageFile').value = '';
        })
        .catch(error => {
            console.error('Error adding book:', error);
        });
}

// Function to display books in the list
function displayBooks() {
    const bookList = document.getElementById('bookList');
    bookList.innerHTML = '';

    books.forEach(book => {
        const bookElement = document.createElement('div');
        bookElement.className = 'card mb-3';
        bookElement.innerHTML = `
            <div class="card-body">
                ${book.image_url ? `<img src="${book.image_url}" class="img-fluid mb-3" alt="${book.title}" style="max-height: 300px; object-fit: cover;">` : ''}
                <h5 class="card-title">${book.title}</h5>
                <p class="card-text"><strong>Author:</strong> ${book.author}</p>
                <p class="card-text"><strong>Publication Year:</strong> ${book.publication_year}</p>
                <span class="badge badge-success">Added Successfully</span>
            </div>
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
                        ${book.image_url ? `<img src="${book.image_url}" class="card-img-top" alt="${book.title}" style="height: 300px; object-fit: cover;">` : ''}
                        <div class="card-body">
                            <h5 class="card-title">${book.title}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">${book.author}</h6>
                            <p class="card-text">
                                <span class="badge badge-info">${book.publication_year}</span>
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