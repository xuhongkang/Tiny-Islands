import tkinter as tk
import os
import glob
from PIL import Image, ImageTk
from game import Game

class TinyIslandsGUI:
    def __init__(self, tilesize=50):
        self.root = tk.Tk()
        self.images = []

        self.set_images()

        self.game = Game()
        self.tilesize = tilesize

        self.root.minsize(self.game.xlength * self.tilesize * 2, self.game.ylength * self.tilesize)

        self.pmain = tk.Frame(self.root)
        self.pside = tk.Frame(self.root, bg = 'lime')

        self.pmain.grid(row=0, column=0, sticky="nsew")
        self.pside.grid(row=0, column=1, sticky="nsew")

        self.root.grid_columnconfigure(0, weight=1, uniform="group1")
        self.root.grid_columnconfigure(1, weight=1, uniform="group1")

        self.draw_board()
        self.draw_panel()
        self.root.mainloop()
    
    def set_images(self):
        filelist = glob.glob(os.path.join("./images", '*.png'))
        for filename in sorted(filelist, key=lambda s: s.lower()): 
            self.images.append(ImageTk.PhotoImage(Image.open(filename).resize((50, 50), Image.ANTIALIAS)))

    def draw_board(self):
        rownum = 0
        for row in self.game.board.tiles:
            colnum = 0
            for tile in row:
                label = tk.Label(self.pmain,image=self.images[tile.type],width=50,height=50,padx=0,pady=0)
                label.grid(row=rownum,column=colnum,sticky=(tk.N, tk.W, tk.E, tk.S))
                colnum += 1
            rownum += 1
    
    def draw_panel(self):
        counter = tk.Label(self.pside, text="TURN "+str(self.game.turn))
        counter.pack()


TinyIslandsGUI()