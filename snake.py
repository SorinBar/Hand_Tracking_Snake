import pygame , sys , random , Tracker , pygame_menu
from pygame.math import Vector2
import time

detector = Tracker.Hand()

class GAME:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit_rect = FRUIT()
    
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
       pygame.quit()
       sys.exit()
     
 
class SNAKE: 
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(6,10)]
        self.direction = Vector2(1,0)
        self.newblock = False
        
    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x*cell_size)
            y_pos = int(block.y*cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,(255,255,255),block_rect)
    def move_snake(self):
        if self.newblock == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.newblock = False
        else:   
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
    
    def grow(self):
        self.newblock = True

class FRUIT: 
    def __init__(self):
        self.randomize()
        
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x*cell_size),int (self.pos.y*cell_size),cell_size,cell_size)
        screen.blit(apple,fruit_rect)
        
    def randomize(self):
        self.x = random.randint(1 , cell_number - 2)
        self.y = random.randint(1 , cell_number - 2)
        self.pos = Vector2( self.x, self.y)

        
pygame.init()
cell_size = 20
cell_number =40
screen = pygame.display.set_mode((cell_size*cell_number,cell_number*cell_size))
pygame.display.set_caption("Snake game")
game_paused = True
clock = pygame.time.Clock()
main_game = GAME()
SCREEN_UPDATE = pygame.USEREVENT
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
pygame.time.set_timer(SCREEN_UPDATE,150)
font = pygame.font.Font('FreeSansBold.ttf', 24)
white = (255,255,255)
black = (0,0,0)
text = font.render('Press P or SPACE to Start', True, white, black)
textRect = text.get_rect()
textRect.center = (800 // 2, 800 // 2)
main_menu = True
playing = True
while True:
    if main_menu:
        screen.blit(text, textRect)
        pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                main_menu = False
            if event.key == pygame.K_SPACE:
                main_menu = False
        if main_menu == False:
            if event.type == SCREEN_UPDATE:
                main_game.update()
        if playing == True:
            move = detector.get_move()
            if move == detector.UP:
                if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0,-1)
            if move == detector.RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)
            if move == detector.DOWN:
                if main_game.snake.direction.y != 1:
                     main_game.snake.direction = Vector2(0,1)
            if move == detector.LEFT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(-1,0)
            


    screen.fill(pygame.Color('black'))
    main_game.draw_elements()
    if main_menu: 
        screen.blit(text, textRect)
    pygame.display.update()
    clock.tick(60)
    