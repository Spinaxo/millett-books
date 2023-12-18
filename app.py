from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import bcrypt
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password1@localhost/millettbooks'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255))
    role = db.Column(db.String(50), default='user')

class Genre(db.Model):
    __tablename__ = 'genres'
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer)
    isbn = db.Column(db.String(20), unique=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'))
    synopsis = db.Column(db.Text)
    cover_image = db.Column(db.String(255))

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    rating = db.Column(db.Integer)
    review_text = db.Column(db.Text)

class UserBookshelf(db.Model):
    __tablename__ = 'user_bookshelf'
    shelf_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    status = db.Column(db.String(50))


def password_hasher(plain_text_password):
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password





@app.route('/')
def home():
    books = Book.query.all()  # Fetch all books
    featured_books = random.sample(books, 4)
    print (featured_books)
    return render_template('home.html', featured_books=featured_books)



@app.route('/books')
def books():
    books = Book.query.all()  # Fetch all books
    return render_template('browse_books.html', books=books)



@app.route('/books/<int:book_id>')
def book_page(book_id):
    book = Book.query.get(book_id)
    print (book_id)
    return render_template('book_page_base.html', book=book)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            return render_template('error_base.html', error_title='Error', error_message='Passwords do not match.')

        try:
            hashed_password = generate_password_hash(password)

            new_user = User(username=username, email=email, password_hash=hashed_password)
            print (new_user)

            # db.session.add(new_user)
            # db.session.commit()

            return redirect(url_for('login'))

        except IntegrityError:
            db.session.rollback()


    return render_template('login_signup_base.html', 
                           page_title='Signup', 
                           greeting_message='Create an Account',
                           instruction_message='Please fill in the details to create an account.',
                           form_action=url_for('signup'), 
                           is_signup=True, 
                           button_text='Sign Up')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('login_signup_base.html', 
                            page_title='Login', greeting_message='Welcome Back!', 
                            instruction_message='Please log in to your account.', 
                            form_action=url_for('login'), 
                            is_signup=False, 
                            button_text='Login')



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_base.html', error_title='Error: 404 Page not found', error_message="Sorry it doesn't seem like that page exists"), 404




if __name__ == "__main__":
    app.run(debug=True)

