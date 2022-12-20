import pygame , sys , random
from pygame.math import Vector2

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
            run = False
        if not 0 <= self.snake.body[0].y  < cell_number:
            run = False
        for i in self.snake.body[1:]:
            if i == self.snake.body[0]:
                run = False
            
    def game_over(self):
        print
        
class SNAKE: 
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(6,10)]
        self.direction = Vector2(1,0)
        self.newblock = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

       # self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
       # self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
         #self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
         #self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()


        
    def draw_snake(self):
        self.update_head_graphics()

        for index,block in enumerate(self.body):
                x_pos = int(block.x*cell_size)
                y_pos = int(block.y*cell_size)
                block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
                
                if index == 0:
                    screen.blit(self.head,block_rect)
                else:
                    pygame.draw.rect(screen,(238,0,0),block_rect)
    
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down



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
        #pygame.draw.rect( screen, (126,166,114) ,fruit_rect)
        
    def randomize(self):
        self.x = random.randint(0 , cell_number - 1)
        self.y = random.randint(0 , cell_number - 1)
        self.pos = Vector2( self.x, self.y)
        
pygame.init()
cell_size = 20
cell_number = 40
screen = pygame.display.set_mode((cell_size*cell_number,cell_number*cell_size))
clock = pygame.time.Clock()      
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
main_game = GAME()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,100)
run = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if run == True:
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    main_game.snake.direction = Vector2(0,-1)
                if event.key == pygame.K_RIGHT:
                    main_game.snake.direction = Vector2(1,0)
                if event.key == pygame.K_DOWN:
                    main_game.snake.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    main_game.snake.direction = Vector2(-1,0)
    screen.fill(pygame.Color('black'))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
    