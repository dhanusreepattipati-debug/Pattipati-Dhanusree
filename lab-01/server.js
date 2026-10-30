
const express = require("express");

const app = express();

// Change these to your actual details
const studentName = "Pattipati Dhanusree";
const studentSection = "CSE-2D 19 Sec";

// GET / - Welcome route
app.get("/", (req, res) => {
  res.status(200).send("Welcome to my Node.js and Express Lab 1 server!");
});

// GET /about - Student details
app.get("/about", (req, res) => {
  res.status(200).json({
    name: studentName,
    section: studentSection
  });
});

// GET /time - Current date and time
app.get("/time", (req, res) => {
  res.status(200).json({
    currentDateTime: new Date().toString()
  });
});

// Handle unknown routes (keep this after the other routes)
app.use((req, res) => {
  res.status(404).json({
    error: "404 Not Found",
    message: "The requested endpoint does not exist."
  });
});

// Use the hosting platform's port, or 3000 locally
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log(`Express server running at http://localhost:${PORT}`);
});
