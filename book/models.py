from django.db import models
import uuid
from django.conf import settings
from django.db.models.fields import DecimalField
# Create your models here.

class BookDetail(models.Model):
    id = models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    isbn=models.CharField(max_length=300)
    title=models.CharField(max_length=300)
    publisher=models.CharField(max_length=300)
    language=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    cover = models.ImageField(upload_to='covers/',null=True)
    def __str__(self):
        return self.title

class Rack(models.Model):
    rack_number=models.CharField(max_length=100)
    rack_loaction=models.CharField(max_length=300)
    def __str__(self):
        return self.rack_number

class BookItem(models.Model):
    id = models.UUIDField(
                        primary_key=True,
                        default=uuid.uuid4,
                        editable=False)
    book_details=models.ForeignKey(BookDetail, on_delete=models.CASCADE)
    location=models.ForeignKey(Rack, on_delete=models.CASCADE)
    purchase_date=models.DateTimeField(auto_now=False, auto_now_add=False)
    pulication_date=models.DateTimeField(auto_now=False, auto_now_add=False)
    borrowed_date =models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)#DateField(input_formats=settings.DATE_INPUT_FORMATS)
    due_date=models.DateTimeField(auto_now=False, auto_now_add=False,blank=True,null=True)
    StatusType = models.TextChoices('status', 'Available Reserved Lost Loaned')
    status = models.CharField(blank=False, choices=StatusType.choices, max_length=10)
    price = models.DecimalField(max_digits=6, decimal_places=2)


class Book_Reservation(models.Model):
    reserver_detials=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reserved_book_details= models.ForeignKey(BookItem, on_delete=models.CASCADE)
    creation_date=models.DateTimeField(auto_now=False, auto_now_add=False)
    StatusType = models.TextChoices('status', 'Waiting Pending Canceled Completed None')
    status=models.CharField(blank=False, choices=StatusType.choices, max_length=10)
    def __str__(self):
        return self.status
class book_Lending(models.Model):
    lender_details=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lender_book_details=models.ForeignKey(BookItem, on_delete=models.CASCADE)
    creation_date=models.DateTimeField(auto_now=False, auto_now_add=False)
    due_date=models.DateTimeField(auto_now=False, auto_now_add=False)
    return_date=models.DateTimeField(auto_now=False, auto_now_add=False,null=True)
class Fine(models.Model):
    reservation_details=models.OneToOneField(Book_Reservation, on_delete = models.CASCADE)
    lending_details=models.OneToOneField(book_Lending, on_delete = models.CASCADE)
    amount=models.FloatField(null=True)
class Checkout_Details(models.Model):
    user_details=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_checkout=models.DecimalField(max_digits=6, decimal_places=2)




