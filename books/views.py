from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Book, BorrowRecord
from .forms import BookForm, SearchForm, BorrowForm
from django.contrib.auth.models import User


def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser

# Login View
def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('book_list')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('book_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    """Custom logout view"""
    auth_logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required
@user_passes_test(is_admin)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
def search_books(request):
    form = SearchForm()
    results = None
    
    if request.method == 'GET' and 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            search_type = form.cleaned_data['search_type']
            query = form.cleaned_data['query']
            
            if search_type == 'title':
                results = Book.objects.filter(title__icontains=query)
            elif search_type == 'author':
                results = Book.objects.filter(author__icontains=query)
            elif search_type == 'isbn':
                results = Book.objects.filter(isbn__icontains=query)
            elif search_type == 'category':
                results = Book.objects.filter(category__icontains=query)
    
    return render(request, 'search_books.html', {'form': form, 'results': results})

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if not book.is_available():
        messages.error(request, 'This book is not available for borrowing.')
        return redirect('book_list')
    
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            try:
                user = User.objects.get(id=user_id)
                
                # Check if user already has this book borrowed
                existing_borrow = BorrowRecord.objects.filter(
                    user=user, book=book, status='BORROWED'
                ).exists()
                
                if existing_borrow:
                    messages.error(request, f'{user.username} already has this book borrowed.')
                else:
                    borrow_record = BorrowRecord.objects.create(
                        user=user,
                        book=book,
                        status='BORROWED'
                    )
                    book.available_copies -= 1
                    book.save()
                    messages.success(request, f'Book "{book.title}" borrowed by {user.username}')
                    return redirect('book_list')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
    else:
        form = BorrowForm()
    
    return render(request, 'borrow_book.html', {'book': book, 'form': form})

@login_required
def return_book(request, borrow_id):
    borrow_record = get_object_or_404(BorrowRecord, id=borrow_id, status='BORROWED')
    
    if request.method == 'POST':
        borrow_record.status = 'RETURNED'
        borrow_record.save()
        messages.success(request, f'Book "{borrow_record.book.title}" has been returned.')
        return redirect('borrowed_books')
    
    fine = borrow_record.calculate_fine()
    return render(request, 'return_book.html', {
        'borrow_record': borrow_record,
        'fine': fine
    })

@login_required
def borrowed_books(request):
    borrowed_records = BorrowRecord.objects.filter(status='BORROWED').select_related('user', 'book')
    
    # Update overdue status
    for record in borrowed_records:
        if timezone.now() > record.due_date:
            record.status = 'OVERDUE'
            record.save()
    
    return render(request, 'borrowed_books.html', {'borrowed_records': borrowed_records})

@login_required
@user_passes_test(is_admin)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    
    return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'delete_book.html', {'book': book})
