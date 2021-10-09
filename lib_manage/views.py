from accounts.admin import CustomUser
from typing import DefaultDict
from django.db.models.fields import UUIDField
from django.shortcuts import render
from django.http import HttpResponse, request
from book.models import BookDetail,Checkout_Details,Book_Reservation,BookItem,book_Lending
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
import datetime
from book.form import CheckOutForm
from django.contrib import messages
import pickle
from django.views.generic import ListView
from book.models import BookDetail

def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['Stuff', 'Supper_admin']).exists()



def Success(request):
    return render(request,'success.html')


#@user_passes_test(lambda u: Group.objects.get(name='Stuff') in u.groups.all())
def HomePage(request):
    book_list=BookDetail.objects.all()
    contex={}
    contex['books']=book_list
    contex['group']=Group
    return render(request,'home.html',contex)

#@user_passes_test(lambda u: Group.objects.get(name='Stuff') in u.groups.all())
@user_passes_test(is_in_multiple_groups)
def Book_Checkout(request):
     #b=Checkout_Details.objects.all()
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            print("Ok form is valid")
            contex={}
            user=form.cleaned_data['User_ID']
    
            #print(user)
            user_details=CustomUser.objects.get(id=user)

            try:
                book_item_id_by_user=form.cleaned_data['Book_ID']
                
                book_item_id_by_user_obj=BookItem.objects.get(id=book_item_id_by_user)
                print(book_item_id_by_user_obj)
                
            except:
                messages.success(request, 'Book not Found')
                return HttpResponseRedirect(reverse_lazy('book_checkout'))
            
            try:
                total_checkout_by_user=Checkout_Details.objects.get(user_details=user) #match checkout_details with user
                total_checkout_by_user=total_checkout_by_user.total_checkout # #total book check out by user
            except:
                total_checkout_by_user=-1 #thouh user didn't creat any checkout

            try:
                book_reservation_status=Book_Reservation.objects.get(reserved_book_details=book_item_id_by_user,status="Pending")#match the book has reservation
                print(book_reservation_status.status+' hello')
            except:
                book_reservation_status=None #book is empty
            try:
                book_reserver_id=Book_Reservation.objects.get(reserver_detials=user,reserved_book_details=book_item_id_by_user,status="Pending")
               # print()) #match the id with reserver if thake

                #book_reserver_id=book_reserver_id.reserver_details
                

                book_reserver_id=book_reserver_id.reserver_detials.id
                print(book_reserver_id,'hi')
                #book_reservation_status=book_reserver_id.status

            except:
                book_reserver_id=None #didn't find any id

            def Check_Eligibilty(check_value):
                get_status= BookItem.objects.get(id=book_item_id_by_user)
                get_status=get_status.status
                if get_status == "Available":
                    return True   
                elif get_status == "Reserved" and check_value == 1:
                    return True
                else:
                    return False

            if total_checkout_by_user < 10 :
                #contex['ch']=total_checkout_by_user
                check_value=0
                if book_reservation_status != None and book_reserver_id != int(user):
                    #print(type(book_reserver_id))
                    print(book_reserver_id,user)
                    
                    messages.success(request, 'This book is reserved by another member ')
                    return HttpResponseRedirect(reverse_lazy('book_checkout'))
                elif book_reserver_id == int(user): #check the id made an reservation
                    #Upadate reservation status
                        book_reservation_status.status="Completed"
                        book_reservation_status.save()
                        check_value=1
                if Check_Eligibilty(check_value):
                    #update BookItem
                    book_element_change=BookItem.objects.get(id=book_item_id_by_user)
                    book_element_change.status="Loaned"
                    book_element_change.borrowed_date=datetime.datetime.now(timezone.utc)
                    book_element_change.due_date=datetime.datetime.now(timezone.utc)+datetime.timedelta(days=10)
                    book_element_change.save()
                    #update Checkout_Details /creat  Checkout_Details
                    if total_checkout_by_user != -1:
                        checkout_details_change=Checkout_Details.objects.get(user_details=user)
                        checkout_details_change.total_checkout=checkout_details_change.total_checkout+1
                        checkout_details_change.save()
                    else:
                        custom_user=CustomUser.objects.get(id=user)
                        checkout_details_create = Checkout_Details(total_checkout=1,user_details=custom_user)
                        checkout_details_create.save()
                    #update book_Lending /creat  book_Lending
                    lended_book=BookItem.objects.get(id=book_item_id_by_user)
                    try:
                        custom_user=CustomUser.objects.get(id=user)
                    except:
                        custom_user=request.user

                    book_lending_create=book_Lending(lender_details=custom_user,lender_book_details=lended_book,creation_date=lended_book.borrowed_date,due_date=lended_book.due_date)
                    book_lending_create.save()
                    #return HttpResponseRedirect(reverse_lazy('success'))
                    #return render(request,'home.html',contex)
                    messages.success(request, 'Ok this book is lended')
                    return HttpResponseRedirect(reverse_lazy('book_checkout'))
                else:
                   # return HttpResponseRedirect(reverse_lazy('success'))
                    messages.success(request, 'This book is already loaned')
                    return HttpResponseRedirect(reverse_lazy('book_checkout'))
            else:
                #contex['ch']="The user has already checked-out maximum number of books"
                #return HttpResponseRedirect(reverse_lazy('success'))
                messages.success(request, 'The user has already checked-out maximum number of books')
                return HttpResponseRedirect(reverse_lazy('book_checkout'))
        else:
            #return HttpResponseRedirect(reverse_lazy('success'))
            messages.success(request, 'value is not correct')
            return HttpResponseRedirect(reverse_lazy('book_checkout'))
            
    else:
         form = CheckOutForm()
         return render(request,'__checkout.html',{'form': form})


