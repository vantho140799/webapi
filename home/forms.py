# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import PricingPlan
class CustomUserCreationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, help_text='Required. 150 characters or fewer.')
    email = forms.EmailField(required=True, help_text='Required.')
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='Required.')
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='Required. Enter the same password as above, for verification.')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user
class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, help_text='Enter your username.')
    password = forms.CharField(widget=forms.PasswordInput, required=True, help_text='Enter your password.')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password")
        return self.cleaned_data
class PricingPlanForm(forms.ModelForm):
    class Meta:
        model = PricingPlan
        fields = ['plan_name', 'price', 'description', 'item', 'image'] 