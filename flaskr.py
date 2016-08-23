from flask import Flask
from pymongo import MongoClient
from flask import render_template, request, session, g, redirect, \
    url_for, abort, jsonify, flash

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")


client = MongoClient()
db = client[app.config["DB"]]
collection = db[app.config['COLLECTION']]


def get_all_entries():
    global collection
    return collection.find()

# Routes


@app.route("/")
def index():
    entries = get_all_entries()
    return render_template("index.html", entries=entries)


@app.route("/login", methods=["POST", "GET"])
def login():
    """ user login authentication/sessionmanagement/ """
    error = None
    if request.method == "POST":
        if request.form['username'] != app.config['USERNAME']:
            error = "Invalid Username"
        elif request.form['password'] != app.config['PASSWORD']:
            error = "Invalid Password"
        else:
            session.logged_in = True
            flash("You Were Logged In !")
            return redirect(url_for('index'))
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """ User Logout """
    session.pop('logged_in', None)
    flash("You Were Logged Out")
    return redirect(url_for('index'))


@app.route("/add")
def add_entry():
    """ Add new Entry in database """
    if not session.get('logged_in'):
        abort(401)
    collection.insert_one(
        {"title": request.form['title'], "text": request.form['text']})
    flash("Entry Was Succesfully Posted")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
