from Algoritmy.Sort import Sort
class QuickSort(Sort):
    def __init__(self, canvas):
        super().__init__()
        pole = []
        self.canvas = canvas

    def vymena(self, list, min, max):
        print(self.pole)
        #self.kresli(list)
        i = (min - 1)  # index of smaller element
        pivot = list[max]  # pivot


        for j in range(min, max):
            clanky = min, max
            self.kresli(list, self.canvas, clanky)
            # If current element is smaller than the pivot
            if list[j] < pivot:
                # increment index of smaller element
                i = i + 1
                clanky = i,j
                self.kresli(list, self.canvas, clanky)
                list[i], list[j] = list[j], list[i]

        clanky = list[i + 1], list[max]
        self.kresli(list, self.canvas, clanky)
        list[i + 1], list[max] = list[max], list[i + 1]
        return (i + 1)

    def sortovanie(self, list, min, max):
        if min < max:
            # pi is partitioning index, arr[p] is now
            # at right place
            self.kresli(list, self.canvas, [min, max])
            pi = self.vymena(list, min, max)
            # Separately sort elements before
            # partition and after partition
            self.sortovanie(list, min, pi - 1)
            self.sortovanie(list, pi + 1, max)

    def sort(self, list):
        # self.vykres()
        self.pole = list
        self.sortovanie(list, 0, len(list)-1)
        return list

def get_name(self):
        return "QuickSort"