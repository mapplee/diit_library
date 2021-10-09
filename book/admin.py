from django.contrib import admin
from .models import BookItem,BookDetail,Rack,Book_Reservation,book_Lending,Fine,Checkout_Details
class BookItemAdmin(admin.ModelAdmin):
    list_display = ("book_details", "borrowed_date", "due_date", "status",)

class BookDetaiAdmin(admin.ModelAdmin):
    list_display = ( "title", "id", "language", "author",)

class Book_LendingAdmin(admin.ModelAdmin):
    list_display = ( "lender_details", "lender_book_details", "return_date","return_status",)

class Book_ReservationAdmin(admin.ModelAdmin):
    list_display = ( "reserver_detials", "reserved_book_details", "status",)

class Checkout_DetailsAdmin(admin.ModelAdmin):
    list_display = ( "user_details", "total_checkout",)



admin.site.register(Rack)
admin.site.register(BookDetail,BookDetaiAdmin)
admin.site.register(BookItem,BookItemAdmin)
admin.site.register(Book_Reservation,Book_ReservationAdmin)
admin.site.register(book_Lending,Book_LendingAdmin)
admin.site.register(Fine)
admin.site.register(Checkout_Details,Checkout_DetailsAdmin)


# Register your models here.