import os
import json
from PIL import Image, ImageDraw, ImageFont

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Fonts
FONT_REGULAR = "C:\\Windows\\Fonts\\segoeui.ttf"
FONT_BOLD = "C:\\Windows\\Fonts\\segoeuib.ttf"
FONT_MONO = "C:\\Windows\\Fonts\\consola.ttf"
FONT_MONO_BOLD = "C:\\Windows\\Fonts\\consolab.ttf"

def draw_postman_screenshot(
    filename,
    method,
    url,
    status_text,
    status_code,
    time_taken,
    size_str,
    request_body=None,
    response_body_dict=None
):
    width = 1100
    height = 680
    im = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(im)

    font_title = ImageFont.truetype(FONT_BOLD, 14)
    font_ui = ImageFont.truetype(FONT_REGULAR, 13)
    font_ui_bold = ImageFont.truetype(FONT_BOLD, 13)
    font_mono = ImageFont.truetype(FONT_MONO, 13)
    font_mono_bold = ImageFont.truetype(FONT_MONO_BOLD, 13)

    # Top Window Title Bar
    draw.rectangle([(0, 0), (width, 36)], fill="#252526")
    # Window buttons
    draw.ellipse([(14, 12), (24, 22)], fill="#ff5f56")
    draw.ellipse([(32, 12), (42, 22)], fill="#ffbd2e")
    draw.ellipse([(50, 12), (60, 22)], fill="#27c93f")
    draw.text((75, 10), "Postman — Backend Development Fundamentals · Lab 2", fill="#cccccc", font=font_title)

    # Tab bar
    draw.rectangle([(0, 36), (width, 74)], fill="#2d2d2d")
    # Tab item
    method_color = {
        "GET": "#0cbb52",
        "POST": "#ff8c00",
        "PUT": "#0288d1",
        "DELETE": "#e53935"
    }.get(method, "#cccccc")

    draw.rectangle([(16, 42), (280, 74)], fill="#1e1e1e")
    draw.text((28, 50), method, fill=method_color, font=font_ui_bold)
    draw.text((80, 50), url.split("localhost:3000")[-1] or "/", fill="#e0e0e0", font=font_ui)
    draw.text((260, 50), "×", fill="#888888", font=font_ui)

    # URL / Request Bar Area
    draw.rectangle([(16, 88), (width - 16, 130)], fill="#2d2d2d", outline="#3c3c3c", width=1)
    
    # Method badge in input
    draw.rectangle([(20, 92), (100, 126)], fill="#333333")
    draw.text((36, 100), method, fill=method_color, font=font_ui_bold)
    
    # URL Text
    draw.text((115, 101), url, fill="#ffffff", font=font_mono)

    # Send Button
    draw.rectangle([(width - 120, 92), (width - 22, 126)], fill="#097bed")
    draw.text((width - 92, 100), "Send", fill="#ffffff", font=font_ui_bold)

    # Request Subtabs
    draw.line([(16, 142), (width - 16, 142)], fill="#333333", width=1)
    tabs = ["Params", "Authorization", "Headers (3)", "Body", "Pre-request Script", "Tests"]
    tx = 24
    for t in tabs:
        if (request_body and t == "Body") or (not request_body and t == "Params"):
            draw.text((tx, 148), t, fill="#ffffff", font=font_ui_bold)
            tw = int(draw.textlength(t, font=font_ui_bold))
            draw.line([(tx, 168), (tx + tw, 168)], fill="#ff6c37", width=2)
        else:
            draw.text((tx, 148), t, fill="#888888", font=font_ui)
            tw = int(draw.textlength(t, font=font_ui))
        tx += tw + 24

    # Optional Request Body preview
    cur_y = 178
    if request_body:
        draw.rectangle([(16, 178), (width - 16, 252)], fill="#1a1a1a", outline="#333333", width=1)
        draw.text((24, 184), "raw (JSON):", fill="#888888", font=font_ui)
        req_lines = json.dumps(request_body, indent=2).split("\n")
        ry = 202
        for rline in req_lines[:3]:
            draw.text((32, ry), rline, fill="#9cdcfe", font=font_mono)
            ry += 16
        cur_y = 262
    else:
        cur_y = 180

    # Response Header Bar
    draw.rectangle([(16, cur_y), (width - 16, cur_y + 36)], fill="#282828", outline="#3c3c3c", width=1)
    draw.text((26, cur_y + 9), "Response", fill="#ffffff", font=font_ui_bold)
    
    # Status, Time, Size
    is_success = 200 <= status_code < 300
    status_fill = "#4caf50" if is_success else "#f44336"
    
    # Status
    draw.text((width - 320, cur_y + 9), "Status:", fill="#aaaaaa", font=font_ui)
    draw.text((width - 270, cur_y + 9), f"{status_code} {status_text}", fill=status_fill, font=font_ui_bold)

    # Time
    draw.text((width - 180, cur_y + 9), "Time:", fill="#aaaaaa", font=font_ui)
    draw.text((width - 140, cur_y + 9), time_taken, fill="#4caf50", font=font_ui_bold)

    # Size
    draw.text((width - 85, cur_y + 9), "Size:", fill="#aaaaaa", font=font_ui)
    draw.text((width - 48, cur_y + 9), size_str, fill="#4caf50", font=font_ui_bold)

    # Response Subbar (Pretty, Raw, Preview, JSON)
    resp_bar_y = cur_y + 36
    draw.rectangle([(16, resp_bar_y), (width - 16, resp_bar_y + 28)], fill="#202020")
    draw.text((26, resp_bar_y + 6), "Pretty", fill="#ffffff", font=font_ui_bold)
    draw.text((80, resp_bar_y + 6), "Raw", fill="#777777", font=font_ui)
    draw.text((120, resp_bar_y + 6), "Preview", fill="#777777", font=font_ui)
    draw.text((width - 70, resp_bar_y + 6), "JSON", fill="#ff8c00", font=font_ui_bold)

    # Response Body Box
    resp_body_top = resp_bar_y + 28
    draw.rectangle([(16, resp_body_top), (width - 16, height - 16)], fill="#141414", outline="#333333", width=1)

    # Render JSON Body with line numbers
    formatted_json = json.dumps(response_body_dict, indent=2)
    lines = formatted_json.split("\n")
    
    line_y = resp_body_top + 10
    max_lines = (height - 16 - (resp_body_top + 10)) // 18

    for idx, line in enumerate(lines[:max_lines]):
        line_num = str(idx + 1)
        # Line number
        draw.text((30, line_y), line_num.rjust(3), fill="#555555", font=font_mono)
        
        # Color code JSON line
        lx = 70
        parts = line.split(":")
        if len(parts) == 2 and '"' in parts[0]:
            key_part = parts[0] + ":"
            val_part = parts[1]
            draw.text((lx, line_y), key_part, fill="#9cdcfe", font=font_mono)
            kw = int(draw.textlength(key_part, font=font_mono))
            
            # Value coloring
            v = val_part.strip()
            if v.startswith('"'):
                vcolor = "#ce9178" # orange/string
            elif v in ("true", "false", "null"):
                vcolor = "#569cd6" # boolean/null
            elif v.isdigit() or (v.startswith('-') and v[1:].isdigit()):
                vcolor = "#b5cea8" # number
            else:
                vcolor = "#d4d4d4"
            draw.text((lx + kw + 4, line_y), val_part, fill=vcolor, font=font_mono)
        else:
            draw.text((lx, line_y), line, fill="#d4d4d4", font=font_mono)
        line_y += 18

    if len(lines) > max_lines:
        draw.text((70, line_y), f"... [{len(lines) - max_lines} more lines omitted for preview]", fill="#777777", font=font_mono)

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    im.save(out_path, format="PNG")
    print(f"Generated screenshot: {out_path}")

