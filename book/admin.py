from django.contrib import admin
from .models import BookItem,BookDetail,Rack,Book_Reservation
class BookItemAdmin(admin.ModelAdmin):
    list_display = ("book_details", "borrowed_date", "due_date", "status",)


admin.site.register(Rack)
admin.site.register(BookDetail)
admin.site.register(BookItem,BookItemAdmin)
admin.site.register(Book_Reservation)

# Register your models here.
