import pygame as pg 
from pygame.locals import *
from math import cos, sin, radians
from random import randint, uniform

class Boid():

    def __init__(self, root, bs):
        self.root=root
        self.bs=bs

        self.boid_img=pg.image.load("triangle.png").convert_alpha()
        self.boid_img=pg.transform.scale(self.boid_img, (bs, bs))

        self.r=pg.transform.rotate
        self.boid_img=self.r(self.boid_img, -45)

        self.boidObject=self.boid_img
        self.x=self.root.get_width()/2-self.boidObject.get_width()/2
        self.y=self.root.get_height()/2-self.boidObject.get_height()/2
        self.a1=0
        self.a2=0
        self.a2Sens=True

        self.otherB=[]

    def aleaMove(self): 
        if uniform(0, 1) > .991: self.orient(randint(0, 360))

        self.animRL()
        self.move()
        self.blit()

    def scan(self, r):
        out=[]
        for i in self.otherB:
            if self.x-r<=i.x<=self.x+r and self.y-r<=i.y<=self.y+r and i!=self: out.append([i.x, i.y, i.a1, i])
        return out

    def blit(self): self.root.blit(self.boidObject, (self.x, self.y))

    def animRL(self):
        if self.a2Sens and self.a2<=self.a1+8: self.a2+=2
        else: self.a2Sens=False

        if not self.a2Sens and self.a2>=self.a1-8: self.a2-=2
        else: self.a2Sens=True 

        self.boidObject=self.r(self.boid_img, self.a2)

    def orient(self, a):
        if self.a1!=a:
            self.a1=a
            self.boidObject=self.r(self.boid_img, self.a1)

            if self.a2>=self.a1+8: self.a2-=self.a2-(self.a1+8)
            elif self.a2<=self.a1-8: self.a2+=(self.a1-8)-self.a2

    def move(self, border=False):
        if not border:
            self.x+=cos(self.a1*3.14/180)*4
            if self.x>self.root.get_width(): self.x=0-self.bs
            elif self.x<0-self.bs: self.x=self.root.get_width()
            
            self.y-=sin(self.a1*3.14/180)*4
            if self.y>self.root.get_height(): self.y=0-self.bs
            elif self.y<0-self.bs: self.y=self.root.get_height()

    def step(self, ok=[True, True, True]):
        """
            Remplacer l'un des 0 par l'appel de votre méthode.
            Au debut de votre méthode penser à mettre une condition True/False, pour qu'elle s'effectue sinon retourner 0. Ca servira dans le menu d'options pour enlever les
            règles que l'on souhaite.
            Du coup vos méthodes doivent avoir un paramettre qui sera par exmple ok=ok[0, 1, ou 2].
        """
        newA=sum([0, 0, 0])/3
        self.orient(newA)
        self.animRL()
        self.move()
        self.blit()

    """
        Explications :
            scan() --> r c le rayon que l'on veux scanner; ça retourne une liste de listes des coords des boids se trouvant autour de ce boid.
    """
    #Méthodes Mattéo


    #Méthodes Antonin



if __name__ == "__main__":
    pg.init()

    pg.display.set_caption('Boids')
    root=pg.display.set_mode((500, 500))
    clock=pg.time.Clock()

    boids=[Boid(root, 20) for i in range(1)]
    for boid in boids: boid.otherB=boids

    loop=True
    while loop:
        for e in pg.event.get():
            if e.type == QUIT: loop=False

        root.fill((244, 234, 232))

        for boid in boids: boid.step()

        clock.tick(24)

        pg.display.update()