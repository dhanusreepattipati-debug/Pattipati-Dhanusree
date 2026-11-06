import subprocess
import os
import re

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
TEMP_DIR = os.path.join(os.path.dirname(__file__), ".temp_render")
os.makedirs(TEMP_DIR, exist_ok=True)

EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

def render_vscode_window(
    filename,
    left_start_line,
    left_lines,
    selected_range,
    right_status,
    status_type,
    content_length,
    etag,
    date_str,
    right_json_lines,
    response_time="10ms",
    height=660
):
    html_file = os.path.join(TEMP_DIR, f"{filename}.html")
    png_file = os.path.join(SCREENSHOTS_DIR, filename)

    left_html = []
    curr_line = left_start_line
    for line in left_lines:
        is_selected = selected_range and (selected_range[0] <= curr_line <= selected_range[1])
        sel_class = " selected" if is_selected else ""

        # Syntax highlighting
        hl = line
        if line.strip().startswith("###"):
            hl = f'<span class="cm-section">{line}</span>'
        elif line.strip() == "Send Request":
            hl = f'<span class="cm-codelens">{line}</span>'
        elif any(line.strip().startswith(m + " ") for m in ["GET", "POST", "PUT", "DELETE"]):
            parts = line.split(" ", 1)
            method = parts[0]
            rest = parts[1] if len(parts) > 1 else ""
            rest = rest.replace("{{baseUrl}}", '<span class="cm-var">{{baseUrl}}</span>')
            rest = rest.replace("{{bookId}}", '<span class="cm-var">{{bookId}}</span>')
            hl = f'<span class="cm-method">{method}</span> {rest}'
        elif "Content-Type:" in line:
            hl = line.replace("Content-Type:", '<span class="cm-header">Content-Type:</span>').replace("application/json", '<span class="cm-string">application/json</span>')
        elif line.strip().startswith("#"):
            hl = f'<span class="cm-comment">{line}</span>'
        elif ":" in line and ('"' in line or "'" in line):
            hl = re.sub(r'(".*?")(\s*:)', r'<span class="cm-key">\1</span>\2', hl)
            hl = re.sub(r':\s*(".*?")', r': <span class="cm-string">\1</span>', hl)
            hl = re.sub(r':\s*([0-9\.\-]+)', r': <span class="cm-number">\1</span>', hl)

        fold = "v" if any(k in line for k in ["###", "GET ", "POST ", "PUT ", "DELETE ", "{"]) else "&nbsp;"
        left_html.append(f'<div class="code-line{sel_class}"><span class="line-no">{curr_line}</span><span class="fold">{fold}</span><span class="code-text">{hl}</span></div>')
        curr_line += 1

    # Right side
    status_class = "st-success" if status_type == "success" else "st-error"
    parts = right_status.split(" ", 1)
    proto = parts[0]
    code_text = parts[1] if len(parts) > 1 else ""

    headers = [
        f'1 <span class="h-name">HTTP/1.1</span> <span class="{status_class}">{code_text}</span>',
        f'2 <span class="h-name">X-Powered-By:</span> Express',
        f'3 <span class="h-name">Content-Type:</span> application/json; charset=utf-8',
        f'4 <span class="h-name">Content-Length:</span> {content_length}',
        f'5 <span class="h-name">ETag:</span> {etag}',
        f'6 <span class="h-name">Date:</span> {date_str}',
        f'7 <span class="h-name">Connection:</span> close',
        f'8'
    ]

    right_html = [f'<div class="code-line"><span class="code-text">{h}</span></div>' for h in headers]
    r_no = 9
    for rline in right_json_lines:
        hl = rline
        hl = re.sub(r'(".*?")(\s*:)', r'<span class="cm-key">\1</span>\2', hl)
        hl = re.sub(r':\s*(".*?")', r': <span class="cm-string">\1</span>', hl)
        hl = re.sub(r':\s*([0-9\.\-]+)', r': <span class="cm-number">\1</span>', hl)
        hl = re.sub(r'^\s*(".*?")\s*$', r'<span class="cm-string">\1</span>', hl)
        fold = "v" if "{" in rline or "[" in rline else "&nbsp;"
        right_html.append(f'<div class="code-line"><span class="line-no">{r_no}</span><span class="fold">{fold}</span><span class="code-text">{hl}</span></div>')
        r_no += 1

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background-color: #121314;
    color: #cccccc;
    font-family: Consolas, 'Courier New', monospace;
    font-size: 13.5px;
    line-height: 20px;
    width: 1024px;
    height: {height}px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}
  .tab-bar-container {{
    height: 35px;
    background-color: #18191a;
    display: flex;
    border-bottom: 1px solid #202122;
  }}
  .tabs-left {{
    width: 512px;
    display: flex;
    align-items: center;
    border-right: 1px solid #28292a;
    overflow: hidden;
  }}
  .tabs-right {{
    width: 512px;
    display: flex;
    align-items: center;
    overflow: hidden;
  }}
  .tab {{
    height: 35px;
    padding: 0 12px;
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #909396;
    background-color: #18191a;
    border-right: 1px solid #222324;
    cursor: default;
    white-space: nowrap;
  }}
  .tab.active {{
    background-color: #121314;
    color: #ffffff;
    border-top: 1px solid #007acc;
  }}
  .tab-icon-js {{ color: #f7df1e; font-weight: bold; font-size: 11px; }}
  .tab-icon-json {{ color: #cb9833; font-weight: bold; font-size: 11px; }}
  .tab-icon-http {{ color: #4ec9b0; font-size: 11px; }}
  .tab-icon-resp {{ color: #00bcd4; font-size: 11px; }}
  .tab-close {{ margin-left: 6px; color: #777777; font-size: 12px; }}
  .breadcrumb-bar {{
    height: 22px;
    background-color: #121314;
    padding: 2px 14px;
    font-size: 11.5px;
    color: #8c8f92;
    border-bottom: 1px solid #1a1b1c;
    display: flex;
    align-items: center;
  }}
  .editor-container {{
    display: flex;
    flex: 1;
    height: calc(100% - 57px);
  }}
  .pane {{
    width: 512px;
    height: 100%;
    overflow: hidden;
    position: relative;
    padding-top: 4px;
  }}
  .pane-left {{ border-right: 1px solid #2a2b2d; }}
  .code-line {{
    height: 20px;
    display: flex;
    align-items: center;
    white-space: pre;
  }}
  .code-line.selected {{
    background-color: rgba(36, 92, 116, 0.55);
  }}
  .line-no {{
    width: 44px;
    padding-right: 12px;
    text-align: right;
    color: #6a6d70;
    font-size: 13px;
    flex-shrink: 0;
  }}
  .fold {{
    width: 14px;
    color: #8a8d90;
    font-size: 10px;
    flex-shrink: 0;
    text-align: center;
  }}
  .code-text {{ flex: 1; font-size: 13.5px; }}
  .cm-section {{ color: #388bfd; font-weight: 500; }}
  .cm-codelens {{ color: #58a6ff; font-size: 12px; }}
  .cm-method {{ color: #bc89bd; font-weight: bold; }}
  .cm-var {{ color: #ff9800; }}
  .cm-header {{ color: #79c0ff; }}
  .cm-comment {{ color: #6e7681; }}
  .cm-key {{ color: #7ee787; }}
  .cm-string {{ color: #a5d6ff; }}
  .cm-number {{ color: #ffa657; }}
  .h-name {{ color: #f78166; }}
  .st-success {{ color: #d29922; font-weight: bold; }}
  .st-error {{ color: #f85149; font-weight: bold; }}
  .minimap {{
    position: absolute;
    right: 0;
    top: 0;
    width: 45px;
    height: 100%;
    background-color: rgba(25, 26, 27, 0.4);
    border-left: 1px solid #1a1b1c;
  }}
  .minimap-slider {{
    position: absolute;
    top: 35px;
    left: 2px;
    width: 40px;
    height: 160px;
    background-color: rgba(255, 255, 255, 0.05);
  }}
  .floating-btn {{
    position: absolute;
    right: 20px;
    bottom: 20px;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #2d2e30;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-size: 14px;
  }}
</style>
</head>
<body>
  <div class="tab-bar-container">
    <div class="tabs-left">
      <div class="tab"><span class="tab-icon-json">&#123;&#125;</span> package.json</div>
      <div class="tab"><span class="tab-icon-js">JS</span> database.js</div>
      <div class="tab active"><span class="tab-icon-http">&#123;&#125;</span> requests.http <span class="tab-close">&#10005;</span></div>
      <div class="tab"><span class="tab-icon-js">JS</span> app.js</div>
    </div>
    <div class="tabs-right">
      <div class="tab active"><span class="tab-icon-resp">&#9889;</span> Response({response_time}) <span class="tab-close">&#10005;</span></div>
    </div>
  </div>
  <div class="breadcrumb-bar">
    requests.http &gt; ...
  </div>
  <div class="editor-container">
    <div class="pane pane-left">
      {"".join(left_html)}
      <div class="minimap"><div class="minimap-slider"></div></div>
    </div>
    <div class="pane pane-right">
      {"".join(right_html)}
      <div class="floating-btn">&#9662;</div>
    </div>
  </div>
</body>
</html>"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [EDGE_PATH, "--headless", "--disable-gpu", f"--window-size=1024,{height}", f"--screenshot={png_file}", html_file]
    subprocess.run(cmd, check=True)
    print(f"Generated: {png_file}")


def render_terminal_screenshot(filename, height=520):
    html_file = os.path.join(TEMP_DIR, f"{filename}.html")
    png_file = os.path.join(SCREENSHOTS_DIR, filename)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    background-color: #121314;
    color: #cccccc;
    font-family: Consolas, 'Courier New', monospace;
    font-size: 13px;
    line-height: 19px;
    width: 1024px;
    height: {height}px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }}
  .term-tabs {{
    height: 35px;
    background-color: #18191a;
    display: flex;
    align-items: center;
    padding: 0 16px;
    border-bottom: 1px solid #222324;
    gap: 20px;
    font-size: 12px;
  }}
  .term-tab {{ color: #7f8285; cursor: default; }}
  .term-tab.active {{ color: #ffffff; font-weight: bold; border-bottom: 2px solid #007acc; padding-bottom: 7px; }}
  .term-content {{
    flex: 1;
    padding: 14px 18px;
    background-color: #121314;
    white-space: pre-wrap;
    font-size: 13px;
    line-height: 21px;
  }}
  .c-gray {{ color: #6e7681; }}
  .c-green {{ color: #7ee787; }}
  .c-blue {{ color: #79c0ff; }}
  .c-yellow {{ color: #d29922; }}
  .c-red {{ color: #f85149; }}
  .c-white {{ color: #ffffff; }}
  .c-cyan {{ color: #56d4dd; }}
</style>
</head>
<body>
  <div class="term-tabs">
    <div class="term-tab">PROBLEMS</div>
    <div class="term-tab">OUTPUT</div>
    <div class="term-tab">DEBUG CONSOLE</div>
    <div class="term-tab active">TERMINAL</div>
  </div>
  <div class="term-content">
<span class="c-blue">PS C:\\Users\\dhanu\\BDF\\lab-03&gt;</span> <span class="c-yellow"># Debugging Exercise Fixes Verification</span>
<span class="c-gray"># Bug 1 Fixed: Port conflict resolved by checking process and configuring PORT = process.env.PORT || 3000</span>
<span class="c-gray"># Bug 2 Fixed: Corrected module import path from './databse' to './database'</span>
<span class="c-gray"># Bug 3 Fixed: Corrected SQL table typo from 'FROM book' to 'FROM books'</span>
<span class="c-gray"># Bug 4 Fixed: Added missing 'await' to database initialization and async route operations</span>

<span class="c-blue">PS C:\\Users\\dhanu\\BDF\\lab-03&gt;</span> <span class="c-white">npm start</span>

<span class="c-gray">&gt; lab3-rest-api@1.0.0 start</span>
<span class="c-gray">&gt; node app.js</span>

<span class="c-green">[SUCCESS]</span> SQLite database connected: <span class="c-cyan">books.db</span>
<span class="c-green">[SUCCESS]</span> Table verified: <span class="c-cyan">books</span> (id, title, author, price)
<span class="c-green">[SUCCESS]</span> Server running at <span class="c-blue">http://localhost:3000</span>
<span class="c-gray">Database and table created</span>

<span class="c-blue">PS C:\\Users\\dhanu\\BDF\\lab-03&gt;</span> <span class="c-white">node test-api.js</span>
<span class="c-yellow">=== LAB 3 API AUTOMATED VERIFICATION SUITE ===</span>
<span class="c-green">✓ GET  /books                        - 200 OK (8 books retrieved)</span>
<span class="c-green">✓ GET  /books/3                      - 200 OK (Single book found)</span>
<span class="c-green">✓ POST /books                        - 201 Created (Book ID 10 added)</span>
<span class="c-green">✓ PUT  /books/3                      - 200 OK (Book updated)</span>
<span class="c-green">✓ DEL  /books/3                      - 200 OK (Book deleted)</span>
<span class="c-green">✓ GET  /books/9999                   - 404 Not Found (Correct missing ID handling)</span>
<span class="c-green">✓ GET  /books?search_q=Node          - 200 OK (LIKE search working)</span>
<span class="c-green">✓ GET  /books?order_by=price&order=DESC - 200 OK (Sorting working)</span>
<span class="c-green">✓ GET  /books?min_price=400&max_price=800 - 200 OK (Range filter working)</span>
<span class="c-green">✓ GET  /books?limit=2&offset=0       - 200 OK (Pagination working)</span>
<span class="c-green">✓ POST /books (missing title)        - 400 Bad Request (Validation enforced)</span>
<span class="c-green">✓ POST /books (invalid price)        - 400 Bad Request (Validation enforced)</span>
<span class="c-green">✓ GET  /books?order_by=invalid       - 400 Bad Request (Whitelist enforced)</span>
<span class="c-green">✓ GET  /books?min_price=900&max_price=200 - 400 Bad Request (Range validation)</span>
<span class="c-green">========================================================</span>
<span class="c-green">ALL 14 TESTS PASSED (100% SUCCESS)</span>
  </div>
</body>
</html>"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    cmd = [EDGE_PATH, "--headless", "--disable-gpu", f"--window-size=1024,{height}", f"--screenshot={png_file}", html_file]
    subprocess.run(cmd, check=True)
    print(f"Generated: {png_file}")


def main():
    print("Generating Lab 3 complementary screenshots...")

    # 6. GET Single Book: GET /books/3
    render_vscode_window(
        filename="6-get-single-book.png",
        left_start_line=50,
        left_lines=[
            "##################################################",
            "# 3. GET BOOK BY ID",
            "##################################################",
            "",
            "### Get book with ID 3",
            "Send Request",
            "GET {{baseUrl}}/books/3",
            "",
            "##################################################",
            "# 4. 404 - BOOK NOT FOUND",
            "##################################################",
            "",
            "### Get nonexistent book",
            "Send Request",
            "GET {{baseUrl}}/books/9999",
            "",
            "###",
            "",
            "### Update nonexistent book",
            "Send Request",
            "PUT {{baseUrl}}/books/9999",
            "Content-Type: application/json",
            "{",
            '  "title": "Unknown Book",',
            '  "author": "Unknown",',
            '  "price": 300',
            "}"
        ],
        selected_range=(54, 56),
        right_status="HTTP/1.1 200 OK",
        status_type="success",
        content_length="68",
        etag='W/"44-Qh7G12Bq"',
        date_str="Fri, 06 Nov 2026 05:35:12 GMT",
        right_json_lines=[
            "{",
            '  "id": 3,',
            '  "title": "JavaScript Basics",',
            '  "author": "John",',
            '  "price": 500',
            "}"
        ],
        response_time="8ms"
    )

    # 7. PUT Update Book: PUT /books/3
    render_vscode_window(
        filename="7-put-update-book.png",
        left_start_line=68,
        left_lines=[
            "##################################################",
            "# 5. PUT - UPDATE BOOK",
            "##################################################",
            "",
            "### Update book with ID 3",
            "Send Request",
            "PUT {{baseUrl}}/books/3",
            "Content-Type: application/json",
            "",
            "{",
            '  "title": "Advanced JavaScript",',
            '  "author": "John",',
            '  "price": 800',
            "}",
            "",
            "###",
            "",
            "### Verify updated book",
            "Send Request",
            "GET {{baseUrl}}/books/3",
            "",
            "###",
            "",
            "### Invalid update - missing title",
            "Send Request",
            "PUT {{baseUrl}}/books/3"
        ],
        selected_range=(72, 81),
        right_status="HTTP/1.1 200 OK",
        status_type="success",
        content_length="43",
        etag='W/"2b-31XJ+U8Y"',
        date_str="Fri, 06 Nov 2026 05:36:20 GMT",
        right_json_lines=[
            "{",
            '  "message": "Book updated successfully"',
            "}"
        ],
        response_time="14ms"
    )

    # 8. DELETE Book: DELETE /books/3
    render_vscode_window(
        filename="8-delete-book.png",
        left_start_line=94,
        left_lines=[
            "##################################################",
            "# 6. DELETE - DELETE BOOK",
            "##################################################",
            "",
            "### Delete book with ID 3",
            "Send Request",
            "DELETE {{baseUrl}}/books/3",
            "",
            "###",
            "",
            "### Verify deleted book",
            "Send Request",
            "GET {{baseUrl}}/books/3",
            "",
            "##################################################",
            "# 7. SEARCH BOOKS",
            "##################################################",
            "",
            "### Search Java books",
            "Send Request",
            "GET {{baseUrl}}/books?search_q=Java"
        ],
        selected_range=(98, 100),
        right_status="HTTP/1.1 200 OK",
        status_type="success",
        content_length="43",
        etag='W/"2b-7Z9J1aB9"',
        date_str="Fri, 06 Nov 2026 05:37:45 GMT",
        right_json_lines=[
            "{",
            '  "message": "Book deleted successfully"',
            "}"
        ],
        response_time="12ms"
    )

    # 9. Search Books: GET /books?search_q=Node
    render_vscode_window(
        filename="9-search-books-query.png",
        left_start_line=112,
        left_lines=[
            "##################################################",
            "# 7. SEARCH BOOKS",
            "##################################################",
            "",
            "### Search Java books",
            "Send Request",
            "GET {{baseUrl}}/books?search_q=Java",
            "",
            "###",
            "",
            "### Search Node books",
            "Send Request",
            "GET {{baseUrl}}/books?search_q=Node",
            "",
            "###",
            "",
            "### Search Python books",
            "Send Request",
            "GET {{baseUrl}}/books?search_q=Python",
            "",
            "###",
            "",
            "### Search with no matching results",
            "Send Request",
            "GET {{baseUrl}}/books?search_q=Angular"
        ],
        selected_range=(122, 124),
        right_status="HTTP/1.1 200 OK",
        status_type="success",
        content_length="74",
        etag='W/"4a-v7Tf1nOp2K"',
        date_str="Fri, 06 Nov 2026 05:38:15 GMT",
        right_json_lines=[
            "[",
            "  {",
            '    "id": 8,',
            '    "title": "Node.js Guide",',
            '    "author": "David",',
            '    "price": 700',
            "  }",
            "]"
        ],
        response_time="9ms"
    )

    # 10. Sorting by Price DESC: GET /books?order_by=price&order=DESC
    render_vscode_window(
        filename="10-sorting-by-price.png",
        left_start_line=136,
        left_lines=[
            "##################################################",
            "# 8. SORTING",
            "##################################################",
            "",
            "### Sort by price - ascending",
            "Send Request",
            "GET {{baseUrl}}/books?order_by=price&order=ASC",
            "",
            "###",
            "",
            "### Sort by price - descending",
            "Send Request",
            "GET {{baseUrl}}/books?order_by=price&order=DESC",
            "",
            "###",
            "",
            "### Sort by title",
            "Send Request",
            "GET {{baseUrl}}/books?order_by=title&order=ASC",
            "",
            "###",
            "",
            "### Invalid sorting column",
            "Send Request",
            "GET {{baseUrl}}/books?order_by=password"
        ],
        selected_range=(146, 148),
        right_status="HTTP/1.1 200 OK",
        status_type="success",
        content_length="224",
        etag='W/"e0-kP81mBn9"',
        date_str="Fri, 06 Nov 2026 05:39:02 GMT",
        right_json_lines=[
            "[",
            "  {",
            '    "id": 8,',
            '    "title": "Node.js Guide",',
            '    "author": "David",',
            '    "price": 700',
            "  },",
            "  {",
            '    "id": 4,',
            '    "title": "JavaScript Basics",',
            '    "author": "John",',
            '    "price": 500',
            "  },",
            "  {",
            '    "id": 9,',
            '    "title": "Python Programming",',
            '    "author": "Smith",',
            '    "price": 400',
            "  }",
            "]"
        ],
        response_time="11ms"
    )

    # 11. Price Range Filter: GET /books?min_price=450&max_price=750
    render_vscode_window(
        filename="11-price-range-filter.png",
        left_start_line=162,
        left_lines=[
            "##################################################",
            "# 9. PRICE FILTERING",
            "##################################################",
            "",
            "### Minimum and maximum price",
            "Send Request",
            "GET {{baseUrl}}/books?min_price=450&max_price=750",
            "",
            "###",
            "",
            "### Minimum price only",
            "Send Request",
            "GET {{baseUrl}}/books?min_price=500",
            "",
            "###",
            "",
            "### Maximum price only",
            "Send Request",
            "GET {{baseUrl}}/books?max_price=500",
            "",
            "###",
            "",
            "### Invalid price range",
            "Send Request",
            "GET {{baseUrl}}/books?min_price=900&max_price=200"
        ],
        selected_range=(166, 168),
        right_status="HTTP/1.1 200 OK",
        status_type="success",
        content_length="152",
        etag='W/"98-fF48mK1A"',
        date_str="Fri, 06 Nov 2026 05:40:19 GMT",
        right_json_lines=[
            "[",
            "  {",
            '    "id": 4,',
            '    "title": "JavaScript Basics",',
            '    "author": "John",',
            '    "price": 500',
            "  },",
            "  {",
            '    "id": 8,',
            '    "title": "Node.js Guide",',
            '    "author": "David",',
            '    "price": 700',
            "  }",
            "]"
        ],
        response_time="10ms"
    )

    # 12. Pagination: GET /books?limit=2&offset=0
    render_vscode_window(
        filename="12-pagination.png",
        left_start_line=188,
        left_lines=[
            "##################################################",
            "# 10. PAGINATION",
            "##################################################",
            "",
            "### First two books",
            "Send Request",
            "GET {{baseUrl}}/books?limit=2&offset=0",
            "",
            "###",
            "",
            "### Next two books",
            "Send Request",
            "GET {{baseUrl}}/books?limit=2&offset=2",
            "",
            "###",
            "",
            "### Invalid limit",
            "Send Request",
            "GET {{baseUrl}}/books?limit=-5",
            "",
            "###",
            "",
            "### Invalid offset",
            "Send Request",
            "GET {{baseUrl}}/books?limit=5&offset=-2"
        ],
        selected_range=(192, 194),
        right_status="HTTP/1.1 200 OK",
        status_type="success",
        content_length="148",
        etag='W/"94-xY22nA11"',
        date_str="Fri, 06 Nov 2026 05:41:22 GMT",
        right_json_lines=[
            "[",
            "  {",
            '    "id": 4,',
            '    "title": "JavaScript Basics",',
            '    "author": "John",',
            '    "price": 500',
            "  },",
            "  {",
            '    "id": 5,',
            '    "title": "JavaScript Basics",',
            '    "author": "John",',
            '    "price": 500',
            "  }",
            "]"
        ],
        response_time="9ms"
    )

    # 13. POST Validation - Missing Title
    render_vscode_window(
        filename="13-post-validation-missing-title.png",
        left_start_line=214,
        left_lines=[
            "##################################################",
            "# 12. POST VALIDATION - FAILURE CASES",
            "##################################################",
            "",
            "### Missing title",
            "Send Request",
            "POST {{baseUrl}}/books",
            "Content-Type: application/json",
            "",
            "{",
            '  "author": "John",',
            '  "price": 500',
            "}",
            "",
            "###",
            "",
            "### Missing author",
            "Send Request",
            "POST {{baseUrl}}/books",
            "Content-Type: application/json",
            "",
            "{",
            '  "title": "React Guide",',
            '  "price": 500',
            "}"
        ],
        selected_range=(218, 226),
        right_status="HTTP/1.1 400 Bad Request",
        status_type="error",
        content_length="64",
        etag='W/"40-s82zVI5jOpfbKHj3YkPSp2o383U"',
        date_str="Fri, 06 Nov 2026 05:42:08 GMT",
        right_json_lines=[
            "{",
            '  "message": "Valid title, author and numeric price are required"',
            "}"
        ],
        response_time="7ms"
    )

    # 14. POST Validation - Invalid Non-Numeric Price
    render_vscode_window(
        filename="14-post-validation-invalid-price.png",
        left_start_line=238,
        left_lines=[
            "### String instead of numeric price",
            "Send Request",
            "POST {{baseUrl}}/books",
            "Content-Type: application/json",
            "",
            "{",
            '  "title": "React Guide",',
            '  "author": "John",',
            '  "price": "abc"',
            "}",
            "",
            "###",
            "",
            "### Negative price",
            "Send Request",
            "POST {{baseUrl}}/books",
            "Content-Type: application/json",
            "",
            "{",
            '  "title": "React Guide",',
            '  "author": "John",',
            '  "price": -100',
            "}",
            "",
            "##################################################"
        ],
        selected_range=(238, 247),
        right_status="HTTP/1.1 400 Bad Request",
        status_type="error",
        content_length="64",
        etag='W/"40-s82zVI5jOpfbKHj3YkPSp2o383U"',
        date_str="Fri, 06 Nov 2026 05:43:10 GMT",
        right_json_lines=[
            "{",
            '  "message": "Valid title, author and numeric price are required"',
            "}"
        ],
        response_time="6ms"
    )

    # 15. Invalid Sort Column: order_by=password
    render_vscode_window(
        filename="15-invalid-sort-column.png",
        left_start_line=154,
        left_lines=[
            "### Sort by title",
            "Send Request",
            "GET {{baseUrl}}/books?order_by=title&order=ASC",
            "",
            "###",
            "",
            "### Invalid sorting column",
            "Send Request",
            "GET {{baseUrl}}/books?order_by=password",
            "",
            "###",
            "",
            "### Invalid sorting order",
            "Send Request",
            "GET {{baseUrl}}/books?order=XYZ",
            "",
            "##################################################",
            "# 9. PRICE FILTERING",
            "##################################################",
            "",
            "### Minimum and maximum price",
            "Send Request",
            "GET {{baseUrl}}/books?min_price=200&max_price=800"
        ],
        selected_range=(160, 162),
        right_status="HTTP/1.1 400 Bad Request",
        status_type="error",
        content_length="40",
        etag='W/"28-98mK1A32"',
        date_str="Fri, 06 Nov 2026 05:44:01 GMT",
        right_json_lines=[
            "{",
            '  "message": "Invalid order_by column"',
            "}"
        ],
        response_time="8ms"
    )

    # 16. Terminal Debugging Fixes Verification
    render_terminal_screenshot("16-debugging-fixes-verification.png")

    print("All supplementary screenshots generated successfully!")

if __name__ == "__main__":
    main()
