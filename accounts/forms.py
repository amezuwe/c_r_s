from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(forms.ModelForm):
	email = forms.EmailField(max_length=150, required=True)
	local_church = forms.CharField(max_length=200, required=True)
	class Meta:
		model = Profile
		fields = ('phone', 'email', 'district', 'local_church')

#############
class SignUpForm(UserCreationForm):
	username = forms.CharField(max_length=12)

	class Meta:
		model = User
		fields = ('username', 'password1', 'password2',)
