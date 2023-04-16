import datetime

import pygame
import random

from os import listdir
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 1200, 700

colors = ['blue', 'pink', 'green', 'gray', 'red', 'purple', 'orange', 'yellow']
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

font = pygame.font.SysFont('Verdana', 50)  # scores font & color

main_surface = pygame.display.set_mode(screen)

img_index = 0

IMGS_PATH = 'goose'

player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = player_imgs[0]
player = pygame.transform.scale(player, (player.get_width() // 1.5, player.get_height() // 1.5))
player_rect = player.get_rect()
player_speed = 5

CHANGE_ANIM = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_ANIM, 125)

scores = 0


# ENEMY

def create_enemy():
    enemy = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(3, 7, )
    return [enemy, enemy_rect, enemy_speed]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

enemies = []


# BONUS

def create_bonus():
    bonus = pygame.image.load('bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus, (bonus.get_width() // 1.3, bonus.get_height() // 1.3))
    bonus_rect = pygame.Rect(random.randint(0, width - 40), 0, bonus.get_width(), bonus.get_height())
    bonus_speed = random.randint(1, 3)
    return [bonus, bonus_rect, bonus_speed]


CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3500)

bonuses = []

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen)
bgH = 0
bgW = bg.get_width()
bg_speed = 3

is_working = True

while is_working:

    FPS.tick(90)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_ANIM:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]

    pressed_keys = pygame.key.get_pressed()

    bgH -= bg_speed
    bgW -= bg_speed

    if bgH < - bg.get_width():
        bgH = bg.get_width()

    if bgW < - bg.get_width():
        bgW = bg.get_width()

    main_surface.blit(bg, (bgH, 0))
    main_surface.blit(bg, (bgW, 0))

    main_surface.blit(player, player_rect)

    main_surface.blit(font.render(str(scores), True, RED), (width - 60, 0))

    # ENEMY CICLE

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            is_working = False

    # BONUS CICLE

    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    # KEYBOARD

    if pressed_keys[K_DOWN] and not player_rect.bottom >= height:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    # print(len(enemies))

    pygame.display.flip()

