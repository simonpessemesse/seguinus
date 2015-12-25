from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'seguinus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^chambres/',include('chambres.urls')),
	url(r'^taches/',include('taches.urls')),
	url(r'^menus/',include('menus.urls')),
	url(r'^$','chambres.views.racine'),

	url(r'^collectage/', include('collectage.urls')),
	url(r'^restaurant/', include('restaurant.urls' )),
	url(r'^telephones/', include('telephones.urls')),
	url(r'^easyPoS/', include('easyPoS.urls')),

	url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

