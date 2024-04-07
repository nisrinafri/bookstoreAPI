import os
from datetime import datetime
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify


create_books_table = "CREATE TABLE IF NOT EXISTS books (book_id SERIAL PRIMARY KEY, title VARCHAR(50) NOT NULL, author VARCHAR(50) NOT NULL, genre VARCHAR(50) NOT NULL, publisher VARCHAR(50), publish_year INT);"
create_users_table = "CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, user_name VARCHAR(50) NOT NULL, user_age INT NOT NULL, user_gender VARCHAR(10) NOT NULL);"
create_authors_table = "CREATE TABLE IF NOT EXISTS authors (author_id SERIAL PRIMARY KEY, author_name VARCHAR(50) NOT NULL, author_age INT NOT NULL, author_gender VARCHAR(10) NOT NULL);"
create_borrowings_table = "CREATE TABLE IF NOT EXISTS borrowings (borrowing_id SERIAL PRIMARY KEY, user_id INT NOT NULL, book_id INT NOT NULL, borrowing_date DATE NOT NULL, return_date DATE, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (book_id) REFERENCES books(book_id));"

insert_books = "INSERT INTO books (title, author, genre, publisher, publish_year) VALUES (%s, %s, %s, %s, %s) RETURNING book_id;"
insert_users = "INSERT INTO users (user_name, user_age, user_gender) VALUES (%s, %s, %s ) RETURNING user_id;"
insert_authors = "INSERT INTO authors (author_name, author_age, author_gender) VALUES (%s, %s, %s) RETURNING author_id;"
insert_borrowings = "INSERT INTO borrowings (user_id, book_id, borrowing_date, return_date) VALUES (%s, %s, %s, %s) RETURNING borrowing_id;"

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url)
ACCESS_TOKEN = "15ed874984a4a6de95409919e106b80b"


