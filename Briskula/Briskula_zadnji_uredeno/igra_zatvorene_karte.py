import pygame, sys          #This module provides access to some variables used or maintained by the interpreter and to
from pygame.locals import *        #tu se QUIT nalzi...pygame.locals.konstant mozemo pisati samo konstant
import time

from Briskula_klasa import * 
from UCT_briskula import *
from heuristike import *

import pygame._view

def main():
    pygame.init()
    b=briskula()
    b.pocetak()
    b.play()
    runda = 1
    while True:
        b.postavi_karte_na_stol()
        #print b.print1()
        if(b.pobjednik==1):     #prvo igra comp, pa covjek
            b.igra_comp()
            b.igra_covjek()
        else:                   #prvo igra covjek, pa comp
            b.igra_covjek()
            b.igra_comp()
        b.kraj_runde()
        #print "kraj runde: " +str(runda)
        #print b.bodovi
        runda+=1


main()
