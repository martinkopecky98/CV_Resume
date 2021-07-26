from Algoritmy.Sort import Sort
class BoublleSort(Sort):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

    def sort(self, list):
        #self.vykres()
        self.pole = list
        self.sortovanie(list)

    def sortovanie(self, list ):

        change = True
        while change:
            # print(self.pole)

            change = False
            for index, i in enumerate(list):
                indexy = []
                indexy.append(index)
                indexy.append(index+1)
                self.kresli(list, self.canvas, indexy)
                if(len(list) > index+1):
                    if (i > list[index+1]):
                        #self.kresli(list, screen,index)
                        pom = list[index]
                        list[index] = list[index + 1]
                        list[index + 1] = pom
                        change = True


    def get_name(self):
        return "BoubleSort"