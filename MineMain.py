'''
Author: Chloris
LastData: 2021-12-25
'''

import pygame
import sys
import script
from pygame.locals import *

''' 
import and load resources
'''

# -- start --
# image loader
image_blank = pygame.image.load("resources/blank.png")
image_num_zero = pygame.image.load("resources/num_zero.png")
image_num_one = pygame.image.load("resources/num_one.png")
image_num_two = pygame.image.load("resources/num_two.png")
image_num_three = pygame.image.load("resources/num_three.png")
image_num_four = pygame.image.load("resources/num_four.png")
image_mine = pygame.image.load("resources/mine.png")
image_boom = pygame.image.load("resources/boom.png")
image_flag = pygame.image.load("resources/flag.png")
image_smile = pygame.image.load("resources/smile.png")
image_victory = pygame.image.load("resources/victory.png")
image_lose = pygame.image.load("resources/cryface.png")
image_author = pygame.image.load("resources/rights.png")

dic = { 'mine': image_mine, 
        'boom': image_boom,
        'zero': image_num_zero,
        'one': image_num_one,
        'two': image_num_two, 
        'three': image_num_three,
        'four': image_num_four,
        'blank': image_blank,
        'flag': image_flag}
# -- end --

def transform_num(num):
    if num == 0:
        return 'zero'
    if num == 1:
        return 'one'
    if num == 2:
        return 'two'
    if num == 3:
        return 'three'
    if num == 4:
        return 'four'

def BLITPIC(winning = False): # Update each Unit's status
    screen = pygame.display.set_mode((480, 300)) # (360, 300)
    for i in range(9):
        for j in range(9):
            tmp = script.MineMap[i][j]
            if tmp.revealed == False:
                screen.blit(image_blank, (30 * i + 10, 30 * j + 10))
                continue
            if tmp.marked == True:
                screen.blit(image_flag, (30 * i + 10, 30 * j + 10))
                continue
            if tmp.status == 'Num':
                screen.blit(dic[transform_num(tmp.value)], (30 * i + 10, 30 * j + 10))
            if tmp.status == 'Mine':
                screen.blit(image_mine, (30 * i + 10, 30 * j + 10))
    screen.blit(image_author, (300, 155))
    if not winning:
        screen.blit(image_smile, (300, 105))
    else:
        screen.blit(image_victory, (300, 105))
    
    return screen

def OutPut():
    screen = pygame.display.set_mode((480, 300))
    for i in range(9):
        for j in range(9):
            tmp = script.MineMap[i][j]
            if tmp.status == 'Mine':
                screen.blit(image_mine, (30 * i + 10, 30 * j + 10))
                continue
            if tmp.revealed == False:
                screen.blit(image_blank, (30 * i + 10, 30 * j + 10))
                continue
            if tmp.status == 'Num':
                screen.blit(dic[transform_num(tmp.value)], (30 * i + 10, 30 * j + 10))
                continue
            if tmp.marked == True:
                screen.blit(image_flag, (30 * i + 10, 30 * j + 10))
                continue
    screen.blit(image_lose, (300, 105))
    screen.blit(image_author, (300, 155))
    return screen


'''
<Event(1025-MouseButtonDown {'pos': (293, 292), 'button': 1, 'touch': False, 'window': None})>
<Event(1026-MouseButtonUp {'pos': (293, 292), 'button': 1, 'touch': False, 'window': None})>
'''

def get_id(pos): # return the row and col through the click position
    x, y = pos[0], pos[1]
    for i in range(9):
        for j in range(9):
            x_ = 30 * i + 10; y_ = 30 * j + 10
            if x >= x_ and x <= x_ + 30 and y >= y_ and y <= y_ + 30:
                return (i, j)
    return (-1, -1)  # click not in the gameboard

def Check():  # Check every mine unit to see if every unit has been marked successfully
    Win = True
    for i in range(9):
        if Win == False:
            break
        for j in range(9):
            if script.MineMap[i][j].status == 'Mine':
                if script.MineMap[i][j].marked == False:
                    Win = False
                    break
    return Win

def main():
    FirstClick = True
    pygame.init()
    
    pygame.display.set_caption("MineSweeper")

    #background = pygame.Surface((500, 500))
    #background = background.convert()
   
    # screen.blit(background, (0, 0))
    screen = BLITPIC()
    pygame.display.flip()
    IsWin = -1
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            screen = BLITPIC()
            pygame.display.flip()
            
            if event.type == 1025: # Click Mouse Button
                if event.button == 1: # Left Button   
                    position = event.pos
                    Mine_id = get_id(position)
                    tmp_Mine = script.MineMap[Mine_id[0]][Mine_id[1]]
                    if Mine_id == (-1, -1): # Check if the click in the gameboard reigion
                        continue
                    if FirstClick:
                        script.Init(Mine_id[0], Mine_id[1])
                        FirstClick = not FirstClick
                    if tmp_Mine.revealed == False and tmp_Mine.status == 'Mine':
                        IsWin = False
                        break
                    if tmp_Mine.revealed == True and tmp_Mine.status == 'Num':
                        script.double_click(Mine_id[0], Mine_id[1])
                        continue
                    if tmp_Mine.status == 'Mine':
                        IsWin = 0
                        break
                    script.click(Mine_id[0], Mine_id[1])
                if event.button == 3: # Right Button
                    position = event.pos
                    Mine_id = get_id(position)
                    x = Mine_id[0]; y = Mine_id[1]
                    if script.MineMap[x][y].status == 'Num' and script.MineMap[x][y].revealed == True and script.MineMap[x][y].marked == False:
                        continue
                    if script.MineMap[x][y].marked == True:
                        script.MineMap[x][y].marked = False
                        script.MineMap[x][y].revealed = False
                        script.Remain_Mine_Num += 1
                    else: 
                        script.MineMap[x][y].marked = True
                        script.MineMap[x][y].revealed = True
                        script.Remain_Mine_Num -= 1
                if Check():
                    IsWin = 1
                    break
        if IsWin != -1:
            break
    if IsWin == 1:
        screen = BLITPIC(True)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
    else:
        screen = OutPut()
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

if __name__ == '__main__':
    main()
    
