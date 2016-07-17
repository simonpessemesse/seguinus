from easyPoS.models import Tva, Categorie, Produit, MoyenPaiement, Facture, Paiement, LigneFacture, DonneesEntreprise, \
    Arrhe, Famille, RemiseCheque, PreparationFacture, LogFacture
from django.contrib import admin
from chambres.models import Client


class ResaInline(admin.StackedInline):
    model = Client
    max_num = 1
    extra = 0
    exclude = ()


class PaiementInline(admin.StackedInline):
    model = Paiement
    fieldsets = (
        (None, {
            'fields': (('montant', 'moyenPaiement'), ('date'))
        }),)
    max_num = 1
    exclude = ('facture', 'entreprise', 'numero', 'valide')
    extra = 0


class ArrheAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('montantChequeNonEncaisse', 'date'), ('divers'))
        }),)
    inlines = [PaiementInline]
    exclude = ('client',)


class PaiementAdmin(admin.ModelAdmin):
    exclude = ('facture', 'entreprise', 'arrhe', 'numero', 'valide')


admin.site.register(Tva)
admin.site.register(Famille)
admin.site.register(PreparationFacture)
admin.site.register(LogFacture)
admin.site.register(Categorie)
admin.site.register(Produit)
admin.site.register(MoyenPaiement)
admin.site.register(Facture)
admin.site.register(RemiseCheque)
admin.site.register(Paiement, PaiementAdmin)
admin.site.register(LigneFacture)
admin.site.register(DonneesEntreprise)
admin.site.register(Arrhe, ArrheAdmin)
