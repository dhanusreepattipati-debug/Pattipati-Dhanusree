const express = require("express");
const path = require("path");
const initializeDB = require("./database");

const app = express();

app.use(express.json());

// Serve static assets (e.g. interactive tester UI)
app.use(express.static(path.join(__dirname, "public")));

let db = null;

const getDB = async () => {
  if (!db) {
    db = await initializeDB();
  }
  return db;
};

// Root endpoint: API Overview & Health Check
app.get("/", (req, res) => {
  res.status(200).json({
    message: "Welcome to the Books REST API with Search, Filtering & Validation (Lab 3)",
    student: "Pattipati Dhanusree",
    rollNumber: "252U1R1186",
    section: "CSE-2D (19 Sec)",
    subject: "Backend Development Fundamentals - Aurora",
    interactiveTester: "/tester",
    endpoints: {
      getAllBooks: "GET /books",
      searchBooks: "GET /books?search_q=Node",
      sortBooks: "GET /books?order_by=price&order=DESC",
      filterByPrice: "GET /books?min_price=400&max_price=800",
      paginateBooks: "GET /books?limit=2&offset=0",
      getSingleBook: "GET /books/:id",
      createBook: "POST /books",
      updateBook: "PUT /books/:id",
      deleteBook: "DELETE /books/:id",
    },
  });
});

// Interactive in-browser tester UI route
app.get("/tester", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "tester.html"));
});

// Database connection middleware - guarantees DB is initialized before any route executes
app.use(async (req, res, next) => {
  try {
    if (!db) {
      db = await getDB();
    }
    next();
  } catch (err) {
    console.error("Database connection failed in middleware:", err);
    res.status(500).json({
      message: "Internal server error: Database initialization failed",
    });
  }
});

// ==========================================
// API 1: GET ALL BOOKS (WITH SEARCH, SORT, FILTER & PAGINATION)
// GET /books
// ==========================================
app.get("/books", async (request, response) => {
  try {
    const {
      search_q = "",
      order_by = "id",
      order = "ASC",
      limit = "10",
      offset = "0",
      min_price,
      max_price,
    } = request.query;

    // 1. Whitelist validation for sorting column
    const allowedColumns = ["id", "title", "author", "price"];
    if (!allowedColumns.includes(order_by)) {
      return response.status(400).json({
        message: "Invalid order_by column",
      });
    }

    // 2. Validate sort direction (case-insensitive conversion)
    const sortOrder = order.toUpperCase();
    if (!["ASC", "DESC"].includes(sortOrder)) {
      return response.status(400).json({
        message: "Order must be ASC or DESC",
      });
    }

    // 3. Validate limit and offset (must be non-negative integers, limit > 0)
    const limitValue = Number(limit);
    const offsetValue = Number(offset);

    if (
      !Number.isInteger(limitValue) ||
      !Number.isInteger(offsetValue) ||
      limitValue <= 0 ||
      offsetValue < 0
    ) {
      return response.status(400).json({
        message: "Invalid limit or offset",
      });
    }

    // 4. Validate price filter inputs
    if (
      (min_price !== undefined && (min_price.trim() === "" || !Number.isFinite(Number(min_price)))) ||
      (max_price !== undefined && (max_price.trim() === "" || !Number.isFinite(Number(max_price))))
    ) {
      return response.status(400).json({
        message: "Price filters must be numeric",
      });
    }

    if (
      min_price !== undefined &&
      max_price !== undefined &&
      Number(min_price) > Number(max_price)
    ) {
      return response.status(400).json({
        message: "min_price cannot exceed max_price",
      });
    }

    // 5. Construct parameterized query
    let query = `
      SELECT * FROM books
      WHERE title LIKE ?
    `;
    const params = [`%${search_q}%`];

    if (min_price !== undefined) {
      query += " AND price >= ?";
      params.push(Number(min_price));
    }

    if (max_price !== undefined) {
      query += " AND price <= ?";
      params.push(Number(max_price));
    }

    query += ` ORDER BY ${order_by} ${sortOrder} LIMIT ? OFFSET ?`;
    params.push(limitValue, offsetValue);

    const books = await db.all(query, params);
    response.status(200).json(books);
  } catch (error) {
    console.error("GET /books error:", error);
    response.status(500).json({
      message: "Internal server error",
    });
  }
});

