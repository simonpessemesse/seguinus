from chambres.models import Chambre,Souci,Client,Reservation,Tache,Amour,TourOperateur,Entite,TacheLog
from django import forms
from django.contrib import admin

from django.db.models.signals import pre_save,pre_delete
from django.dispatch import receiver


class ChambreAdmin(admin.ModelAdmin):
	ordering=('-note',)
	class Meta:
		ordering = ['-note']
	
class SouciAdmin(admin.ModelAdmin):
	list_filter = ( 'chambre',)

class ChangeSizeChambresAssigneesForm(forms.ModelForm):
	class Meta:
		model = Reservation
		widgets = {
			'chambresAssignees': forms.SelectMultiple(attrs={'size': 30})
		}
		exclude=()



class ClientInline(admin.StackedInline):
	model = Reservation
	extra = 1
	form = ChangeSizeChambresAssigneesForm
	fieldsets = (
			(None, {
				'fields': (('dateArrivee', 'dateDepart'),('chambres', 'chambresSingle','chambresDoubles','chambresTwin'),('placesDortoir','chambresTriples','chambresQuadruples','chambresQuintuples'),('chambresAssignees','nbEnfants'))
				}),
			)
	


class ReservationAdmin(admin.ModelAdmin):
	pass

class ClientAdmin(admin.ModelAdmin):
	fieldsets = (
			(None, {
				'fields': (('nom', 'tourOperateur','optionJusquau'),('divers','protege','surbooking'))
				}),)
			
	search_fields = ['nom']
	inlines = [ClientInline]

class TacheAdmin(admin.ModelAdmin):
	search_fields = ['description']
	fieldsets = (
			(None, {
				'fields': ('description', ('date','rappel'), ('priorite','entite'))
				}),
			('Options Avancees', {
				'classes': ('collapse',),
				'fields': ('chaqueLundi', 'chaqueMardi', 'chaqueMercredi','chaqueJeudi','chaqueVendredi','chaqueSamedi','chaqueDimanche','expiration')
				}),
			)
	


admin.site.register(Chambre,ChambreAdmin)
admin.site.register(Souci,SouciAdmin)
admin.site.register(Client,ClientAdmin)
admin.site.register(Tache,TacheAdmin)
admin.site.register(Amour)
admin.site.register(TacheLog)
admin.site.register(Entite)
admin.site.register(TourOperateur)
admin.site.register(Reservation,ReservationAdmin)
