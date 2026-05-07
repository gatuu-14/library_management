from django.contrib import admin
from .models import Book, BorrowRecord

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'isbn', 'category', 'total_copies', 'available_copies']
    list_filter = ['category', 'publication_year']
    search_fields = ['title', 'author', 'isbn']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'borrow_date', 'due_date', 'status', 'fine_amount']
    list_filter = ['status', 'borrow_date']
    search_fields = ['book__title', 'user__username']
    readonly_fields = ['borrow_date', 'fine_amount']
