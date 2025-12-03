from django.contrib.auth.forms import UserCreationForm as UCF
from django.contrib.auth.forms import AuthenticationForm

from django import forms

from .models import User


class UserCreationForm(UCF):
    first_name = forms.CharField(max_length=100, help_text="Ismni kiriting", label="Ismni kiriting", widget=forms.TextInput({'placeholder':'Ism'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email', 'telefon', 'viloyat', 'tuman', 'maktab')

class UserModelForm(forms.ModelForm):
    profile_image = forms.ImageField(widget=forms.FileInput({"accept":"image/*"}), required=False)
    class Meta:
        model = User
        fields = ("first_name","last_name","username","telefon","telegram","viloyat","tuman","maktab", "profile_image")

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': (
            "Iltimos, to‘g‘ri %(username)s va parolni kiriting. E'tibor bering, har ikki "
            "maydon katta-kichik harflarga sezgir bo‘lishi mumkin."
        ),
        'inactive': ("Bu hisob muzlatilgan."),
    }