// ==========================================
// API 2: GET BOOK BY ID
// GET /books/:id
// ==========================================
app.get("/books/:id", async (request, response) => {
  try {
    const { id } = request.params;

    const book = await db.get(
      "SELECT * FROM books WHERE id = ?",
      [id]
    );

    if (!book) {
      return response.status(404).json({
        message: "Book not found",
      });
    }

    response.status(200).json(book);
  } catch (error) {
    console.error("GET /books/:id error:", error);
    response.status(500).json({
      message: "Internal server error",
    });
  }
});

// ==========================================
// API 3: CREATE A NEW BOOK
// POST /books
// ==========================================
app.post("/books", async (request, response) => {
  try {
    const { title, author, price } = request.body;

    // Validate body attributes
    if (
      typeof title !== "string" ||
      !title.trim() ||
      typeof author !== "string" ||
      !author.trim() ||
      price === undefined ||
      typeof price !== "number" ||
      !Number.isFinite(price) ||
      price < 0
    ) {
      return response.status(400).json({
        message: "Valid title, author and numeric price are required",
      });
    }

    const query = `
      INSERT INTO books (title, author, price)
      VALUES (?, ?, ?)
    `;

    const result = await db.run(query, [
      title.trim(),
      author.trim(),
      price,
    ]);

    response.status(201).json({
      message: "Book created successfully",
      book_id: result.lastID,
    });
  } catch (error) {
    console.error("POST /books error:", error);
    response.status(500).json({
      message: "Internal server error",
    });
  }
});

// ==========================================
// API 4: UPDATE A BOOK
// PUT /books/:id
// ==========================================
app.put("/books/:id", async (request, response) => {
  try {
    const { id } = request.params;
    const { title, author, price } = request.body;

    // Check whether the book exists
    const existingBook = await db.get(
      "SELECT * FROM books WHERE id = ?",
      [id]
    );

    if (!existingBook) {
      return response.status(404).json({
        message: "Book not found",
      });
    }

    // Validate body attributes
    if (
      typeof title !== "string" ||
      !title.trim() ||
      typeof author !== "string" ||
      !author.trim() ||
      price === undefined ||
      typeof price !== "number" ||
      !Number.isFinite(price) ||
      price < 0
    ) {
      return response.status(400).json({
        message: "Valid title, author and numeric price are required",
      });
    }

    await db.run(
      `UPDATE books
       SET title = ?, author = ?, price = ?
       WHERE id = ?`,
      [title.trim(), author.trim(), price, id]
    );

    response.status(200).json({
      message: "Book updated successfully",
    });
  } catch (error) {
    console.error("PUT /books/:id error:", error);
    response.status(500).json({
      message: "Internal server error",
    });
  }
});

// ==========================================
// API 5: DELETE A BOOK
// DELETE /books/:id
// ==========================================
app.delete("/books/:id", async (request, response) => {
  try {
    const { id } = request.params;

    // Check whether the book exists
    const existingBook = await db.get(
      "SELECT * FROM books WHERE id = ?",
      [id]
    );

    if (!existingBook) {
      return response.status(404).json({
        message: "Book not found",
      });
    }

    await db.run("DELETE FROM books WHERE id = ?", [id]);

    response.status(200).json({
      message: "Book deleted successfully",
    });
  } catch (error) {
    console.error("DELETE /books/:id error:", error);
    response.status(500).json({
      message: "Internal server error",
    });
  }
});

// Fallback for unhandled routes
app.use((request, response) => {
  response.status(404).json({
    message: "Endpoint not found",
  });
});

// ==========================================
// SERVER INITIALIZATION
// ==========================================
const PORT = process.env.PORT || 3000;

// Connect to DB immediately and start server when running standalone
getDB()
  .then(() => {
    if (require.main === module || !process.env.VERCEL) {
      app.listen(PORT, () => {
        console.log(`Server running at http://localhost:${PORT}`);
      });
    }
  })
  .catch((err) => {
    console.error("Database initialization failed:", err);
  });

module.exports = app;
