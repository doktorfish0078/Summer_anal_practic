from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///library.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
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
        return '<UserToBook %r>' % self.id

# db.session.query(Book).delete()
# db.session.commit()

# matvey's gayshit block (не трогай этот блок и он не будет вонять)
# bookses = []
# book = Book(name="Твоё слово(СИ)", author="Лисканова Яна", genre="gaysex", annotation="Пиздатая книга", year=211, pageCount=555, roomNum=5,  publishingHouse="gayFbric")
# bookses.append(book)
# book = Book(name="Твоё слово(СИ)", author="Лисканава Яна", genre="gaysex", annotation="Так - хуета", year=211, pageCount=555, roomNum=5,  publishingHouse="gayFbric")
# bookses.append(book)
# book = Book(name="Ка к насрать себе врот", author="Лисканова Она", genre="gaysex",
#             annotation=" Я большой динозавер в маленькой пещере она такая узкая и ни аднаго наскального рисунка дадададад ооооооо похоже это не пещера, а пещер",
#             year=211, pageCount=555, roomNum=5,  publishingHouse="gayFbric")
# bookses.append(book)
# try:
#     for book in bookses:
#         db.session.add(book)
#         db.session.commit()
# except Exception as ex:
#     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
#     message = template.format(type(ex).__name__, ex.args)
#     print("подмойся")
#     print(message)


@app.route('/')
@app.route('/home')
def home():
    books = Book.query.order_by(Book.id).all()
    return render_template("home.html", books=books)


@app.route('/book/<int:id>')
def book(id):
    book_info = Book.query.filter(Book.id == str(id)).first()
    return render_template("show_description_book.html", book=book_info)


@app.route('/genres')
def genres():
    return render_template("genres.html")


if __name__ == "__main__":
    app.run(debug=True)


