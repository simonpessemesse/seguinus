from collectage.models import Plage, Personne, Employe, HeurePlanifiee, Individu, Contrat, Pourboire, DonPourboire
from django.contrib import admin
from django import forms


class ChangeSizeChambresAssigneesForm(forms.ModelForm):
    class Meta:
        model = Pourboire
        exclude = ()
        widgets = {
            'individus': forms.SelectMultiple(attrs={'size': 25})
        }


class PlageAdmin(admin.ModelAdmin):
    list_filter = ('personne', 'heureFin')


class HeurePlanifieeAdmin(admin.ModelAdmin):
    save_as = True


class PersonneAdmin(admin.ModelAdmin):
    list_display = (
    'nom', 'heureNormaleDebutTravailMatin', 'heureNormaleDebutTravailAprem', 'nbHeuresParSemaine', 'actif')


class ContratAdmin(admin.ModelAdmin):
    pass


# fields = ('individu','dateDebut',	'dateFin',	'emploi',	'typeDuContrat' ,	'nombreHeuresSemaine',	'nbRepasJour',	'fonction', 'tauxHoraireBrut')
admin.site.register(Plage, PlageAdmin)
admin.site.register(Personne, PersonneAdmin)
admin.site.register(HeurePlanifiee, HeurePlanifieeAdmin)
admin.site.register(Employe)
admin.site.register(Individu)
admin.site.register(Contrat, ContratAdmin)


class PB(admin.ModelAdmin):
    form = ChangeSizeChambresAssigneesForm


admin.site.register(Pourboire, PB)
admin.site.register(DonPourboire)
