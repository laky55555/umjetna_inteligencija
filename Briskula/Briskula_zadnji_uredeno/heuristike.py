from Briskula_klasa import *

def jace_karte_u_igri(briska, karta, igrac):
        #jace su one koje pripadaju istoj kategoriji ili su briskule
        #u igri su one koje nisu u briska.izasle i nisu kod mene
        brojac=0
        s = set(briska.izasle)
        moje_karte = set(briska.karte_igraca[igrac])  #igrac zna svoje karte
        for i in range (40):
            if i in s:
                # i je izaso
                continue
            elif i in moje_karte:
                continue
            else: #provjeri jel jaca karta
                if i/10 ==briska.briskula/10: #ako je i briskula
                    if karta/10 == i/10 and karta%10 < i%10: #karta je manja briskula od i
                        brojac+=1
                    if karta/10 != i/10:    #karta nije briskula
                        brojac+=1
                else:       #i nije briskula
                    if i/10 == karta/10 and i%10>karta%10:  #iste boje i i veca 
                        brojac+=1
        #koliko karata je slabije od mene povrh 3
        #print "u igri ima "+str(brojac)+" jacih karata od "+str(karta)
        return brojac
    
def slabije_karte_u_igri(briska, karta, igrac):
        return 40-len(briska.izasle)-3-jace_karte_u_igri(briska,karta, igrac)
    
def vj_protivnik_ima_jacu(briska, karta, igrac):
        brojnik1 = slabije_karte_u_igri(briska, karta, igrac)
        brojnik2=40-3-len(briska.izasle)
        nazivnik = 3*briska.players/2 #3 ako je jedan protivnik, 6 ako je drugi protivnik
        povrh1 = 1.0
        povrh2=1.0
        if(brojnik2<=3):
            return 1
        for i in range (1,nazivnik+1):
            povrh1 *=(brojnik1-i+1)/i
        for i in range (1, nazivnik+1):
            povrh2*=(brojnik2-i+1)/i
        #print "vjerojatnost da protivnik ima jacu kartu je "+str(1-povrh1/povrh2)
        return 1-povrh1/povrh2
    
def vj_protivnik_ima_slabiju(briska, karta, igrac):
        brojnik1 = jace_karte_u_igri(briska, karta, igrac)
        brojnik2=40-3-len(briska.izasle)
        nazivnik = 3*briska.players/2 #3 ako je jedan protivnik, 6 ako je drugi protivnik
        povrh1 = 1.0
        povrh2=1.0
        if(brojnik2<=3):
            return 1
        for i in range (1,nazivnik+1):
            povrh1 *=(brojnik1-i+1)/i
        for i in range (1, nazivnik+1):
            povrh2*=(brojnik2-i+1)/i
        #print "vjerojatnost da protivnik ima slabiju kartu je "+str(1-povrh1/povrh2)
        return 1-povrh1/povrh2

def izasao_as_i_trica(briska, karta):
        s = set(briska.izasle)
        as_ = (karta/10)*10+9
        trica = (karta/10)*10+8
        if(as_ in s and trica in s):
            return 1
        if(as_ in s or trica in s):
            return 2        #ako je izasao barem jedan
        return 0
