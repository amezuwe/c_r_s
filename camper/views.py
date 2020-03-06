from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Camper
from .forms import CamperForm
from django.contrib import messages
from accounts.models import Profile


def index(request):
	return render(request, 'index.html')

### Camper list
@login_required(login_url='accounts:login')
def camper_list(request):
	user = request.user
	camper_list = Camper.objects.filter(created_by=user)
	return render(request, 'camper/list.html', {'camper_list': camper_list})

### Camper form: New
@login_required(login_url='accounts:login')
def camper_form_new(request):
	user = request.user
	user_profile = Profile.objects.get(user=user)
	user_profile_balance = user_profile.balance
	registration_fee = 80
	# Checking for balance
	if user_profile_balance < registration_fee:
			messages.info(request, f"Your balance is GHS {user_profile_balance}, which is insufficient. Kindly top up!", extra_tags='alert-danger')
			return redirect('camper:list')
	if request.method=='POST':
		form = CamperForm(request.POST, initial={'created_by': user})
		if form.is_valid():
			form.save()
			user_profile.balance = user_profile_balance - registration_fee
			user_profile.save()
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			messages.success(request, f"{first_name} {last_name} has been successfully registered as a camper. Your balance is now GHS {user_profile.balance}.")
			return redirect('camper:list')
	else:
		form = CamperForm(initial={'created_by': user})
	return render(request, 'camper/form.html', {'form': form})

### Camper Update form
@login_required(login_url='accounts:login')
def camper_form_update(request, id):
	user = request.user
	camper = get_object_or_404(Camper, pk=id)
	if camper.created_by.id != user.id:
		messages.info(request, "You are not authorized to do this.", extra_tags='alert-danger')
		return redirect('camper:list')
	if request.method=='POST':
		form = CamperForm(request.POST, instance=camper)
		if form.is_valid():
			form.save()
			first_name = form.cleaned_data.get('first_name')
			last_name = form.cleaned_data.get('last_name')
			messages.success(request, f"{first_name} {last_name} has been successfully updated.")
			return redirect('camper:list')
	else:
		form = CamperForm(instance=camper)
	return render(request, 'camper/form.html', {'form': form})


### Camper Delete
@login_required(login_url='accounts:login')
def camper_delete(request, id):
	user = request.user
	camper = get_object_or_404(Camper, pk=id)
	if camper.created_by.id != user.id:
		messages.info(request, "You are not authorized to do this.", extra_tags='alert-danger')
		return redirect('camper:list')
	user_profile = Profile.objects.get(user=user)
	registration_fee = 80
	first_name = camper.first_name
	last_name = camper.last_name
	camper.delete()
	user_profile.balance = user_profile.balance + registration_fee
	user_profile.save()
	messages.info(request, f"{first_name} {last_name} has been deleted as a camper. Your balance is now GHS {user_profile.balance}", extra_tags='alert-danger')
	return redirect('camper:list')

### Camper Dashboard
@login_required(login_url='accounts:login')
def dashboard(request):
	user = request.user
	user_profile = Profile.objects.get(user=user)
	campers_info = Camper.objects.filter(created_by=user)
	genders = [g.gender for g in campers_info]
	gender_total = len(genders)
	gender_male = genders.count('M')
	gender_female = genders.count('F')

	return render(request, 'camper/dashboard.html', {'user_profile': user_profile, 'gender_total': gender_total, 'gender_male': gender_male, 'gender_female': gender_female})
