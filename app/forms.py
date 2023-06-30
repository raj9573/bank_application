from app.models import *
from django import forms 
class User_form(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={'password':forms.PasswordInput}
class Profile_Form(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['address','mobile_number']
        