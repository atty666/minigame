import pygame
import random

from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1200, 700

colors = [ 'blue', 'pink', 'green', 'gray', 'red', 'purple', 'orange', 'yellow' ]
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255,0,0
GREEN = 0, 255, 0

font = pygame.font.SysFont('Verdana', 20) #scores font & color

main_surface = pygame.display.set_mode(screen)

# player = pygame.Surface((20, 20))
# player.fill(WHITE)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()
player_speed = 5

scores = 0

#ENEMY

def create_enemy():
   # enemy = pygame.Surface ((30,30))
   # enemy.fill (RED)
   enemy = pygame.image.load('enemy.png').convert_alpha()
   enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
   enemy_speed = random.randint(3, 5,)
   return [enemy, enemy_rect, enemy_speed]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []

#BONUS

def create_bonus():
   #  bonus = pygame.Surface((15, 15))
   #  bonus.fill(GREEN)
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = pygame.Rect(random.randint(0, width - 20), 0, *bonus.get_size())
    bonus_speed = random.randint(3, 5)
    return [bonus, bonus_rect, bonus_speed]

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)

bonuses = []

bg = pygame.transform.scale (pygame.image.load('background.png').convert(), screen)
bgH = 0
bgW = bg.get_width()
bg_speed =  3

is_working = True 

while is_working:

   FPS.tick(100)

   for event in pygame.event.get():
    if event.type == QUIT: 
        is_working = False

    if event.type == CREATE_ENEMY:
       enemies.append(create_enemy())

    if event.type == CREATE_BONUS:
       bonuses.append(create_bonus())


   pressed_keys = pygame.key.get_pressed()

   # main_surface.fill(BLACK)

   # main_surface.blit(bg, (0, 0))

   bgH -= bg_speed
   bgW -= bg_speed

   if bgH < - bg.get_width():
      bgH = bg.get_width()

   if bgW <- bg.get_width(): 
      bgW = bg.get_width()

   main_surface.blit(bg, (bgH, 0))
   main_surface.blit(bg, (bgW, 0))

   main_surface.blit(player, player_rect)

   main_surface.blit(font.render(str(scores), True, GREEN), (width - 30, 0))

 #ENEMY CICLE

   for enemy in enemies:
      enemy[1] = enemy[1].move(-enemy[2], 0)
      main_surface.blit(enemy[0], enemy[1])

      if enemy[1].left < 0:
         enemies.pop(enemies.index(enemy))

      if player_rect.colliderect(enemy[1]):
         is_working=False

#BONUS CICLE

   for bonus in bonuses:
    bonus[1] = bonus[1].move(0, bonus[2])
    main_surface.blit(bonus[0], bonus[1])

    if bonus[1].bottom >= height:
        bonuses.pop(bonuses.index(bonus))

    if player_rect.colliderect(bonus[1]):
        bonuses.pop(bonuses.index(bonus))
        scores += 1

#KEYBOARD

   if pressed_keys[K_DOWN] and not player_rect.bottom >=height:
      player_rect = player_rect.move(0, player_speed)
   
   if pressed_keys[K_UP] and not player_rect.top <= 0:
      player_rect = player_rect.move(0, -player_speed)

   if pressed_keys[K_LEFT] and not player_rect.left <=0:
      player_rect = player_rect.move(-player_speed, 0)

   if pressed_keys[K_RIGHT] and not player_rect.right >=width:
      player_rect = player_rect.move(player_speed, 0)

   # delete "#"" to show amount enemy on screen console
   #print(len(enemies))

   pygame.display.flip()   