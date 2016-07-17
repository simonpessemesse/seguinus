from django.forms.models import inlineformset_factory
from django import forms
from django.forms import ModelForm
from django.forms.formsets import formset_factory
from chambres.models import Chambre, Souci, Client, Reservation, Tache, Amour, CacheJour, Entite, TourOperateur
from easyPoS.models import Paiement, MoyenPaiement


class NonEncaissesForm(forms.Form):
    montantCheque = forms.DecimalField()


# commentaire=forms.CharField()

class BonKdoForm(forms.Form):
    client = forms.CharField()


class PaiementForm(forms.Form):
    montant = forms.DecimalField()
    moyen = forms.ModelChoiceField(queryset=MoyenPaiement.objects.all())


class ClientForm(forms.Form):
    montantChequeNonEncaisse = forms.DecimalField()
    divers = forms.CharField()
    paiements = formset_factory(PaiementForm, extra=1)
