from Controler import *
from tkinter import *
from tkinter import messagebox

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
sirka, vyska, medzera = 800, 600, 5
root = Tk()
canvas = Canvas(root, bg="blue", height=vyska, width=sirka)
controler = Controler(canvas)

def info():
    messagebox.showinfo(title="Info", message="Toto je program sluziaci na vyzualizaciu trediacich algoritmov "
                                              "zadaj pocet, zamiesaj a vyber si algortmus")
def zamiesanie():
    controler.zamiesanie()
def end():
    root.destroy()

def b_sort():
    controler.boubllesort()
    messagebox.showinfo(title="Hotovo", message="Program utriedil pole" )

def i_sort():
    controler.insertionsort()
    messagebox.showinfo(title="Hotovo", message="Program utriedil pole" )

def q_sort():
    controler.quicksort()
    messagebox.showinfo(title="Hotovo", message="Program utriedil pole" )

# def m_sort():
#     controler.mergesort()
#     messagebox.showinfo(title="Hotovo", message="Program utriedil pole")
#
def s_sort():
    controler.shellsort()
    messagebox.showinfo(title="Hotovo", message="Program utriedil pole")


# tlac_zamiesaj = Button(root, text ="Zamiesaj", command =zamiesanie)
# tlac_zamiesaj.pack()
#
# tlac_info = Button(root, text ="Info", command = info)
# tlac_info.pack()
#
# tlac_info = Button(root, text ="Sortuj", command = info)
# tlac_info.pack()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Boublle Sort", command=b_sort)
filemenu.add_command(label="Insertion Sort", command=i_sort)
filemenu.add_command(label="Quick Sort", command=q_sort)
filemenu.add_command(label="Shell Sort", command=s_sort)
# filemenu.add_command(label="Marge Sort", command=m_sort)
filemenu.add_separator()
filemenu.add_command(label="Close", command=end)
menubar.add_cascade(label="Algoritmy", menu=filemenu)

commandMenu = Menu(menubar, tearoff=0)
commandMenu.add_command(label="Zamiesaj", command=zamiesanie)
commandMenu.add_separator()
commandMenu.add_command(label="Info", command=info)

menubar.add_cascade(label="Pomocky", menu=commandMenu)

root.config(menu=menubar)

L1 = Label(root, text="Velkost pola")
L1.pack()
E1 = Entry(root, bd =5)
E1.pack()

def set_velkost():
    controler.zamiesanie(int(E1.get()))
tlac_potvrd = Button(root, text ="Potvrd", command = set_velkost)
tlac_potvrd.pack()

controler.zamiesanie()

root.mainloop()

