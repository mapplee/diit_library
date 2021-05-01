import uuid
from django.shortcuts import render
from .models import BookDetail

def Book_Details(request, id):

    context={}

    n=BookDetail.objects.get(id=id)
    context['books']=n
    return render(request,'book_details.html',context)


# Create your views here.
