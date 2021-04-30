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
def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['Stuff', 'Supper_admin']).exists()



def Success(request):
    contex={}
    m1="success"
    contex['message']=m1
    return render(request,'success.html',contex)


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
    contex={}
    user=request.user #user details 

    #total_checkout_by_user=Checkout_Details.objects.get(user_details=user.id) #total book check out by user
    
    try:
        total_checkout_by_user=Checkout_Details.objects.get(user_details=user.id) #match checkout_details with user
        total_checkout_by_user=total_checkout_by_user.total_checkout # #total book check out by user
    except:
         total_checkout_by_user=-1 #thouh user didn't creat any checkout
    book_item_id_by_user='6b5bfa99-ba85-4c31-9087-a619d190b485'
    try:
        book_reservation_status=Book_Reservation.objects.get(reserved_book_details=book_item_id_by_user)#match the book has reservation
    except:
        book_reservation_status='None' #book is empty
    try:
        book_reserver_id=Book_Reservation.objects.get(reserver_detials=user.id) #match the id with reserver if thake
        book_reserver_id= book_reserver_id.id
    except:
        book_reserver_id="None" #didn't find any id

    def Check_Eligibilty():
        get_status= BookItem.objects.get(id=book_item_id_by_user)
        get_status=get_status.status
        if get_status == "Available":
            return True
        else:
            return False

        return True



    if total_checkout_by_user < 10 :
        #contex['ch']=total_checkout_by_user
        if book_reservation_status != 'None' and book_reserver_id!=user.id: #chceck there is status and it is not user
                contex['ch']="This book is reserved by another member "
                return render(request,'__checkout.html',contex)
        elif book_reserver_id == user.id: #check the id made an reservation
                book_reservation_status.status='Completed'
                book_reservation_status.save()
                contex=book_reservation_status.status
        if Check_Eligibilty():
            #update BookItem
            book_element_change=BookItem.objects.get(id=book_item_id_by_user)
            book_element_change.status="Loaned"
            book_element_change.borrowed_date=datetime.datetime.now(timezone.utc)
            book_element_change.due_date=datetime.datetime.now(timezone.utc)+datetime.timedelta(days=10)
            book_element_change.save()
            #update Checkout_Details /creat  Checkout_Details
            if total_checkout_by_user != -1:
                checkout_details_change=Checkout_Details.objects.get(user_details=user.id)
                checkout_details_change.total_checkout=checkout_details_change.total_checkout+1
                checkout_details_change.save()
            else:
                checkout_details_create = Checkout_Details(total_checkout=1,user_details=user)
                checkout_details_create.save()
            lended_book=BookItem.objects.get(id=book_item_id_by_user)
            book_lending_create=book_Lending(lender_details=user,lender_book_details=lended_book,creation_date=lended_book.borrowed_date,due_date=lended_book.due_date)
            book_lending_create.save()
            return HttpResponseRedirect(reverse_lazy('success'))
            #return render(request,'home.html',contex)
        else:
            contex['ch']="Somthing Went wrong "
            return render(request,'__checkout.html',contex)
    else:
        contex['ch']="The user has already checked-out maximum number of books"
        return render(request,'__checkout.html',contex)
   
    #contex['ch']=ch.total_checkout

    
