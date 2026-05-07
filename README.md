Library Management System
A complete web-based Library Management System built with Django that allows libraries to manage books, handle borrowing/returns, search for books, and track borrowed items.

Features
Add Books: Admin users can add new books to the library inventory

Borrow Books: Users can borrow available books with automatic due date calculation (14-day borrowing period)

Return Books: Users can return books with automatic fine calculation for overdue books ($0.50 per day)

Search Books: Search for books by title, author, ISBN, or category

View Borrowed Books: See all currently borrowed books with due dates and fines

User Authentication: Secure login and logout functionality

Admin Panel: Django admin interface for advanced management

User Dashboard: Users can view their own borrowing history

Tech Stack
Backend: Django 4.2.0 (Python)

Database: SQLite (default, can be changed to PostgreSQL/MySQL)

Frontend: Bootstrap 5 with responsive design

Authentication: Django built-in authentication system

Installation
Prerequisites
Python 3.8 or higher installed

pip (Python package manager)

Step-by-Step Setup
Clone or download the project

bash
cd library_management
Create a virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
Install Django

bash
pip install django
Run database migrations

bash
python manage.py makemigrations
python manage.py migrate
Create a superuser (admin account)

bash
python manage.py createsuperuser
Follow the prompts to create an admin username and password.

Add sample books (optional)

bash
python manage.py shell
Then run this Python code:

python
from books.models import Book

books = [
    Book(title="The Great Gatsby", author="F. Scott Fitzgerald", isbn="9780743273565",
         publisher="Scribner", publication_year=1925, category="Fiction",
         total_copies=3, available_copies=3, location="Section A, Shelf 2"),
    Book(title="Atomic Habits", author="James Clear", isbn="9780735211292",
         publisher="Avery", publication_year=2018, category="Non-Fiction",
         total_copies=5, available_copies=5, location="Section C, Shelf 5"),
    Book(title="Python Crash Course", author="Eric Matthes", isbn="9781593279288",
         publisher="No Starch Press", publication_year=2019, category="Technology",
         total_copies=4, available_copies=4, location="Section D, Shelf 1"),
]

for book in books:
    book.save()
    print(f"Added: {book.title}")
Run the development server

bash
python manage.py runserver
Open your browser and navigate to: http://127.0.0.1:8000/

Project Structure
text
library_management/
├── manage.py
├── db.sqlite3
├── library/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── books/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   └── templates/
│       └── books/
│           ├── base.html
│           ├── book_list.html
│           ├── add_book.html
│           ├── edit_book.html
│           ├── delete_book.html
│           ├── borrow_book.html
│           ├── return_book.html
│           ├── search_books.html
│           ├── borrowed_books.html
│           ├── my_borrowed_books.html
│           └── login.html
└── static/
Usage Guide
Login
Access the system at http://127.0.0.1:8000/

Login with your superuser credentials or create regular users via admin panel

Admin User (Full Access)
Add, edit, and delete books

View all borrowed books

Manage users

Access Django admin at /admin

Regular User (Limited Access)
View all books

Search for books

Borrow available books

Return borrowed books

View personal borrowing history

Book Operations
Add a Book (Admin only)

Click "Add Book" in navigation bar

Fill in book details (title, author, ISBN, etc.)

Click "Add Book" to save

Borrow a Book

Find the book in the book list

Click "Borrow" button next to the book

Enter the User ID of the borrower

Click "Confirm Borrow"

Return a Book

Go to "Borrowed Books" page

Find the borrowed book

Click "Return" button

Confirm return (fine will be calculated if overdue)

Search for Books

Click "Search" in navigation bar

Select search type (Title, Author, ISBN, Category)

Enter search term

Click "Search"

Key Features Explained
Borrowing System
Books can be borrowed for 14 days

Due date automatically calculated

Users cannot borrow the same book twice

Available copies decrease when borrowed

Fine System
$0.50 per day overdue

Fine automatically calculated when returning

Fine amount shown before confirming return

Book Management
Track total copies and available copies

Each book has unique ISBN

Books can be categorized (Fiction, Non-Fiction, Technology, History, Biography, Children)

Location tracking for physical books

API Endpoints
URL Pattern	View Name	Description
/	book_list	Display all books
/login/	login	User login
/logout/	logout	User logout
/books/add/	add_book	Add new book (admin)
/books/search/	search_books	Search books
/books/borrow/<id>/	borrow_book	Borrow a book
/books/return/<id>/	return_book	Return a book
/books/borrowed/	borrowed_books	View all borrowed books
/books/my-borrowed/	my_borrowed_books	View user's borrowed books
/books/edit/<id>/	edit_book	Edit book (admin)
/books/delete/<id>/	delete_book	Delete book (admin)
/admin/	admin	Django admin interface
Database Models
Book Model
title (CharField)

author (CharField)

isbn (CharField, unique)

publisher (CharField)

publication_year (IntegerField)

category (CharField)

total_copies (IntegerField)

available_copies (IntegerField)

location (CharField)

description (TextField)

BorrowRecord Model
user (ForeignKey to User)

book (ForeignKey to Book)

borrow_date (DateTimeField)

due_date (DateTimeField)

return_date (DateTimeField, nullable)

status (CharField: BORROWED, RETURNED, OVERDUE)

fine_amount (DecimalField)

Common Issues and Solutions
Issue: Template not found error
Solution: Make sure all HTML files are in books/templates/books/ folder

Issue: Permission denied for add/edit/delete
Solution: Login with a staff/superuser account or add is_staff=True to your user

Issue: Book cannot be borrowed
Solution: Check if available_copies > 0 in the book details

Issue: User not found when borrowing
Solution: User IDs can be found in Django admin panel under Users section

Customization Options
Change Borrowing Duration
Edit books/models.py in the save method of BorrowRecord:

python
self.due_date = timezone.now() + timedelta(days=14)  # Change 14 to desired days
Change Fine Amount
Edit books/models.py in the calculate_fine method:

python
fine = days_overdue * 0.50  # Change 0.50 to desired amount
Add New Book Categories
Edit books/forms.py in the `category


