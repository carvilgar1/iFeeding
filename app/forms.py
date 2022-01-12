from django import forms

from django.contrib.auth.models import User

class register_form(forms.Form):
    firstname = forms.CharField(max_length=50, widget=forms.TextInput({'class':'form-control', 'placeholder':'Enter Firstname'}))
    lastname = forms.CharField(max_length=50, widget=forms.TextInput({'class':'form-control', 'placeholder':'Enter Lastname'}))
    username = forms.CharField(max_length=50,required=True, widget=forms.TextInput({'class':'form-control', 'placeholder':'Enter Username'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput({'class':'form-control', 'placeholder':'Enter Password'}))
    error_class = "alert alert-danger"
    def clean_username(self):
        if User.objects.filter(username = self.data['username']).exists():
            raise forms.ValidationError('This user is already registered')
        return self.data['username']