import pygame
import math
class Policko:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.susedia = []
        self.visible = True
        self.ciel = False
        self.stena = False 
        self.value = math.inf
        self.previous= None

    def show(self, color, st):
        if self.ciel == False :
            pygame.draw.rect(screen, color, (self.x * w, self.y * h, w, h), st)
            pygame.display.update()

    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.x * w, self.y * h, w, h), st)
        pygame.display.update()

    def addNeighbors(self, pole):
        i = self.x
        j = self.y
        if i < stlpce-1 and pole[i + 1][j].stena == False:
            self.susedia.append(pole[i + 1][j])
        if i > 0 and pole[i - 1][j].stena == False:
            self.susedia.append(pole[i - 1][j])
        if j < riadky-1 and pole[i][j + 1].stena == False:
            self.susedia.append(pole[i][j + 1])
        if j > 0 and pole[i][j - 1].stena == False:
            self.susedia.append(pole[i][j - 1])