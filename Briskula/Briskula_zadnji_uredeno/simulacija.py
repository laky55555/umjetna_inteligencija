import pygame, sys          #This module provides access to some variables used or maintained by the interpreter and to
from pygame.locals import *        #tu se QUIT nalzi...pygame.locals.konstant mozemo pisati samo konstant
import time
    
from Briskula_klasa import * 
from UCT_briskula import *
from heuristike import *


brojac = 0
for i in range (10):
    #print "prosa sam jedan krug"
    b = briskula()
    #print b.karte
    b.podjeli_karte_na_pocetku(0)
    b.podjeli_karte_na_pocetku(1)
    runde = 1
    iteracija = 0
    b.postavi_briskulu()
    while True:
        """print "na pocetku runde ima jos karti za podjeliti:    "  + str(len(b.karte))
        print str(runde)+  ". runda"
        print str(len(b.karte_igraca[1]))+ "  broj karti " + str(len(b.karte_igraca[0]))
        print b.bodovi"""
        runde +=1
        #print "jos jedna iteracija"
        if(b.pobjednik == 1):
            #print "prije igranja runde stanje je :"+b.print1()
            #print "prije uct a"
            #if verbose = True ne ispisuje nista
            odluka_compa = UCT(rootstate = b, itermax = 5000, verbose = True,brojac = iteracija)
            #print "prije do move od compa"
            b.DoMove(odluka_compa)
            iteracija+=1
            #print "nakon do move od compa"
            odluka_covjeka = odaberi_kartu_za_bacanje(b,2, 0)
            b.DoMove(odluka_covjeka)
            iteracija+=1
            #print "nakon do move od covjeka"

        else:
            #print "prije igranja runde stanje je :"+b.print1()
            odluka_covjeka = odaberi_kartu_za_bacanje(b,1, 0)
            b.DoMove(odluka_covjeka)
            iteracija+=1
            odluka_compa = UCT(rootstate = b, itermax = 1000, verbose = True, brojac = iteracija)
            b.DoMove(odluka_compa)
            iteracija+=1
        #print "igrac 0 ima karti: " + str(len(b.karte_igraca[0]))
        #print len(b.izasle)
        #time.sleep(2)
        if(len(b.karte_igraca[0])==0):
            print "Heuristika: "+str(b.bodovi[0])+", UCT: "+str(b.bodovi[1])
            #print "gubitnik ima "+str(b.bodovi[1-b.pobjednik])

            if(b.bodovi[1]>60):
                brojac +=1
            break
        
print "UCT je pobjedio: "+str(brojac)+" puta"
 

