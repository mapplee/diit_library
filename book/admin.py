from django.contrib import admin
from .models import BookItem,BookDetail,Rack,Book_Reservation,book_Lending,Fine,Checkout_Details
class BookItemAdmin(admin.ModelAdmin):
    list_display = ("book_details", "borrowed_date", "due_date", "status",)


admin.site.register(Rack)
admin.site.register(BookDetail)
admin.site.register(BookItem,BookItemAdmin)
admin.site.register(Book_Reservation)
admin.site.register(book_Lending)
admin.site.register(Fine)
admin.site.register(Checkout_Details)


# Register your models here.
