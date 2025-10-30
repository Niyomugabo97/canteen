from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order

# LOGIN FORM
class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

# SIGNUP FORM
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

# CHECKOUT FORM
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'placeholder': 'Delivery address', 'rows': 3}),
        }
