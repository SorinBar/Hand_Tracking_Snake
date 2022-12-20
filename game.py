import pygame , sys , random , pygame_menu
from pygame.math import Vector2

class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit_rect = FRUIT()
        self.menu = MENU()
    
    def update(self):
        self.snake.move_snake()
        self.collision()
        self.check_collision()
        
    def draw_elements(self):
        self.fruit_rect.draw_fruit()
        self.snake.draw_snake()
    
    def collision(self):
        if self.fruit_rect.pos == self.snake.body[0]:
            self.fruit_rect.randomize()
            self.snake.grow()
    
    def check_collision(self):
        if not 0 <= self.snake.body[0].x  < cell_number:
            self.game_over()
        if not 0 <= self.snake.body[0].y  < cell_number:
            self.game_over()
        for i in self.snake.body[1:]:
            if i == self.snake.body[0]:
                self.game_over()
            
    def game_over(self):
        run = False
        