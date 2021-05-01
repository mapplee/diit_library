from django.urls import path
from .views import HomePage,Book_Checkout, Reservation, Success,Reservation,SearchResultsListView
urlpatterns = [
    path('', HomePage, name='home'),
    path('book_checkout',Book_Checkout,name='book_checkout'),
    path('reservation/<uuid:id>',Reservation,name='reservation'),
    path('success',Success,name='success'),
    path('search', SearchResultsListView.as_view(), name ='search_results')
]