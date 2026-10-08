import sys
import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group

class Bullet(Sprite):
    def __init__(self, screen, ship):
         super(Bullet, self).__init__()
         self.screen = screen

         bullet_width = 5
         bullet_height = 20

         bullet_speed_factor = 3
         
         self.rect = pygame.Rect(0, 0, bullet_width, bullet_height)   
         self.rect.centerx = ship.rect.centerx
         self.rect.top = ship.rect.top
         self.x = self.rect.x
         self.y = self.rect.y

         self.color =(3, 252, 65)
         self.speed_factor = bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
