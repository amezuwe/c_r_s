from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class District(models.Model):
    name = models.CharField(max_length=200)
    
    class Meta:
    	ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email = models.EmailField(max_length=150)
	phone = models.CharField(max_length=10)
	district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
	local_church = models.CharField(max_length=200, blank=True)
	balance = models.IntegerField(default=0)

	class Meta:
		ordering = ['district']

	def __str__(self):
		return self.user.username


@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created,	**kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()
	

