from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

class plant(models.Model):
	plantname=models.CharField(max_length=255)
	cityname= models.CharField(max_length=255)
	latitude=models.CharField(max_length=50)
	longitude=models.CharField(max_length=50)
	def get_absolute_url(self):
		return reverse('sensors:index')
	def __str__(self):
		return self.plantname+"-"+self.cityname

class plantdetails(models.Model):
	idOfPlant = models.ForeignKey(plant,on_delete=models.CASCADE,default=0)
	soilmoisture=models.FloatField(default=0)
	actuatorstate=models.CharField(max_length=50)
	dateAndTime=models.CharField(max_length=255)
	temperature = models.FloatField(default=0)
	humidity = models.FloatField(default=0)
	waterlevel=models.FloatField(default=0)
	rainfall=models.CharField(max_length=50)
	ms=models.FloatField(default=0)
	msdisplay=models.CharField(max_length=50)
	def __str__(self):
		return str(self.dateAndTime)

class Manual(models.Model):
    motorstate = models.FloatField(default=0)

class UserProfile(models.Model):
	user = models.OneToOneField(User)

#creates new account
def create_profile(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)
