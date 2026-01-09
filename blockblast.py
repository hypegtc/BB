import pygame
import random as rm                                                             #Import delle librerie del file pezzi.py                                                          
from pezzi import pezziDisponibili, Lu, DIMENSIONE_CELLA, MARGINE
import sys


#===== Setup griglia e finestra =====#

RIGHE, COLONNE = 8, 8                                               #Definizione della griglia 8x8
LARG_SCHERMO, ALT_SCHERMO = 700, 800                                #Definizione della schermata pygame
GRID_X = (LARG_SCHERMO - (COLONNE*(DIMENSIONE_CELLA+MARGINE)+MARGINE))//2           #Calcolo per centrare la griglia (asse x)
GRID_Y = (ALT_SCHERMO - (RIGHE*(DIMENSIONE_CELLA+MARGINE)+MARGINE))//2 - 80         #Calcolo per posizionare la griglia (asse y)
ALT_GRIGLIA = COLONNE*(DIMENSIONE_CELLA+MARGINE)+MARGINE                           #Calcolo altezza griglia in pixel


#==== Setup delle tuple colore =====#

COLORE_SFONDO = (0, 134, 139)           #Colore sfondo 
COLORE_CELLA_VUOTA = (50, 50, 50)       #Colore celle vuote (grigio)
COLORE_TESTO = (255, 255, 255)          #Colore testo punteggio (bianco)
COLORE_BEST_SCORE = (255, 215, 0)       #Colore miglior punteggio (oro)


#===== Setup file di testo per il miglior punteggio e funzioni per accesso al file ======#

FILE_BEST_SCORE = "best_score.txt"              #Definizione del file 


def carica_best_score():                        #Funzione di lettura del file per caricare il miglior punteggio
    try:
        with open(FILE_BEST_SCORE, "r") as f:
            return int(f.read())
    except:
        return 0

def salva_best_score(score):                     #Funzione di scrittura sul file per salvare l'eventuale nuovo best score
    with open(FILE_BEST_SCORE, "w") as f:
        f.write(str(score))

best_score = carica_best_score()                 #Inizialmente carico il miglior punteggio nella variabile best_score





#====== Inizializzazione griglia 8x8 e punteggio iniziale=====#


griglia = [[False for _ in range(COLONNE)] for _ in range(RIGHE)]        #Crea una matrice booleana 8x8 False
punteggio = 0                                                            #Punteggio iniziale settato a 0




#======= Funzioni di controllo, creazione pezzi e game over ======= #


def nuovi_pezzi():                                              #nuovi_pezzi restituisce tre pezzi casuali
    pezzi = []                                                  #a patto che siano tutti e tre piazzabili
    tentativi = 0                                               #e crea le istanze delle classi pezzi create in pezzi.py
    max_tentativi = 1000

    while len(pezzi) < 3 and tentativi < max_tentativi:         #Ciclo fino a trovare 3 pezzi o raggiunge un max_tentativi
        tentativi += 1                                          #Aggiorna il numero di tentativi
        candidato = rm.choice(pezziDisponibili)                     #Prende una classe pezzo qualsiasi dalla lista passata da pezzi.py
        piazzabile = False                                                  #Inizialmente setta piazzabile False che diventerá True se il pezzo sará piazzabile
        for row in range(RIGHE - candidato().righe() + 1):                    #Inizia il controllo di ogni riga e crea l'istanza del pezzo scelto da random
            for col in range(COLONNE - candidato().colonne() + 1):            #Controlla ogni colonna
                if posizionabile(candidato(), row, col):                      #Richiama la funzione posizionabile che restituisce un booleano
                    piazzabile = True                                         #Se posizionabile True allora piazzabile diventa True  
                    break
            if piazzabile:                                                    
                break
        if piazzabile:                                              
            pezzi.append(candidato())                                           #Aggiunge il pezzo alla lista pezzi
    return pezzi                                                                #Restituisce la lista 





def get_posizioni_pezzi(pezzi):                                                   #Calcola la posizione di ogni pezzo e li posiziona in basso alla griglia
    larghezza_totale = sum(p.colonne()*(DIMENSIONE_CELLA+MARGINE) for p in pezzi) + (len(pezzi)-1)*20
    x_iniziale = (LARG_SCHERMO - larghezza_totale)//2
    y_iniziale = GRID_Y + ALT_GRIGLIA + 40
    posizioni = []
    x = x_iniziale
    for p in pezzi:
        posizioni.append((p, x, y_iniziale))
        x += p.colonne()*(DIMENSIONE_CELLA+MARGINE) + 20                              #Restituisce la posizione di ogni pezzo disponendoli in fila e in basso alla griglia
    return posizioni

