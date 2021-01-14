import pygame as pg
from pygame.locals import *
import tkinter as tk
from threading import Thread
from PIL import Image

class Pensil():

    def __init__(self, root, ps=6, c=(0, 210, 180), rs=5):
        self.root=root

        self.ps=ps
        self.rs=rs
        self.c=c
        self.h=[]
        self.okP=False
        self.okE=False

    def draw(self): 
        if self.h!=[]:
            for i in self.h: pg.draw.circle(self.root, self.c, (i[0], i[1]), self.ps)
        
    def mouseDraw(self, pos): 
        if self.okP and pos not in self.h: self.h.append(pos)

    def erase(self, pos): 
        if self.okE:
            pg.draw.polygon(self.root, self.c, [(pos[0]-self.rs, pos[1]-self.rs), (pos[0]+self.rs, pos[1]-self.rs), (pos[0]+self.rs, pos[1]+self.rs), (pos[0]-self.rs, pos[1]+self.rs)], 2)
            size=len(self.h)-1
            for i in range(len(self.h)): 
                if self.h[size-i][0]<=pos[0]+self.rs and self.h[size-i][0]>=pos[0]-self.rs and self.h[size-i][1]>=pos[1]-self.rs and self.h[size-i][1]<=pos[1]+self.rs: del self.h[size-i]
                    
    def onOff(self, a, b): self.okP, self.okE=a, b

    def clear(self): self.h=[]

    def scan(self, pos, r):
        out=[]
        for i in range(len(self.h)):
            if pos[0]-r+self.ps<=self.h[i][0]<=pos[0]+r-self.ps and pos[1]-r+self.ps<=self.h[i][1]<=pos[1]+r-self.ps: out.append(self.h[i])
        return out

def settingGUI(pensil):
    palette=Image.open('palette.png')
    paletteRGB=palette.convert('RGB')

    def pixelC(e): 
        pensil.c=paletteRGB.getpixel((e.x, e.y))
        c2.config(bg="#%02x%02x%02x" % pensil.c)
    def pensilSize(x): pensil.ps=int(x)
    def rubberSize(x): pensil.rs=int(x)

    root=tk.Tk()
    root.title("Draw Option")
    posY=root.winfo_screenheight()/2-172
    root.geometry(f'176x344+0+{int(posY)}')
    root.resizable(False, False)
    root.attributes('-toolwindow', 1)

    paletteP=tk.PhotoImage(file='palette.png')

    c=tk.Canvas(root, width=palette.size[0], height=palette.size[1], highlightthickness=0)
    c.create_image(0, 0, anchor=tk.NW, image=paletteP)
    c.pack()

    c2=tk.Canvas(root, width=palette.size[0], height=20, bg="#%02x%02x%02x" % pensil.c)
    c2.pack()

    PensilS=tk.Scale(root, orient=tk.HORIZONTAL, label="Pensil Scale", sliderlength=20, length=palette.size[0], from_=1, to=20, command=lambda x: pensilSize(x))
    PensilS.set(pensil.ps)
    PensilS.pack()

    RubberS=tk.Scale(root, orient=tk.HORIZONTAL, label="Rubber Scale", sliderlength=20, length=palette.size[0], from_=1, to=20, command=lambda x: rubberSize(x))
    RubberS.set(pensil.rs)
    RubberS.pack()

    ResetB=tk.Button(root, width=176, text="Clear", command=pensil.clear)
    ResetB.pack()

    c.bind('<Button-1>', pixelC)

    root.mainloop()

def GUI(pensil):
    th=Thread(target=lambda p=pensil: settingGUI(p))
    th.start()

if __name__ == "__main__":
    pg.init()
    pg.display.set_caption('Draw Option')
    root=pg.display.set_mode((500, 500))

    pensil=Pensil(root)
    GUI(pensil)

    loop=True
    while loop:
        for e in pg.event.get():
            if e.type == QUIT: loop=False

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1: pensil.onOff(True, False)
                elif e.button == 3: pensil.onOff(False, True)
            if e.type == MOUSEBUTTONUP:
                if e.button == 1 or e.button == 3: pensil.onOff(False, False)

        root.fill((244, 234, 232))

        pensil.mouseDraw(pg.mouse.get_pos())
        pensil.erase(pg.mouse.get_pos())
        pensil.draw()

        pg.display.update()