const express = require('express');
const path = require('path');
const { open } = require('sqlite');
const sqlite3 = require('sqlite3');

const app = express();

// Middleware to parse JSON request bodies
app.use(express.json());

// Serve static assets (e.g. interactive tester UI)
app.use(express.static(path.join(__dirname, 'public')));

// Path to SQLite database file
const dbPath = path.join(__dirname, 'books.db');
let db = null;

/**
 * Initialize SQLite Database connection and Express Server
 */
const initializeDBAndServer = async () => {
  try {
    db = await open({
      filename: dbPath,
      driver: sqlite3.Database,
    });

    const PORT = process.env.PORT || 3000;
    app.listen(PORT, () => {
      console.log(`Server Running at http://localhost:${PORT}/`);
    });
  } catch (error) {
    console.log(`DB Error: ${error.message}`);
    process.exit(1);
  }
};

// Root endpoint: API overview & health check
app.get('/', (req, res) => {
  res.status(200).json({
    message: 'Welcome to the SQLite Books CRUD API (Lab 02)',
    student: 'Pattipati Dhanusree',
    section: 'CSE-2D',
    interactiveTester: '/tester',
    endpoints: {
      getAllBooks: 'GET /books/',
      getSingleBook: 'GET /books/:bookId/',
      addBook: 'POST /books/',
      updateBook: 'PUT /books/:bookId/',
      deleteBook: 'DELETE /books/:bookId/',
    },
  });
});

// Interactive in-browser tester UI route
app.get('/tester', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'tester.html'));
});

/**
 * Route 1: GET /books/
 * Retrieves all books from the database
 */
app.get('/books/', async (req, res) => {
  try {
    const getBooksQuery = `
      SELECT *
      FROM book
      ORDER BY id ASC;
    `;
    const booksArray = await db.all(getBooksQuery);
    res.status(200).json(booksArray);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * Route 2: GET /books/:bookId/
 * Retrieves a single book matching the specified ID using parameterized query (?)
 */
app.get('/books/:bookId/', async (req, res) => {
  try {
    const { bookId } = req.params;
    const getBookQuery = `
      SELECT *
      FROM book
      WHERE id = ?;
    `;
    const book = await db.get(getBookQuery, [bookId]);

    if (!book) {
      return res.status(404).json({ error: 'Book not found' });
    }

    res.status(200).json(book);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * Route 3: POST /books/
 * Inserts a new book record into the database using parameterized query (?)
 */
app.post('/books/', async (req, res) => {
  try {
    const { title, author, price, pages } = req.body;

    if (!title || !author || price === undefined || pages === undefined) {
      return res.status(400).json({
        error: 'Missing required fields: title, author, price, and pages are required.',
      });
    }

    const addBookQuery = `
      INSERT INTO book (title, author, price, pages)
      VALUES (?, ?, ?, ?);
    `;
    const dbResponse = await db.run(addBookQuery, [title, author, price, pages]);

    res.status(201).json({
      message: 'Book Successfully Added',
      bookId: dbResponse.lastID,
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * Route 4: PUT /books/:bookId/
 * Updates an existing book record matching bookId using parameterized query (?)
 */
app.put('/books/:bookId/', async (req, res) => {
  try {
    const { bookId } = req.params;
    const { title, author, price, pages } = req.body;

    if (!title || !author || price === undefined || pages === undefined) {
      return res.status(400).json({
        error: 'Missing required fields: title, author, price, and pages are required.',
      });
    }

    // Check if the book exists prior to update
    const checkBookQuery = `SELECT * FROM book WHERE id = ?;`;
    const existingBook = await db.get(checkBookQuery, [bookId]);

    if (!existingBook) {
      return res.status(404).json({ error: 'Book not found' });
    }

    const updateBookQuery = `
      UPDATE book
      SET
        title = ?,
        author = ?,
        price = ?,
        pages = ?
      WHERE id = ?;
    `;
    await db.run(updateBookQuery, [title, author, price, pages, bookId]);

    res.status(200).json({
      message: 'Book Details Updated Successfully',
      bookId: parseInt(bookId, 10),
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * Route 5: DELETE /books/:bookId/
 * Deletes an existing book record matching bookId using parameterized query (?)
 */
app.delete('/books/:bookId/', async (req, res) => {
  try {
    const { bookId } = req.params;

    // Check if the book exists prior to deletion
    const checkBookQuery = `SELECT * FROM book WHERE id = ?;`;
    const existingBook = await db.get(checkBookQuery, [bookId]);

    if (!existingBook) {
      return res.status(404).json({ error: 'Book not found' });
    }

    const deleteBookQuery = `
      DELETE FROM book
      WHERE id = ?;
    `;
    await db.run(deleteBookQuery, [bookId]);

    res.status(200).json({
      message: 'Book Deleted Successfully',
      bookId: parseInt(bookId, 10),
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Fallback 404 handler for unknown routes
app.use((req, res) => {
  res.status(404).json({
    error: '404 Not Found',
    message: 'The requested endpoint does not exist.',
  });
});

initializeDBAndServer();

module.exports = app;
