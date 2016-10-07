import copy
import random                            #functions that interact strongly with the interpreter = sys
from heuristike import *
from UCT_briskula import *

import pygame, sys          #This module provides access to some variables used or maintained by the interpreter and to
from pygame.locals import *        #tu se QUIT nalzi...pygame.locals.konstant mozemo pisati samo konstant
import time

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

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
                ctypes.windll.user32.SetProcessDPIAware()



        def pocetak(self): 
                #self.SCREEN_SIZE= (1000, 600)      #velicina ekrana...(VODORAVNO, OKOMITO)
                self.infoObject = pygame.display.Info()
                self.x =int(self.infoObject.current_w)
                self.y=int(self.infoObject.current_h)
                self.SCREEN_SIZE = (self.x, self.y)
                self.green = (0, 128, 0)
                pygame.display.set_icon(pygame.image.load("icona.jpg"))
                self.screen = pygame.display.set_mode(self.SCREEN_SIZE, 0, 32)        #SCREEN_SIZE, FULLSCREEN, 32
                pygame.display.set_caption("Briscola")       #naslov
                self.slike_load=[]
                for i in range(40):
                        self.slike_load.append(pygame.image.load("karte2/slika"+str(i)+".jpg"))
                self.opposite = pygame.image.load("opposite1.jpg")
                self.play_img = pygame.image.load("play.png")
                self.next_img = pygame.image.load("next.png")
                self.exit_img = pygame.image.load("exit.jpg")
                self.winner_img = pygame.image.load("winner.png")
                self.loser_img = pygame.image.load("loser.jpg")
                self.usklicnik_img = pygame.image.load("usklicnik.jpg")
                self.rect0 = []      #covjekove karte
                self.rect1 = []      #compove_karte

                
                
                
        def postavi_karte_na_stol(self):
                brojac=0
                self.screen.fill(self.green)
                if(len(self.izasle)==0):
                        self.podjeli_karte_na_pocetku(0)
                        self.podjeli_karte_na_pocetku(1)
                        self.postavi_briskulu()
                #print self.print1()
                for i in range (len(self.karte_igraca[0])):
                        #print "ispisujemo duljinu karata 0 tog i 1 igraca"
                        #print len(self.karte_igraca[0])
                        #print len(self.karte_igraca[1])
                        self.rect0.append(self.screen.blit(self.slike_load[self.karte_igraca[0][i]], (0.05*self.x+brojac, 0.6*self.y)))
                        #self.rect1.append(self.screen.blit(self.slike_load[self.karte_igraca[1][i]], (20+brojac, 50)))
                        self.rect1.append(self.screen.blit(self.opposite, (0.05*self.x+brojac, 0.05*self.y)))
                        brojac+=150
                brojac=0
                if len(self.karte)!=0 and self.karte[0]!=-1:
                        rotate=pygame.transform.rotate(self.slike_load[self.briskula], 90)     #rotiranje
                        self.screen.blit(rotate, (0.65*self.x, 0.15*self.y))
                        for i in range (len(self.karte)):
                                self.screen.blit(self.opposite, (0.75*self.x+brojac, 0.10*self.y))
                                brojac+=1
                if(len(self.karte)==1):
                        self.screen.blit(self.usklicnik_img, (0.90*self.x+brojac, 0.2*self.y))
                pygame.display.update()
                #time.sleep(1)
        def kraj_runde(self):
                nasao = 0
                pocetak = 0
                font1 = pygame.font.Font("C:/Windows/Fonts/arial.TTF", 30)
                if len(self.karte_igraca[0])==0:
                        self.screen.fill(self.green)
                        """text1 = font1.render("kraj igre", 1, (10, 10, 10))
                        text2 = font1.render("igraj novu igru", 1, (10, 10, 10))"""
                        text3 = font1.render("You: "+str(self.bodovi[0]), 1, (10, 10, 10))
                        text4 = font1.render("Computer: "+str(self.bodovi[1]), 1, (10, 10, 10))
                        rect_tmp1 = self.screen.blit(self.exit_img, (0.5*self.x, 0.5*self.y))
                        rect_tmp2 = self.screen.blit(self.play_img, (0.5*self.x, 0.70*self.y))
                        self.screen.blit(text3, (0.05*self.x, 0.05*self.y))
                        self.screen.blit(text4, (0.05*self.x, 0.10*self.y))
                        if(self.bodovi[0]>self.bodovi[1]):
                                self.screen.blit(self.winner_img, (0.05*self.x, 0.20*self.y))
                        else:
                                self.screen.blit(self.loser_img, (0.05*self.x, 0.2*self.y))
                        pygame.display.update()
                        while True:
                                for event in pygame.event.get():
                                        if event.type == QUIT:
                                                pygame.quit()           #suprotno od pygame.init()
                                                sys.exit() 
                                        if event.type == MOUSEBUTTONDOWN:
                                                pozicija = pygame.mouse.get_pos()
                                                if rect_tmp1.collidepoint(pozicija):        #kraj igre
                                                        pygame.quit()           #suprotno od pygame.init()
                                                        sys.exit()
                                                if rect_tmp2.collidepoint(pozicija):        #igramo novu igru
                                                        pocetak = 1
                                                        self.__init__()
                                                        self.pocetak()
                                                        break
                                if pocetak==1:
                                        break
                                
                        if pocetak==1:
                            self.bodovi=[0, 0]
                            self.izasle = []
                            self.karte = []
                            self.player_na_potezu = 2
                            for i in range (40):
                                    self.karte.append(i)
                else:
                        rect_tmp = self.screen.blit(self.next_img, (0.15*self.x, 0.4*self.y))
                        pygame.display.update()
                        while True:
                                for event in pygame.event.get():
                                        if event.type == MOUSEBUTTONDOWN:
                                                pozicija = pygame.mouse.get_pos()
                                                if rect_tmp.collidepoint(pozicija):
                                                        del self.rect0[:]
                                                        del self.rect1[:]
                                                        #self.tko_je_pobjedio()
                                                        #self.player_na_potezu=self.pobjednik+1
                                                        nasao=1
                                                        break
                                if(nasao):
                                        break
                                                        
                                
                        
                
        def provjeri0(self, pozicija):
                vracam = -1
                for i in range (len(self.karte_igraca[0])):
                        if self.rect0[i].collidepoint(pozicija):
                                return i
                return vracam
        def ekran(self, klik):     #bacamo odabranu kartu, preostale dvije ispisujemo
                brojac1=0
                #print "u ekranu su duljine"
                #print len(self.karte_igraca[0])
                #print len(self.karte_igraca[1])
                if self.broj_karti_na_stolu == 0:
                        #ako su oba igraca bacili karte onda im moramo zadju prebrisat, a one sto su ostale po redu ispisat, duljina karata je za 1 veca(mozda)
                        if klik == 1:
                                if(len(self.karte_igraca[1])==3):               #onda zadnju brisemo
                                        brisemo = 2   
                                else:
                                        brisemo = len(self.karte_igraca[1])
                                pygame.draw.rect(self.screen, self.green, self.rect1[brisemo])
                                rotate=pygame.transform.rotate(self.slike_load[self.izasle[len(self.izasle)-1]], 90)     #rotiranje
                                self.screen.blit(rotate, (0.5*self.x, 0.60*self.y))
                                for i in range (brisemo):
                                        self.rect1[i]=self.screen.blit(self.opposite, (0.05*self.x+brojac1, 0.05*self.y))
                                        #self.rect1[i] = self.screen.blit(self.slike_load[self.karte_igraca[1][i]], (50+brojac1, 50))
                                        brojac1+=150
                                        
        
                        if klik == 0:
                                if(len(self.karte_igraca[0])==3):               #onda zadnju brisemo
                                        brisemo = 2
                                else:
                                        brisemo = len(self.karte_igraca[0])
                                pygame.draw.rect(self.screen,self.green, self.rect0[brisemo])
                                rotate=pygame.transform.rotate(self.slike_load[self.izasle[len(self.izasle)-1]], 0) 
                                self.screen.blit(rotate, (0.6*self.x, 0.55*self.y))
                                for i in range (brisemo):
                                        self.rect0[i]=self.screen.blit(self.slike_load[self.karte_igraca[0][i]], (0.05*self.x+brojac1, 0.6*self.y))
                                        brojac1+=150
                if self.broj_karti_na_stolu == 1:
                        #ako je samo jedan igrac bacio kartu onda taj igrac mora prebrisati posljenju i ispisati karte normalno,
                        #jer je duljina njegovih karata realna
                        if klik == 1:
                                if(len(self.karte_igraca[1])==3):              
                                        brisemo = 2   
                                else:
                                        brisemo = len(self.karte_igraca[1])
                                pygame.draw.rect(self.screen, self.green, self.rect1[brisemo])
                                rotate=pygame.transform.rotate(self.slike_load[self.izasle[len(self.izasle)-1]], 90) 
                                self.screen.blit(rotate, (0.6*self.x, 0.55*self.y))
                                for i in range (len(self.karte_igraca[1])):
                                        self.rect1[i]=self.screen.blit(self.opposite, (0.05*self.x+brojac1, 0.05*self.y))
                                        #self.rect1[i]=self.screen.blit(self.slike_load[self.karte_igraca[1][i]], (50+brojac1, 50))
                                        brojac1+=150
                        if klik == 0:
                                if(len(self.karte_igraca[0])==3):               
                                        brisemo = 2
                                else:
                                        brisemo = len(self.karte_igraca[0])
                                pygame.draw.rect(self.screen,self.green, self.rect0[brisemo])
                                rotate=pygame.transform.rotate(self.slike_load[self.izasle[len(self.izasle)-1]], 0)     #rotiranje
                                self.screen.blit(rotate, (0.6*self.x, 0.60*self.y))
                                for i in range (len(self.karte_igraca[0])):
                                        self.rect0[i]=self.screen.blit(self.slike_load[self.karte_igraca[0][i]], (0.05*self.x+brojac1, 0.6*self.y))
                                        brojac1+=150
                        

                        
                                
                                        
        def igra_comp(self):            #UCT nam sugerira koju kartu bacamo
                karta_za_bacanje = UCT(rootstate = self, itermax = 5000, verbose = True)
                self.DoMove(karta_za_bacanje)
                self.ekran(1)
                pygame.display.update()
                if(len(self.karte)==0):
                        time.sleep(1)
        def igra_covjek(self):
                while True:
                        gotovo = 0
                        for i in range(len(self.karte_igraca[0])):
                                if self.rect0[i].collidepoint(pygame.mouse.get_pos()) and gotovo==0:
                                        pygame.draw.rect(self.screen,(100, 0, 0), self.rect0[i],5)
                                        pygame.display.update()
                                if self.rect0[i].collidepoint(pygame.mouse.get_pos())!=1 and gotovo==0:
                                        pygame.draw.rect(self.screen,self.green, self.rect0[i], 5)
                                        pygame.display.update()
                        for event in pygame.event.get():
                                if event.type == QUIT:
                                        pygame.quit()           #suprotno od pygame.init()
                                        sys.exit()                   #terminates the program
                                if event.type == MOUSEBUTTONDOWN:
                                        pozicija = pygame.mouse.get_pos()   #(pixel_x, pixel_y)
                                        odluka = self.provjeri0(pozicija)
                                        if (odluka!=-1):
                                                self.DoMove(odluka)
                                                pygame.draw.rect(self.screen,self.green, self.rect0[odluka], 5)
                                                pygame.display.update()
                                                self.ekran(0)
                                                pygame.display.update()
                                                #time.sleep(2)
                                                gotovo = 1
                                                break
                        if(gotovo):
                                break
   

        def play(self):
                self.screen.fill(self.green)
                rect_tmp = self.screen.blit(self.play_img, (0.42*self.x, 0.42*self.y))
                klik=0
                pygame.display.update()
                while True:
                        for event in pygame.event.get():
                                        if event.type == QUIT:
                                                pygame.quit()           #suprotno od pygame.init()
                                                sys.exit() 
                                        if event.type == MOUSEBUTTONDOWN:
                                                pozicija = pygame.mouse.get_pos()
                                                if rect_tmp.collidepoint(pozicija):        #kraj igre
                                                        pygame.mixer.music.load('music1.mp3')
                                                        pygame.mixer.music.play(0, 0.0)
                                                        time.sleep(1)
                                                        klik=1
                                                        break
                        if klik:
                                break
                        

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











        
 
