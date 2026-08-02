""""""""""
This Game is Snake, but the fruit go flying around randomly
"""""""""""
import pygame
import time
from pygame.math import Vector2
import random
import sys
TESTTIMERSTA = time.time()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
Snake_Tick = 120
Apple_TIck = 300
"""""""""
Window Parameters
"""""""""
#Grid Parametrs too
cell_size = 40
cell_amount = 20
Fps_cap = 60
Font = pygame.font.Font(None,35)
Width,Height = (cell_size * cell_amount),(cell_size * cell_amount)
Window = pygame.display.set_mode((Width,Height))
pygame.display.set_caption("Snake Tab")
"""
colors
"""
RED = (206,84,47)
DARK_GREEN = (173,205,95)
LIGHT_GREEN = (180,211,102)
MID_BLUE = (98,128,229)
DARK_BLUE = (86,115,219)
SCORE_GREEN = (86,115,55)

"""
Object Parameters
"""
#Apple Image
Apple_img =pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Apple.png").convert_alpha()),(cell_size,cell_size))
#Element Classes
class Background:
    def __init__(self):
        self.surface = pygame.Surface((Width, Height))
        self.surface.fill(LIGHT_GREEN)
        self.generate_grass()

    def generate_grass(self):
        for y in range(cell_amount):
            for x in range(cell_amount):
                if (x + y) % 2 == 0: # Cleaner checkerboard logic
                    grass_draw = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
                    pygame.draw.rect(self.surface, DARK_GREEN, grass_draw)

    def draw(self, window):
        window.blit(self.surface, (0, 0))
class Scoreboard:
    def __init__(self):
        self.font = Font

    def draw_score(self, snake_length):
        score_text = str(snake_length - 3)
        score_surface = self.font.render(score_text, True, (0, 0, 0))
        
        score_x = int(cell_size * cell_amount - 60)
        score_y = int(cell_size * cell_amount - 60)
        
        score_box = score_surface.get_rect(center=(score_x, score_y))
        apple_box = Apple_img.get_rect(midright=(score_box.left, score_box.centery))
        
        score_bg = pygame.Rect(apple_box.left, apple_box.top, apple_box.width + score_box.width + 10, apple_box.height)
        
        pygame.draw.rect(Window, SCORE_GREEN, score_bg)
        Window.blit(score_surface, score_box)
        Window.blit(Apple_img, apple_box)
class Apple:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.pos = Vector2(self.x, self.y)
        self.old_pos = Vector2(self.x, self.y)
        self.dir = Vector2(0, 0)
        
        self.directions = [
            Vector2(0, -1), Vector2(0, 1), Vector2(-1, 0), Vector2(1, 0),
            Vector2(-1, -1), Vector2(1, -1), Vector2(-1, 1), Vector2(1, 1)
        ]
        self.Apple_reroll([])
        
    def write_apple(self,fraction):
        current_x = self.old_pos.x + (self.pos.x - self.old_pos.x) * fraction
        current_y = self.old_pos.y + (self.pos.y - self.old_pos.y) * fraction
    
        Apple_cell = pygame.Rect(int(current_x * cell_size),int(current_y* cell_size),cell_size,cell_size)
        Window.blit(Apple_img, Apple_cell)
    def Apple_reroll(self,inside_snake):
        while True:
            self.x = random.randint(0, (cell_amount - 1))
            self.y = random.randint(0, (cell_amount - 1))
            self.pos = Vector2(self.x, self.y)
            if self.pos not in inside_snake:
                break
            print(f"Apple coords: {self.x} , {self.y}")
        self.old_pos = Vector2(self.pos.x, self.pos.y)
        self.dir = random.choice(self.directions)
    def Apple_movement(self):
        self.old_pos = Vector2(self.pos.x, self.pos.y)
        
        if self.pos.x + self.dir.x < 0 or self.pos.x + self.dir.x >= cell_amount:
            self.dir.x *= -1 
        if self.pos.y + self.dir.y < 0 or self.pos.y + self.dir.y >= cell_amount:
            self.dir.y *= -1 
        self.pos += self.dir



