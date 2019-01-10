from flask import Flask, g, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)

app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "a random text string"


def connect_db():
    sql = sqlite3.connect("data.db")
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    if not hasattr(g, "sqlite3"):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "sqlite_db"):
        g.sqlite_db.close()


@app.route("/")
def index():
    return "yup"


@app.route("/home", methods=["POST", "GET"])
def home():
    db = get_db()
    cur = db.execute("select id, name, location from users")
    results = cur.fetchall()

    return render_template("home.html", results=results)


@app.route("/viewresults")
def viewresults():
    db = get_db()
    cur = db.execute("select id, name, location from users")
    results = cur.fetchall()
    return "<h1>The ID is {}. The name is {}. The location is {}.</h1>".format(
        results[2]["id"], results[2]["name"], results[2]["location"]
    )


@app.route("/theform", methods=["GET", "POST"])
def theform():
    if request.method == "GET":
        return render_template("form.html")
    else:
        name = request.form["name"]
        location = request.form["location"]

        db = get_db()
        db.execute("insert into users (name, location) values (?, ?)", [name, location])
        db.commit()
        return redirect(url_for("theform"))


if __name__ == "__main__":
    app.run()
