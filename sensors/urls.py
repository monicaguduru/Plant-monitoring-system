from django.conf.urls import url
from . import views
from django.contrib.auth.views import login,logout

app_name='sensors'

urlpatterns = [
    # /sensors/
	url(r'^home/$', views.index , name='index'),
	url(r'^display/$', views.new_disp, name="new_disp"),
	url(r'^display/macrographs/$', views.macrographs, name="macrographs"),
	url(r'^display/table/$', views.table, name="table"),
	url(r'^display/table2/$', views.table2, name="table2"),
	url(r'^display/soilmoisture/$', views.soil, name="soilmoisture"),
	url(r'^display/(?P<temperature>[0-9]+.[0-9]+)/(?P<humidity>[0-9]+.[0-9]+)/(?P<plant1_soilmoisture>[0-9]+.[0-9]+)/(?P<plant2_soilmoisture>[0-9]+.[0-9]+)/(?P<waterlevel>[0-9]+.?[0-9]*)/(?P<ms>[0-9]+.?[0-9]*)/(?P<r>[0-9]+.?[0-9]*)/',views.Display,name="Display"),
	#To add plant
	url(r'^plant/add/$',views.AddPlant.as_view(),name='plant-add'),
    	url(r'^update/(?P<pk>\d+)/$',views.UpdatePlant.as_view(),name='plant-update '),
    	url(r'^delete/(?P<d>\d+)/$',views.delete,name='delete '),
	#set
	url(r'^display/set/$', views.set1, name="set1"),
	url(r'^display/set/show/$', views.setshow, name="set-show"),
	url(r'^display/set/(?P<motorstate>[0-9]+.[0-9]+)/', views.set2, name="motorsta"),
	#For user login/register/logout
	url(r'^login/$',login,{'template_name':'sensors/login.html'}),
	url(r'^logout/$',logout,{'template_name':'sensors/logout.html'}),
	url(r'^register/$',views.register,name="register")

]
