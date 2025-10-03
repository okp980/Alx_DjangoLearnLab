from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from blog.models import User


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError()("Email already exists")
        return email
    
class ProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'profile_photo']

    def clean_profile_photo(self):
        profile_photo = self.cleaned_data.get('profile_photo')
        if profile_photo and profile_photo.size > 1024 * 1024 * 5:
            raise forms.ValidationError()("Profile photo must be less than 5MB")
        return profile_photo