#@login_required(login_url='/accounts/login/')
def Reservation(request,id):
    # ms=id
    # book_items=BookItem.objects.filter(book_details=ms,status='Available')[0]
    # messages.success(request, book_items.id)
    # return HttpResponseRedirect(reverse_lazy('success'))
    if request.user.is_authenticated:
        user=request.user
        user=user.id
        print(user)

        try:
            #check_reserve_item=BookItem.objects.get(status="Available")
            check_reserve_item=BookItem.objects.filter(book_details=id,status='Available')[0]
            reservation_status="Pending"
            check_reserve_item.status="Reserved"
            
        except:
            try:
                #check_reserve_item=BookItem.objects.get(status="Loaned")
                check_reserve_item=BookItem.objects.filter(book_details=id,status='Loaned')[0]
                reservation_status="Waiting"
                check_reserve_item.status="Loaned"
                
            except:
                messages.success(request, 'Soorry there is no book for your reservation ')
                return HttpResponseRedirect(reverse_lazy('success'))
               
        try:
            try:
                b=Book_Reservation.objects.filter(reserved_book_details=check_reserve_item.id,status="Waiting")[0]
                #print(check_reserve_item.id)
                messages.success(request, 'Sorrry all books are reserved')
                return render(request,'success.html')
            except:
                print("Not Ok")
            try:
                b=Book_Reservation.objects.filter(reserved_book_details=check_reserve_item.id,status="Pending")[0]
                #print(check_reserve_item.id)
                messages.success(request,'Sorrry all books are reserved')
                return render(request,'success.html')
            except:
                print("Not Ok")
            Book_Reservation.objects.get(reserved_book_details=check_reserve_item.id,reserver_detials=user,status="Pending")#match the book already reserved by this id
            messages.success(request, 'Soorry book has been already reserveved by you')
            return HttpResponseRedirect(reverse_lazy('success'))
        except:
            user=request.user
            reserving_book_id=check_reserve_item
            reserved_date=datetime.datetime.now(timezone.utc)
            reservation_details_create=Book_Reservation(reserver_detials=user,reserved_book_details=reserving_book_id,creation_date=reserved_date,status=reservation_status)
            reservation_details_create.save()
            check_reserve_item.save()
            messages.success(request, 'reserved success')
            return render(request,'success.html')
    else:
        messages.success(request, 'You Must Login')
        return HttpResponseRedirect(reverse_lazy('login'))

from django.db.models import Q

class SearchResultsListView(ListView):
    model = BookDetail
    context_object_name = 'book_list'
    template_name = 'search_results.html'
    def get_queryset(self):
        query = self.request.GET.get('q')
        return BookDetail.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(publisher__icontains = query)
        )

def AddBook(request):
    if request.method=="POST":
            isbn = request.POST['isbn']
            title = request.POST['title']
            publisher = request.POST['publisher']
            language = request.POST['language']
            author = request.POST['author']
            cover = request.POST['cover']
            print(isbn,title,publisher,language,author,cover)
            ins = BookDetail(isbn=isbn, title=title, publisher=publisher ,language=language, author=author, cover=cover)
            ins.save()
    #context = {'form':form}
    return render(request, 'add_book_detail.html')

def AddItem(request):
    return render(request, 'AddBookitem.html')








    
