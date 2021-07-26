from Algoritmy.Sort import Sort
class MergeSort(Sort):
    def __init__(self, canvas):
        super().__init__()
        pole = []
        self.canvas = canvas

    def sort(self, zoznam):
        self.pole = zoznam
        #self.vykres()
        return(self.sortovanie(zoznam))

    def sortovanie(self, zoznam):
        if (len(zoznam) <= 1):
            return zoznam
        middle = len(zoznam)//2
        leftZ = zoznam[:middle]
        rightZ = zoznam[middle:]

        leftZ = self.sortovanie(leftZ)
        rightZ = self.sortovanie(rightZ)

        return list(self.merge(leftZ,rightZ))

    def merge(self, leftZ, rightZ):
        res = []
        index = 0
        while len(leftZ) != 0 and len(rightZ) != 0:

            self.kresli(self.pole, self.canvas, [leftZ[index], rightZ[index]])
            if leftZ[0] < rightZ[0]:
                res.append(leftZ[0])
                leftZ.remove(leftZ[0])
                # res.append(leftZ.remove(leftZ.index(0)))
            else:
                res.append(rightZ[0])
                rightZ.remove(rightZ[0])
                # res.append(rightZ.remove(rightZ.index(0)))
            index += 1
        if len(leftZ) == 0:
            res += rightZ
        else:
            res += leftZ
        print(res)
        return res

    def __call__(self):
        return "MergeSort"