from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
    UserMixin,
)
from sqlalchemy.exc import IntegrityError
import bcrypt
import random
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:password1@localhost/millettbooks"
app.config["SECRET_KEY"] = "really-secret-key"

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255))
    role = db.Column(db.String(50), default="user")

    def get_id(self):
        return str(self.user_id)

    def is_admin(self):
        return self.role == "admin"


class Genre(db.Model):
    __tablename__ = "genres"
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    isbn = db.Column(db.String(20), unique=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"))
    synopsis = db.Column(db.Text)
    cover_image = db.Column(db.String(255))


class Review(db.Model):
    __tablename__ = "reviews"
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    rating = db.Column(db.Integer)
    review_text = db.Column(db.Text)


class UserBookshelf(db.Model):
    __tablename__ = "user_bookshelf"
    shelf_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"))
    status = db.Column(db.String(50))


def get_all_usernames():
    usernames = []
    for i in User.query.all():
        usernames.append(i.username)
    return usernames


@app.route("/")
def home():
    books = Book.query.all()
    featured_books = random.sample(books, 4)
    # print(featured_books)
    return render_template("home.html", featured_books=featured_books)


@app.route("/books")
def books():
    books = Book.query.all()  # Fetch all books
    return render_template("browse_books.html", books=books)


@app.route("/books/<int:book_id>")
def book_page(book_id):
    book = Book.query.get(book_id)
    # print(book_id)
    return render_template("book_page_base.html", book=book)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        if password != confirm_password:
            return render_template(
                "error_base.html",
                error_title="Error",
                error_message="Passwords do not match.",
            )

        try:
            hashed_password = password_hasher(password)
            print(hashed_password)
            new_user = User(
                username=username, email=email, password_hash=hashed_password
            )
            # print(new_user.username)

            db.session.add(new_user)
            db.session.commit()
            print(User.query.all())

            return redirect(url_for("login"))

        except IntegrityError:
            db.session.rollback()

    return render_template(
        "login_signup_base.html",
        page_title="Signup",
        greeting_message="Create an Account",
        instruction_message="Please fill in the details to create an account.",
        form_action=url_for("signup"),
        is_signup=True,
        button_text="Sign Up",
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    print(get_all_usernames())
    if request.method == "POST":
        form = request.form
        username = form["username"]
        password = form["password"]
        user = User.query.filter_by(username=username).first()
        if user:
            if user and check_password(password, user.password_hash):
                print("check1")
                user.authenticated = True
                print("check2")
                db.session.add(user)
                print("check3")
                db.session.commit()
                print("check4")
                login_user(user, remember=True)
                print("check5")
                return redirect(url_for("home"))
            else:
                # User doesn't exist or password is wrong
                return render_template(
                    "error_base.html",
                    error_title="Error",
                    error_message="Username or password is incorrect.",
                )
    return render_template(
        "login_signup_base.html",
        page_title="Login",
        greeting_message="Welcome Back!",
        instruction_message="Please log in to your account.",
        form_action=url_for("login"),
        is_signup=False,
        button_text="Login",
    )


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("home.html")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def password_hasher(plain_text_password):
    hashed_password = bcrypt.hashpw(
        plain_text_password.encode("utf-8"), bcrypt.gensalt()
    )
    return hashed_password


def decrypt_password(hashed_password_str):
    cleaned_hash = hashed_password_str.replace("\\x", "")
    hashed_password_bytes = bytes.fromhex(cleaned_hash)
    return hashed_password_bytes


def check_password(plain_text_password, hashed_password_str):
    hashed_password_bytes = decrypt_password(hashed_password_str)
    return bcrypt.checkpw(plain_text_password.encode("utf-8"), hashed_password_bytes)


@app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "error_base.html",
            error_title="Error: 404 Page not found",
            error_message="Sorry it doesn't seem like that page exists",
        ),
        404,
    )


if __name__ == "__main__":
    app.run(debug=True)
