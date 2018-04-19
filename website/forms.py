from django import forms

class AddBookForm(forms.Form):
    new_title = forms.CharField(label='Title', max_length=50)
    new_author = forms.CharField(label='Author', max_length=30)
    new_width = forms.IntegerField(label='Book width (mm)')
    #new_description = forms.CharField(attrs={'title': 'Write a short description (200 characters max):'}, widget=forms.Textarea)
    new_description = forms.CharField(widget=forms.Textarea, label='', max_length=200)