def posizionabile(pezzo, row, col):                                                    #Funzione di controllo per poter posizionare un detrminato pezzo
    for r, c in pezzo.quads:                                                           #pezzo.quads, da pezzi.py, restituisce le coordinate delle celle True di ogni matrice pezzo
        rr = row + r                                                                   #Passa dalle coordinate relative del pezzo a quelle assolute della griglia. In pratica vede il pezzo rispetto a tutta la griglia 
        cc = col + c
        if rr<0 or rr>=RIGHE or cc<0 or cc>=COLONNE:                                    #Controlla che il pezzo non esca dai bordi della griglia
            return False
        if griglia[rr][cc]:                                                             #Controlla che sulla griglia, in quelle coordinate, non ci sia un altro pezzo
            return False
    return True                                                                         #Se il pezzo supera i controlli la funzione restituisce True

def piazza_pezzo(pezzo, row, col):                                                      #É la funzione che inserisce i pezzi nella griglia, gestisce le righe e le colonne complete e aggiorna il punteggio 
    global punteggio
    for r, c in pezzo.quads:                                                            
        griglia[row+r][col+c] = pezzo.colore                                             #Quando viene piazzato un pezzo le celle della griflia si colorano dello stesso colore del pezzo 

    righe_complete = [r for r in range(RIGHE) if all(griglia[r][c] for c in range(COLONNE))]                
    colonne_complete = [c for c in range(COLONNE) if all(griglia[r][c] for r in range(RIGHE))]          #Crea le liste delle righee delle colonne complete scorrendo le righe e verificando quali restituiscono True (all)

    for r in righe_complete:
        for c in range(COLONNE):
            griglia[r][c] = False                                                   
    for c in colonne_complete:                              #Ogni volta che si completa una riga o una colonna, la griglia viene resettata a False
        for r in range(RIGHE):
            griglia[r][c] = False

    punteggio += len(righe_complete)*COLONNE + len(colonne_complete)*RIGHE          #Il punteggio aumenta a multipli di 8 (dá 8 punti per ogni riga, colonna completata)


def disegna_ghost(surface, pezzo, mouse_x, mouse_y, offset_x, offset_y):                #É la funzione che crea il ghost del pezzo sulla griglia
    
    col = round((mouse_x - GRID_X - offset_x)/(DIMENSIONE_CELLA+MARGINE))               #Quando il mouse si muove viene calcolata la posizione del pezzo rispetto al mouse in modo tale che segua il cursore
    row = round((mouse_y - GRID_Y - offset_y)/(DIMENSIONE_CELLA+MARGINE))
    
    col = max(0, min(COLONNE - pezzo.colonne(), col))                 
    row = max(0, min(RIGHE - pezzo.righe(), row))                                      #Crea un bound per non far uscire il ghost dalla griglia
    
    valido = posizionabile(pezzo, row, col)                                               #valido eredita il booleano restituito da posizionabile()   

    s = pygame.Surface((LARG_SCHERMO, ALT_SCHERMO), pygame.SRCALPHA)                    #Crea una schermata dove viene disegnato il ghost      
   
    color = (*pezzo.colore, 110) if valido else (255, 0, 0, 110)                        #Se il pezzo é posizionabile il colore del ghos é quello del pezzo, altrimenti é rosso
    
    for r, c in pezzo.quads:
        x = GRID_X + (col+c)*(DIMENSIONE_CELLA+MARGINE)                                 #x e y sono le coordinate sullo schermo di dove verrá disegnato il ghost
        y = GRID_Y + (row+r)*(DIMENSIONE_CELLA+MARGINE)
        pygame.draw.rect(s, color, (x, y, DIMENSIONE_CELLA, DIMENSIONE_CELLA))          #Funzione di pygame che permete di disegnare un rettangolo di grandezza DIMENSIONE_CELLA x DIMENSIONE_CELLA, di colore color, sulla superficie s 
    surface.blit(s, (0,0))                                                              #Posiziona la superficie al di sopra della griglia 
    return row, col, valido                                                 #Restituisce le coordinate del pezzo e se questo é piazzabile o meno

def controlla_game_over(pezzi):                                       #É la funzione che controlla se possono essere piazzati nuovi pezzi sulla griglia
    for p in pezzi:
        for row in range(RIGHE - p.righe() + 1):
            for col in range(COLONNE - p.colonne() + 1):
                if posizionabile(p, row, col):
                    return False
    return True

#====== Setup di pygame =======#

pygame.init()                                                   #Inizializza pygame
screen = pygame.display.set_mode((LARG_SCHERMO, ALT_SCHERMO))       #Crea la finestra di gioco
pygame.display.set_caption("Block Blast")                           #Titolo della finestra 
clock = pygame.time.Clock()                                         #Clock per fps (quante volte al secondo si aggiorna lo schermo)
font = pygame.font.SysFont(None, 40)                                
font_gameover = pygame.font.SysFont(None, 60)                       #Font delle scritte 

#====== Easter egg =====# 

