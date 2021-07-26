# import pygame
import time
class Sort:
    def __init__(self):
        pass

    RED =  (255,0,0)
    BLUE = (0,0,255)
    GREEN = (0,255,0)
    sirka, vyska, medzera = 800, 600, 5

   # pygame.init()
    #screen = pygame.display.set_mode((vyska, sirka))
    def get_name(self):
        pass

    def sort(self, list, screen):
        pass

    #
    # def vykres(self):
    #     #
    #     # pygame.init()
    #     # screen = pygame.display.set_mode((self.vyska, self.sirka))
    #     self.screen.fill(self.GREEN)
    #     pygame.display.update()
    #     time.sleep(3)

    def kresli(self, pole, canvas, clanky):
        # dlzka_policka = len(pole)// self.sirka
        # #velkosti = []
        #
        # okno = pygame.display.set_mode((800, 600))
        # osX = 0
        # screen.fill(self.GREEN)
        # for index, i in enumerate(pole):
        #     #velkosti.append(vyska // 10 * i)
        #     pygame.draw.rect(okno, self.GREEN, (osX, self.sirka, self.vyska // 50 * i, dlzka_policka))
        #     osX += dlzka_policka + 5
        # pygame.display.update()
        # time.sleep(0.5)
        canvas.delete("all")
        canvas.create_rectangle(0, 0, self.sirka, self.vyska, fill='blue')
        osX = 0
        dlzka_policka = self.sirka / (len(pole))
        done = False
        for index, i in enumerate(pole):
            if index in clanky:
                if not done:
                    canvas.create_rectangle(osX, self.vyska, (osX + dlzka_policka), self.vyska - i, fill='green')
                    done = True
                else:
                    canvas.create_rectangle(osX, self.vyska, (osX + dlzka_policka), self.vyska - i, fill='yellow')

            else:
                canvas.create_rectangle(osX, self.vyska, (osX + dlzka_policka), self.vyska - i, fill='red')

            osX = osX + dlzka_policka
        canvas.pack()
        canvas.update()
        time.sleep(0.01)