# 📚 Library Management System

A simple **Flask + MySQL** based Library Management System with dashboard stats, book management, and book issue/return tracking.

---

## 🚀 Features
- View **dashboard stats** (total books, issued books, books returned today)
- Add, view, and delete books
- Issue and return books
- MySQL database integration

---

## 🛠️ Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

git clone [https://github.com/your-username/library-management-system](https://github.com/pratham07816/Library_Management_System.git)
cd library-management-system 

---

2️⃣ Install dependencies
pip install flask mysql-connector-python

---

3️⃣ Configure MySQL
CREATE DATABASE library;
CREATE TABLE books (
  BOOK_NAME VARCHAR(100) NOT NULL,
  BCODE VARCHAR(20) NOT NULL PRIMARY KEY,
  TOTAL INT NOT NULL,
  SUBJECT VARCHAR(50)
);

CREATE TABLE issue (
  NAME VARCHAR(100) NOT NULL,
  REG_NO VARCHAR(20) NOT NULL,
  BCODE VARCHAR(20),
  ISSUE_DATE DATE NOT NULL,
  RETURN_DATE DATE
);


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="your_mysql_password",
        database="library"
    )

---

4️⃣ Run the application
python app.py

Visit: http://127.0.0.1:5000
