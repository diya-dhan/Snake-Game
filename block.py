import pygame
pygame.init()

def create_block(x,y,size):                     #creates a rectangluar block representing fruit or snake
    return pygame.Rect(x*size,y*size,size,size)   

def create_text_block(score):                   #creates a text block for the score
    font_list = pygame.font.get_fonts()
    chosen_font = pygame.font.SysFont(font_list[0],25,bold=True)
    return chosen_font.render(str(score),True,(0,0,0))
