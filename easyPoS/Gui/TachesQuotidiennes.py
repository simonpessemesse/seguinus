import logging
from easyPoS.models import DonneesEntreprise
from restaurant.models import Resa
from chambres.models import Chambre, Souci, Client, Reservation, Tache, Amour, TourOperateur
from collectage.models import Contrat, Individu
from collectage.views import registreDuPersonnel
from chambres.views import OneDayStats
from datetime import datetime, date, timedelta
from datetime import time
import save
import SauvegardeEtMaintenance
import preferences

logging.basicConfig(level=preferences.LOGGING_LEVEL)


def creeSiExistePasTache(desc, jour=date.today(), priorite="B", heure=None):
    logging.info("on m'a demande de voir pour la tache: " + desc)
    taches = Tache.objects.filter(description__startswith=desc)
    if len(taches) == 0:
        task = Tache(description=desc, date=jour, priorite="M", rappel=heure)
        task.save()


def nettoieAllotements():
    logging.info("on nettoie allotements")
    try:
        inn = TourOperateur.objects.get(nom="Inn Travel")
        inn.nettoieAllotements()
    except:
        print("inn travel n'existe pas")


def souhaiteAnniversaires():
    logging.info("on regarde les anniv")
    inds = Individu.objects.all()
    for i in inds:
        #		logging.info(i)
        t = date.today()
        if i.dateNaissance:
            anniv = date(t.year, i.dateNaissance.month, i.dateNaissance.day)
            diff = (anniv - t).days
            if diff > 0 and diff < 10:
                creeSiExistePasTache(i.anniv(t.year), anniv - timedelta(2), "H", time(18, 36, 22))


def mutuelleInscriptionDesinscription():
    logging.info("on regarde mutuelles")
    contrats = Contrat.objects.all()
    t = date.today()
    for c in contrats:
        if c.dateFin:
            diff = abs((c.dateFin - t).days)
            if diff < 7 and ((c.dateFin - c.dateDebut).days) > 32:
                logging.info("date fin de " + str(c))
                text = "Faire les papiers ANI de " + str(c.individu)
                logging.info(text)
                creeSiExistePasTache(text, t, "H")
    if t.day in [1, 2, 3]:
        logging.info("debut mois on regarde la mutuelle si il faut donner des papiers")
        for c in contrats:
            if c.dateDebut:
                d = t - timedelta(15)
                if d.year == c.dateDebut.year and d.month == c.dateDebut.month and (
                    (not c.dateFin) or ((c.dateFin - c.dateDebut).days) > 32):
                    text = "Donner les papier pour la mutuelle a " + str(c.individu)
                    logging.info(text)
                    creeSiExistePasTache(text, t, "H")


def trouveMagiquementTourOp():
    rs = Client.objects.all()
    tt = TourOperateur.objects.all()

    for c in tt:
        tou = (c.nom.replace(" ", "")).lower()
        for r in rs:
            if tou in r.nom.replace(" ", "").lower() and not r.tourOperateur:
                logging.info("on va mettre tourop a " + str(r))
                r.tourOperateur = c
                r.save()


def envoieOccupationOfficeTourisme():
    logging.info("on prepare occupation OT")
    txt = "Occupation de l'auberge pour les prochains jours\n"
    for i in range(7):
        jour = date.today() + timedelta(i)
        txt += "Pour le {0}, ".format(jour.strftime("%A %d %B"))
        stats = OneDayStats(jour)
        txt += "il y a {0} places libres au dortoir et {1} chambres\n".format(stats.nbPlacesLibreDortoir,
                                                                              30 - stats.chambresReservees)
    SauvegardeEtMaintenance.envoieOccupation(txt)
    logging.info("occup envoyee")


def saveDb():
    logging.info("on sauve db")
    #			save.EnvoieParMail()
    SauvegardeEtMaintenance.dumpDatabase()
    logging.info("sauve db a fonctionne")


def creerTachePicNicPlusieursJours(r, tourOp=False):
    for i in range((r.dateDepart - r.dateArrivee).days):
        jour = r.dateArrivee + timedelta(i)
        if tourOp:
            desc = str(
                r.nbPersonnes()) + " pique nique pour " + r.client.nom + " de " + r.client.tourOperateur.nom + " le " + str(
                jour) + " ?? Se renseigner "
        else:
            desc = str(r.nbPersonnes()) + " pique nique pour " + r.client.nom + " le " + str(
                jour) + " ?? Se renseigner "
        creeSiExistePasTache(desc, jour, "M", time(10, 36, 22))


