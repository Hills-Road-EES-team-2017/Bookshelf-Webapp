from django import forms

class AddBookForm(forms.Form):
    new_title = forms.CharField(label='Title', max_length=50)
    new_author = forms.CharField(label='Author', max_length=30)
    new_width = forms.IntegerField()