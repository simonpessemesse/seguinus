
from django.conf.urls import patterns, include, url
from django.contrib import admin


from telephones import views

urlpatterns = [
	url(r'^$',  views.index),
	]
