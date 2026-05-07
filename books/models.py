from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    category = models.CharField(max_length=50)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    location = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def is_available(self):
        return self.available_copies > 0

    class Meta:
        ordering = ['title']

class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('BORROWED', 'Borrowed'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField()
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='BORROWED')
    fine_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"

    def calculate_fine(self):
        if self.status == 'RETURNED':
            return self.fine_amount
        
        if timezone.now() > self.due_date:
            days_overdue = (timezone.now() - self.due_date).days
            fine = days_overdue * 0.50  # $0.50 per day overdue
            return round(fine, 2)
        return 0

    def save(self, *args, **kwargs):
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=14)  # 14 days borrowing period
        
        if self.status == 'RETURNED' and not self.return_date:
            self.return_date = timezone.now()
            self.fine_amount = self.calculate_fine()
            # Increase available copies when book is returned
            self.book.available_copies += 1
            self.book.save()
        
        super().save(*args, **kwargs)
