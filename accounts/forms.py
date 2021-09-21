
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django import forms
from .models import CustomUser, Profile, Address

error = {
    'required': 'این فیلد اجباری است',
    'invalid': 'ایمیل شما نامعتبر است',
}


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


    def clean_user_name(self):
        user = self.cleaned_data['username']
        if CustomUser.objects.filter(username=user).exists():
            raise forms.ValidationError('user exist')
        return user
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('این ایمیل از قبل وجود دارد')
        return email


    def clean_password_2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 !=password2:
            raise forms.ValidationError('password not math')
        elif len(password2)<8:
            raise forms.ValidationError('password too short')
        elif not any (x.isupper for x in password2):
            raise forms.ValidationError('پسورد شما باید حداقل یک حرف بزرگ داشته باشد')
        return password1


class UserLoginForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField()

"""
for our model using model form
"""


class UserUpdateForm(forms.ModelForm):
    class Meta:
         model = CustomUser
         fields=['email','first_name','last_name','date_joined']



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone','company','fax']



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country','city','state','street','street_2','postal_code']