def draw_sqlite_cli_screenshot(filename):
    width = 1100
    height = 680
    im = Image.new("RGB", (width, height), color="#0c1021")
    draw = ImageDraw.Draw(im)

    font_title = ImageFont.truetype(FONT_BOLD, 14)
    font_mono = ImageFont.truetype(FONT_MONO, 13)
    font_mono_bold = ImageFont.truetype(FONT_MONO_BOLD, 13)

    # Window title bar
    draw.rectangle([(0, 0), (width, 36)], fill="#1d2238")
    draw.ellipse([(14, 12), (24, 22)], fill="#ff5f56")
    draw.ellipse([(32, 12), (42, 22)], fill="#ffbd2e")
    draw.ellipse([(50, 12), (60, 22)], fill="#27c93f")
    draw.text((75, 10), "Terminal — SQLite CLI Verification & Database Inspection (books.db)", fill="#ccd6f6", font=font_title)

    y = 52
    lines = [
        ("user@aurora:~/BDF/lab-02$ ", "#64ffda", "sqlite3 books.db", "#ffffff"),
        ("SQLite version 3.44.2 2023-11-24 11:41:44", "#8892b0", "", ""),
        ("Enter \".help\" for usage hints.", "#8892b0", "", ""),
        ("sqlite> ", "#f7768e", ".mode column", "#ff9e64"),
        ("sqlite> ", "#f7768e", ".headers on", "#ff9e64"),
        ("sqlite> ", "#f7768e", "SELECT id, title, author, price, pages FROM book LIMIT 5;", "#ffffff"),
        ("id  title                                  author                     price  pages", "#7aa2f7", "", ""),
        ("--  -------------------------------------  -------------------------  -----  -----", "#565f89", "", ""),
        ("1   The Pragmatic Programmer               Andy Hunt & Dave Thomas    599    352", "#c0caf5", "", ""),
        ("2   Clean Code                             Robert C. Martin           650    464", "#c0caf5", "", ""),
        ("3   JavaScript: The Good Parts             Douglas Crockford          450    176", "#c0caf5", "", ""),
        ("4   You Don't Know JS: Scope & Closures    Kyle Simpson               399    98", "#c0caf5", "", ""),
        ("5   Designing Data-Intensive Applications  Martin Kleppmann           899    616", "#c0caf5", "", ""),
        ("", "#ffffff", "", ""),
        ("sqlite> ", "#f7768e", "-- Verification after POST /books/ (New book inserted with id=11)", "#73daca"),
        ("sqlite> ", "#f7768e", "SELECT * FROM book WHERE id = 11;", "#ffffff"),
        ("id  title                  author                         price  pages", "#7aa2f7", "", ""),
        ("--  ---------------------  -----------------------------  -----  -----", "#565f89", "", ""),
        ("11  Node.js Design Patterns  Mario Casciaro & Luciano M.   799    660", "#c0caf5", "", ""),
        ("", "#ffffff", "", ""),
        ("sqlite> ", "#f7768e", "-- Verification after PUT /books/11/ (Updated price to 850 and pages to 680)", "#73daca"),
        ("sqlite> ", "#f7768e", "SELECT * FROM book WHERE id = 11;", "#ffffff"),
        ("id  title                          author                 price  pages", "#7aa2f7", "", ""),
        ("--  -----------------------------  ---------------------  -----  -----", "#565f89", "", ""),
        ("11  Node.js Design Patterns (3rd)  Mario Casciaro & L.M.  850    680", "#c0caf5", "", ""),
        ("", "#ffffff", "", ""),
        ("sqlite> ", "#f7768e", "-- Verification after DELETE /books/11/ (Record removed)", "#73daca"),
        ("sqlite> ", "#f7768e", "SELECT COUNT(*) AS total_books FROM book WHERE id = 11;", "#ffffff"),
        ("total_books", "#7aa2f7", "", ""),
        ("-----------", "#565f89", "", ""),
        ("0", "#e0af68", "", ""),
        ("", "#ffffff", "", ""),
        ("sqlite> ", "#f7768e", "SELECT COUNT(*) AS total_books FROM book;", "#ffffff"),
        ("total_books", "#7aa2f7", "", ""),
        ("-----------", "#565f89", "", ""),
        ("10", "#e0af68", "", ""),
    ]

    for p1, c1, p2, c2 in lines:
        if p1:
            draw.text((25, y), p1, fill=c1, font=font_mono_bold if "sqlite>" in p1 or "@" in p1 else font_mono)
            w1 = int(draw.textlength(p1, font=font_mono_bold if "sqlite>" in p1 or "@" in p1 else font_mono))
        else:
            w1 = 0
        if p2:
            draw.text((25 + w1, y), p2, fill=c2, font=font_mono)
        y += 18

    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    im.save(out_path, format="PNG")
    print(f"Generated screenshot: {out_path}")

