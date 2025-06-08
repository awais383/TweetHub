from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from PIL import Image


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
       


class userRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo']  

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')

        if photo:
            img = Image.open(photo)

            min_width = 300
            min_height = 300
            max_width = 1920
            max_height = 1080

            width, height = img.size

            if width < min_width or height < min_height:
                raise forms.ValidationError(
                    f"Image is too small. Minimum size is {min_width}x{min_height}px."
                )

            if width > max_width or height > max_height:
                raise forms.ValidationError(
                    f"Image is too large. Maximum size is {max_width}x{max_height}px."
                )

        return photo        
        
# class userRegistrationForm(UserCreationForm):
#     email = forms.EmailField()

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password1', 'password2')


# class LoginForm(forms.Form):
#     username = forms.CharField(
#         label='Username',
#         max_length=150,
#         widget=forms.TextInput(attrs={
#             'class': 'bg-gray-700 text-white border-2 border-gray-600 rounded-lg w-full p-2 text-base focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder-gray-400',
#             'placeholder': 'Enter username',
#             'autocomplete': 'username',
#         })
#     )
#     password = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput(attrs={
#             'class': 'bg-gray-700 text-white border-2 border-gray-600 rounded-lg w-full p-2 text-base focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder-gray-400',
#             'placeholder': 'Enter password',
#             'autocomplete': 'current-password',
#         })
#     )
#     remember_me = forms.BooleanField(
#         required=False,
#         label='Remember Me',
#         widget=forms.CheckboxInput(attrs={
#             'class': 'text-teal-500 focus:ring-teal-400',
#         })
#     )