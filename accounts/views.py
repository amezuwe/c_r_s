from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from django.contrib import messages


@transaction.atomic
def register(request):
	if request.method == 'POST':
		user_form = SignUpForm(request.POST)
		profile_form = ProfileForm(request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			username = user_form.cleaned_data.get('username')
			user.refresh_from_db() #This will load the Profile created by Signal
			profile_form = ProfileForm(request.POST, instance=user.profile) # Reload the profile form with the profile instance
			profile_form.full_clean() # Manually clean the form this time. It's implicitly called by "is_valid()" method
			profile_form.save()
			messages.info(request, "Your account has been successfully created!")
			login(request, user)
			messages.info(request, f"You are now logged in as {username}.")
			return redirect('camper:list')
		else:
			messages.error(request, "Correct the errors below")
	else:
		user_form = SignUpForm()
		profile_form = ProfileForm()
	return render(request, 'accounts/register.html', {'user_form': user_form, 'profile_form': profile_form})

def login_request(request):
	if request.method =='POST':
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = (form.cleaned_data.get('password'))
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}")
				return redirect('camper:list')
			else:
				messages.error(request, "Invalid username or password")
		else:
			messages.error(request, "Invalid username or password")
	else:
		form = AuthenticationForm()
	return render(request, 'accounts/login.html', {'form': form})

def logout_request(request):
	logout(request)
	messages.info(request, "You are logged out successfully!")
	return redirect('camper:home')
