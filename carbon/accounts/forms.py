from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateUser(UserCreationForm):
    class Meta():
        model = get_user_model() #gets model of user for this form
        fields = ['username' , 'email' , 'password1' , 'password2']

    def clean_email(self): # check account with similar email is not made
        email = self.cleaned_data.get('email') # grabbing the email inserted in form

        try:
            match = User.objects.get(email=email)

        except User.DoesNotExist:
            return email

        raise forms.ValidationError('This email is already in use. Use another email.')    
