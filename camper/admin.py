from django.contrib import admin
from .models import DifferentClasses, Camper
from datetime import date

admin.site.site_header = "G.A. East Youth Camp 2020"
admin.site.site_title = "G.A. East Youth Camp 2020 Admin Area"
admin.site.index_title = "Welcome to the G.A. East Youth Camp 2020 Admin Area"


class CamperAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'phone', 'different_class', 'created_by', 'local_church', 'district', 'calculate_age')
	list_filter = ('gender',)
	search_fields = ['last_name', 'different_class']
	prepopulated_fields = {}

	def local_church(self, obj):
		return obj.created_by.profile.local_church
	local_church.short_description = 'CB_Loc_Church'

	def district(self, obj):
		return obj.created_by.profile.district
	district.short_description = 'CB_District'

	def calculate_age(self, obj):
		today = date.today()
		birth_date = obj.date_of_birth
		age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
		return age
	calculate_age.short_description = "Age"


admin.site.register(DifferentClasses)
admin.site.register(Camper, CamperAdmin)