def heuristika_igraj_prvi(briska, igrac):
        vj_jacih_od = []
        vj_slabijih_od = []
        liso_ne = []
        liso_da = []
        ljudi_ne=[]
        ljudi_da = []
        as_da =[]
        as_ne=[]
        
        """for i in range (len(briska.karte_igraca[igrac])):
            #za svaku kartu izracunamo koliko ima karata koje su jos u igri (kod protivnika ili neiskoristene)...
            #ili jos bolje VJEROJATNOSTI..barem priblizno da je kod protivnika
            vj_jacih_od.append(briska.vj_protivnik_ima_jacu(briska.karte_igraca[igrac][i]), igrac)
            vj_slabijih_od.append(briska.vj_protivnik_ima_slabiju(briska.karte_igraca[igrac][i]), igrac)"""
        for i in range (len(briska.karte_igraca[igrac])):
            karta = briska.karte_igraca[igrac][i]
            vj_jacih_od.append(vj_protivnik_ima_jacu(briska, karta, igrac))
            vj_slabijih_od.append(vj_protivnik_ima_slabiju(briska, karta, igrac))
            if karta/10 == briska.briskula/10:      #ako je karta briskula
                if karta%10<5:
                    liso_da.append(i)
                if karta%10>4 and karta%10<8:
                    ljudi_da.append(i)
                else:
                    as_da.append(i)
            else:
                if karta%10 < 5:
                    liso_ne.append(i)
                if karta%10>4 and karta%10<8:
                    ljudi_ne.append(i)
                else:
                    as_ne.append(i)

        
        #biramo ne brikulu koja ima 0 jacih od sebe u igri i nosi najvise bodova
        max_bodovi = -1
        max_karta = -1
        for i in range (len(briska.karte_igraca[igrac])):
            karta = briska.karte_igraca[igrac][i]
            if(vj_jacih_od[i]==0 and karta/10 != briska.briskula/10):
                if(max_bodovi < briska.poeni(karta)):
                    max_bodovi= briska.poeni(karta)
                    max_karta = i
        if(max_karta!=-1):
            return max_karta
        #biramo onu koja nema as i trice u igri i nosi najvise? bodova
        for i in range (len(briska.karte_igraca[igrac])):
            karta = briska.karte_igraca[igrac][i]
            if(izasao_as_i_trica(briska,karta) and karta%10!=9 and karta %10!=8):
                if(max_bodovi < briska.poeni(karta)):
                    max_bodovi=briska.poeni(karta)
                    max_karta = i
        if(max_karta!=-1):
            return max_karta
                
        #prvo pokusamo baciti liso_ne, neku proizvoljnu
        if len(liso_ne)!=0:
            return liso_ne[random.randint(0, len(liso_ne)-1)]
        
        #ako nema liso provjerimo koliko ima liso briskula, ako je vise od jedne onda baacimo neku
        if len(liso_da)+len(ljudi_da)>1 and len(liso_da)>0:  #tu ulazim ako imam bar 2 briskule i od toga je jedna liso
            return liso_da[0]
        #inace bacamo [2, 3 , 4] ne briskulu   bojlje baciti 4 ako nema kariga od te boje nekgo 2 gdje ima kariga
        for i in range (len(ljudi_ne)):
            if(izasao_as_i_trica(briska, ljudi_ne[i])==2):
                if(briska.poeni(ljudi_ne[i])>max_bodovi):
                    max_bodovi=briska.poeni(ljudi_ne[i])
                    max_karta=ljudi_ne[i]
        if(max_karta!=-1):
            return max_karta
        if(len(ljudi_ne)>0):
            return ljudi_ne[random.randint(0, len(ljudi_ne)-1)]
        #ako ni to nije moguce onda bacamo liso briskulu ako je imamo
        if len(liso_da)>0:
            return liso_da[0]
        #ako toga nema onda bacamo ljudi_da     ako je vjerojatnost da ima briskulu jako mala ~>20% baci asa_ne
        if len(ljudi_da)>0:
            return ljudi_da[0]
        #inace imamo samo aseve ili trice..bacamo liso asa ili tricu ako imamo inace nekog drugog
        #ako je vj da ima briskulu veca od pola onda bacamo as_da
        if len(as_da)!=0:
            return as_da[0]
        if len(as_ne)!=0:
            return as_ne[0]
        #ovo se ne bi nikada trebalo dogodit
        return -1
    
def odaberi_kartu_za_bacanje(briska, koji_po_redu, igrac):
        if koji_po_redu==1:
            return heuristika_igraj_prvi(briska,igrac)
        else:
            return igram_zadnji(briska,igrac)
            #return 0
    
def tko_je_pobjedio(briska):
        vektor = b.trenutno_uzima(2)
        briska.pobjednik = vektor[1] 
        briska.bodovi[briska.pobjednik]+=vektor[0]
        
        
        
def poeni(briska,karta1):
        if karta1%10 == 0 or karta1%10 == 1 or karta1%10 == 2 or karta1%10 == 3 or karta1%10 == 4:
            return 0
        elif karta1%10 == 5 or karta1%10 == 6 or karta1%10 == 7:
            return karta1%10-3
        elif karta1%10 == 8:
            return 10
        else:
            return 11

