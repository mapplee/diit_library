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
            print(user_details.id)
            try:
                book_item_id_by_user=form.cleaned_data['Book_ID']
            except:
                messages.success(request, 'Book not Found')
                return HttpResponseRedirect(reverse_lazy('book_checkout'))
            
            try:
                total_checkout_by_user=Checkout_Details.objects.get(user_details=user) #match checkout_details with user
                total_checkout_by_user=total_checkout_by_user.total_checkout # #total book check out by user
            except:
                total_checkout_by_user=-1 #thouh user didn't creat any checkout

            try:
                book_reservation_status=Book_Reservation.objects.get(reserved_book_details=book_item_id_by_user)#match the book has reservation
                print(book_reservation_status.status)
            except:
                book_reservation_status='None' #book is empty
            try:
                book_reserver_id=Book_Reservation.objects.get(reserver_detials=user,reserved_book_details=book_item_id_by_user,status="Pending")
               # print()) #match the id with reserver if thake
                print("hello")
                #book_reserver_id=book_reserver_id.reserver_details
                print("eeee")
                book_reserver_id=book_reserver_id.reserver_detials.id
                print("ok")
            except:
                book_reserver_id="None" #didn't find any id

            def Check_Eligibilty():
                get_status= BookItem.objects.get(id=book_item_id_by_user)
                get_status=get_status.status
                if get_status == "Available":
                    return True   
                else:
                    return False

            if total_checkout_by_user < 10 :
                #contex['ch']=total_checkout_by_user
                if book_reservation_status.status != 'None' and book_reserver_id != int(user):
                    print(book_reserver_id+'33')
                    messages.success(request, 'This book is reserved by another membelllllr ')
                    return HttpResponseRedirect(reverse_lazy('book_checkout'))
                elif book_reserver_id == int(user): #check the id made an reservation
                    #Upadate reservation status
                        book_reservation_status.status='Completed'
                        book_reservation_status.save()
                if Check_Eligibilty():
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
                        checkout_details_create = Checkout_Details(total_checkout=1,user_details=user)
                        checkout_details_create.save()
                    #update book_Lending /creat  book_Lending
                    lended_book=BookItem.objects.get(id=book_item_id_by_user)
                    custom_user=CustomUser.objects.get(id=user)
                    book_lending_create=book_Lending(lender_details=custom_user,lender_book_details=lended_book,creation_date=lended_book.borrowed_date,due_date=lended_book.due_date)
                    book_lending_create.save()
                    #return HttpResponseRedirect(reverse_lazy('success'))
                    #return render(request,'home.html',contex)
                    messages.success(request, 'Ok this book is lended')
                    return HttpResponseRedirect(reverse_lazy('book_checkout'))
                else:
                   # return HttpResponseRedirect(reverse_lazy('success'))
                    messages.success(request, 'This book is alreary lended')
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
                messages.success(request, 'Soorry book has been reservevd by another person')
                return HttpResponseRedirect(reverse_lazy('success'))
        try:
            Book_Reservation.objects.filter(reserved_book_details=check_reserve_item.id)[0]#match the book already reserved by this id
            messages.success(request, 'Soorry book has been reservevd ')
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








    
