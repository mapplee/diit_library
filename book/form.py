from django import forms



class CheckOutForm(forms.Form):
    User_ID=forms.CharField(label='User ID', max_length=100)
    Book_ID = forms.CharField(label='Book ID', max_length=100)
