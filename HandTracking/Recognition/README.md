# HAND POSTURE RECOGNITION

## Dataset

### Presentation of the database

We've decided to buil our own dataset made of the 8 following gestures:
1, 2, 4, A, B, O, ROCK and V.

*Images bellow*:

### Détails de suivi des mouvements

Selon la documentation,
> The instantaneous frame rate:
The rate at which the Leap Motion software is providing frames of data (in frames per second). The frame rate can fluctuate depending on available computing resources, activity within the device field of view, software tracking settings, and other factors.

En temp normal le leap motion renvoi 30 frame par seconde.
En cas de mouvement rapide ou très rapide, on est respectivement à $55 fps$ ou $115 fps$.

Sur une fenêtre de $1/2$ secondes, on collectionne les différentes postures prédicte par le modèle par frame. Ce qui donne entre $55/2$ et $115/2$ frames.

On détermine le nombre de frame classée commeétant une représenation de tel ou tel frame. Ensuite on en déduis la posture la plus prédite avec le pourcentage de présence.
Avant de renvoyer cette classe de geste, il faut que le pourcentage calculé soit supérieur à 60% au moins lorsque le nombre de geste candidat dans cette fenêtre de 1/2 seconde est inferieur à 3.
Si nons on répète la même action sur une autre fenêtre.

**ATTENTION :** FAUDRAIT PREVOIR ARRÊTER LA BOUCLE UN MOMENT !!!