fiore = Lu(LARG_SCHERMO//2 + 100, 5)    #Crea un'istanza della classe Lu (pezzi.py). Alla persona che mi ha fatto scoprire, qualche mese, fase questo gioco (ricorda che ti ho sempre battuto) <3 


pezzo_trascinato = None             #Nessun pezzo trascinato all'inizio
offset_x = offset_y = 0             #Offset mouse nullo
pezzi = nuovi_pezzi()               #Crea nuovi pezzi
game_over = False                   #Stato del gioco 

#======== Main ========#

running = True                      
while running:
    clock.tick(60)
    for event in pygame.event.get():      
        if event.type == pygame.QUIT:
            pygame.quit()                      #Ogni volta che il ciclo inizia controlla se l'utente esce dal gioco, se si il gioco si chiude
            sys.exit()

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:            #Da pygame controlla se viene clickato il tasto sinistro del mouse
                mx, my = event.pos                                                      #Prende la posizione dove avviene l'evento
                posizioni = get_posizioni_pezzi(pezzi)                                  #Prende la posizione dei pezzi 
                for p, x, y in posizioni:
                    rect = pygame.Rect(x, y, p.colonne()*(DIMENSIONE_CELLA+MARGINE), p.righe()*(DIMENSIONE_CELLA+MARGINE))  #Crea un rettangolo fantasma attorno ai pezzi
                    if rect.collidepoint(mx, my):                                   #Se l'evento é avvenuto all'interno di questo rettangolo il pezzo attuale diventa il pezzo trascinato
                        pezzo_trascinato = p
                        offset_x = mx - x
                        offset_y = my - y
                        break

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and pezzo_trascinato: 
                mx, my = event.pos
                row, col, valid = disegna_ghost(screen, pezzo_trascinato, mx, my, offset_x, offset_y)
                if valid:
                    piazza_pezzo(pezzo_trascinato, row, col)
                    pezzi.remove(pezzo_trascinato)                                                      #Se l'evento é il rilascio del tasto sinstro del mouse e ho un pezzo in mano, avvengono i controlli di posizionamento con le funzioni di cui sopra, e viene rilasciato il pezzo
                    if len(pezzi)==0:                                               #Se finiscono i pezzi, la lista viene riaggionata
                        pezzi = nuovi_pezzi()
                    if controlla_game_over(pezzi):                                  #Controlla il possibile game over
                        game_over = True
                pezzo_trascinato = None

        if game_over and event.type == pygame.KEYDOWN:                  
            if event.key == pygame.K_r:
                griglia = [[False for _ in range(COLONNE)] for _ in range(RIGHE)]               #Se l'evento é il tasto R e lo stato dell gioco é il game over, il gioco riparte 
                punteggio = 0
                pezzi = nuovi_pezzi()
                game_over = False

    
    screen.fill(COLORE_SFONDO)                        #Colora lo sfondo 

    for r in range(RIGHE):                                                                      #Disegna la griglia nella finestra di gioo
        for c in range(COLONNE):
            x = GRID_X + c*(DIMENSIONE_CELLA+MARGINE)
            y = GRID_Y + r*(DIMENSIONE_CELLA+MARGINE)
            color = COLORE_CELLA_VUOTA if not griglia[r][c] else griglia[r][c]
            pygame.draw.rect(screen, color, (x, y, DIMENSIONE_CELLA, DIMENSIONE_CELLA))         #Crea la superficie su cui disegnare i quadratini della griglia e di che colore

    
    posizioni = get_posizioni_pezzi(pezzi)
    for p, x, y in posizioni:
        if p != pezzo_trascinato:                                   #Disegna i pezzi sotto la griglia 
            p.disegna(screen, x, y)

    
    if pezzo_trascinato:
        mx, my = pygame.mouse.get_pos()
        disegna_ghost(screen, pezzo_trascinato, mx, my, offset_x, offset_y)         #Disegna il pezzo trascinato e il relativo ghost
        pezzo_trascinato.disegna(screen, mx - offset_x, my - offset_y)

    
    score_color = COLORE_TESTO
    score_text = font.render(f"Punteggio: {punteggio}", True, score_color)              #Mostra il punteggio a schermo
    screen.blit(score_text, ((LARG_SCHERMO-score_text.get_width())//2, 10))

    
    if punteggio > best_score:
        best_score = punteggio
        salva_best_score(best_score)
    best_text = font.render(f"Best: {best_score}", True, COLORE_BEST_SCORE)             #Mostra e aggiorna il best score
    screen.blit(best_text, (10, 10))

    
    if punteggio >= 22:
        fiore.disegna(screen)                       #Quando il punteggio supera il 22 disegna il fiore 

    
    if game_over:
        overlay = pygame.Surface((LARG_SCHERMO, ALT_SCHERMO))
        overlay.set_alpha(180)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))                                                                     #Gestisce il game over creando una superficie nuova su cui pygame scrive i vari testi del game over
        go_text = font_gameover.render("GAME OVER", True, (255,0,0))
        screen.blit(go_text, ((LARG_SCHERMO-go_text.get_width())//2, ALT_SCHERMO//2 - 50))
        screen.blit(score_text, ((LARG_SCHERMO-score_text.get_width())//2, ALT_SCHERMO//2 + 20))
        restart_text = font.render("Premi R per ricominciare", True, (255,255,255))
        screen.blit(restart_text, ((LARG_SCHERMO-restart_text.get_width())//2, ALT_SCHERMO//2 + 60))

    pygame.display.flip()






































