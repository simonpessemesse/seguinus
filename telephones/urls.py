
from django.conf.urls import patterns, include, url
from django.contrib import admin
from chambres import views



urlpatterns = patterns('telephones.views',
	url(r'^$', 'index'),
	)
