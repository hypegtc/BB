import numpy as np
import pygame
import sys
import os




def resource_path(fiore):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, fiore)


#======= Setup delle dimensioni delle celle e del margine ======#
DIMENSIONE_CELLA = 50           
MARGINE = 2


#======== Creazione della classe "stampo" Pezzo =======#
class Pezzo:
    def __init__(self, matrice, nome, colore):
        self.matrice = np.array(matrice, dtype=bool)
        self.nome = nome
        self.colore = colore
        self.quads = [(r, c) for r in range(self.matrice.shape[0]) for c in range(self.matrice.shape[1]) if self.matrice[r, c]]

    def righe(self):                          #Metodo della classe che restituisce il numero di righe e colonne di ogni pezzo
        return self.matrice.shape[0]

    def colonne(self):
        return self.matrice.shape[1]
    
    def disegna(self, surface, start_x, start_y):               #Metodo per disegnare ogni pezzo
        for r, c in self.quads:
            x = start_x + c*(DIMENSIONE_CELLA+MARGINE)
            y = start_y + r*(DIMENSIONE_CELLA+MARGINE)
            pygame.draw.rect(surface, self.colore, (x, y, DIMENSIONE_CELLA, DIMENSIONE_CELLA))

#======== Creazione delle singole classi Pezzo ========#
class P(Pezzo):
    def __init__(self):
        super().__init__([[True, True, True, True]], "P", (255, 255, 0))

class J(Pezzo):
    def __init__(self):
        super().__init__([
            [False, True],
            [False, True],
            [True, True]
        ], "J", (100, 200, 0))

class S(Pezzo):
    def __init__(self):
        super().__init__([
            [True, True, True],
            [True, True, True],
            [True, True, True]
        ], "S", (30, 144, 255))

class L(Pezzo):
    def __init__(self):
        super().__init__([
            [True, False],
            [True, False],
            [True, True]
        ], "L", (100, 0, 200))

class O(Pezzo):
    def __init__(self):
        super().__init__([
            [True, True],
            [True, True]
        ], "O", (200, 100, 150))

class T(Pezzo):
    def __init__(self):
        super().__init__([
            [False, True, False],
            [True, True, True]
        ], "T", (255, 165, 0))

class I(Pezzo):
    def __init__(self):
        super().__init__([
            [True],
            [True],
            [True],
            [True]
        ], "I", (255, 0, 255))

class W(Pezzo):
    def __init__(self):
        super().__init__([
            [True, False, False],
            [True, True, True]
        ], "W", (0, 191, 255))

class F(Pezzo):
    def __init__(self):
        super().__init__([
            [True, True, True],
            [True, False, False]
        ], "F", (139, 26, 26))

class Y(Pezzo):
    def __init__(self):
        super().__init__([
            [True, True],
            [True, False]
        ], "Y", (255, 255, 0))

class U(Pezzo):
    def __init__(self):
        super().__init__([
            [True, True],
            [False, True]
        ], "U", (139, 139, 0))

class D(Pezzo):
    def __init__(self):
        super().__init__([
            [True, True],
            [True, False],
            [True, False],
        ], "D", (144, 238, 144))

class E(Pezzo):
    def __init__(self):
        super().__init__([
            [False, True],
            [True, True],
            [False, True]
        ], "E", (205, 102, 29))

class R(Pezzo):
    def __init__(self):
        super().__init__([
            [True, False],
            [True, True],
            [True, False]
        ], "R", (202, 225, 255))

class Q(Pezzo):
    def __init__(self):
        super().__init__([
            [True, False],
            [True, True],
            [False, True]
        ], "Q", (255, 246, 143))

class X(Pezzo):
    def __init__(self):
        super().__init__([
            [True, False],
            [False, True]
        ], "X", (0, 255, 127))

class Z(Pezzo):
    def __init__(self):
        super().__init__([
            [False, True],
            [True, False]
        ], "Z", (107, 142, 35))

class A(Pezzo):
    def __init__(self):
        super().__init__([
            [True],
            [True],
            [True]
        ], "A", (139, 62, 47))

class G(Pezzo):
    def __init__(self):
        super().__init__([
            [True, True, True]
        ], "G", (171, 130, 255))

class bigJ(Pezzo):
    def __init__(self):
        super().__init__([
            [False, False, True],
            [False, False, True],
            [True, True, True]
        ], "bigJ", (255, 106, 106))

class bigL(Pezzo):
    def __init__(self):
        super().__init__([
            [True, False, False],
            [True, False, False],
            [True, True, True]
        ], "bigL", (205, 133, 63))

class Zeta(Pezzo):
    def __init__(self):
        super().__init__([
            [True, True, False],
            [False, True, True]
        ], "Zeta", (139, 37, 0))

 

pezziDisponibili = [P, J, L, O, T, I, F, W, U, Y, D, E, R, Q, S, X, Z, A, G, bigJ, bigL, Zeta]  #Lista con i pezzi disponibili (classi)




#====== Creazione classe easter egg =======#
class Lu:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load('fiore.webp').convert_alpha()
        self.image = pygame.transform.scale(self.image, (DIMENSIONE_CELLA, DIMENSIONE_CELLA))

    def disegna(self, surface):
        surface.blit(self.image, (self.x, self.y))













