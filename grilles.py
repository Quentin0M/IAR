import numpy as np
import copy

# Grille de base
grille1 = np.ones((13,13))
grille1[0,:] = 0
grille1[12,:] = 0
grille1[:,0] = 0
grille1[:,12] = 0
grille1[:,6] = 0
grille1[6,:6] = 0
grille1[7,6:] = 0
grille1[6,2] = 1
grille1[3,6] = 1
grille1[10,6] = 1
grille1[7,9] = 1
grille1[8,2] = 2

# Grille avec fenetres
grille2 = copy.copy(grille1)
grille2[0,2] = 3
grille2[0,9] = 3
grille2[3,0] = 3
grille2[3,12] = 3
grille2[10,0] = 3
grille2[10,12] = 3
grille2[12,2] = 3
grille2[12,9] = 3

# grille avec ouverture au milieu
grille3 = copy.copy(grille1)
grille3[6,6] = 1

