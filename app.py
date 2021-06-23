from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///library.db'
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    genre = db.Column(db.String(255), nullable=False)
    annotation = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    pageCount = db.Column(db.Integer, nullable=False)
    roomNum = db.Column(db.Integer, nullable=False)
    publishingHouse = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Book %r>' % self.id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


class UserToBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    bookId = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<UserToBook>'



@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/book/<int:id>')
def book(id):
    return render_template("show_description_book.html")


@app.route('/genres')
def genres():
    return render_template("genres.html")


if __name__ == "__main__":
    app.run(debug=True)
