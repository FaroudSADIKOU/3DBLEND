Pour installer l'add-on, ne pas hésiter à lire "Tuto installation.txt"
Les diagrammes du projet sont disponibles dans le dossier "DiagrammesProjet" (classes...)

Outre ces diagrammes voici le fonctionnement global du programme :

Il s'agit d'un Add-on (plugin) pour Blender faisant intervenir l'usage du Leap Motion

toute la logique du code est dans le dossier BlenderAddOn/leaplib. 
Dossier qui contiendra l'addon en lui-même.
Le fichier AddOn_PanelWithButtons.py est le fichier principal qui une fois importé dans Blender, permettra le lancement 
des différentes opérations 3D dans l'onglet "3DBLEND" en bas à droite de l'interface de blender pour peu qu'un Leap motion soit
connecté à l'ordinateur
En plus des bouttons déclenchant les opréations 3D (tranform, deform...), il y a également présence du boutton "use Leap"
qui utilisera en plus la reconaissance de geste pour se passer de l'usage de la souris. (expérimental)
Ce boutton déclenche le lancement du modal "AddOn_MainModalReco" qui va se mettre à l'écoute du module de reconaissance de geste 
(contenu dans handTracking) et recevra des entrée de type "1", ou "A" et qui se tâchera alors de lancer tel ou tel module 3D selon.
Les classes des modules 3D sont contenu dans les autres fichier du type "AddOn_Deform", "AddOn_SimpleTransform..." etc...
le fichier interactions.txt contient les informations d'interactions et le déclenchement actuellement implémenté