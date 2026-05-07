from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/search/', views.search_books, name='search_books'),
    path('books/borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),
    path('books/return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('books/borrowed/', views.borrowed_books, name='borrowed_books'),
    path('books/edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:book_id>/', views.delete_book, name='delete_book'),
]