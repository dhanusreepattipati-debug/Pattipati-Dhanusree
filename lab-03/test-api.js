const http = require("http");

const BASE_URL = "http://localhost:3000";

function request(options, postData) {
  return new Promise((resolve, reject) => {
    const req = http.request(options, (res) => {
      let body = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => {
        let json = null;
        try {
          json = JSON.parse(body);
        } catch (e) {
          json = body;
        }
        resolve({ status: res.statusCode, headers: res.headers, body: json });
      });
    });

    req.on("error", (err) => reject(err));

    if (postData) {
      req.write(typeof postData === "string" ? postData : JSON.stringify(postData));
    }
    req.end();
  });
}

async function runTests() {
  console.log("=== LAB 3 API AUTOMATED VERIFICATION SUITE ===");
  let passed = 0;
  let total = 0;

  function assert(condition, name) {
    total++;
    if (condition) {
      console.log(`✓ [PASS] ${name}`);
      passed++;
    } else {
      console.error(`✗ [FAIL] ${name}`);
    }
  }

  try {
    // 1. GET /books
    const r1 = await request({ host: "localhost", port: 3000, path: "/books", method: "GET" });
    assert(r1.status === 200 && Array.isArray(r1.body), "GET /books returns 200 OK and an array");

    // 2. POST /books - Success
    const r2 = await request(
      {
        host: "localhost",
        port: 3000,
        path: "/books",
        method: "POST",
        headers: { "Content-Type": "application/json" },
      },
      { title: "Automated Test Book", author: "Tester", price: 350 }
    );
    assert(r2.status === 201 && r2.body.book_id, "POST /books returns 201 Created with book_id");
    const createdId = r2.body.book_id;

    // 3. GET /books/:id - Success
    const r3 = await request({ host: "localhost", port: 3000, path: `/books/${createdId}`, method: "GET" });
    assert(r3.status === 200 && r3.body.title === "Automated Test Book", `GET /books/${createdId} returns 200 OK with correct record`);

    // 4. PUT /books/:id - Success
    const r4 = await request(
      {
        host: "localhost",
        port: 3000,
        path: `/books/${createdId}`,
        method: "PUT",
        headers: { "Content-Type": "application/json" },
      },
      { title: "Updated Test Book", author: "Tester", price: 450 }
    );
    assert(r4.status === 200 && r4.body.message === "Book updated successfully", `PUT /books/${createdId} returns 200 OK`);

    // 5. DELETE /books/:id - Success
    const r5 = await request({ host: "localhost", port: 3000, path: `/books/${createdId}`, method: "DELETE" });
    assert(r5.status === 200 && r5.body.message === "Book deleted successfully", `DELETE /books/${createdId} returns 200 OK`);

    // 6. GET /books/:id - 404 After Delete
    const r6 = await request({ host: "localhost", port: 3000, path: `/books/${createdId}`, method: "GET" });
    assert(r6.status === 404 && r6.body.message === "Book not found", `GET /books/${createdId} returns 404 Not Found after deletion`);

    // 7. GET /books?search_q=JavaScript - Search
    const r7 = await request({ host: "localhost", port: 3000, path: "/books?search_q=JavaScript", method: "GET" });
    assert(r7.status === 200 && Array.isArray(r7.body), "GET /books?search_q=JavaScript returns 200 OK");

    // 8. GET /books?order_by=price&order=DESC - Sort
    const r8 = await request({ host: "localhost", port: 3000, path: "/books?order_by=price&order=DESC", method: "GET" });
    assert(r8.status === 200 && r8.body.length >= 2 && r8.body[0].price >= r8.body[1].price, "GET /books?order_by=price&order=DESC sorts in descending order");

    // 9. GET /books?min_price=400&max_price=800 - Filter
    const r9 = await request({ host: "localhost", port: 3000, path: "/books?min_price=400&max_price=800", method: "GET" });
    const allInRange = r9.body.every((b) => b.price >= 400 && b.price <= 800);
    assert(r9.status === 200 && allInRange, "GET /books?min_price=400&max_price=800 filters by price range");

    // 10. GET /books?limit=2&offset=0 - Pagination
    const r10 = await request({ host: "localhost", port: 3000, path: "/books?limit=2&offset=0", method: "GET" });
    assert(r10.status === 200 && r10.body.length <= 2, "GET /books?limit=2&offset=0 enforces pagination");

    // 11. POST /books - Validation (Missing title)
    const r11 = await request(
      {
        host: "localhost",
        port: 3000,
        path: "/books",
        method: "POST",
        headers: { "Content-Type": "application/json" },
      },
      { author: "Author Only", price: 200 }
    );
    assert(r11.status === 400 && r11.body.message, "POST /books (missing title) returns 400 Bad Request");

    // 12. POST /books - Validation (Non-numeric price)
    const r12 = await request(
      {
        host: "localhost",
        port: 3000,
        path: "/books",
        method: "POST",
        headers: { "Content-Type": "application/json" },
      },
      { title: "Invalid Book", author: "Author", price: "free" }
    );
    assert(r12.status === 400 && r12.body.message, "POST /books (non-numeric price) returns 400 Bad Request");

    // 13. GET /books?order_by=invalid - Whitelist
    const r13 = await request({ host: "localhost", port: 3000, path: "/books?order_by=invalid_col", method: "GET" });
    assert(r13.status === 400 && r13.body.message === "Invalid order_by column", "GET /books?order_by=invalid_col returns 400 Bad Request");

    // 14. GET /books?min_price=900&max_price=200 - Range validation
    const r14 = await request({ host: "localhost", port: 3000, path: "/books?min_price=900&max_price=200", method: "GET" });
    assert(r14.status === 400 && r14.body.message === "min_price cannot exceed max_price", "GET /books?min_price=900&max_price=200 returns 400 Bad Request");

    console.log("=================================================");
    console.log(`TOTAL: ${passed}/${total} TESTS PASSED (${Math.round((passed / total) * 100)}%)`);
  } catch (err) {
    console.error("Test execution failed. Is the server running?", err.message);
  }
}

runTests();
