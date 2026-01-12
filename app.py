from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "secret_key"

USERS_FILE = "users.json"
BOOKS_FILE = "books.json"
ISSUES_FILE = "issues.json"

# ---------- Helper Functions ----------
def load_json(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def find_user(email):
    users = load_json(USERS_FILE)
    return next((u for u in users if u["email"] == email), None)

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template("index.html")

# ---------- REGISTER ----------
@app.route('/register', methods=['POST'])
def register():
    users = load_json(USERS_FILE)
    email = request.form['email']

    if find_user(email):
        flash("User already exists!")
        return redirect(url_for('home'))

    user = {
    "first_name": request.form['fName'],
    "last_name": request.form['lName'],
    "email": email,
    "password": generate_password_hash(request.form['password']),
    "role": request.form.get('role', 'student'),
    "active": True
}
    users.append(user)
    save_json(USERS_FILE, users)
    flash("Registered successfully!")
    return redirect(url_for('home'))


# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = find_user(email)

    if user and check_password_hash(user['password'], password):
        session['user'] = email

        role = user.get('role', 'student')
        session['role'] = role

        if role == "librarian":
            return redirect(url_for('librarian_dashboard'))
        else:
            return redirect(url_for('student_dashboard'))

    flash("Invalid email or password!")
    return redirect(url_for('home'))




# ---------- LOGOUT ----------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ---------- LIBRARIAN DASHBOARD ----------
@app.route('/librarian/dashboard')
def librarian_dashboard():
    if 'user' not in session or session.get('role') != 'librarian':
        return redirect(url_for('home'))

    books = load_json(BOOKS_FILE)
    users = load_json(USERS_FILE)
    issues = load_json(ISSUES_FILE)

    return render_template(
        "dashboard.html",
        books=books,
        users=users,
        issues=issues
    )

# ---------- STUDENT DASHBOARD ----------
@app.route('/student/dashboard')
def student_dashboard():
    if 'user' not in session or session.get('role') != 'student':
        return redirect(url_for('home'))

    books = load_json(BOOKS_FILE)
    return render_template("student.html", books=books)

# ---------- BOOK MANAGEMENT (LIBRARIAN ONLY) ----------
@app.route('/add_book', methods=['POST'])
def add_book():
    if session.get('role') != 'librarian':
        return redirect(url_for('home'))

    books = load_json(BOOKS_FILE)
    book = {
        "id": len(books) + 1,
        "title": request.form['title'],
        "author": request.form['author'],
        "category": request.form['category'],
        "quantity": int(request.form['quantity']),
        "issued": 0
    }
    books.append(book)
    save_json(BOOKS_FILE, books)
    flash("Book added!")
    return redirect(url_for('librarian_dashboard'))

# ---------- ISSUE BOOK ----------
@app.route('/issue_book', methods=['POST'])
def issue_book():
    if session.get('role') != 'librarian':
        return redirect(url_for('home'))

    user_email = request.form['user_email']
    book_id = int(request.form['book_id'])

    books = load_json(BOOKS_FILE)
    issues = load_json(ISSUES_FILE)

    book = next((b for b in books if b["id"] == book_id), None)

    if not book or book["quantity"] - book["issued"] <= 0:
        flash("Book not available!")
        return redirect(url_for('librarian_dashboard'))

    issue = {
        "id": len(issues) + 1,
        "user_email": user_email,
        "book_id": book_id,
        "issue_date": datetime.now().strftime("%Y-%m-%d"),
        "return_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "returned": False,
        "fine": 0
    }

    issues.append(issue)
    book["issued"] += 1

    save_json(ISSUES_FILE, issues)
    save_json(BOOKS_FILE, books)

    flash("Book issued!")
    return redirect(url_for('librarian_dashboard'))

# ---------- RETURN BOOK ----------
@app.route('/return_book/<int:issue_id>')
def return_book(issue_id):
    if session.get('role') != 'librarian':
        return redirect(url_for('home'))

    issues = load_json(ISSUES_FILE)
    books = load_json(BOOKS_FILE)

    for issue in issues:
        if issue["id"] == issue_id and not issue["returned"]:
            due = datetime.strptime(issue["return_date"], "%Y-%m-%d")
            late_days = (datetime.now() - due).days
            issue["fine"] = max(0, late_days * 5)
            issue["returned"] = True

            book = next(b for b in books if b["id"] == issue["book_id"])
            book["issued"] -= 1
            break

    save_json(ISSUES_FILE, issues)
    save_json(BOOKS_FILE, books)
    flash("Book returned!")
    return redirect(url_for('librarian_dashboard'))

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True) 