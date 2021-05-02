from django import forms



class CheckOutForm(forms.Form):
    User_ID=forms.CharField(label='User ID', max_length=100)
    Book_ID = forms.CharField(label='Book ID', max_length=100)
class ReturnForm(forms.Form):
    User_ID=forms.CharField(label='User ID', max_length=100)
    Book_ID = forms.CharField(label='Book ID', max_length=100)

from django import forms



class BookdetailForm(forms.Form):
    
    isbn=forms.CharField(label='isbn',max_length=300)
    title=forms.CharField(label='title',max_length=300)
    publisher=forms.CharField(label='publilsher',max_length=300)
    language=forms.CharField(label='language',max_length=100)
    author=forms.CharField(label='author',max_length=100)
    cover = forms.ImageField(label='cover')
