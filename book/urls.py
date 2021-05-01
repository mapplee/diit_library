from django.db.models.fields import UUIDField
from django.urls import path
from .views import Book_Details
urlpatterns = [
path('details/<uuid:id>', Book_Details, name='book_details'),

]