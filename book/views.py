import uuid
from django.contrib.auth.decorators import user_passes_test
from django.db.models.deletion import SET_NULL
from django.db.models.fields import NullBooleanField
from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from .models import BookDetail, Checkout_Details,book_Lending,BookItem,Book_Reservation
from .form import ReturnForm
from django.contrib import messages
from django.utils import timezone
import datetime
from accounts.admin import CustomUser





def Book_Details(request, id):

    context={}

    n=BookDetail.objects.get(id=id)
    context['books']=n
    return render(request,'book_details.html',context)

def Book_Return(request):
    if request.method == 'POST':
        form = ReturnForm(request.POST)
        if form.is_valid():
            
            user=form.cleaned_data['User_ID']
            user_obj=CustomUser.objects.get(id=user)
            book_item_id_by_user=form.cleaned_data['Book_ID']
            book_item_id_by_user_obj=BookItem.objects.get(id=book_item_id_by_user)
            print(book_item_id_by_user)
            try:
                #lended_book_details=book_Lending.objects.filter(lender_details=user,lender_book_details=book_item_id_by_user).first()
                lended_book_details=book_Lending.objects.get(lender_details=user,lender_book_details=book_item_id_by_user,return_status="No")
                print("okkk1")
                lended_book_id=lended_book_details.lender_book_details
                print("okkk2")
                #change book Details
                book_details_change=BookItem.objects.get(id=lended_book_id.id)
                print("okk3")
                book_details_change.status="Available"
                book_details_change.borrowed_date=None
                print("okk4")
                book_details_change.due_date=None
                
                book_details_change.save()
                lended_book_change=lended_book_details
                lended_book_change.return_status="Yes"
                lended_book_change.return_date=datetime.datetime.now(timezone.utc)
                lended_book_change.save()
                print("okk5")

                try:
                    #change Reservation
                    reserved_book_details=Book_Reservation.objects.filter(reserved_book_details=book_item_id_by_user,status="Waiting")[0]
                    print(reserved_book_details.status)
                    reserved_book_change=reserved_book_details
                    reserved_book_change.status="Pending"
                    reserved_book_change.save()
                    #change checkout total
                    checkout_details=Checkout_Details.objects.get(user_details=user)
                    checkout_change=checkout_details
                    checkout_change.total_checkout-=1
                    checkout_change.save()
                    messages.success(request, 'Put the book on the rack')
                    return HttpResponseRedirect(reverse_lazy('success'))
                except:
                     #change checkout total
                    checkout_details=Checkout_Details.objects.get(user_details=user)
                    checkout_change=checkout_details
                    checkout_change.total_checkout-=1
                    checkout_change.save()
                    messages.success(request, 'Put the book on the rack')
                    return HttpResponseRedirect(reverse_lazy('success'))
            except:
                messages.success(request, 'Faild')
                return HttpResponseRedirect(reverse_lazy('success'))
    else:
        form = ReturnForm()
        return render(request,'__return_book.html',{'form': form})



def My_Reserved_Book(request):
    request_id=request.user
    books=Book_Reservation.objects.filter(reserver_detials=request_id)
    books_list=list(books)
    context={}
    context["books"]=books_list
    print(books_list)
    return render(request,'reserved_status.html',context)


def My_Books(request):
    request_id=request.user
    books=book_Lending.objects.filter(lender_details=request_id)
    books_list=list(books)
    context={}
    context["books"]=books_list


    return render(request,'my_books.html',context)



