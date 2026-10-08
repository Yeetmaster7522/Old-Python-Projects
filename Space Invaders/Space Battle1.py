import sys
import pygame
import time
from ship import Ship
from bullet import Bullet
from button import Button
from pygame.sprite import Sprite
from pygame.sprite import Group

screen_width=1000
screen_height=600
bg_color = (0,0,0)

alien_speed_factor = 1.5
fleet_drop_speed = 15
fleet_direction = 1
Alien_increase_speed = 1.3
highscore= 0

class Alien(Sprite):
    def __init__(self,screen):
        super(Alien, self).__init__()
        self.screen = screen

        self.image = pygame.image.load("alien.bmp")
        self.rect = self.image.get_rect()

        self.x = self.rect.width
        self.y = self.rect.height

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        self.x += (alien_speed_factor * fleet_direction)
        self.rect.x = int(self.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

def displayText(screen,text):
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 50)
    textsurface = font.render(text, False, (76, 0, 153))
    screen.blit(textsurface, (int(screen_width * 0.38), int(screen_height * 0.75)))

def displayscore(screen, score):
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    textsurface = font.render("Score: " + str(score), False, (76, 0, 153))
    screen.blit(textsurface, (int(screen_width * 0.55), 10))

def displayhighscore(screen, highscore):
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    textsurface = font.render("Highscore: " + str(highscore), False, (76, 0, 153))
    screen.blit(textsurface, (int(screen_width * 0.75), 10))

def displaylevel(screen, level):
    pygame.font.init()
    font = pygame.font.SysFont("Comic Sans MS", 30)
    textsurface = font.render("Level: " + str(level), False, (76, 0, 153))
    screen.blit(textsurface, (20, 10))

def create_fleet(screen, aliens):
    """Create a full fleet of aliens."""
    alien = Alien(screen)
    alien_width = alien.rect.width
    alien_height=alien.rect.height
    available_space_x = screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / ( 2* alien_width))
    available_space_y = (screen_height - (4 * alien_height) )
    number_rows = int(available_space_y / (2 *  alien_height))
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            alien = Alien(screen)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
            aliens.add(alien)

def move_fleet(aliens, screen, ship, bullets, play_button, game_active):
    global highscore
    global fleet_direction
    global alien_speed_factor

    for alien in aliens.sprites():
        if alien.check_edges():
            for alien in aliens.sprites():
                alien.rect.y += fleet_drop_speed
            fleet_direction *= -1 
            break
        if alien.rect.bottom >= ship.rect.bottom:
            aliens.empty()
            bullets.empty()
            displayText(screen,"GAME OVER")
            game_active = 0
            play_button.draw_button()
            pygame.mouse.set_visible(True)

            score = 0
            level = 1
            alien_speed_factor = 1.5

    return game_active
            
def check_collision(aliens, bullets, score):
    global highscore
    collision = pygame.sprite.groupcollide(bullets, aliens, True , True)
    
    if collision:
        score = score + 10
        if score > highscore:
            highscore = score
    return score
    
def run_game():
    score = 0
    level = 1
    game_active = 0
    global alien_speed_factor
    
    bullets = Group()
    aliens = Group()
    pygame.init()

    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("Space Battle")
    
    screen.fill(bg_color)    
    play_button = Button(screen, "Play")
    ship = Ship(screen)
    alien = Alien(screen)
    create_fleet(screen, aliens)
    
    ship.blitme()
    
    aliens.draw(screen)

    play_button.draw_button()
    pygame.display.flip()

    while True:
        if game_active == 0:
            score = 0
            level = 1
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] and ship.rect.left > ship.screen_rect.left:
            ship.rect.centerx -= 2
        elif pressed[pygame.K_RIGHT] and ship.rect.right < ship.screen_rect.right:
            ship.rect.centerx += 2

        bullet = Bullet(screen, ship)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif pressed[pygame.K_SPACE]:
                bullets.add(bullet)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if play_button.rect.collidepoint(mouse_x, mouse_y):
                    pygame.mouse.set_visible(False)
                    game_active = 1
                    aliens.empty()
                    bullets.empty()
                    create_fleet(screen, aliens)

        if game_active == 1:
            screen.fill(bg_color)
            ship.blitme()
            aliens.draw(screen)

            if len(aliens) == 0:
                aliens.empty()
                bullets.empty
                create_fleet(screen, aliens)
                level += 1
                alien_speed_factor += 1
                
            if pygame.sprite.spritecollideany(ship, aliens):
                pygame.mouse.set_visible(True)
                aliens.empty()
                bullets.empty()
                displayText(screen,"GAME OVER")
                game_active = 0
                alien_speed_factor = 1.5
                play_button.draw_button()
            
            bullets.update()

            for bullet in bullets.sprites():
                bullet.draw_bullet()
            game_active = move_fleet(aliens, screen, ship, bullets,play_button, game_active)
            score = check_collision(aliens, bullets, score)
            displayscore(screen, score)
            displayhighscore(screen, highscore)
            displaylevel(screen, level)
            aliens.update()
           
        pygame.display.flip()

run_game()