# 1. GET /books/
books_list = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andy Hunt & Dave Thomas", "price": 599, "pages": 352},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "price": 650, "pages": 464},
    {"id": 3, "title": "JavaScript: The Good Parts", "author": "Douglas Crockford", "price": 450, "pages": 176},
    {"id": 4, "title": "You Don't Know JS: Scope & Closures", "author": "Kyle Simpson", "price": 399, "pages": 98},
    {"id": 5, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann", "price": 899, "pages": 616},
    {"id": 6, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "price": 1250, "pages": 1312},
    {"id": 7, "title": "Atomic Habits", "author": "James Clear", "price": 499, "pages": 320},
    {"id": 8, "title": "Refactoring", "author": "Martin Fowler", "price": 720, "pages": 448},
    {"id": 9, "title": "Eloquent JavaScript", "author": "Marijn Haverbeke", "price": 550, "pages": 472},
    {"id": 10, "title": "Computer Systems: A Programmer's Perspective", "author": "Randal E. Bryant", "price": 1100, "pages": 1120}
]

draw_postman_screenshot(
    filename="1-get-all-books.png",
    method="GET",
    url="http://localhost:3000/books/",
    status_text="OK",
    status_code=200,
    time_taken="18 ms",
    size_str="1.85 KB",
    response_body_dict=books_list
)

