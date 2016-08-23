from flask import Flask
from pymongo import MongoClient
from flask import render_template, request, session, g, redirect, \
    url_for, abort, jsonify

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

# Routes

client = MongoClient()
db = client[app.config["DB"]]
collection = db[app.config['COLLECTION']]


def get_all_entries():
    global collection
    return collection.find()


@app.route("/")
def index():
    entries = get_all_entries()
    return render_template("index.html",entries=entries)

if __name__ == "__main__":
    app.run()
