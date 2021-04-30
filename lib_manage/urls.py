from django.urls import path
from .views import HomePage,Book_Checkout, Success
urlpatterns = [
path('', HomePage, name='home'),
path('book_checkout',Book_Checkout,name='book_checkout'),
path('success',Success,name='success'),
]