from django.urls import path, include
from .views import index, camper_list, camper_form_new, camper_form_update, camper_delete, dashboard

app_name = 'camper'

urlpatterns = [
    path('', index, name='home'),
    path('campers/list/', camper_list, name='list'),
    path('campers/new/', camper_form_new, name='form'),
    path('campers/<int:id>/', camper_form_update, name='update'),
    path('campers/delete/<int:id>/', camper_delete, name='delete'),
    path('dashboard', dashboard, name='dashboard'),
]