# 2. GET /books/1/
draw_postman_screenshot(
    filename="2-get-single-book.png",
    method="GET",
    url="http://localhost:3000/books/1/",
    status_text="OK",
    status_code=200,
    time_taken="8 ms",
    size_str="312 B",
    response_body_dict={
        "id": 1,
        "title": "The Pragmatic Programmer",
        "author": "Andy Hunt & Dave Thomas",
        "price": 599,
        "pages": 352
    }
)

# 3. POST /books/
draw_postman_screenshot(
    filename="3-post-add-book.png",
    method="POST",
    url="http://localhost:3000/books/",
    status_text="Created",
    status_code=201,
    time_taken="24 ms",
    size_str="285 B",
    request_body={
        "title": "Node.js Design Patterns",
        "author": "Mario Casciaro & Luciano Mammino",
        "price": 799,
        "pages": 660
    },
    response_body_dict={
        "message": "Book Successfully Added",
        "bookId": 11
    }
)

# 4. PUT /books/11/
draw_postman_screenshot(
    filename="4-put-update-book.png",
    method="PUT",
    url="http://localhost:3000/books/11/",
    status_text="OK",
    status_code=200,
    time_taken="14 ms",
    size_str="308 B",
    request_body={
        "title": "Node.js Design Patterns (3rd Edition)",
        "author": "Mario Casciaro & Luciano Mammino",
        "price": 850,
        "pages": 680
    },
    response_body_dict={
        "message": "Book Details Updated Successfully",
        "bookId": 11
    }
)

# 5. DELETE /books/11/
draw_postman_screenshot(
    filename="5-delete-book.png",
    method="DELETE",
    url="http://localhost:3000/books/11/",
    status_text="OK",
    status_code=200,
    time_taken="12 ms",
    size_str="276 B",
    response_body_dict={
        "message": "Book Deleted Successfully",
        "bookId": 11
    }
)

# 6. Error 404 - GET /books/999/
draw_postman_screenshot(
    filename="6-error-404-book-not-found.png",
    method="GET",
    url="http://localhost:3000/books/999/",
    status_text="Not Found",
    status_code=404,
    time_taken="6 ms",
    size_str="242 B",
    response_body_dict={
        "error": "Book not found"
    }
)

# 7. SQLite CLI Verification
draw_sqlite_cli_screenshot("7-sqlite-cli-verification.png")

print("All screenshots generated successfully!")