def creerTachesPiqueNique():
    logging.info("on regarde les picnic")
    t = date.today()
    resas = Reservation.objects.filter(dateArrivee=t)
    for r in resas:
        if r.client.tourOperateur:
            logging.info("faut il un pn pour :" + str(r) + " ????")
            if (r.client.tourOperateur.nom == "Inn Travel" and "Allotement" not in r.client.nom) or (
                    "Chemins" in r.client.tourOperateur.nom and r.nbPersonnes() > 4):
                desc = str(
                    r.nbPersonnes()) + " pique nique pour " + r.client.nom + " de " + r.client.tourOperateur.nom + " le " + str(
                    t)
                creeSiExistePasTache(desc, r.dateDepart - timedelta(1), "M", time(10, 36, 22))
            elif r.client.tourOperateur.nom == "Walk inn" and r.nbPersonnes() > 4:
                creerTachePicNicPlusieursJours(r, True)
            else:
                logging.info("PAs de PN")
        if r.client.asPicnicDansLeNom():
            creerTachePicNicPlusieursJours(r)


def confirmeResasAvecArrhesOuDuPasse():
    logging.info("on regarde resas avec arrhes")
    clientsNonConfirmes = Client.objects.filter(optionJusquau__isnull=False)
    for c in clientsNonConfirmes:
        arrhes = c.arrhe_set.all()
        if len(arrhes) != 0:
            logging.info("on va enlever option a " + str(c) + " car " + str(arrhes))
            c.optionJusquau = None
            c.save()
        resas = c.reservation_set.all()
        if not resas:
            logging.info("on va enlever option a " + str(c) + " car il n'y a pas de resa")
            c.optionJusquau = None
            c.save()
        for r in resas:
            if r.dateArrivee <= date.today():
                logging.info("on va enlever option a " + str(c) + " car " + str(r))
                c.optionJusquau = None
                c.save()


def descriptionChangement(resD, resA):
    chD = ",".join([ch.nom for ch in resD.chambresAssignees.all()])
    if resD.placesDortoir != 0:
        chD += ", " + str(resD.placesDortoir) + " dortoir)"
    chA = ",".join([ch.nom for ch in resA.chambresAssignees.all()])
    if resA.placesDortoir != 0:
        chA += ", " + str(resA.placesDortoir) + " dortoir)"
    return "Renommer les bons de " + resD.client.nom + " de (" + chD + ") vers (" + chA + ")"


def creerTacheChangementChambre():
    logging.info("on regarde les changements de chambre")
    demain = date.today() + timedelta(1)
    resaDep = Reservation.objects.filter(dateDepart=demain)
    resasArr = Reservation.objects.filter(dateArrivee=demain)
    for rDep in resaDep:
        for rArr in resasArr:
            if rDep.client.id == rArr.client.id:
                desc = descriptionChangement(rDep, rArr)
                creeSiExistePasTache(desc, rDep.dateDepart, "H")


def trouvePensionComplete():
    from chambres.repas import trouveNomSpecialSiIlExiste
    logging.info("trouve pension complete")
    dateDemandee = date.today()
    reservations = Reservation.objects.filter(dateArrivee__lte=dateDemandee).filter(dateDepart__gt=dateDemandee)
    for r in reservations:
        if "#" in r.client.nom:
            nom = trouveNomSpecialSiIlExiste(r.client.nom) + "#"
            resas = Resa.objects.filter(jour=dateDemandee).filter(nom=nom)
            if len(resas) == 1:
                resas[0].nb += r.nbPersonnes()
                resas[0].save()
            else:
                resa = Resa(nom=nom, nb=r.nbPersonnes(), nbEnfants=0, jour=dateDemandee)
                resa.save()


def remplisRegistreDuPersonnel():
    logging.info("on regarde registre personnel")
    reg = registreDuPersonnel()
    for r in reg:
        creeSiExistePasTache("ajouter dans registre personnel " + str(r.individu) + " debut le " + str(r.debut),
                             heure=time(1, 3, 2))


def go():
    remplisRegistreDuPersonnel()
    trouvePensionComplete()
    nettoieAllotements()
    confirmeResasAvecArrhesOuDuPasse()
    souhaiteAnniversaires()
    trouveMagiquementTourOp()
    envoieOccupationOfficeTourisme()
    mutuelleInscriptionDesinscription()
    creerTachesPiqueNique()
    creerTacheChangementChambre()
    if preferences.AUTOSAVE:
        saveDb()

    donnees = DonneesEntreprise.objects.get(id=preferences.ENTREPRISE)
    donnees.derniereSauvegarde = datetime.now()
    donnees.save()