def uzima(briska):        #dodaje bodove timu koji je uzeo karte i vraca broj igraca koji je uzeo
        najveca_briskula = -1
        najveca_prva_boja = -1
        poeni_u_krugu = 0
        """for i in range (len(briska.izasle)):
            print "izasle su: "
            print briska.izasle[i]"""
        for i in range(briska.players):
            nova_karta = briska.izasle[len(briska.izasle)-briska.players+i]    #ucitavanje karata koje su na stolu
            if i==0:
                prva_karta = nova_karta
            poeni_u_krugu += briska.poeni(nova_karta)
            if (nova_karta/10 == briska.briskula/10 and nova_karta>najveca_briskula): #provjera je li karta briskula
                najveca_briskula = nova_karta
            if (nova_karta/10 == prva_karta/10 and nova_karta>=prva_karta ): #provjera je li karta iste boje kao prva
                najveca_prva_boja = nova_karta
        if(najveca_briskula != -1):     #ako ima briskule na stolu
            #print "najveca briskula je "+str(najveca_briskula)
            for i in range (briska.players):
                if briska.karte_igraca[i][briska.karte_za_bacanje[i]]==najveca_briskula:
                    pobjednik = i
           # print pobjednik
            #print najveca_briskula
            briska.bodovi[pobjednik] += poeni_u_krugu
            return pobjednik
        else:
            for i in range (briska.players):
                #print "igrac " + str(i)+" je bacio kartu "+ str(briska.karte_igraca[i][briska.karte_za_bacanje[i]])
                if briska.karte_igraca[i][briska.karte_za_bacanje[i]]==najveca_prva_boja:
                    pobjednik = i
            #print pobjednik
           # print najveca_prva_boja
            briska.bodovi[pobjednik] += poeni_u_krugu
            return pobjednik

def je_li_briskula(briska, karta):        #vraca 1 ako je poslana karta briskula
        if(karta/10 == briska.briskula/10):
            return 1
        return 0
        
    #vraca BODOVE na stolu, IGRACA koji je uzeo i KARTU koja uzima
    #za slucaj grafika ovo radi jer se tek na kraju karte igraca updataju
    #za doMove nije dobro jer se u njemu ponisiti karta koja je bacena
    #zato je bolje korisitit briska.izasle
def trenutno_uzima(briska, broj_karti_na_stolu):
        #print "funkcija trenutno uzima"
        a = []          #lista koja ima bodove na stolu, pobjednika, i najjacu kartu
        for i in range (3):
            a.append(0)
        najveca_briskula = -1
        najveca_prva_boja = -1
        poeni_u_krugu = 0
        #ova for petlja nade najjacu kartu na stolu   treba samo jos naci ko ju je bacio
        for i in range(broj_karti_na_stolu):
            nova_karta = briska.izasle[len(briska.izasle)- broj_karti_na_stolu + i]    #ucitavanje karata koje su na stolu
            if i==0:
                prva_karta = nova_karta
            poeni_u_krugu += briska.poeni(nova_karta)
            if (briska.je_li_briskula(nova_karta) and nova_karta>najveca_briskula): #provjera je li karta briskula
                najveca_briskula = nova_karta
            if (nova_karta/10 == prva_karta/10 and nova_karta>=prva_karta ): #provjera je li karta iste boje kao prva
                najveca_prva_boja = nova_karta


        if(najveca_briskula != -1):     #ako ima briskule na stolu
        #print "najveca briskula je "+str(najveca_briskula)
            #u briska.player_na_potezu imamo igraca koji je prvi igrao, npr 1.igrac onda je karta koju je on bacio predzadnja u listi izisle
            if(briska.izasle[len(briska.izasle)-2]==najveca_briskula):
                a[0] = poeni_u_krugu
                a[1] = briska.player_na_potezu-1
                a[2] = najveca_briskula
                return a
            else:
                a[0] = poeni_u_krugu
                a[1] = 3-briska.player_na_potezu-1
                a[2] = najveca_briskula
                return a
                
        else:
            if(briska.izasle[len(briska.izasle)-2]==najveca_prva_boja):
                a[0] = poeni_u_krugu
                a[1] = briska.player_na_potezu-1
                a[2] = najveca_prva_boja
                return a
            else:
                a[0] = poeni_u_krugu
                a[1] = 3-briska.player_na_potezu-1
                a[2] = najveca_prva_boja
                return a


    #igramo tu kartu ako je vec nase i zelim dat sto vise poena
