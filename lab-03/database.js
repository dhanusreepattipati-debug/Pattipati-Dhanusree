const sqlite3 = require("sqlite3");
const { open } = require("sqlite");
const path = require("path");
const fs = require("fs");

const getDbPath = () => {
  // On Vercel / AWS Lambda serverless environments, the deployment root is read-only.
  // We copy the database to /tmp so both reads and writes (INSERT, UPDATE, DELETE) work smoothly.
  if (process.env.VERCEL || process.env.AWS_LAMBDA_FUNCTION_NAME) {
    const tmpDbPath = path.join("/tmp", "books.db");
    const sourceDbPath = path.join(__dirname, "books.db");
    if (!fs.existsSync(tmpDbPath) && fs.existsSync(sourceDbPath)) {
      try {
        fs.copyFileSync(sourceDbPath, tmpDbPath);
      } catch (e) {
        console.error("Error copying books.db to /tmp:", e);
      }
    }
    return tmpDbPath;
  }
  return path.join(__dirname, "books.db");
};

const initializeDB = async () => {
  const dbPath = getDbPath();

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
  if (!countResult || countResult.count === 0) {
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

  console.log(`Database connected (${dbPath}) and table ready.`);
  return db;
};

module.exports = initializeDB;
