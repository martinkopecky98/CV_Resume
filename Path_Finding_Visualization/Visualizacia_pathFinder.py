
import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os

mapaX, mapaY = 800, 600
screen = pygame.display.set_mode((600, 600))
white = (255,255,255)

screen.fill((white))

class Policko:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.susedia = []
        self.visible = True
        self.ciel = False
        self.stena, self.prekazka = False, False 
        self.value = math.inf
        self.prechod = 1
        self.previous = None
        self.f, self.g, self.h = 0,0,0

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


stlpce = 50
stena = True
pole = [0 for i in range(stlpce)]
riadky = 50
openSet = []
closedSet = []
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
black = (0,0,0)
yellow = (255, 255, 0)
w = 600 / stlpce
h = 600 / riadky
hodnota_prekazky = 10
cameFrom = []
tlacidla = []


# vytvorenie pola
for i in range(stlpce):
    pole[i] = [0 for i in range(riadky)]

# vytvorenie policok
for i in range(stlpce):
    for j in range(riadky):
        pole[i][j] = Policko(i, j)


# Set start and end node
start = pole[5][5]
end = pole[45][45]

# vykreslenie mapky
for i in range(stlpce):
    for j in range(riadky):
        pole[i][j].show(blue, 1)

for i in range(0,riadky):
    pole[0][i].show(grey, 0)
    pole[i][0].show(grey, 0)
    pole[stlpce-1][i].show(grey, 0)
    pole[i][riadky-1].show(grey, 0)
    pole[0][i].stena = True
    pole[i][0].stena = True
    pole[stlpce-1][i].stena = True
    pole[i][riadky-1].stena = True


def onsubmit():
    global start
    global end
    try:
        st = startBox.get().split(',')
        ed = endBox.get().split(',')
        # hp = prekazka_box.get()
        # hodnota_prekazky = int(hp)
        start = pole[int(st[0])][int(st[1])]
        end = pole[int(ed[0])][int(ed[1])]
    except:
        start = pole[10][10]
        end = pole[40][40]
        hodnota_prekazky = 10
    finally:
        if start == end:
            start = pole[10][10]
            end = pole[40][40]
    window.quit()
    window.destroy()

window = Tk()
label = Label(window, text='Start(x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End(x,y): ')
endBox = Entry(window)
# label2 = Label(window, text='Hodnota prekazky: ')
# prekazka_box = Entry(window)

djisktra, a_star = IntVar(), IntVar()
#showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
check_djisktra = ttk.Checkbutton(window, text='Djisktra', onvalue=1, offvalue=0, variable=djisktra)
check_a_star = ttk.Checkbutton(window, text='A*', onvalue=1, offvalue=0, variable=a_star)

submit = Button(window, text='Submit', command=onsubmit)

check_djisktra.grid(columnspan=1, row=3)
check_a_star.grid(columnspan=3, row=3)
submit.grid(columnspan=2, row=4)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)
# label2.grid(row=2, pady=3)
# prekazka_box.grid(row=2, column=1, pady=3)

window.update()
mainloop()

pygame.init()
openSet.append(start)

