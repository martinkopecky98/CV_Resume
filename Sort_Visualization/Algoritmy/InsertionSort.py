from Algoritmy.Sort import Sort
class InsertionSort(Sort):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

    def sort(self, list):
        #self.vykres()
        self.pole = list
        self.sortovanie(list)

    def sortovanie(self, list ):

        for i in range(1, len(list)):

            key = list[i]
            j = i - 1
            while j >= 0 and key < list[j]:
                self.kresli(list, self.canvas,[j+1, j])
                list[j + 1] = list[j]
                j -= 1
            self.kresli(list, self.canvas, [j + 1, i])
            list[j + 1] = key


    def __call__(self):
        return "Insertion_Sort"