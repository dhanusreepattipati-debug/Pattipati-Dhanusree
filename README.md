# Lab 1: Node.js and Express Server

## Student Details

- **Name:** Pattipati Dhanusree
- **Registration Number:** 252U1R1186
- **Section:** CSE-2D(19 SEC)
- **Course:** Backend Development Fundamentals
- **Module:** Node.js and Express.js Fundamentals
- **Lab Number:** Lab 1

---

## Live Deployment Link

**Live URL:** ``


## 1. Objective

The objective of this lab is to understand the fundamentals of Node.js and Express.js by creating a basic web server.

In this lab, I implemented a server using the built-in Node.js HTTP module and then recreated the server using Express.js. I also created different API endpoints, handled unknown routes, and tested the server responses and HTTP status codes.

## 2. Technologies Used

- **Node.js** – JavaScript runtime environment.
- **Express.js** – Web framework for Node.js.
- **JavaScript** – Programming language.
- **npm** – Node Package Manager.
- **Git and GitHub** – Version control and repository hosting.
- **VS Code** – Code editor.

## 3. Project Structure

```text
lab-01/
│
├── screenshots/
│   ├── home.png
│   ├── about.png
│   ├── time.png
│   └── 404.png
│
├── server.js
├── http-server.js
├── package.json
├── package-lock.json
├── .gitignore
└── README.md
```

**Note:** The filenames above are a suggested structure. Adjust them to match your actual project files.

## 4. Installation and Setup

### Prerequisites

Make sure the following software is installed:

- Node.js
- npm
- Visual Studio Code
- Git

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### Step 2: Navigate to the Project Folder

```bash
cd YOUR_REPOSITORY_NAME/lab-01
```

### Step 3: Install Dependencies

```bash
npm install
```

### Step 4: Install Express

```bash
npm install express
```

### Step 5: Start the Server

```bash
node server.js
```

The server will start on port 3000.

Open the following URL in your browser:

```text
http://localhost:3000
```

### Environment Variables

No environment variables are required for this basic lab implementation.

## 5. Implementation

### Task 1: Initialize Node.js Project

Created a project folder and initialized the Node.js project using:

```bash
npm init -y
```

This generated the `package.json` file containing project information and dependencies.

### Task 2: Install Express.js

Installed Express using:

```bash
npm install express
```

Express was added as a project dependency and installed inside the `node_modules` directory.

### Task 3: Create a Basic HTTP Server

Implemented a basic server using Node.js's built-in `http` module.

The server responds with the message:

```text
Hello
```

The server listens on port 3000.

### Task 4: Create an Express Server

Reimplemented the server using Express.js.

Used:

```javascript
const express = require('express');
const app = express();

app.listen(3000);
```

### Task 5: Implement API Routes

Created three GET endpoints using Express.js.

### Task 6: Handle Unknown Routes

Implemented a 404 error response for requests to undefined routes.

### Task 7: Test API Endpoints

Tested all endpoints using a web browser and verified their responses and HTTP status codes.

## 6. API Endpoints

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| GET | `/` | Displays the welcome message. | 200 |
| GET | `/about` | Returns student name and section in JSON format. | 200 |
| GET | `/time` | Returns the current date and time. | 200 |
| GET | Unknown routes | Returns a 404 Not Found message. | 404 |

### Endpoint URLs

**Home Route**
```text
http://localhost:3000/
```

**About Route**
```text
http://localhost:3000/about
```

**Time Route**
```text
http://localhost:3000/time
```

**404 Error Testing**
```text
http://localhost:3000/unknown
```

## 7. Screenshots

The following screenshots demonstrate the successful execution of the API endpoints.

### 1. Home Route

Displays the welcome message returned by the server.

![Home Route](screenshots/home.png)

### 2. About Route

Displays student information in JSON format.

![About Route](screenshots/about.png)

### 3. Time Route

Displays the current date and time generated using JavaScript's `new Date()`.

![Time Route](screenshots/time.png)

### 4. 404 Not Found

Displays the error response when an undefined endpoint is accessed.

![404 Error](screenshots/404.png)

## 8. HTTP Status Codes

| Status Code | Meaning | Usage |
|---|---|---|
| 200 | OK | Request completed successfully. |
| 404 | Not Found | Requested endpoint does not exist. |

## 9. Viva Questions and Answers

**1. What is the difference between package.json and node_modules?**

`package.json` contains project metadata, scripts, and dependency information. `node_modules` contains the actual installed packages and their dependencies.

**2. What does app.listen() do?**

The `app.listen()` method starts the Express server and makes it listen for incoming requests on the specified port.

**3. What do request and response represent?**

The request object contains information about the incoming HTTP request, while the response object is used to send data and status codes back to the client.

## 10. Problems Faced and Solutions

- **Problem:** Understanding the difference between the Node.js HTTP module and Express.js.

  **Solution:** Implemented the same basic server functionality using both approaches.

- **Problem:** Handling requests to undefined routes.

  **Solution:** Added a 404 error-handling route to return an appropriate response.

- **Problem:** Testing API endpoints.

  **Solution:** Opened each endpoint in the browser and verified the returned content and status codes.

## 11. GitHub Submission

The complete Lab 1 implementation is available in the following GitHub repository:

**GitHub Repository:** `YOUR_GITHUB_REPOSITORY_URL`

## 12. Conclusion

Successfully completed Lab 1 by creating a basic Node.js HTTP server and an Express.js server. Implemented GET endpoints for the home page, student information, and current date and time. Also implemented 404 error handling and tested the API endpoints to verify their responses and status codes.

This lab provided practical knowledge of Node.js server creation, Express.js routing, HTTP methods, and response handling.

---

**End of Lab 1: Node.js and Express Server**
