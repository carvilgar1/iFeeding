from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

class header_search(forms.Form):
    key_word = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2'}))

class extended_search_form(forms.Form):
    ingredients = forms.CharField(label="Ingredients to include", max_length=200, widget=forms.Textarea, required=False)
    ingredients_to_exclude = forms.CharField(label="Ingredients to exclude", max_length=200)
    page_num = forms.IntegerField(validators=[MinValueValidator(1)])
    page_len = forms.IntegerField(min_value=15, validators=[MinValueValidator(15), MaxValueValidator(30)])