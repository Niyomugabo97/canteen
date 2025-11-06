from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.contrib.auth import authenticate
from .models import Item
from .models import Order

# ------------------------------
# SIGNUP FORM (email-based)
# ------------------------------
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def save(self, commit=True):
        try:
            user = super().save(commit=False)
            user.username = self.cleaned_data["email"].lower()  # Use email as username
            user.email = self.cleaned_data["email"].lower()

            if commit:
                user.save()

            return user

        except IntegrityError:
            raise forms.ValidationError(
                "An account with this email already exists. Please log in instead."
            )
        except Exception as e:
            raise forms.ValidationError(
                f"An unexpected error occurred: {str(e)}"
            )


# ------------------------------
# LOGIN FORM
# ------------------------------
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        # Prevent NoneType errors
        if not email or not password:
            raise forms.ValidationError("Please enter both email and password.")

        try:
            user = User.objects.filter(email=email).first()
            if user is None:
                raise forms.ValidationError(
                    "No account found with this email. Please sign up first."
                )

            user = authenticate(username=user.username, password=password)
            if user is None:
                raise forms.ValidationError(
                    "Invalid email or password. Please try again."
                )

            self.user = user
            return self.cleaned_data

        except Exception as e:
            raise forms.ValidationError(f"An error occurred: {str(e)}")

    def get_user(self):
        return getattr(self, "user", None)


# ------------------------------
# ITEM FORM (for admin dashboard)
# ------------------------------
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'price', 'image', 'category']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name', 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number', 'class': 'form-control'}),
            'address': forms.TextInput(attrs={'placeholder': 'Delivery address', 'class': 'form-control'}),
        }
