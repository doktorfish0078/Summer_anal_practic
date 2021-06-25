from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///library.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

thisUser = None


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


# del books
# db.session.query(Book).delete()
# db.session.commit()

# del users
# db.session.query(User).delete()
# db.session.commit()

# del u2books
# db.session.query(UserToBook).delete()
# db.session.commit()


# look into db
# for i in UserToBook.query.all():
#     print(i.id, i.bookId, i.userId)
#
# for i in User.query.all():
#     print(i.id, i.name, i.mail, i.password)
#
# for i in Book.query.all():
#     print(i.id, i.name) прописал не все поля, мне лень



@app.context_processor
def utility_processor():
    def current_user():
        global thisUser
        return thisUser

    return dict(current_user=current_user)


@app.route('/')
@app.route('/home')
def home():
    books = Book.query.order_by(Book.id).all()
    return render_template("home.html", books=books[0:7])


def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n, m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)  # Keep current and previous row, not entire matrix
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


@app.route('/book/<int:id>', methods=['POST', 'GET'])
def book(id):
    if request.method == "POST":
        if thisUser is None:
            return redirect("/book/"+str(id))

        utb = UserToBook.query.filter(UserToBook.userId == thisUser.id).all()

        bookIds = []
        for userBook in utb:
            bookIds.append(userBook.bookId)
        if id in bookIds:
            return redirect("/book/"+str(id))

        userToBook = UserToBook(userId=int(thisUser.id), bookId=int(id))
        try:
            db.session.add(userToBook)
            db.session.commit()
            return redirect("/book/"+str(id))
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return "ERROR (%r)" % message
    else:
        book_info = Book.query.filter(Book.id == str(id)).first()
        books = Book.query.filter(Book.genre == book_info.genre, Book.id != book_info.id).all()
        books = sorted(books, key=lambda bk: distance(book_info.name, bk.name))
        if thisUser is not None:
            utob = UserToBook.query.filter(UserToBook.userId == thisUser.id).all()
            bookIds = []
            for userBook in utob:
                bookIds.append(userBook.bookId)
            for currBook in books:
                if currBook.id in bookIds:
                    books.remove(currBook)
        return render_template("show_description_book.html", book=book_info, books=books)


@app.route('/genres')
def genres():
    return render_template("genres.html")


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == "POST":

        mail = request.form['mail']
        password = request.form['pass']

        if (User.query.filter(User.mail == mail).first()) is not None:
            return render_template('registration.html', err=True)

        user = User(name=mail.split('@')[0], mail=mail, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            global thisUser
            thisUser = user
            return redirect("/home")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return "ERROR (%r)" % message
    else:
        return render_template('registration.html')


@app.route('/authorization', methods=['POST', 'GET'])
def authorization():
    if request.method == "POST":

        mail = request.form['mail']
        password = request.form['pass']

        currentUser = User.query.filter(User.mail == mail).first()

        if (currentUser is None) or (currentUser.password != password):
            return render_template('authorization.html', err=True)

        global thisUser
        thisUser = currentUser

        return redirect("/home")
    else:
        return render_template('authorization.html')


@app.route('/add_book', methods=['POST', 'GET'])
def add_book():
    if request.method == "POST":
        name = request.form["title_book"]
        genre = request.form["genre_book"]
        annotation = request.form["description_book"]
        author = request.form["author_book"]
        year = request.form["year_book"]
        pageCount = request.form["count_pages_book"]
        roomNum = -1
        publishingHouse = request.form["publishing_house_book"]

        book = Book(name=name, genre=genre, annotation=annotation, author=author, year=year, pageCount=pageCount,
                    roomNum=roomNum,
                    publishingHouse=publishingHouse)
        try:
            db.session.add(book)
            db.session.commit()
            return redirect("/book/" + str(book.id))
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            return "ERROR (%r)" % message
    else:
        return render_template('add_book.html')


if __name__ == "__main__":
    app.run(debug=True)
