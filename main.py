import block, pygame, random, time, sys
from pygame.math import Vector2

class Fruit:
    def __init__(self,screen):
        self.img = pygame.image.load("resources/apple.png").convert_alpha() #load the apple image and convert into a python app. format
        self.screen = screen         
        self.x = random.randint(3, cell_number-5)                      #initial coordinates of the fruit and vector for the fruit block
        self.y = random.randint(3, cell_number-5)
        self.pos = Vector2(self.x,self.y)

    def display_fruit(self):
        fruit_block = block.create_block(int(self.pos.x), int(self.pos.y), cell_size)   #draw fruit block
        self.screen.blit(self.img,fruit_block)                            #display the image on the block

    def modify(self,snake_body):
        flag = True                      #find a random new position for the fruit block such that 
        while flag:                      #it does not coincide with the snake's body
            flag = False
            self.x = random.randint(3, cell_number-5)         
            self.y = random.randint(3, cell_number-5)
            for body in snake_body:
                if(self.x==body.x and self.y==body.y):
                    flag = True
                    break
        self.pos = Vector2(self.x,self.y)


class Snake:
    def __init__(self,screen):
        self.screen = screen                   #uses the sreen created by the Game_Screen class
        self.block_x = cell_number/2           #initial coordinates for the block
        self.block_y = cell_number/2

        #vector contains the beginning position of the snake
        self.body = [Vector2(self.block_x,self.block_y), Vector2(self.block_x+1,self.block_y),Vector2(self.block_x+2,self.block_y)]  
        #the snake will consist of three blocks initially each having their own vectors or positions     

        #set a default direction for the snake's movement which will be stationary at the beginning
        self.direction = Vector2(0,0)                           
        self.new_block = False               #if True, it will indicate the need for adding new blocks 

        #get all the snake images
        self.head_up = pygame.image.load('resources/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('resources/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('resources/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('resources/head_left.png').convert_alpha()
		
        self.tail_up = pygame.image.load('resources/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('resources/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('resources/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('resources/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('resources/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('resources/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('resources/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('resources/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('resources/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('resources/body_bl.png').convert_alpha()

    def display_snake(self):                                                        
        for index,body in enumerate(self.body):                                                               
            snake_block = block.create_block(int(body.x), int(body.y), cell_size)   #get each block
            
            #direction of the head will be determined by the direction of movement
            if(index==0):
                if(self.direction == (1,0)):
                    self.screen.blit(self.head_right,snake_block)
                elif(self.direction == (-1,0)  or self.direction == (0,0)):
                    self.screen.blit(self.head_left,snake_block)
                elif(self.direction == (0,1)):
                    self.screen.blit(self.head_down,snake_block)
                elif(self.direction == (0,-1)):
                    self.screen.blit(self.head_up,snake_block)

            #direction of the tail will depend on the second last block's movement
            elif(index == len(self.body)-1):
                pos = self.body[index-1] - body
                if(pos == (1,0)):
                    self.screen.blit(self.tail_left,snake_block)
                elif(pos == (-1,0)):
                    self.screen.blit(self.tail_right,snake_block)
                elif(pos == (0,1)):
                    self.screen.blit(self.tail_up,snake_block)
                elif(pos == (0,-1)):
                    self.screen.blit(self.tail_down,snake_block)
            
            #if the prev and next blocks x coordinates are equal, body will be vertical
            elif(self.body[index-1].x == self.body[index+1].x):
                self.screen.blit(self.body_vertical,snake_block)

            #vice-versa for the y coordinates
            elif(self.body[index-1].y == self.body[index+1].y):
                self.screen.blit(self.body_horizontal,snake_block)

            #for the turns consider each turn as the corner of a box
            #each side of the box represents the x and y coordinates depending the direction being considered
            #left and up being indicated by -1 and right and down being indicated by +1
            #if we know the relation between the current, prev and next blocks
            #we can manipulate the snake's movement
            else:
                previous_block = self.body[index - 1] - body
                next_block = self.body[index + 1] - body
                #x coordinate to the left and y coordinate to the top -> bottom right
                if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                    self.screen.blit(self.body_br,snake_block)
                #or conditions represent the anti-clockwise movement of the snake
                elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                    self.screen.blit(self.body_tr,snake_block)
                elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                    self.screen.blit(self.body_bl,snake_block)
                #x coordinate to the right and y coordinate to the bottom -> top left
                elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                    self.screen.blit(self.body_tl,snake_block)
                                
    def move_snake(self):
        if(self.direction != (0,0)):                          #if snake is in the starting position, the foll. steps are not required
            if(self.new_block):                               #make a copy of the whole list if new block needs to be added
                body_copy = self.body[:]
                self.new_block = False
            else:
                body_copy = self.body[:-1]                              #else make a copy of the current vectors except the last 
            body_copy.insert(0,body_copy[0]+ Vector2(self.direction))   #change the direction of the head by adding the direction to the first element
            self.body = body_copy[:]                                    #copy the new body blocks                                          
        self.display_snake()

    def modify(self):
        self.new_block = True      #add a new block

    def reset(self):
        #reset to the original position
        self.body = [Vector2(self.block_x,self.block_y), Vector2(self.block_x+1,self.block_y),Vector2(self.block_x+2,self.block_y)]
        self.direction = Vector2(0,0)


class Game_Screen:
    def __init__(self):
        pygame.display.init()                                                  #initialising pygame.display module
        #sets the screen for the game
        self.game_screen = pygame.display.set_mode((cell_number*cell_size,cell_number*cell_size))       
        pygame.display.set_caption("WELCOME TO THE SNAKE GAME!")  

    def display_score(self,score): 
        text_block = block.create_text_block(score)
        img = pygame.image.load("resources/apple.png").convert_alpha()
        
        #blocks for the score and image respectively
        score_block = block.create_block(cell_number-2,cell_number-2,cell_size)
        image_block = block.create_block(cell_number-3,cell_number-2,cell_size)

        self.game_screen.blit(text_block,score_block) 
        self.game_screen.blit(img,image_block)


class Main:
    def __init__(self):
        self.screen = Game_Screen()         #creates a game_screen, fruit and snake object for the game
        self.fruit = Fruit(self.screen.game_screen)             
        self.snake = Snake(self.screen.game_screen) 
        self.score = 0            

    def display_main(self):
        self.screen.game_screen.fill((167,209,61))   #bg color for game screen
        self.screen.display_score(self.score)
        self.fruit.display_fruit()                   #display the score, fruit and snake
        self.snake.move_snake() 
        pygame.display.flip()                        #allow the screen to reflect necessary changes
        time.sleep(0.15)                             #allow time delay

    def check_collision(self):

        #if fruit and the snake's head meet
        if(self.snake.body[0] == self.fruit.pos):      
            self.score += 1                      #increment scores
            self.fruit.modify(self.snake.body)   #reposition fruit
            self.snake.modify()                  #add a new snake block
            self.display_main()

        #check if the snake collides with the walls
        elif(self.snake.body[0].x<0 or self.snake.body[0].y<0 or self.snake.body[0].x==cell_number or self.snake.body[0].y==cell_number):
            self.reset()
        
        #check if the snake collides with itself
        else:
            for index,body in enumerate(self.snake.body):
                if(index!=0 and self.snake.body[0]==body):
                    self.reset()
                
    def run(self):
        while True:   
            #the event module handles all the events in the form of a queue  
            #pygame.event.get() will get each event from the queue                                                                                                                       
            for event in pygame.event.get():               
                #the type attribute checks the kind of event (mousclick, keyboard etc..)                         
                if(event.type == pygame.KEYDOWN):     
                    
                    #determine the key pressed and change the coordinates of the snake block respectively
                    if(event.key == pygame.K_UP and self.snake.direction!=(0,1)):  
                        self.snake.direction = Vector2(0,-1)
                    elif(event.key == pygame.K_DOWN and self.snake.direction!=(0,-1)):
                        self.snake.direction = Vector2(0,1)
                    elif(event.key == pygame.K_RIGHT and self.snake.direction!=(-1,0) and self.snake.direction!=(0,0)):
                        self.snake.direction = Vector2(1,0)
                    elif(event.key == pygame.K_LEFT and self.snake.direction!=(1,0)):
                        self.snake.direction = Vector2(-1,0)

                #this statement will be true when the pygame screen is closed    
                elif(event.type == pygame.QUIT):                                    
                    sys.exit()

            self.display_main()
            self.check_collision()

    def reset(self):    #resets the game
        time.sleep(0.2)
        self.score = 0
        self.snake.reset()
        self.fruit.modify(self.snake.body)
        self.display_main()


if __name__ == "__main__":
    cell_size = 40
    cell_number = 16
    start = Main()        #start the game
    start.run()

    

        

                                                              
   
    

    
