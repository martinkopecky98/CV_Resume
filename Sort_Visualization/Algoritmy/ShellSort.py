from Algoritmy.Sort import *
class ShellSort(Sort):
    def __init__(self, canvas):
        super().__init__()
        pole = []
        self.canvas = canvas

    def sort(self,list):
        return(self.sortuj(list))

    def sortuj(self, list):
        gap = len(list) // 2
        while gap > 0:
            print(list)
            for i in range(gap, len(list)):
                print(list)
                temp = list[i]
                j = i
                # Sort the sub list for this gap

                while j >= gap and list[j - gap] > temp:
                    self.kresli(list,self.canvas,[j,j-gap])
                    list[j] = list[j - gap]
                    j = j - gap
                list[j] = temp

            # Reduce the gap for the next element

            gap = gap // 2
        return(list)