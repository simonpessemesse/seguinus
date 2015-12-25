from django.template import RequestContext

from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from datetime import datetime,date,timedelta
from chambres.models import Chambre,Souci,Client,Reservation,Tache,Amour
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django import forms

jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]


#def resasCommunes(setIn,setOut):
#	setCommun=set()
#	for resa in setIn:
#		for out in setOut:
#			if(
#	return setCommun

#def rempliSetAdequat(resaInit,resas):
#	setIn=set(resaInit)
#	setOut=set(resas)-setIn
#	commun,setOut=resasCommunes(setIn,setOut)
#	while commun:
#		setIn=setIn|commun
#		commun,setOut=resasCommunes(setIn,setOut)
#	return setIn

def cmpD(a):
	return a[0]

def formatte(jour):
	return jours[jour.weekday()]+" "+str(jour.day)+"/"+str(jour.month)

def caseTab(checked,chambre,jour):
	value=str(chambre.id)+"_"+str(jour)
	pre="<td title=\""+chambre.nom+" le "+formatte(jour)+"\"><input type=\"checkbox\" name=\""+"magie"+"\" value=\""+value+"\""
	post=">"+"</td>"
	if(checked):
		result= " checked "
	else:
		result=""
	return pre+result+post


def cmpResa(x):
	return x.nom.lower()

def interieur(resas):
	dictParDate=dict()
	for r in resas:
		for numJour in range((r.dateDepart-r.dateArrivee).days):
			jour=r.dateArrivee+timedelta(numJour)
			if jour in dictParDate:
				dictParDate[jour].append(r)
			else:
				dictParDate[jour]=[r]

	liste=[(cle,valeur) for (cle,valeur) in list(dictParDate.items())]
	liste.sort(key=cmpD)

	chs=Chambre.objects.all().order_by('nom')
	ch=[c for c in chs]
	ch.sort(key=cmpResa)
	chs=ch
	result="<tr><td />"
	for jour in liste:
		result+="<th>"+formatte(jour[0])+"</th>"
	for i in chs:
		result+="<tr><th title=\""+i.nom+"\">"+i.nom+"</th>"
		for jour in liste:
			assignees=set()
			for resa in jour[1]:
				assignees|=set([ch for ch in resa.chambresAssignees.all()])

			if(i in assignees):
				result+=caseTab(True,i,jour[0])
			else:
				result+=caseTab(False,i,jour[0])
		result+="</tr>"
	result+="</tr><tr>"
	result+="<th>Dortoir</th>"
	for jour in liste:
		totalPlDortoir=0
		for resa in jour[1]:
			totalPlDortoir+=resa.placesDortoir
		result+="<td><INPUT type=\"text\" size=\"1\" value=\""+str(totalPlDortoir)+"\" name=\""+str(jour[0])+"\"></td>"

	result+="</tr>"
	return result

def strToDate(str):
	da=str.split("-")
	datee=date(int(da[0]),int(da[1]),int(da[2]))
	return datee

def ajouterCleValeur(dico,cle,valeur):
	if cle in dico:
		dico[cle].append(valeur)
	else:
		dico[cle]=[valeur]

def crec(resum,sejours):
	jours=list(resum.keys())
	jours.sort()
	deb=None
	allEmpty=True
	for j in jours:
		if(resum[j]==0):
			if deb:
				key=(deb,j)
				if key in sejours:
					sejours[key]+=1
				else:
					sejours[key]=1
				deb=None
			else:
				pass #ajouter sejours du prec
		else:
			allEmpty=False
			if not deb:
				deb=j
			resum[j]-=1
	if deb:
		key=(deb,jours[-1]+timedelta(1))
		if key in sejours:
			sejours[key]+=1
		else:
			sejours[key]=1

	if not allEmpty:
		return crec(resum,sejours)
#	print sejours
	return sejours
	

def calculeDortoir(resum):
	sejours=dict()
	result=crec(resum,sejours)
#	for (deb,fin),item in result.iteritems():
#		print(str(deb)+" au "+str(fin)+" de "+str(item))
	return result

@login_required
def index(request,resa):

	laResa=Reservation.objects.get(pk=resa)
	resas=Reservation.objects.filter(client__id=laResa.client.id)


	if request.method == 'POST': # If the form has been submitted...
		dortoirs=[ddd for ddd in request.POST.lists() if ddd[0]!= "magie" and ddd[0]!="referer" and ddd[0]!="csrfmiddlewaretoken"]
		resumeDortoir=dict()
		for d in dortoirs:
			dateDor=strToDate(d[0])
			resumeDortoir[dateDor]=int(d[1][0])
		resultDortoir=calculeDortoir(resumeDortoir)

		magie=request.POST.getlist("magie")
		dicoParChambre=dict()
		for m in magie:
			r=m.split("_")
			numCh=r[0]
			ch=Chambre.objects.get(pk=int(numCh))
			dateR=strToDate(r[1])
			if ch in dicoParChambre:
				dicoParChambre[ch].append(dateR)
			else:
				dicoParChambre[ch]=[dateR]
		dicoParSejour=dict()
		for (cle,valeur) in list(dicoParChambre.items()):
			valeur.sort()
			debutCourant=courant=valeur[0]
			finCourant=debutCourant+timedelta(1)
			for i in range(1,len(valeur)):
				cc=valeur[i]
				if (cc-courant).days==1:
					courant=cc
					finCourant=courant+timedelta(1)
				else:
					ajouterCleValeur(dicoParSejour,(debutCourant,finCourant),cle)
					debutCourant=courant=cc
					finCourant=debutCourant+timedelta(1)
			ajouterCleValeur(dicoParSejour,(debutCourant,finCourant),cle)
		for res in resas: #on supprime les vieilles resas
			res.delete()
		for ((c1,c2),valeur) in list(dicoParSejour.items()):
			plDor=0
			if (c1,c2) in list(resultDortoir.keys()):
				plDor=resultDortoir[(c1,c2)]
				del resultDortoir[(c1,c2)]
			resa=Reservation(client=laResa.client,dateArrivee=c1,dateDepart=c2,chambres=len(valeur),placesDortoir=plDor)
			resa.save()
			for ch in valeur:
				resa.chambresAssignees.add(ch)
			resa.save()
		for ((c1,c2),valeur) in list(resultDortoir.items()):
			resa=Reservation(client=laResa.client,dateArrivee=c1,dateDepart=c2,placesDortoir=valeur)
			resa.save()
		return HttpResponseRedirect(request.POST["referer"]+"#recapitulatif")

	tableau="<table border>" + interieur(resas) + "</table>"
	if "HTTP_REFERER" in request.META:
		referer=request.META["HTTP_REFERER"]
	else:
		referer=""
	return render_to_response('chambres/magie.html', {'tableau':tableau,'id':resa,'referer':referer},context_instance=RequestContext(request))

