from django import forms

class simple_search_form(forms.Form):
    query = forms.CharField(label='Insert your query here', max_length=200)