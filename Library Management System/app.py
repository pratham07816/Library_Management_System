from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="# Your MySQL password", 
        database="library"
    )

@app.route("/")
def home():
    return render_template("index.html")

# API to get dashboard stats
@app.route("/api/stats")
def get_stats():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM books")
    total_books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issue WHERE RETURN_DATE IS NULL")
    issued_books = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM issue WHERE RETURN_DATE = CURDATE()")
    returned_today = cur.fetchone()[0]

    return jsonify({
        "total_books": total_books,
        "issued_books": issued_books,
        "returned_today": returned_today
    })

# API to view all books
@app.route("/api/books")
def get_books():
    con = connect_db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT * FROM books")
    return jsonify(cur.fetchall())

# API to add book
@app.route("/api/add", methods=["POST"])
def add_book():
    data = request.json
    con = connect_db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO books VALUES (%s, %s, %s, %s)",
        (data["book_name"], data["bcode"], int(data["total"]), data["subject"])
    )
    con.commit()
    return jsonify({"status": "success"})

# API to issue book
@app.route("/api/issue", methods=["POST"])
def issue_book():
    data = request.json
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT TOTAL FROM books WHERE BCODE = %s", (data["bcode"],))
    result = cur.fetchone()
    if result and result[0] > 0:
        cur.execute(
            "INSERT INTO issue (NAME, REG_NO, BCODE, ISSUE_DATE, RETURN_DATE) VALUES (%s, %s, %s, %s, NULL)",
            (data["student_name"], data["reg_no"], data["bcode"], datetime.now().strftime("%Y-%m-%d"))
        )
        cur.execute(
            "UPDATE books SET TOTAL = TOTAL - 1 WHERE BCODE = %s",
            (data["bcode"],)
        )
        con.commit()
        return jsonify({"status": "success"})
    return jsonify({"status": "failed", "message": "Book not available"})

@app.route("/api/return", methods=["POST"])
def return_book():
    data = request.json
    con = connect_db()
    cur = con.cursor()
    cur.execute(
        "UPDATE books SET TOTAL = TOTAL + 1 WHERE BCODE = %s",
        (data["bcode"],)
    )
    cur.execute(
        "UPDATE issue SET RETURN_DATE = %s WHERE BCODE = %s AND RETURN_DATE IS NULL",
        (datetime.now().strftime("%Y-%m-%d"), data["bcode"])
    )
    con.commit()
    return jsonify({"status": "success"})


# API to delete book
@app.route("/api/delete", methods=["POST"])
def delete_book():
    data = request.json
    con = connect_db()
    cur = con.cursor()
    cur.execute("DELETE FROM books WHERE BCODE = %s", (data["bcode"],))
    con.commit()
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=True)

