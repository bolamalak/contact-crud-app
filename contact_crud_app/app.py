from flask import Flask, render_template, request, redirect
import pymysql
app = Flask(__name__)
def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="Bola@2040",
        database="contact_crud_app"
    )
    return connection
@app.route("/")


@app.route("/")
def home():
    search = request.args.get("search", "")
    page = request.args.get("page", 1, type=int)

    per_page = 5
    offset = (page - 1) * per_page

    connection = get_db_connection()
    cursor = connection.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM contacts WHERE name LIKE %s LIMIT %s OFFSET %s",
            ("%" + search + "%", per_page, offset)
        )
    else:
        cursor.execute(
            "SELECT * FROM contacts LIMIT %s OFFSET %s",
            (per_page, offset)
        )

    contacts = cursor.fetchall()

    if search:
        cursor.execute(
            "SELECT COUNT(*) FROM contacts WHERE name LIKE %s",
            ("%" + search + "%",)
        )
    else:
        cursor.execute("SELECT COUNT(*) FROM contacts")

    total_contacts = cursor.fetchone()[0]
    total_pages = (total_contacts + per_page - 1) // per_page

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        contacts=contacts,
        page=page,
        total_pages=total_pages,
        search=search
    )



@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)",
            (name, phone, email)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return redirect("/")

    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]

        cursor.execute(
            "UPDATE contacts SET name=%s, phone=%s, email=%s WHERE id=%s",
            (name, phone, email, id)
        )

        connection.commit()
        cursor.close()
        connection.close()

        return redirect("/")

    cursor.execute("SELECT * FROM contacts WHERE id=%s", (id,))
    contact = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit.html", contact=contact)

@app.route("/delete/<int:id>")
def delete_contact(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM contacts WHERE id=%s", (id,))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)