class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)] 
        self.old_body = self.body[:]
        self.dir = Vector2(1, 0)
        self.apple_eaten = False
        self.can_move = True
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
        #Body
        self.body_x = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Body_X.png").convert_alpha()),(cell_size,cell_size))
        self.body_y = pygame.transform.scale((pygame.image.load("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\Snake\\Body_Y.png").convert_alpha()),(cell_size,cell_size))
        #Sound
        self.eating_sound = pygame.mixer.Sound("C:\\Users\\ADMIN\\Documents\\Coding\\Python\\Uni\\Final Proyect\\crunch.wav")

    def write_snake(self, fraction):
        self.update_head()
        self.update_tail()

        for num,x in enumerate(self.body):
            old_pos = self.old_body[num] if num < len(self.old_body) else x
            lerp_x = old_pos.x + (x.x - old_pos.x) * fraction
            lerp_y = old_pos.y + (x.y - old_pos.y) * fraction
            Snake_cell = pygame.Rect(int(lerp_x * cell_size), int(lerp_y * cell_size), cell_size, cell_size)

            if num == 0:
                Window.blit(self.head,Snake_cell)
            elif num == len(self.body)-1:
                Window.blit(self.tail,Snake_cell)
            else:
                prev = self.body[num + 1] - x
                next = self.body[num - 1] - x
                if prev.x == next.x:
                    Window.blit(self.body_y,Snake_cell)
                if prev.y == next.y:
                    Window.blit(self.body_x,Snake_cell)
                else:
                    if prev.x ==-1 and next.y == -1 or prev.y == -1 and next.x == -1:
                        Window.blit(self.cross_lu,Snake_cell)
                    elif prev.x ==1 and next.y == 1 or prev.y == 1 and next.x == 1:
                        Window.blit(self.cross_ld,Snake_cell)
                    elif prev.x ==1 and next.y == -1 or prev.y == -1 and next.x == 1:
                        Window.blit(self.cross_ru,Snake_cell)
                    elif prev.x ==-1 and next.y == 1 or prev.y == 1 and next.x == -1:
                        Window.blit(self.cross_rd,Snake_cell)     
    def update_tail(self):
            tail_dif = self.body[-2] - self.body[-1]
            if tail_dif == Vector2(1,0):
                self.tail = self.tail_left
            elif tail_dif == Vector2(-1,0):
                self.tail = self.tail_right
            elif tail_dif == Vector2(0,1):
                self.tail = self.tail_up
            elif tail_dif == Vector2(0,-1):
                self.tail = self.tail_down
    def update_head(self):
        head_dif = self.body[1] - self.body[0]
        if head_dif == Vector2(1,0):
            self.head = self.head_left
        elif head_dif == Vector2(-1,0):
            self.head = self.head_right
        elif head_dif == Vector2(0,1):
            self.head = self.head_up
        elif head_dif == Vector2(0,-1):
            self.head = self.head_down            
    def movement(self):
        self.old_body = self.body[:]
        if self.apple_eaten == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.dir)
            self.body = body_copy[:]

            self.old_body.append(self.old_body[-1]) 
            self.apple_eaten = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.dir)
            self.body = body_copy[:]
        self.can_move = True

    def grow(self):
        self.apple_eaten = True
        self.eating_sound.play()

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)] 
        self.old_body = self.body[:]
        self.dir = Vector2(1, 0)

"""
Main Loop
"""
class MAINFUNCIONS:
    def __init__(self):
        self.Apple = Apple()
        self.Snake = Snake()
        self.Background = Background()
        self.ScoreBoard = Scoreboard()
        self.last_snake_time = pygame.time.get_ticks()
        self.last_apple_time = pygame.time.get_ticks()
        self.Apple.Apple_reroll(self.Snake.body)

    def game_update(self):
        self.Snake.movement()
        self.apple_collision()
        self.death_collision()

    def write_items(self, snake_fraction, apple_fraction):
        self.Background.draw(Window)
        self.Apple.write_apple(apple_fraction)
        self.Snake.write_snake(snake_fraction)
        self.ScoreBoard.draw_score(len(self.Snake.body))

    def apple_collision(self):
        if self.Apple.pos == self.Snake.body[0]:
            self.Apple.Apple_reroll(self.Snake.body)
            self.Snake.grow()

    def death_collision(self):
        if not (0 <= self.Snake.body[0].x < cell_amount) or not (0 <= self.Snake.body[0].y < cell_amount):
            self.death_state()
            
        if self.Snake.body[0] in self.Snake.body[1:]:
            self.death_state()

    def death_state(self):
        TESTTIMEREND = time.time()
        print(f"time elapsed: {round((TESTTIMEREND - TESTTIMERSTA),2)}, death")
        self.Snake.reset()

def main():
    """
    IMPORTANT VARIABLES
    """
    main_functions = MAINFUNCIONS()
    clock = pygame.time.Clock()
    Screen_Refresh = pygame.USEREVENT
    pygame.time.set_timer(Screen_Refresh,Snake_Tick)
    Apple_Refresh = pygame.USEREVENT + 1
    pygame.time.set_timer(Apple_Refresh, Apple_TIck)
    active = True

    while active:
        clock.tick(Fps_cap)
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                active = False
            if event.type == Screen_Refresh:
                main_functions.game_update()
                main_functions.last_snake_time = current_time 
            if event.type == Apple_Refresh:
                main_functions.Apple.Apple_movement()
                main_functions.apple_collision() 
                main_functions.last_apple_time = current_time 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and main_functions.Snake.can_move:
                    if main_functions.Snake.dir.y != 1:
                        main_functions.Snake.dir = Vector2(0, -1)
                        main_functions.Snake.can_move = False
                elif event.key == pygame.K_LEFT and main_functions.Snake.can_move:
                    if main_functions.Snake.dir.x != 1:
                        main_functions.Snake.dir = Vector2(-1, 0)
                        main_functions.Snake.can_move = False
                elif event.key == pygame.K_RIGHT and main_functions.Snake.can_move:
                    if main_functions.Snake.dir.x != -1:
                        main_functions.Snake.dir = Vector2(1, 0)
                        main_functions.Snake.can_move = False
                elif event.key == pygame.K_DOWN and main_functions.Snake.can_move:
                    if main_functions.Snake.dir.y != -1:
                        main_functions.Snake.dir = Vector2(0, 1)
                        main_functions.Snake.can_move = False
        snake_frac = (current_time - main_functions.last_snake_time) / Snake_Tick
        snake_frac = max(0.0, min(1.0, snake_frac))
        
        apple_frac = (current_time - main_functions.last_apple_time) / Apple_TIck
        apple_frac = max(0.0, min(1.0, apple_frac))

        # Send that sliding fraction to the drawing pipeline
        main_functions.write_items(snake_frac, apple_frac)
        pygame.display.update()
    TESTTIMEREND = time.time()
    print(f"time elapsed: {round((TESTTIMEREND - TESTTIMERSTA),2)}, closed by u")
    pygame.quit()

if __name__ == "__main__":
    main()