def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (600 // stlpce)
    g2 = w // (600 // riadky)
    policko = pole[g1][g2]
    if policko != start and policko != end:
        if policko.stena == False:
            if stena:
                policko.stena = True
                policko.show(black, 0)
            else :
                policko.prekazka = True
                policko.prechod = hodnota_prekazky
                policko.show((125,125,125), 0)
end.show((255, 8, 127), 0)
start.show((255, 8, 127), 0)
loop = True

def set_stena():
    stena = True
    return

def set_prekazka():
    stena = False
    return

def hladaj():
    loop = False
    return

#root = Tk()
#tlac_stena = Button(root, text ="Stena", command = set_stena)
#tlac_stena.pack()

#tlac_prekazka = Button(root, text ="Prekazka", command = set_prekazka)
#tlac_prekazka.pack()

#tlac_hladaj = Button(root, text ="Hladaj", command = hladaj)
#tlac_hladaj.pack()
#root.mainloop()
while loop:
    ev = pygame.event.get()
    
    for event in ev:
        # print(ev)
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break
            elif event.key == pygame.K_w:
                if stena:
                    stena = False
                else: stena = True

for i in range(stlpce):
    for j in range(riadky):
        pole[i][j].addNeighbors(pole)

def heurisitic(n, e):
    d = math.sqrt((n.x - e.x)**2 + (n.y - e.y)**2)
    #d = abs(n.i - e.i) + abs(n.j - e.j)
    return d

#def zamaluj(pole):
#    for node in pole:
#        node.show(yellow,0)

najdene, neexistuje = False,False
vysledok = 0


def vykres(node):
    if node.ciel:
        print("koniec")
    else:
       node.show(yellow,0)
       vykres(node.previous)

#def main():
while not najdene and not neexistuje:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
    metoda = False
    start.ciel = True
    if start != end :
        if not a_star.get() and not djisktra.get(): metoda = True # osetrenie ked sa nezada nic
        start.value = 0
        if djisktra.get() or metoda:
        #if metoda == "dijsktra":
        # dorobit vyber dalsich algortmov 
            current = start #bod ktory prehladava svojich susedov         
            while len(openSet) > 0:
                #lowestIndex = 0
                current = openSet[0]
                current.visable = True
                for node in current.susedia:
                    if node not in closedSet:       # pozrieme sa ci sme ho uz neprehladali
                        if node.x == end.x and node.y == end.y:
                            najdene = True          # porovname s cielom
                            node.previous = current
                            vysledok = current.value
                            vykres(current)
                            break
                        else:
                            if node.value > current.value + node.prechod:  # prepiseme cenu cesty k nemu
                                node.value = current.value + node.prechod  # pozrieme sa ci je tam prekazka
                                node.previous = current
                                if node not in openSet:
                                    openSet.append(node)
                            if not node.prekazka: node.show(green,0)


                end.show((255, 8, 127), 0)
                start.show((255, 8, 127), 0)
                closedSet.append(current)
                current.show((255, 0, 255),4)

                openSet.pop(0)

                if len(openSet) == 0 :
                    neexistuje = True
                pygame.display.update()
                if najdene : break
        #elif metoda == "a":
        elif a_star.get():
            while len(openSet) > 0:
                lowestIndex = 0
                for i in range(len(openSet)):           # najdenie v prislusnych vrcholov ten, co ma najlepsiu cenu
                    if openSet[i].f < openSet[lowestIndex].f:
                        lowestIndex = i


                current = openSet[lowestIndex]
                if current == end:
                    print("koniec programu a_star")
                    vysledok = current.g
                    vykres(current)
                    najdene = True
                    break


                openSet.pop(lowestIndex)
                closedSet.append(current)
                current.show((255, 0, 255),4)
                for i in range(len(current.susedia)):
                    sused = current.susedia[i]
                    sused.value = sused.prechod
                    #sused.show(green,0)
                    if sused not in closedSet:
                        tempG = current.g + current.value
                        if sused in openSet:
                            if sused.g > tempG:
                                sused.g = tempG
                        else:
                            sused.g = tempG
                            openSet.append(sused)
                            if not sused.prekazka: sused.show(green,0)

                    sused.h = heurisitic(sused, end)
                    sused.f = sused.g + sused.h

                    if sused.previous == None:
                        sused.previous = current
                
                end.show((255, 8, 127), 0)
                start.show((255, 8, 127), 0)

Tk().wm_withdraw()
if najdene and not neexistuje :
    result = messagebox.askokcancel('Program Finished', ('Program skoncil \n Najkratsia cesta ' + str(vysledok) + ' policok daleko' ))
elif not najdene and neexistuje:
    result = messagebox.askokcancel('Program Finished', ('Program skoncil \n Cesta sa nenasla' ))

pygame.quit()


