const fs = require('fs');
const path = require('path');
const sqlite3 = require('sqlite3').verbose();

const dbPath = path.join(__dirname, 'books.db');
const sqlPath = path.join(__dirname, 'init-db.sql');

const sql = fs.readFileSync(sqlPath, 'utf8');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error opening database:', err.message);
    process.exit(1);
  }
  console.log('Connected to SQLite database at:', dbPath);
});

db.exec(sql, (err) => {
  if (err) {
    console.error('Error executing seed SQL:', err.message);
    db.close();
    process.exit(1);
  }
  console.log('Successfully created table and seeded 10 records into book table.');
  
  db.all('SELECT * FROM book;', [], (err, rows) => {
    if (err) {
      console.error('Error querying records:', err.message);
    } else {
      console.log(`Database verification: ${rows.length} rows found in book table.`);
      console.table(rows);
    }
    db.close();
  });
});
