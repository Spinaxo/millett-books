# Book Review Website

## Overview

This project is a web application for book enthusiasts. It allows users to browse books, read reviews, and submit their own reviews. Built with Flask and PostgreSQL, it features user authentication, book management, and review functionalities.

## Features

-   **User Authentication**: Users can register, log in, and log out.
-   **Book Browsing**: Browse through a collection of books.
-   **Book Reviews**: Users can read and submit reviews for each book.
-   **Admin Panel**: Administrators can add, edit, or delete book entries.

## Technologies Used

-   **Backend**: Flask (Python)
-   **Database**: PostgreSQL
-   **ORM**: SQLAlchemy
-   **Frontend**: HTML, CSS, JavaScript
-   **Additional Libraries**: Flask-Login, WTForms, etc.

## Getting Started

### Prerequisites

-   Python 3.x
-   pip (Python package manager)
-   PostgreSQL

### Installation

1. **Clone the repository**

git clone https://github.com/Spinaxo/millett-books.git
cd book-review-site

arduino

2. **Set up a virtual environment (optional but recommended)**

python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate

markdown

3. **Install required Python packages**

pip install -r requirements.txt

markdown

4. **Set up PostgreSQL**

-   Create a new PostgreSQL database.
-   Modify the database URI in `app.py` to point to your new database.

5. **Initialize the database**

python

            from app import db
            db.create_all()
            exit()

markdown

6. **Run the application**

python app.py

markdown

7. **Open your browser** and go to `http://localhost:5000`.

## Usage

-   Register a new user account or log in.
-   Browse the list of books.
-   View details about each book and read reviews.
-   Submit your own reviews for books.
-   (Admin) Manage book entries via the admin panel.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes.

## License

[MIT License](LICENSE)

## Contact

-   Aaron - aarondmillett@gmail.com
-   Project Link: https://github.com/Spinaxo/millett-books