# POST method
@app.post("/api/books")
def create_books():
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    data = request.get_json()
    title = data["title"]
    author = data["author"]
    genre = data["genre"]
    publisher = data["publisher"]
    publish_year = data["publish_year"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(create_books_table)
            cursor.execute(
                insert_books, (title, author, genre, publisher, publish_year)
            )
            book_id = cursor.fetchone()[0]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = {
        "book_id": book_id,
        "title": title,
        "author": author,
        "genre": genre,
        "publisher": publisher,
        "publish_year": publish_year,
        "message": f"Book '{title}' by {author} ({genre}) has been added.",
        "time": f"Accessed : {now}",
        "Status Code": 201,
        "Status": "Success",
    }
    return jsonify(response), 201


@app.post("/api/authors")
def create_authors():
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    data = request.get_json()
    author_name = data["author_name"]
    author_age = data["author_age"]
    author_gender = data["author_gender"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(create_authors_table)
            cursor.execute(insert_authors, (author_name, author_age, author_gender))
            author_id = cursor.fetchone()[0]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = {
        "author_id": author_id,
        "author_name": author_name,
        "author_age": author_age,
        "author_gender": author_gender,
        "message": f"{author_name} ({author_age} years old, {author_gender}) is successfully added.",
        "time": f"Accessed : {now}",
    }
    return jsonify(response), 201


@app.post("/api/users")
def create_users():
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    data = request.get_json()
    user_name = data["user_name"]
    user_age = data["user_age"]
    user_gender = data["user_gender"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(create_users_table)
            cursor.execute(insert_users, (user_name, user_age, user_gender))
            user_id = cursor.fetchone()[0]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = {
        "user_id": user_id,
        "user_name": user_name,
        "user_age": user_age,
        "user_gender": user_gender,
        "message": f"{user_name} ({user_age} years old, {user_gender}) is successfully added.",
        "time": f"Accessed : {now}",
    }
    return jsonify(response), 201


@app.post("/api/borrowings")
def create_borrowings():
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    data = request.get_json()
    user_id = data["user_id"]
    book_id = data["book_id"]
    borrowing_date = data["borrowing_date"]
    return_date = data["return_date"]
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(create_borrowings_table)
            cursor.execute(
                insert_borrowings, (user_id, book_id, borrowing_date, return_date)
            )
            borrowing_id = cursor.fetchone()[0]
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = {
        "borrowing_id": borrowing_id,
        "user_id": user_id,
        "book_id": book_id,
        "borrowing_date": borrowing_date,
        "return_date": return_date,
        "message": (
            f"User with ID {user_id} has borrowed a book with ID {book_id} on {borrowing_date}. "
            f"Please ensure its return by {return_date}. Thank you!"
        ),
        "time": f"Accessed : {now}",
        "Status Code": 201,
        "Status": "Success",
    }
    return jsonify(response), 201


# GET methods
@app.get("/books")
def get_books():
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    # to get all from books table
    books = "SELECT * FROM books"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(books)
            book = cursor.fetchall()
    response = {"books": book, "time": f"Accessed : {now}"}
    return jsonify(response), 200


@app.get("/users")
def get_users():
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    # to get all from users table
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = {"users": users, "time": f"Accessed : {now}"}
    return jsonify(response), 200


@app.get("/authors")
def get_authors():
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    # to get all from authors table
    authors = "SELECT * FROM authors"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(authors)
            author = cursor.fetchall()
    response = {"authors": author, "time": f"Accessed : {now}"}
    return jsonify(response)


@app.get("/borrowings")
def get_borrowings_by_user_id():
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    # to get borrowing info from specific user_id
    user_id = request.args.get("user_id")

    # to get all from borrowings table
    query = """
        SELECT borrowings.borrowing_id, users.user_name, books.title, borrowings.borrowing_date, borrowings.return_date
        FROM borrowings
        JOIN users ON borrowings.user_id = users.user_id
        JOIN books ON borrowings.book_id = books.book_id
    """

    if user_id:
        query += f" WHERE borrowings.user_id = {user_id};"
    else:
        query += ";"  # close query if there's no user_id

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            borrowings = cursor.fetchall()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response = []
    for borrowing in borrowings:
        borrowing_id, user_name, book_title, borrowing_date, return_date = borrowing
        borrowing_info = {
            "borrowing_id": borrowing_id,
            "user_name": user_name,
            "book_title": book_title,
            "borrowing_date": borrowing_date.strftime("%Y-%m-%d"),
            "return_date": (return_date.strftime("%Y-%m-%d") if return_date else None),
            "time": now,
        }
        response.append(borrowing_info)

    return jsonify(response)


# DELETE methods - if a user already return the book
@app.route("/api/borrowings/<int:user_id>/<int:borrowing_id>", methods=["DELETE"])
def delete_borrowing(user_id, borrowing_id):
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )
    query = """
        DELETE FROM borrowings
        WHERE user_id = %s AND borrowing_id = %s;
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (user_id, borrowing_id))
            deleted_rows = cursor.rowcount
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if deleted_rows == 0:
        return (
            jsonify(
                {
                    "message": "No borrowing record found for the specified user ID and borrowing ID.",
                    "time": f"Accessed : {now}",
                }
            ),
            404,
        )
    else:
        return (
            jsonify(
                {
                    f"message": "Borrowing record successfully deleted.",
                    "time": f"Accessed : {now}",
                }
            ),
            200,
        )


# PUT methods
@app.put("/api/borrowings/<int:user_id>/<int:borrowing_id>")
def extend_borrowing(user_id, borrowing_id):
    token = request.headers.get("X-Access-Token")
    if token != ACCESS_TOKEN:
        return (
            jsonify(
                {
                    "message": "Unauthorized: Access is denied due to invalid credentials."
                }
            ),
            401,
        )

    data = request.get_json()
    new_return_date = data["new_return_date"]

    update_query = """
        UPDATE borrowings
        SET return_date = %s
        WHERE user_id = %s AND borrowing_id = %s
        RETURNING borrowing_id, user_id, book_id, borrowing_date, return_date;
    """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(update_query, (new_return_date, user_id, borrowing_id))
            updated_borrowing = cursor.fetchone()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not updated_borrowing:
        return (
            jsonify(
                {
                    "message": "No borrowing record found for the specified user ID and borrowing ID."
                }
            ),
            404,
        )
    else:
        borrowing_id, user_id, book_id, borrowing_date, return_date = updated_borrowing
        # Format respons JSON
        response = {
            "borrowing_id": borrowing_id,
            "user_id": user_id,
            "book_id": book_id,
            "borrowing_date": borrowing_date.strftime("%Y-%m-%d"),
            "return_date": return_date.strftime("%Y-%m-%d"),
            "message": f"Return date successfully extended until {new_return_date}.",
            "time": f"Accessed : {now}",
        }
        return jsonify(response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50, debug=True)
