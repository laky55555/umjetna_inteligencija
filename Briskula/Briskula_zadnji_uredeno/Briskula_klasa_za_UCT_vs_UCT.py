import copy
import random                            #functions that interact strongly with the interpreter = sys
from UCT_briskula import *

import time

#klasa Briskula
class briskula:
        def __init__(self, num_players=2):
                self.players = num_players #broj igraca, 2 ili 4
                self.karte = []
                self.izasle = []
                for i in range (40):
                    self.karte.append(i)
                self.karte_igraca = {} #i-tom igracu pridruzujemo listu karata koje su mu na raspolaganju
                self.karte_za_bacanje=[]  #cuva indekse karti koje se bacaju
                for i in range (self.players):
                    self.karte_za_bacanje.append(-1)        #tu cuvamo index karte koja je odabana za bacanje
                self.pobjednik=1    # 0 ako je pobjedio 1 igrac, 1 ako je pobjedio 2 igrac
                self.bodovi = [0, 0]
                self.player_na_potezu = 2   #gleda se 1 ili 2 igrac (2 igrac je komp, ako je pobjednik 1, onda je pobjedio 2 igrac)
                self.broj_karti_na_stolu =0

        #Napravi kopuiju svega tako da simulacija ne utjece na orginal igru
        def Clone(self):
                """ Create a deep clone of this game state.
                """
                st = briskula()
                st.karte_igraca =copy.deepcopy( self.karte_igraca)
                st.briskula = self.briskula
                st.izasle=copy.deepcopy(self.izasle)
                st.karte = copy.deepcopy(self.karte)
                st.karte_za_bacanje =copy.deepcopy( self.karte_za_bacanje)
                st.bodovi = copy.deepcopy(self.bodovi)
                st.player_na_potezu = self.player_na_potezu
                st.pobjednik = self.pobjednik
                st.broj_karti_na_stolu= self.broj_karti_na_stolu
                return st

        #baca kartu koju odluci igrac, poziva ga DoMove, pomocna funkcija DoMove-u
        def baci_kartu(self, move):
                self.karte_za_bacanje[self.player_na_potezu-1]=move
                self.izasle.append(self.karte_igraca[self.player_na_potezu-1][move])
                self.karte_igraca[self.player_na_potezu-1].remove(self.karte_igraca[self.player_na_potezu-1][move])
                self.broj_karti_na_stolu+=1

        #napravi update pobjednika, i njegovih bodova
        def update_pobjednika_i_bodova(self):
                vektor= self.trenutno_uzima(self.players)
                self.bodovi[vektor[1]%2]+=vektor[0]
                self.pobjednik = vektor[1]
                self.player_na_potezu = vektor[1]+1

        #dijeli karte normalno (uvijek random)
        def podijeli_karte(self):
                for i in range (self.player_na_potezu-1, self.players+self.player_na_potezu-1):
                        self.karte_igraca[i%self.players].append(self.dodjeli_kartu())

        def podijeli_karte_zadnji_put(self):
                for i in range (self.player_na_potezu-1, self.players+self.player_na_potezu-2):
                        self.karte_igraca[i%self.players].append(self.dodjeli_kartu())
                self.karte_igraca[self.player_na_potezu%self.players].append(self.briskula)
                
                

        #kako znati kada je zadnji krug, kada moramo dodjeliti briskulu
        def DoMove(self, move):
                """ Update a state by carrying out the given move.
                    Must update player_na_potezu.
                """        
                self.baci_kartu(move)
                if(self.broj_karti_na_stolu == self.players):   #ako su svi u rundi bacili kartu moramo naci i napraviti update na pobjedniku te, podijeliti karte
                        self.update_pobjednika_i_bodova()
                        if(len(self.karte) == self.players-1):
                                self.podijeli_karte_zadnji_put()
                        if(len(self.karte)> self.players):
                                self.podijeli_karte()
                        self.broj_karti_na_stolu = 0
                else:
                        self.player_na_potezu += 1
                        if (self.player_na_potezu > self.players):
                                self.player_na_potezu -= self.players
                        #self.player_na_potezu = 3-self.player_na_potezu
                                

    #ovisno koji je igrac na potezu treba heuristike
        def GetMoves(self):
                """ Get all possible moves from this state.
                """
                """#return [i for i in range (len(self.karte_igraca[self.player_na_potezu]))]
                lista = []
                vektor = []
                #print str(len(self.izasle)) + "  " + str(self.players-1)
                if(len(self.izasle)%self.players == self.players-1):
                    vektor = self.igram_zadnji_nesmijem(self.player_na_potezu-1)
                    #print "ulazi u IF"
                    #print "tu ispiujem vektor "+str(vektor)
                else:
                    vektor = self.igram_prvi_nesmijem(self.player_na_potezu-1)
                #print "vektor je "+str(vektor)
                s = set(vektor)
                #print vektor
                for i in range (len(self.karte_igraca[self.player_na_potezu-1])):
                    if i in s:
                        continue
                    else:
                        lista.append(i)
                """
                #moguci potezi su SVI!!!
                lista = []
                for i in range (len(self.karte_igraca[self.player_na_potezu-1])):
                    lista.append(i)
                
                return lista

        def GetResult(self, playerjm):
                """ Get the game result from the viewpoint of playerjm. 
                """
                if playerjm==2 and self.bodovi[1]>self.bodovi[0]:
                    return 1
                elif playerjm == 1 and self.bodovi[0]>self.bodovi[1]:
                    return 1
                elif self.bodovi[0]==self.bodovi[1]:
                    return 0.5
                else:
                        return 0

        def print1(self):
                """ Don't need this - but good style.
                """
                s = "comp: "
                for i in range (len(self.karte_igraca[1])):
                    s+=str(self.karte_igraca[1][i])+" "
                s+="covjek "
                for i in range (len(self.karte_igraca[0])):
                    s+=str(self.karte_igraca[0][i])+" "
                s+=" na potezu je igrac "+str(self.player_na_potezu)
                s+=" stanje bodova "+str(self.bodovi[0])+"|"+str(self.bodovi[1])
                s+=" briskula je "+str(self.briskula)
                return s
        
        def dodjeli_kartu(self):
                index=random.randint(0, len(self.karte)-1)   #slucajan odabir jednog broja(karte) od preostalih
                vratiti = self.karte[index]      #lista[index]=karta
                self.karte.remove(self.karte[index])  #izbacimo iskoristenu kartu
                return vratiti
    
        def podjeli_karte_na_pocetku(self, igrac):
                self.karte_igraca[igrac]=[]
                for i in range (3):     #podjela karata na pocetku
                    self.karte_igraca[igrac].append(self.dodjeli_kartu())

        def postavi_briskulu(self):
                self.briskula=self.karte[random.randint(0, len(self.karte)-1)]
                self.karte.remove(self.briskula)        #briskulu maknemo iz karti ali NE stavljamo je u iskoristene
                
        def poeni(self,karta1):
                if karta1%10 == 0 or karta1%10 == 1 or karta1%10 == 2 or karta1%10 == 3 or karta1%10 == 4:
                    return 0
                elif karta1%10 == 5 or karta1%10 == 6 or karta1%10 == 7:
                    return karta1%10-3
                elif karta1%10 == 8:
                    return 10
                else:
                    return 11

        def je_li_briskula(self, karta):        #vraca 1 ako je poslana karta briskula
                if(karta/10 == self.briskula/10):
                        return 1
                return 0

        def tko_je_pobjedio(self):
                vektor = self.trenutno_uzima(2)
                self.pobjednik = vektor[1] 
                self.bodovi[self.pobjednik%2]+=vektor[0]
        
        #vraca BODOVE na stolu, IGRACA koji je uzeo i KARTU koja uzima
        #za slucaj grafika ovo radi jer se tek na kraju karte igraca updataju
        #za doMove nije dobro jer se u njemu ponisiti karta koja je bacena
        #zato je bolje korisitit self.izasle
        def trenutno_uzima(self, broj_karti_na_stolu):
                a = []          #lista koja ima bodove na stolu, pobjednika, i najjacu kartu
                for i in range (3):
                    a.append(0)
                najveca_briskula = -1
                najveca_prva_boja = -1
                poeni_u_krugu = 0
                #ova for petlja nade najjacu kartu na stolu   treba samo jos naci ko ju je bacio
                for i in range(broj_karti_na_stolu):
                    nova_karta = self.izasle[len(self.izasle)- broj_karti_na_stolu + i]    #ucitavanje karata koje su na stolu
                    if i==0:
                        prva_karta = nova_karta
                    poeni_u_krugu += self.poeni(nova_karta)
                    if (self.je_li_briskula(nova_karta) and nova_karta>najveca_briskula): #provjera je li karta briskula
                        najveca_briskula = nova_karta
                    if (nova_karta/10 == prva_karta/10 and nova_karta>=prva_karta ): #provjera je li karta iste boje kao prva
                        najveca_prva_boja = nova_karta


                if(najveca_briskula != -1):     #ako ima briskule na stolu
                    #u self.player_na_potezu imamo igraca koji je prvi igrao, npr 1.igrac onda je karta koju je on bacio predzadnja u listi izisle
                    if(self.izasle[len(self.izasle)-2]==najveca_briskula):
                        a[0] = poeni_u_krugu
                        a[1] = self.pobjednik
                        a[2] = najveca_briskula
                        return a
                    else:
                        a[0] = poeni_u_krugu
                        a[1] = (self.pobjednik+1)%2
                        a[2] = najveca_briskula
                        return a
                        
                else:
                    if(self.izasle[len(self.izasle)-2]==najveca_prva_boja):
                        a[0] = poeni_u_krugu
                        a[1] = self.pobjednik
                        a[2] = najveca_prva_boja
                        return a
                    else:
                        a[0] = poeni_u_krugu
                        a[1] = (self.pobjednik+1)%2
                        a[2] = najveca_prva_boja
                        return a

        def koja_je_to_karta(self, karta):
                figura = ""
                if(karta%10==0):
                    broj = "dvojka"
                if(karta%10==1):
                    broj = "cetvroka"
                if(karta%10==2):
                    broj = "petica"
                if(karta%10==3):
                    broj = "sestica"
                if(karta%10==4):
                    broj = "sedmica"
                if(karta%10==5):
                    broj = "fant"
                if(karta%10==6):
                    broj = "caval"
                if(karta%10==7):
                    broj = "rel"
                if(karta%10==8):
                    broj = "trica"
                if(karta%10==9):
                    broj = "as"
                if(karta/10==0):
                    figura = "spad"
                if(karta/10==1):
                    figura = "kop"
                if(karta/10==2):
                    figura = "dinari"
                if(karta/10==3):
                    figura = "bastoni"
                return str(broj) + "  od  " + str(figura)











        
 
