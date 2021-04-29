from django.contrib import admin
from .models import BookItem,BookDetail,Rack,Book_Reservation,book_Lending,Fine
class BookItemAdmin(admin.ModelAdmin):
    list_display = ("book_details", "borrowed_date", "due_date", "status",)


admin.site.register(Rack)
admin.site.register(BookDetail)
admin.site.register(BookItem,BookItemAdmin)
admin.site.register(Book_Reservation)
admin.site.register(book_Lending)
admin.site.register(Fine)


# Register your models here.
