-- SQLite initialization script for Lab 2
-- Creates the book table and inserts 10 sample books

DROP TABLE IF EXISTS book;

CREATE TABLE book (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  price INTEGER NOT NULL,
  pages INTEGER NOT NULL
);

INSERT INTO book (title, author, price, pages) VALUES
  ('The Pragmatic Programmer', 'Andy Hunt & Dave Thomas', 599, 352),
  ('Clean Code', 'Robert C. Martin', 650, 464),
  ('JavaScript: The Good Parts', 'Douglas Crockford', 450, 176),
  ('You Don''t Know JS: Scope & Closures', 'Kyle Simpson', 399, 98),
  ('Designing Data-Intensive Applications', 'Martin Kleppmann', 899, 616),
  ('Introduction to Algorithms', 'Thomas H. Cormen', 1250, 1312),
  ('Atomic Habits', 'James Clear', 499, 320),
  ('Refactoring', 'Martin Fowler', 720, 448),
  ('Eloquent JavaScript', 'Marijn Haverbeke', 550, 472),
  ('Computer Systems: A Programmer''s Perspective', 'Randal E. Bryant', 1100, 1120);