def najvise_bodova_u_ruci(briska, karte): #vraca poziciju karte koja ima najvise bodova a nije briskula, a ako su sve briskule vraca najmanju
        trazena_briskula = -1
        trazena_karta = -1
        for i in range (len(karte)):
            najmanja_briskula=99
            najvise_poena=-1
            if(briska.je_li_briskula(karte[i])):
                if(karte[i] < najmanja_briskula):
                    najmanja_briskula=karte[i]
                    trazena_briskula = i
                else:
                    if(briska.poeni(karte[i])> najvise_poena):
                        najvise_poena = briska.poeni(karte[i])
                        trazena_karta = i
        if(najvise_poena == -1):
            return trazena_briskula
        return trazena_karta

def najslabija_karta_u_ruci(briska, karte): #vraca poziciju najslabije karte s najmanje bodova 
        trazena_briskula = -1
        trazena_karta = -1
        najmanja_briskula=99
        najmanje_poena=99
        for i in range (len(karte)):
            if(briska.je_li_briskula(karte[i])):
                if(karte[i] < najmanja_briskula):
                    najmanja_briskula=karte[i]
                    trazena_briskula = i
            else:
                if(briska.poeni(karte[i])< najmanje_poena):
                    najmanje_poena = briska.poeni(karte[i])
                    trazena_karta = i
        if(najmanje_poena == 99):
            return trazena_briskula
        return trazena_karta

def postoji_jaca(briska, moje_karte, najjaca):
        min_briskula = 99
        if(briska.je_li_briskula(najjaca)):   #ako je najjaca briskula onda moramo baciti vecu briskulu
            for i in range (len(moje_karte)):
                if(briska.je_li_briskula(moje_karte[i]) and moje_karte[i] < min_briskula and moje_karte>najjaca):
                    min_brisklua = moje_karte[i]
                    indeks = i
            if(min_briskula != 99):
                return indeks
        else:   #ako najjaca nije briskula moramo baciti bilo koju briskulu
            for i in range (len(moje_karte)):
                if(briska.je_li_briskula(moje_karte[i]) and moje_karte[i] < min_briskula):
                    min_briskula = moje_karte[i]
                    indeks = i
            if(min_briskula != 99):
                return indeks
        return -1               #ne postoji briskula koja je jaca                    
                        
        
def igram_zadnji(briska, igrac): #vraca indeks karte koju zelim baciti
        indeks = -1
        a = briska.trenutno_uzima(briska.players-1)
        bodovi_na_stolu=a[0]
        igrac_koji_uzima=a[1]
        najjaca_karta_na_stolu =a[2]
        moje_karte = briska.karte_igraca[igrac]
        indeks_karte_s_najmanje_bodova = najslabija_karta_u_ruci(briska,moje_karte)
        karta_s_najmanje_bodova = moje_karte[indeks_karte_s_najmanje_bodova]
        #print "brojevi " + str(a[0])+"  " + str(a[1]) +"  "+ str(a[2])+ " najslabija karta " + str(karta_s_najmanje_bodova)        
        if(briska.je_li_briskula(najjaca_karta_na_stolu)== 0):    #ako najjaca karta nije briskula provjerimo da li imamo jacu i bacimo nju
            karta_koju_bacam = -1
            #print "prva provjera"
            for i in range (len(moje_karte)):
                if(moje_karte[i]/10 == najjaca_karta_na_stolu/10):
                    if(karta_koju_bacam < moje_karte[i] and moje_karte[i] > najjaca_karta_na_stolu):
                        karta_koju_bacam = moje_karte[i]
                        indeks = i
                        print "postoji jaca"
            if (indeks != -1):
                return indeks

        #ako je nase dajem najvise bodova
        nase = (igrac+igrac_koji_uzima+1)%2     #1 ako je od vlastitog tima inace 0
        if(nase):
            #print "Tu nesmiije uci"
            return najvise_bodova_u_ruci(briska, moje_karte)

        #ZELIM PUSTITI pustam tako da bacim kartu s najmanje bodova ili uzmem s najmanjom briskulom
        if(briska.poeni(karta_s_najmanje_bodova) + bodovi_na_stolu<6 and bodovi_na_stolu +briska.poeni(karta_s_najmanje_bodova)<60):        #ZELIM PUSTITI
            #print "Zelim pustit " + str(briska.poeni(karta_s_najmanje_bodova))
            return indeks_karte_s_najmanje_bodova

        # ZELIM UZETI uzet cu tako da bacim najmanju briskulu koja uzima ili dajem najmanje poena
        else:   #(bodovi_na_stolu>4):        #ZELIM UZETI ako je vise of 4 boda na stolu 
            postoji = postoji_jaca(briska,moje_karte, najjaca_karta_na_stolu)
            if(postoji != -1):
                #print "zelim uzet i postoji jaca"
                return postoji
            else:
                #print "zelim uzet i ne postoji jaca, pustamo"
                return najslabija_karta_u_ruci(briska, moje_karte)

    #dobiva broj karte i vraca STRING koja je karta
