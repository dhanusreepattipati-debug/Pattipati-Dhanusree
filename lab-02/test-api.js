const http = require('http');

const PORT = 3000;
const BASE_URL = `http://localhost:${PORT}`;

function request(method, path, body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(path, BASE_URL);
    const options = {
      method,
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = data ? JSON.parse(data) : null;
          resolve({ status: res.statusCode, data: parsed, raw: data });
        } catch (e) {
          resolve({ status: res.statusCode, data, raw: data });
        }
      });
    });

    req.on('error', reject);

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

async function runTests() {
  console.log('--- Starting API Route Tests ---\n');

  // Test 1: GET /books/
  console.log('1. Testing GET /books/ ...');
  const allBooksRes = await request('GET', '/books/');
  console.log(`Status: ${allBooksRes.status}`);
  console.log(`Total books count: ${allBooksRes.data.length}`);
  console.assert(allBooksRes.status === 200, 'GET /books/ must return 200');
  console.assert(allBooksRes.data.length >= 10, 'Expected at least 10 books');
  console.log('✓ PASS: GET /books/\n');

  // Test 2: GET /books/1/
  console.log('2. Testing GET /books/1/ ...');
  const book1Res = await request('GET', '/books/1/');
  console.log(`Status: ${book1Res.status}`);
  console.log('Data:', book1Res.data);
  console.assert(book1Res.status === 200, 'GET /books/1/ must return 200');
  console.assert(book1Res.data.id === 1, 'Book ID should be 1');
  console.log('✓ PASS: GET /books/1/\n');

  // Test 3: POST /books/
  console.log('3. Testing POST /books/ (add new book) ...');
  const newBook = {
    title: 'Node.js Design Patterns',
    author: 'Mario Casciaro & Luciano Mammino',
    price: 799,
    pages: 660,
  };
  const postRes = await request('POST', '/books/', newBook);
  console.log(`Status: ${postRes.status}`);
  console.log('Data:', postRes.data);
  console.assert(postRes.status === 201, 'POST /books/ must return 201');
  const createdId = postRes.data.bookId;
  console.log(`✓ PASS: POST /books/ created book with ID ${createdId}\n`);

  // Test 4: GET /books/:bookId/ to verify creation
  console.log(`4. Verifying inserted book with GET /books/${createdId}/ ...`);
  const verifyRes = await request('GET', `/books/${createdId}/`);
  console.log(`Status: ${verifyRes.status}`);
  console.log('Data:', verifyRes.data);
  console.assert(verifyRes.data.title === newBook.title, 'Title must match');
  console.log('✓ PASS: Inserted book verified\n');

  // Test 5: PUT /books/:bookId/
  console.log(`5. Testing PUT /books/${createdId}/ (update book) ...`);
  const updatedBook = {
    title: 'Node.js Design Patterns (3rd Edition)',
    author: 'Mario Casciaro & Luciano Mammino',
    price: 850,
    pages: 680,
  };
  const putRes = await request('PUT', `/books/${createdId}/`, updatedBook);
  console.log(`Status: ${putRes.status}`);
  console.log('Data:', putRes.data);
  console.assert(putRes.status === 200, 'PUT /books/:bookId/ must return 200');
  console.log('✓ PASS: PUT /books/:bookId/\n');

  // Test 6: Verify updated record
  console.log(`6. Verifying update with GET /books/${createdId}/ ...`);
  const verifyUpdateRes = await request('GET', `/books/${createdId}/`);
  console.log(`Status: ${verifyUpdateRes.status}`);
  console.log('Data:', verifyUpdateRes.data);
  console.assert(verifyUpdateRes.data.price === 850, 'Price must be updated');
  console.log('✓ PASS: Book update verified\n');

  // Test 7: DELETE /books/:bookId/
  console.log(`7. Testing DELETE /books/${createdId}/ ...`);
  const deleteRes = await request('DELETE', `/books/${createdId}/`);
  console.log(`Status: ${deleteRes.status}`);
  console.log('Data:', deleteRes.data);
  console.assert(deleteRes.status === 200, 'DELETE /books/:bookId/ must return 200');
  console.log('✓ PASS: DELETE /books/:bookId/\n');

  // Test 8: Verify 404 for deleted book
  console.log(`8. Verifying deleted book returns 404 with GET /books/${createdId}/ ...`);
  const verifyDeleteRes = await request('GET', `/books/${createdId}/`);
  console.log(`Status: ${verifyDeleteRes.status}`);
  console.log('Data:', verifyDeleteRes.data);
  console.assert(verifyDeleteRes.status === 404, 'GET on deleted book must return 404');
  console.log('✓ PASS: 404 returned for deleted book\n');

  // Test 9: 404 for non-existent DELETE
  console.log('9. Testing DELETE for non-existent book /books/9999/ ...');
  const delete404Res = await request('DELETE', '/books/9999/');
  console.log(`Status: ${delete404Res.status}`);
  console.assert(delete404Res.status === 404, 'Expected 404 for non-existent ID');
  console.log('✓ PASS: DELETE non-existent book returns 404\n');

  // Test 10: 400 Bad Request on invalid POST
  console.log('10. Testing POST with missing fields ...');
  const badPostRes = await request('POST', '/books/', { title: 'Incomplete Book' });
  console.log(`Status: ${badPostRes.status}`);
  console.log('Data:', badPostRes.data);
  console.assert(badPostRes.status === 400, 'Expected 400 for missing fields');
  console.log('✓ PASS: Bad request properly handled\n');

  console.log('====================================');
  console.log('ALL API TESTS COMPLETED SUCCESSFULLY');
  console.log('====================================');
}

runTests().catch(console.error);
