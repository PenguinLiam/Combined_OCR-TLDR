#    Interface    #
'''Interface module for the OCR and TLDR programs... The whole program is displayed through this'''

from tkinter import *


class Application:

    def __init__(self, master):

        frame = Frame(master, width=200, Fill=Y)
        frame.pack()
        




root = Tk()
app = Application(root)
root.mainloop()


