import time
    
from Briskula_klasa_za_UCT_vs_UCT import * 
from UCT_briskula import *

###Unese se zeljeni broj iteracija za svaki utc, te broj rundi igranja
###Ako se zeli mijenjati koeficijent iz MCTS treba ga promijeniti u UCT_briskula.py
###Ako se zeli igrati UCT vs UCT s razlicitim koeficijentima treba pozvat UCT() i UCT2(),
###     te njihove koeficijenti postaviti u UCT_briskula.py

broj_iteracija_UCT1 =  input("Koliko iteracija UCT1? ")
broj_iteracija_UCT0 = input("Koliko iteracija UCT0? ")
broj_igri = input("Koliko rundi igranja? ")


brojac = 0
ukupno_briskula = 0
for i in range (broj_igri):
        #print "prosa sam jedan krug"
        b = briskula()
        #print b.karte
        b.podjeli_karte_na_pocetku(0)
        b.podjeli_karte_na_pocetku(1)
        runde = 1
        broj_briskula = 0
        briskule=[]
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
                        odluka_UCT1 = UCT2(rootstate = b, itermax = broj_iteracija_UCT1, verbose = True,brojac = iteracija)
                        #print "prije do move od compa"
                        if(b.je_li_briskula(b.karte_igraca[1][odluka_UCT1])):
                                broj_briskula += 1
                                briskule.append(b.karte_igraca[1][odluka_UCT1])
                
                        #print str(b.karte_igraca[1]) + "  briskula je " + str(b.briskula)
                        b.DoMove(odluka_UCT1)
                        iteracija+=1
                        #print "nakon do move od compa"
                        odluka_UCT0 = UCT(rootstate = b, itermax = broj_iteracija_UCT0, verbose = True,brojac = iteracija)
                        b.DoMove(odluka_UCT0)
                        iteracija+=1
                        #print "nakon do move od covjeka"

                else:
                        #print "prije igranja runde stanje je :"+b.print1()
                        odluka_UCT0 = UCT(rootstate = b, itermax = broj_iteracija_UCT0, verbose = True,brojac = iteracija)
                        b.DoMove(odluka_UCT0)
                        iteracija+=1
                        odluka_UCT1 = UCT2(rootstate = b, itermax = broj_iteracija_UCT1, verbose = True, brojac = iteracija)
                        if(b.je_li_briskula(b.karte_igraca[1][odluka_UCT1])):
                                broj_briskula += 1
                                briskule.append(b.karte_igraca[1][odluka_UCT1])
                        b.DoMove(odluka_UCT1)
                        iteracija+=1
                #print "igrac 0 ima karti: " + str(len(b.karte_igraca[0]))
                #print len(b.izasle)
                #time.sleep(2)
                if(len(b.karte_igraca[0])==0):
                        print str(i) + ":runda;    UCT0: "+str(b.bodovi[0])+", UCT1: "+str(b.bodovi[1])
                        print "UCT1 je imao:  " + str(broj_briskula) + "  briskula: " + str(briskule)
                        ukupno_briskula += broj_briskula
                        #print "gubitnik ima "+str(b.bodovi[1-b.pobjednik])

                        if(b.bodovi[1]>60):
                                brojac +=1
                        break
print
print "UCT1 je pobjedio: "+str(brojac)+ " / " + str(broj_igri)+  " igri, i imao je: "  + str(ukupno_briskula)
print "UCT0 je igrao s " + str(broj_iteracija_UCT0) + " iteracija, a UCT1 s " + str(broj_iteracija_UCT1)
 

