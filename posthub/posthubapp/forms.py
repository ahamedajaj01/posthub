from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, UserProfile

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=50, label="UserName",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter your username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder': 'Enter your email'}))
    phone = forms.CharField(max_length=10,label="Mobile Number", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.Please use the different one.")
        return email
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if UserProfile.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This number is already exits.Please use different one.")
        return phone


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(user=user, phone=self.cleaned_data['phone'])
            return user

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter your password'})
    )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','image','content']
