from Algoritmy.BoublleSort import *
from Algoritmy.InsertionSort import *
from Algoritmy.QuickSort import *
from Algoritmy.MergeSort import *
from Algoritmy.ShellSort import *

from random import randint

class Controler():
    def __init__(self, canvas):
        self.canvas = canvas
        self.pole = []
        self.tvary = []
        RED = (255, 0, 0)
        BLUE = (0, 0, 255)
        GREEN = (0, 255, 0)
        self.sirka, self.vyska, self.medzera = 800, 600, 5

    def boubllesort(self):
        sort = BoublleSort(self.canvas)
        sort.sort(self.pole)

    def insertionsort(self):
        sort = InsertionSort(self.canvas)
        sort.sort(self.pole)

    def quicksort(self):
        sort = QuickSort(self.canvas)
        sort.sort(self.pole)

        sort = BoublleSort(self.canvas)
        sort.sort(self.pole)
        # sort.sort(self.pole)

    def mergesort(self):
        sort = MergeSort( self.canvas)
        sort.sort(self.pole)

    def shellsort(self):
        sort = ShellSort(self.canvas)
        sort.sort(self.pole )

        sort = BoublleSort(self.canvas)
        sort.sort(self.pole)

    #
    # def zamiesanie(self, pocet):
    #     self.pole.clear()
    #     if pocet == 0:
    #         for i in range(0, 20):
    #             self.pole.append(randint(0, 500))
    #     else:
    #         for i in range(0, pocet):
    #             self.pole.append(randint(0, 500))

    def zamiesanie(self, pocet = 30):
        self.pole.clear()
        for i in range(pocet):
            self.pole.append(randint(0, 500))
        self.kresli(0)

    def info(self):
        pass

    def kresli(self, clanok):
        self.canvas.create_rectangle(0, 0, self.sirka, self.vyska, fill='blue')
        self.canvas.delete("all")
        osX = 0
        dlzka_policka = self.sirka / (len(self.pole))
        for index, i in enumerate(self.pole):
            if index == clanok:
                self.canvas.create_rectangle(osX, self.vyska, (osX + dlzka_policka), self.vyska - i, fill='green')
            else:
                self.canvas.create_rectangle(osX, self.vyska, (osX + dlzka_policka), self.vyska - i, fill='red')

            osX = osX + dlzka_policka
        self.canvas.pack()
        self.canvas.update()

    def vymaz_tvary(self):
        for tvar in self.tvary:
            tvar.delete()
    #
    # def set_velkost(self, velkost):
    #     self.zamiesanie(velkost)