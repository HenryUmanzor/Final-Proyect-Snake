""""""""""
This Game is Snake, but the fruit go flying around randomly
"""""""""""
import pygame
import time
from pygame.math import Vector2
import random
import sys
TESTTIMERSTA = time.time()
pygame.init()
"""""""""
Window Parameters
"""""""""
#Grid Parametrs too
cell_size = 40
cell_amount = 20
Fps_cap = 60
Width,Height = (cell_size * cell_amount),(cell_size * cell_amount)
Window = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("la culebra")
           
"""
Object Parameters
"""
#Images
Apple_img =pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Apple.png").convert_alpha()),(cell_size,cell_size))
#Sounds
#Classes
class Apple:
    def __init__(self):
        self.Apple_reroll()
        
    def write_apple(self):
        Apple_cell = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        Window.blit(Apple_img, Apple_cell)
    def Apple_reroll(self):
        self.x = random.randint(0,(cell_amount - 1))
        self.y = random.randint(0,(cell_amount - 1))
        print(f"Apple coords: {self.x} , {self.y}")
        self.pos = Vector2(self.x,self.y)

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(6,10),Vector2(7,10)]
        self.dir =  Vector2(1,0)
        self.apple_eaten = False
        #Head Img
        self.head_up = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Head_up.png").convert_alpha()),(cell_size,cell_size))
        self.head_down = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Head_Down.png").convert_alpha()),(cell_size,cell_size))
        self.head_left = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Head_Left.png").convert_alpha()),(cell_size,cell_size))
        self.head_right  = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Head_Right.png").convert_alpha()),(cell_size,cell_size))
        #Tail Img
        self.tail_up = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Tail_Up.png").convert_alpha()),(cell_size,cell_size))
        self.tail_down = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Tail_Down.png").convert_alpha()),(cell_size,cell_size))
        self.tail_left = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Tail_Left.png").convert_alpha()),(cell_size,cell_size))
        self.tail_right  = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Tail_Right.png").convert_alpha()),(cell_size,cell_size))
        #Intersecctions
        self.cross_ld = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Cross_Left_Down.png").convert_alpha()),(cell_size,cell_size))
        self.cross_lu = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Cross_Left_Up.png").convert_alpha()),(cell_size,cell_size))
        self.cross_rd = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Cross_Right_Down.png").convert_alpha()),(cell_size,cell_size))
        self.cross_ru = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Cross_Right_Up.png").convert_alpha()),(cell_size,cell_size))
    def write_snake(self):
        for x in self.body:
            Snake_cell = pygame.Rect(x.x * cell_size,x.y * cell_size,cell_size, cell_size)
            pygame.draw.rect(Window,DARK_BLUE,Snake_cell)



            
    def movement(self):
        if self.apple_eaten == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.dir)
            self.body = body_copy[:]
            self.apple_eaten = False
        body_copy = self.body[:-1]
        body_copy.insert(0,body_copy[0] + self.dir)
        self.body = body_copy[:]
    def grow(self):
        self.apple_eaten = True


"""
colors
"""
RED = (206,84,47)
DARK_GREEN = (173,205,95)
LIGHT_GREEN = (180,211,102)
MID_BLUE = (98,128,229)
DARK_BLUE = (86,115,219)

"""
Main Loop
"""
class MAINFUNCIONS:
    def __init__(self):
        self.Apple = Apple()
        self.Snake = Snake()
    def game_update(self):
        self.Snake.movement()
        self.apple_collision()
        self.death_collision()

    def write_items(self):
        self.Apple.write_apple()
        self.Snake.write_snake()
    def apple_collision(self):
        if self.Apple.pos == self.Snake.body[0]:
            self.Apple.Apple_reroll()
            self.Snake.grow()
    def  death_collision(self):
        if not 0 <=self.Snake.body[0].x < cell_amount:
            self.death_state()
        elif not 0 <=self.Snake.body[0].y < cell_amount:
            self.death_state()
    def death_state(self):
        TESTTIMEREND = time.time()
        print(f"time elapsed: {round((TESTTIMEREND - TESTTIMERSTA),2)}, closed by death")
        pygame.quit()
        sys.exit()
def main():
    """
    IMPORTANT VARIABLES
    """
    main_functions = MAINFUNCIONS()
    clock = pygame.time.Clock()
    Screen_Refresh = pygame.USEREVENT
    pygame.time.set_timer(Screen_Refresh,150)
    active = True
    while active:
        clock.tick(Fps_cap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            if event.type == Screen_Refresh:
                main_functions.game_update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_functions.Snake.dir.y !=1:
                        main_functions.Snake.dir = Vector2(0,-1)
                elif event.key == pygame.K_LEFT:
                    if main_functions.Snake.dir.x !=1:
                        main_functions.Snake.dir = Vector2(-1,0)
                elif event.key == pygame.K_RIGHT:
                    if main_functions.Snake.dir.x !=-1:
                        main_functions.Snake.dir = Vector2(1,0)
                elif event.key == pygame.K_DOWN:
                    if main_functions.Snake.dir.y !=-1:
                        main_functions.Snake.dir = Vector2(0,1)
            Window.fill(LIGHT_GREEN)
            main_functions.write_items()
            main_functions.game_update()
        pygame.display.update()
    TESTTIMEREND = time.time()
    print(f"time elapsed: {round((TESTTIMEREND - TESTTIMERSTA),2)}, closed by u")
    pygame.quit()

if __name__ == "__main__":
    main()