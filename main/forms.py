from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Wikipedia', max_length=100)