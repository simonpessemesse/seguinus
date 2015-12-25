from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime,date,timedelta
from chambres.models import Chambre,Souci,Client,Reservation,Tache,Amour,TourOperateur
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django import forms
from django.forms.extras.widgets import SelectDateWidget



class TourOpSearch(forms.Form):
	dateDebut = forms.DateField(required=True,initial=date(date.today().year,1,1))
	#dateDebut = forms.DateField(required=False,widget=SelectDateWidget())
	dateFin = forms.DateField(required=True,initial=date.today)
	operateur = forms.ModelChoiceField(queryset=TourOperateur.objects.filter(actif=True))
		

class RapportTourOp():
	pass

def parDateArrivee(a):
	return a.dateArrivee
@login_required
def index(request):
	result=[]
	if request.method == 'POST': # If the form has been submitted...
		form = TourOpSearch(request.POST) # A form bound to the POST data
		if form.is_valid(): # All validation rules pass
			r=RapportTourOp()
			r.dateDebut = form.cleaned_data['dateDebut']
			r.dateFin = form.cleaned_data['dateFin']
			if not r.dateDebut:
				r.dateDebut=date(1999,1,1)
			if not r.dateFin:
				r.dateFin=date.today()
			r.operateur=form.cleaned_data['operateur']
			clients=r.operateur.client_set.all()
			resas=[]
			r.nuitsDortoir=0
			r.nuitsSingle=0
			r.nuitsDp2p=0
			r.nuitsDp3p=0
			r.nuitsDp4p=0
			r.nuitsDp5p=0
		
			for c in clients:
				for resa in c.reservation_set.all():
					if(r.dateDebut < resa.dateDepart and r.dateFin > resa.dateArrivee):
						r.nuitsDortoir+=resa.placesDortoir*resa.nbNuits()
						r.nuitsDp2p+=resa.chambres*resa.nbNuits()
						r.nuitsSingle+=resa.chambresSingle*resa.nbNuits()
						r.nuitsDp2p+=resa.chambresTwin*resa.nbNuits()
						r.nuitsDp2p+=resa.chambresDoubles*resa.nbNuits()
						r.nuitsDp3p+=resa.chambresTriples*resa.nbNuits()
						r.nuitsDp4p+=resa.chambresQuadruples*resa.nbNuits()
						r.nuitsDp5p+=resa.chambresQuintuples*resa.nbNuits()
						resas.append(resa)

			resas.sort(key=parDateArrivee)
			r.list=resas

			result=r
	else:
		form = TourOpSearch() # An unbound form

	return render_to_response('chambres/tourOperateurs.html', {
		'form': form,'result':result},
		context_instance=RequestContext(request))



@login_required
def index2(request):
	tourOp = TourOperateur.objects.all()
	return render_to_response('chambres/tourOperateurs.html', {'tourOp':tourOp})
