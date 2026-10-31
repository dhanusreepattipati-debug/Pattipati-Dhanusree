# Backend Development Fundamentals (BDF) - Lab Repository

**Student Name**: Pattipati Dhanusree  
**Registration Number**: 252U1R1186  
**Section**: CSE-2D (19 Sec)  
**Academic Year**: Year II Term II  
**Institution**: Aurora  
  

---

## Repository Overview

This repository contains all laboratory assignments, exercises, and project deliverables for the **Backend Development Fundamentals** course. Each laboratory assignment is maintained in its designated subdirectory (`lab-01` through `lab-10`) with independent source code, configuration files, screenshots, and an assignment-specific `README.md`.

---

## Lab Directory Structure

```text
Pattipati-Dhanusree/
├── .gitignore
├── README.md
├── lab-01/
│   ├── .gitignore
│   ├── README.md
│   ├── package.json
│   ├── package-lock.json
│   ├── http-server.js
│   ├── server.js
│   └── screenshots/
│       ├── welcome.png
│       ├── about.png
│       ├── time.png
│       └── 404-not-found.png
├── lab-02/
│   ├── .gitignore
│   ├── README.md
│   ├── package.json
│   ├── package-lock.json
│   ├── server.js
│   ├── books.db
│   ├── init-db.sql
│   ├── init-db.js
│   ├── test-api.js
│   └── screenshots/
│       ├── 1-get-all-books.png
│       ├── 2-get-single-book.png
│       ├── 3-post-add-book.png
│       ├── 4-put-update-book.png
│       ├── 5-delete-book.png
│       ├── 6-error-404-book-not-found.png
│       └── 7-sqlite-cli-verification.png
└── [Future Labs: lab-03 ... lab-10]
```

---

## Labs Progress Table

| Lab No. | Module / Topic | Status | Directory Link |
| :---: | :--- | :---: | :---: |

| **Lab 02** | **SQLite Database and CRUD Routes** | **Completed** | [lab-02/](./lab-02) |


---

## General Course Rules & Standards

- **Version Control Cleanliness**: `node_modules/` and local environment files (`.env`) are strictly excluded via `.gitignore`.
- **Security Compliance**: Parameterized queries are enforced; no credentials, tokens, or plaintext secrets are committed.
- **HTTP Integrity**: Every route returns the exact and appropriate HTTP status code (`200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, etc.).
- **Code Quality**: Modular architecture, structured responses, async/await with error handling, and clean commit messages.
