from .models import Contact

from django.contrib import admin


class ContactAdmin(admin.ModelAdmin):
    search_fields = ['nomTags']


admin.site.register(Contact, ContactAdmin)
