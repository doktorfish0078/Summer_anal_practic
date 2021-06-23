from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///library.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/book/<int:id>')
def book(id):
    return render_template("home.html")


@app.route('/genres')
def genres():
    return render_template("genres.html")


if __name__ == "__main__":
    app.run(debug=True)
