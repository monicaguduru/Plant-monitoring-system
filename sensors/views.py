from django.shortcuts import render,get_object_or_404,redirect
from .models import plant,plantdetails,Manual
from django.http import HttpResponse
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from django.forms.models import model_to_dict
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from sensors.forms import RegistrationForm
from datetime import datetime

#redirecting to main/home page


def register(request):
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/sensors/login/')
	else:
		form = RegistrationForm()
	return render(request,'sensors/reg_form.html',{'form':form})

#sending last 10 sensor values to respected pages
def macrographs(request):
	det = plant.objects.get(pk=11)
	a=plantdetails.objects.filter(idOfPlant=det.id)[::-1]
	x=a[len(a)-10:len(a)-1:]
	return render(request ,'sensors/macro.html',{'x':x,'user':request.user})

def table(request):
	det = plant.objects.get(pk=11)
	a=plantdetails.objects.filter(idOfPlant=det.id)[::-1]
	plant1=a[len(a)-10:len(a)-1:]
	det = plant.objects.get(pk=12)
	b=plantdetails.objects.filter(idOfPlant=det.id)[::-1]
	plant2=b[len(b)-10:len(b)-1:]
	details=zip(plant1,plant2)
	return render(request ,'sensors/table.html',{'details':details,'user':request.user})

def table2(request):
	p=plant.objects.all()
	return render(request ,'sensors/table2.html',{'p':p,'user':request.user})


def soil(request):
	det = plant.objects.get(pk=11)
	a=plantdetails.objects.filter(idOfPlant=det.id)[::-1]
	plant1=a[len(a)-10:len(a)-1:]
	det = plant.objects.get(pk=12)
	a=plantdetails.objects.filter(idOfPlant=det.id)[::-1]
	plant2=a[len(a)-10:len(a)-1:]
	return render(request ,'sensors/soil.html',{'plant1':plant1,'plant2':plant2,'user':request.user})

def Display(request,temperature=None,humidity=None,plant1_soilmoisture=None,plant2_soilmoisture=None,waterlevel=None,r=None,ms=None):
	plant1=plantdetails()
	plant2=plantdetails()
	det = plant.objects.get(pk=11)
	plant1.idOfPlant=det
	#all_users=course.objects.filter(courseId=det.id)
	plant1.soilmoisture=plant1_soilmoisture
	plant1.temperature=temperature
	plant1.humidity=humidity
	plant1.waterlevel=waterlevel
	if ms==0.0:
	    plant1.msdisplay="..."
	elif ms==100.0:
	    plant1.msdisplay="MOTOR-1 TURNED OFF AUTOMATICALLY !"
	elif ms==110.0:
	    plant1.msdisplay="MOTOR-2 TURNED OFF AUTOMATICALLY !"


	if plant1.soilmoisture<20.0 and float(r)<30.0:
	    plant1.actuatorstate="ON( PLANT-1 NEEDS WATER !)"
	else:
	    plant1.actuatorstate="OFF(PLANT-1 DOESN'T NEED WATER !)"

	det = plant.objects.get(pk=12)
	plant2.idOfPlant=det
	plant2.soilmoisture=plant2_soilmoisture
	plant2.temperature=temperature
	plant2.humidity=humidity
	plant2.waterlevel=waterlevel
	if plant2.soilmoisture<20.0 and float(r)<30.0:
	    plant2.actuatorstate="ON( PLANT-2 NEEDS WATER !)"
	else:
	    plant2.actuatorstate="OFF(PLANT-2 DOESN'T NEED WATER !)"
	if float(r)>100.0:
	    plant1.rainfall="RAINING"
	    plant2.rainfall="RAINING"
	else:
	    plant1.rainfall="NOT RAINING"
	    plant2.rainfall="NOT RAINING"
	plant1.save()
	plant2.save()
	return render(request ,'sensors/template/index.html',{'plant1':plant1,'plant2':plant2,'user':request.user})

#sending latest sensor data to template
def new_disp(request):
	det = plant.objects.get(pk=11)
	a=plantdetails.objects.filter(idOfPlant=det.id)[::-1]
	plant1=a[0]
	det1 = plant.objects.get(pk=12)
	b=plantdetails.objects.filter(idOfPlant=det1.id)[::-1]
	plant2=b[0]
	p=plant.objects.all()
	return render(request ,'sensors/template/index.html',{'p':p,'plant1':plant1,'plant2':plant2,'user':request.user})

def index(request):
	return render(request,'sensors/index.html/',{'user':request.user})

def delete(d=None):
	a=plant.objects.get(pk=d)
	a.delete()
	det = plant.objects.get(pk=11)
	a=plantdetails.objects.filter(idOfPlant=det.id)
	plant1=a[0]
	det1 = plant.objects.get(pk=12)
	b=plantdetails.objects.filter(idOfPlant=det.id)
	plant2=b[0]
	p=plant.objects.all()
	return render(request ,'sensors/template/index.html',{'p':p,'plant1':plant1,'plant2':plant2,'user':request.user})

class AddPlant(CreateView):
	model = plant
	fields=['cityname','plantname','latitude','longitude']

class UpdatePlant(UpdateView):
	model = plant
	fields=['cityname','plantname','latitude','longitude']

class DeletePlant(DeleteView):
	model = plant
	success_url=reverse_lazy('core:index')

def set1(request):
    #state2 = Sensors()
    #state2.motorstate2=float(motorstate2)
    #state2.save()
    det = plant.objects.get(pk=11)
    a=plantdetails.objects.filter(idOfPlant=det.id)[::-1]
    plant1=a[0]
    return render(request,'sensors/set.html/',{'plant1':plant1})
def set2(request,motorstate=None):
    state = Manual()
    state.motorstate=float(motorstate)
    state.save()
    return render(request ,'sensors/set1.html',{'state':state})

def setshow(request):
    state = Manual.objects.get(pk=Manual.objects.count())
    return render(request ,'sensors/set1.html/',{'state':state})
