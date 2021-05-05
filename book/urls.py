from django.db.models.fields import UUIDField
from django.urls import path
from .views import Book_Details,Book_Return,My_Reserved_Book,My_Books
urlpatterns = [
path('details/<uuid:id>', Book_Details, name='book_details'),
path('return', Book_Return, name='book_return'),
path('reserved/status',My_Reserved_Book, name='my_reserved_book'),
path('mybooks',My_Books, name='my_books'),

]