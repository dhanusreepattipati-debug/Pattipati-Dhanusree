const sqlite3 = require("sqlite3");
const { open } = require("sqlite");
const path = require("path");

const dbPath = path.join(__dirname, "books.db");

const initializeDB = async () => {
  const db = await open({
    filename: dbPath,
    driver: sqlite3.Database,
  });

  const createTableQuery = `
    CREATE TABLE IF NOT EXISTS books (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      title TEXT NOT NULL,
      author TEXT NOT NULL,
      price REAL NOT NULL
    );
  `;

  await db.exec(createTableQuery);

  // Check if initial books seed is needed
  const countResult = await db.get("SELECT COUNT(*) AS count FROM books;");
  if (countResult.count === 0) {
    const seedQuery = `
      INSERT INTO books (title, author, price) VALUES
        ('JavaScript Basics', 'John', 500),
        ('Node.js Guide', 'David', 700),
        ('Python Programming', 'Smith', 400),
        ('Clean Code', 'Robert Martin', 650),
        ('Eloquent JavaScript', 'Marijn Haverbeke', 550);
    `;
    await db.exec(seedQuery);
  }

  console.log("Database connected and table ready.");
  return db;
};

module.exports = initializeDB;
