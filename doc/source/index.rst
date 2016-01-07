.. seguinus documentation master file, created by
   sphinx-quickstart on Thu Dec 24 16:44:16 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to seguinus's documentation!/Bienvenue sur la doc de seguinus
=====================================================================

Seguinus est un logiciel de gestion d'hôtel/restaurant trés personnalisé 

Intro
-----

Aprés 6 ans d'utilisation et de développement, je publie pour qui voudra Seguinus, un logiciel de facturation et de gestion de reservations d'hôtel/restaurant principalement, et accessoirement de suivi d'heures, de rappel de taches, de fournisseurs et produits, ainsi qu'un mini repertoire telephonique. Sa licence est GPL V3

Son architecture est originale, reposant sur django pour la partie ORM, avec une interface mixte web/PyQt, web pour la majorité de l'application (toute la partie reservations, un bout de la partie facturation) et PyQt pour la partie edition des factures du logiciel de facturation. 

Seguinus est prevu pour une utilisation en local en monoutilisateur/monoposte. Toutes les données sont stockées sur la machine et sont gérées par l'orm de django, donc la base de données peut être sqlite, mysql, postgresql. 

**Attention, ce projet est un vrai bordel avec des trucs sales dans tous les sens et un code trés peu nettoyé**

Il a au debut été developpé et utilisé sous windows, maintenant il l'est uniquement sous linux, mais ca devrait fonctionner a peu prés sur toutes les plateformes ayant django et pyqt fonctionnel (quoique pour la sauvegarde en gpg il y aurait peut etre des modifications a faire)

Philosophie
-----------

Le but de ce projet est surtout personnel, en effet, c'est mon outil de travail, ayant recemment changé de secteur professionnel, passant de l'informatique à l'hotellerie restauration dans une auberge. 
J'ai donc commencé a developper en utilisant la methode de la rache un ensemble de petits programmes qui me servaient au quotidien, en y rajoutant petit a petit des fonctionnalités, certaines s'averaient utiles, d'autres non, et j'en suis arrivé a cet ensemble que je publie a présent.
Je ne souhaite pas forcement en faire un logiciel libre à succés avec plein d'utilisateurs, mais j'ai pris la decision de le publier car il peut toujours servir pour d'autres auberges/hotels/restaurant et puis il est toujours interessant d'avoir un retour.
Ce projet est hautement fait sur mesure pour l'utilisation que j'en fait, par consequent il n'est surement pas adapté en l'état pour n'importe quelle auberge/hotel/restaurant.

Architecture
------------

Tout repose sur django, avec pour des raisons de simplicité de deploiement sqlite comme base de données, mais moyennant quelques modification mineures, le programme devrait parfaitement fonctionner avec n'importe base de données prise en charge par django.
Pour l'instant il est compatible avec django 1.2, pour les autres versions, cela devrait etre possible de le faire fonctionner en changeant deux trois trucs.
La majorité de l'application est web, en local, cependant la partie d'edition des factures est en PyQt, avec une fenêtre par facture, car l'interface devait être optimisée pour la saisie et les modification rapides de factures (quand on a 20 factures à preparer en 2 minutes a la fin d'un gros service c'est bien pratique tiens!) 
Etant fainéant par nature, j'utilise extensivement l'interface d'administration de django pour ajouter/editer/supprimer les reservations/taches/produits. Il en resulte une ergonomie parfois douteuse, mais un reel allegement de code chiant écrire.
La premiere partie a avoir ete developpee est la partie des reservations, puis est venue la gestion des taches, la facturation, et enfin le suivi des heures.

Gestion des reservations
------------------------

C'est ce qui a été développé en premier, cette partie est entierement en django, et utilise l'interface d'administration de django pour créer/editer/supprimer les données. A partir d'une date d'arrive, de depart, d'un nombre de chambres single/double/triple/quadruples ou quintuples, et eventuellement des chambres assignees, est calculé pour chaque jour demandé les arrivées, departs, les chambres libres ce jour la, quelles sont les chambre ou il faut juste faire le menage, et celles ou il faut tout nettoyer, et egalement cela permet de savoir combien de personnes vont manger au restaurant le soir, ainsi que leur menu. Il y a egalement un tableau qui recapitule pour une periode donnée les chambres horizontalement ainsi que les jours verticalement, et chaque case est remplie par la personne qui occupe cette chambre cette nuit la. Une couleur unique est assignée a la case à partir du hash du nom de la personne.


Fonctionnalitées de tueur
-------------------------

Si on veut (et je veux) le systeme envoie un email tous les jours à partir 20h à une adresse specifiée dans preference.py avec comme pièce jointe l'integralité de la base de données en json comprésée, cryptée en gpg avec une clef publique specifiée dans seguinus/crypto/crypteEtSauveMonBiniou.py. Donc, en cas de perte de disque dur ou vol d'ordinateur pendant la nuit, il est enfantin de restaurer un systeme dans l'etat ou il etait la veille a 20h, en clonant le depot mercurial, et utilisant la fonction loadata de django pour importer des données. C'est fait le soir pour ne pas perdre toutes les données ajoutées dans la journée. ( les vols etant souvent la nuit )
Il faut savoir que le logiciel est en production depuis 2009 pour la partie reservations, et fin 2010 pour la partie facturation, et que pour l'instant la base de données ainsi compressée ne pese "que" 450Ko ( sachant que le fichier de la base de données sqlite pese 4Mo )


Comment tester
--------------

Il est necessaire d'avoir python3, PyQt4 et django d'installé (python-qt4 et python-django sous debian)
django doit être dans une version >= 1.8

Pour pouvoir utiliser la sauvegarde cryptée automatique par mail il faut egalement gnupg d'installé.

J'ai fait une version pour que vous puissiez le tester facilement sous linux, (qui marche peut être sous windows mais je n'ai rien pour tester), il suffit de copier le dêpot git depuis github:

::

  git clone https://github.com/simonpessemesse/seguinus.git
  cd seguinus
  sh init.bash
  python3 easyPoS_run.py



telecharger et decompresser le tar.bz2 de https://bitbucket.org/auberge/seguinus/downloads puis d'aller dans le repertoire auberge-seguinus-4ff7312c004f recemment crée, et de tapoter dans son xterm un petit python run.py
On verra alors apparaitre à l'écran la fenetre de la liste des factures. 
En cliquant sur resumé, on verra apparaitre dans une fenetre de son navigateur favori une page de login. Si elle n'apparrait pas, essayer de redemarrer le serveur web en cliquant droit sur l'icone du petit chien qui doit etre dans la zone de notification et choississez "redemarrer programme"
Le nom d'utilisateur/mot de passe pour tester est test/test
Et voila, vous voila sur une sorte de tableau de bord de la partie facturation. Pour la partie gestion de reservations cliquetez sur GESTION HOTEL ou allez a http://127.0.0.1:8000/chambres/today 

Captures d'écran
----------------
.. image:: _static/im.png 


.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

