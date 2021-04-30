from django.shortcuts import render
from django.http import HttpResponse
from book.models import BookDetail
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
def is_in_multiple_groups(user):
    return user.groups.filter(name__in=['Stuff', 'Supper_admin']).exists()

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
    return render(request,'__checkout.html')
