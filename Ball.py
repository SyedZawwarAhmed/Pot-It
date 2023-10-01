import pygame
import math

circle_radius= 50

class Ball():
    max_speed = 30

    def __init__(self, x, y):
        self.pos = (x, y)
        self.speed = 0
        mx, my = pygame.mouse.get_pos()
        self.dir = [-mx + x, -my + y]
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = [0, -1]
        else:
            self.dir = [self.dir[0]/length, self.dir[1]/length]

        self.ball = pygame.Rect(self.pos[0], self.pos[1], circle_radius, circle_radius)

    def update(self):  
        self.pos = (self.pos[0] + self.dir[0] * self.speed, self.pos[1] + self.dir[1] * self.speed)
        self.speed -= 0.08
        self.ball = pygame.Rect(self.pos[0], self.pos[1], circle_radius, circle_radius)


    def setDirection(self):
        mx, my = pygame.mouse.get_pos()
        self.dir = [-mx + self.pos[0], -my + self.pos[1]]
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = [0, -1]
        else:
            self.dir = [self.dir[0]/length, self.dir[1]/length]

        self.ball = pygame.Rect(self.pos[0], self.pos[1], circle_radius, circle_radius)
    
    def setSpeed(self):
        mx, my = pygame.mouse.get_pos()
        calculated_speed = math.sqrt((mx-self.pos[0])**2 + (my-self.pos[1])**2) / 10
        if calculated_speed > self.max_speed:
            self.speed = self.max_speed
        else:
            self.speed = calculated_speed