import pygame

MAX_HEALTH = 100

class Monster:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.health = 100