def koja_je_to_karta(briska, karta):
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

    
    #vraca 1 ako imam briskulu u ruci, inace 0
def imam_briskulu(briska, karte):
        for i in range (len(karte)):
            if(briska.je_li_briskula(karte[i]) ):
                return 1
        return 0

    #vraca 1 ako imam liso, inace 0
def imam_liso_nebriskula(briska, karte):
        for i in range (len(karte)):
            if(briska.poeni(karte[i])== 0  and briska.je_li_briskula(karte[i]) == 0):
                return 1
        return 0

    #vraca 1 ako imam poene koji nisu briskula i manji su od max poeeni, inace 0
def imam_poene_nebriskula(briska, karte, max_poeni):
        for i in range (len(karte)):
            if(briska.poeni(karte[i])<max_poeni  and briska.je_li_briskula(karte[i]) == 0):
                return 1
        return 0

    #vraca 0 ako ne mogu, ili 1 ako mogu
def mogu_uzeti(briska, najjaca_karta, karte):
        if(briska.je_li_briskula(najjaca_karta)):
            for i in range (len(karte)):
                if (briska.je_li_briskula(karte[i]) and  karte[i]>najjaca_karta):
                    return 1
        else:
            for i in range (len(karte)):
                if (briska.je_li_briskula(karte[i] )) or (najjaca_karta/10 == karte[i]/10 and najjaca_karta<karte[i]):
                    return 1
        return 0

    #varraca 1 ako je karta1 jaca, ako je karta 2 jaca vraca 0
def je_li_karta_jaca(briska, karta1, karta2):
        if(briska.je_li_briskula(karta2)):
            if(briska.je_li_briskula(karta1)and  karta1>karta2):
                return 1
        else:
            if(briska.je_li_briskula(karta1)):
                return 1
            elif(karta2/10 == karta1/10 and karta1>karta2):
                return 1
        return 0


    #vraca vektor pozicija koje se nesmiju igrati, HEURISTIKA KOJA REZE POTEZE
