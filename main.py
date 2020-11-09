# coding:utf-8
class Boids():
    # classe Boids initialisé
    nb_boids = 0  # compteur nombre boids créer

    def __init__(self):
        # instance création boids
        Boids.nb_boids += 1  # incrémente le compteur de boids de 1 à chaque création d'1 objet

    def move(self, x, y, teta):
        # instance déplacement en x,y et teta angle d'orientation
        pass