def igram_zadnji_nesmijem(briska, igrac):
        nesmijem_odigrati = []  #pozicije koje nesmijem odigrati
        a = briska.trenutno_uzima(briska.players-1)
        bodovi_na_stolu=a[0]
        igrac_koji_uzima=a[1]
        najjaca_karta_na_stolu =a[2]
        moje_karte = briska.karte_igraca[igrac]

        #ima puno poena i nije nase
        nase = (igrac+igrac_koji_uzima+1)%2     #1 ako je od vlastitog tima inace 0
        if(nase == 0):
            if(bodovi_na_stolu > 4*briska.players):   #ima puno poena TREBA SE DOGOVORITI KOLIKO JE TO
                if(briska.mogu_uzeti(najjaca_karta_na_stolu, moje_karte)):#mogu uzeti, izbacujem sve karte koje ne mogu uzeti
                    for i in range (len(moje_karte)):
                        if(briska.je_li_karta_jaca(najjaca_karta_na_stolu, moje_karte[i])):
                            nesmijem_odigrati.append(i)

            if(briska.mogu_uzeti(najjaca_karta_na_stolu, moje_karte)== 0):#ako ne mogu uzet idem ovdje
                if(briska.imam_liso_nebriskula(moje_karte)):       #ako ne mogu uzet i imam liso (koji nije briskula)ne smijem bacati poene
                    for i in range (len(moje_karte)):
                        if(briska.poeni(moje_karte[i])or briska.je_li_briskula(moje_karte[i])):
                            nesmijem_odigrati.append(i)

        else:   #nase je (treba samo kod 4 igraca)
            if(briska.imam_poene_nebriskula(moje_karte,6)):
                for i in range (len(moje_karte)):
                    if(briska.poeni(moje_karte[i])== 0 or briska.je_li_briskula(moje_karte[i])):
                        nesmijem_odigrati.append(i)        
        
        
        imam_na = 0    #1 ako imam kartu koja nije briskula, a mogu uzet prvom
        if(briska.je_li_briskula(najjaca_karta_na_stolu)== 0):    #ako najjaca karta nije briskula provjerimo da li imamo jacu i bacimo nju
            for i in range (len(moje_karte)):
                if(moje_karte[i]/10 == najjaca_karta_na_stolu/10 and moje_karte[i]>najjaca_karta_na_stolu):
                    imam_na = 1
        if (imam_na):     #ako imam na ne smijem baciti briskulu, i nesmijem dati vise od 4 poena
            for i in range (len(moje_karte)):
                if(briska.je_li_briskula(moje_karte[i]) and briska.izasle <32):
                    nesmijem_odigrati.append(i)
                if(briska.poeni(moje_karte[i]) >6 and moje_karte[i]/10 != najjaca_karta_na_stolu/10):
                    nesmijem_odigrati.append(i)

        #ako imamo vise briskula i sve izmedu su vec vani bolje baciti vecu (to je mozda bolje samo za 2 igraca)
        broj_briskula =0    
        najslabija_briskula=99
        najjaca_briskula =-1
        postoji_izmedu = 0
        s = set(briska.izasle)
        for i in range (len(moje_karte)):
            if (briska.je_li_briskula(moje_karte[i])):
                broj_briskula +=1
        if(broj_briskula >1):
            for i in range (len(moje_karte)):
                if(najslabija_briskula>moje_karte[i] and briska.je_li_briskula(moje_karte[i])):
                    najslabija_briskula = moje_karte[i]
                if(najjaca_briskula<moje_karte[i] and briska.je_li_briskula(moje_karte[i])):
                    najslabija_briskula = moje_karte[i]
            for i in range (najslabija_briskula+1, najjaca_briskula):
                if i not in s:
                    postoji_izmedu = 1
            if (postoji_izmedu == 0):
                for i in range (len(moje_karte)):
                    if(moje_karte[i] == najslabija_briskula):
                        nesmijem_odigrati.append(i)

        #print nesmijem_odigrati                       
        return nesmijem_odigrati               

    #vraca vektor pozicija koje se nesmiju igrati, HEURISTIKA KOJA REZE POTEZE
def igram_prvi_nesmijem(briska, igrac):
        nesmijem_odigrati = []  #pozicije koje nesmijem odigrati
        moje_karte = briska.karte_igraca[igrac]
        if (briska.imam_liso_nebriskula(moje_karte)and len(briska.izasle)<30): #ako imam liso i briskulu bolje baciti liso, osim mozda na kraju
            for i in range (len(moje_karte)):
                if(briska.je_li_briskula(moje_karte[i])):
                    nesmijem_odigrati.append(i)

        if (briska.imam_poene_nebriskula(moje_karte,6)): #ako vec imam poene u ruci, koji su manji od 6 bolje ne baciti karig prvi
            for i in range (len(moje_karte)):
                if(briska.poeni(moje_karte[i])>6):
                    nesmijem_odigrati.append(i)
        #ako imamo vise briskula i sve izmedu su vec vani bolje baciti vecu (to je mozda bolje samo za 2 igraca)
        broj_briskula =0    
        najslabija_briskula=99
        najjaca_briskula =-1
        postoji_izmedu = 0
        s = set(briska.izasle)
        for i in range (len(moje_karte)):
            if (briska.je_li_briskula(moje_karte[i])):
                broj_briskula +=1
        if(broj_briskula >1):
            for i in range (len(moje_karte)):
                if(najslabija_briskula>moje_karte[i] and briska.je_li_briskula(moje_karte[i])):
                    najslabija_briskula = moje_karte[i]
                if(najjaca_briskula<moje_karte[i] and briska.je_li_briskula(moje_karte[i])):
                    najslabija_briskula = moje_karte[i]
            for i in range (najslabija_briskula+1, najjaca_briskula):
                if i not in s:
                    postoji_izmedu = 1
            if (postoji_izmedu == 0):
                for i in range (len(moje_karte)):
                    if(moje_karte[i] == najslabija_briskula):
                        nesmijem_odigrati.append(i)

        #print nesmijem_odigrati                              
        return nesmijem_odigrati 

