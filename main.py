import pygame
import sys
import random

def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_position))
    top_pipe =pipe_surface.get_rect(midbottom=(700,random_pipe_position-400)) # the minus is the gap between the two tunnels
    return bottom_pipe,top_pipe



def pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True) #flip in y not x direction
            screen.blit(flip_pipe,pipe)

def collision(pipes):
    for pipe in pipes:
        if rect_item.colliderect(pipe):
            return False

    if rect_item.top <= -100 or rect_item.bottom >= 900:
        return False
    return True
    
def rotation(crypto):
	newcrypto = pygame.transform.rotozoom(crypto,-crypto_moves * 5,1) # * is how fast it animates
	return newcrypto
    #animation work by having multiple in a list and cycling throught them
def animation_crypto_char():
	newcrypto = crypto_list_items[index]
	new_rect_item = newcrypto.get_rect(center = (100,rect_item.centery))
	return newcrypto,new_rect_item 
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255)) #colour of text
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
pygame.init()
width, height = 576 ,1024
screen = pygame.display.set_mode((width,height)) #screen
clock = pygame.time.Clock() # this just helps limit frame rate
game_font = pygame.font.Font('04B_19.TTF',50)
# variables
gravity = 0.4;crypto_moves = 0;game_active = True;score = 0;high_score = 0
background = pygame.image.load('assets/background-crypto-2.png').convert()
background = pygame.transform.scale2x(background)
floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
xgroundlocation = 0
crypto_down = pygame.transform.scale2x(pygame.image.load('assets/up.png').convert_alpha())
crypto_middle = pygame.transform.scale2x(pygame.image.load('assets/mid.png').convert_alpha())
crypto_up = pygame.transform.scale2x(pygame.image.load('assets/down.png').convert_alpha())
crypto_list_items = [crypto_down,crypto_middle,crypto_up]
index = 0;surf = crypto_list_items[index]
rect_item = surf.get_rect(center = (100,512))

crypto_animation_counter = pygame.USEREVENT + 1
pygame.time.set_timer(crypto_animation_counter,200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
PIPESPAWNER = pygame.USEREVENT #triggered by timer
pygame.time.set_timer(PIPESPAWNER,1200)
pipe_height = [400,600,800] #position of pipes

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288,512))
while True:
  for event in pygame.event.get():  #Looking for all event that are happening (clicking keys)
    if event.type == pygame.QUIT: #or game_active== False:
        pygame.quit()
        sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and game_active:
            crypto_moves = 0 #disables gravity momentarily 
            crypto_moves -= 12
        if event.key == pygame.K_SPACE and game_active == False:
            game_active = True
            pipe_list.clear()
            rect_item.center = (100,512)
            crypto_moves=0
            score = 0
        if game_active and score>5:
            high_score_surface = game_font.render(f' High score: {int(high_score)}',True,(255,255,255)) #colour of text
            high_score_rect = high_score_surface.get_rect(center = (288,850))
            screen.blit(high_score_surface,high_score_rect)

        if event.type == crypto_animation_counter:
            if index < 2:
                index += 1
            else:
                index = 0
            surf,rect_item = animation_crypto_char()

    if event.type == PIPESPAWNER:
        pipe_list.extend(create_pipe()) # when a tuple is returned

  # This block is being always redrawn....
  screen.blit(background,(0,0))

  if game_active:
    crypto_moves += gravity # increasing number
    rotated_bird = rotation(surf)
    rect_item.centery += crypto_moves
    screen.blit(rotated_bird,rect_item)
    game_active = collision(pipe_list)

    # Pipes

    for pipe in pipe_list:
        pipe.centerx -= 5
        pipes(pipe_list)
    

    score += 0.01

    if 'main_game' == 'main_game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255)) #colour of text
        score_rect = score_surface.get_rect(center = (288,100))
        screen.blit(score_surface,score_rect)
  else:
      screen.blit(game_over_surface,game_over_rect)

  #Floor
  xgroundlocation -=5
  if xgroundlocation > 0:
      xgroundlocation = 10
  # This just has two floors and when floor is too far off, change in x axis
  screen.blit(floor_surface,(xgroundlocation,900))
  screen.blit(floor_surface,(xgroundlocation+576,900))
  if xgroundlocation <= - width:
      xgroundlocation = 0
   # puts a surface on another surface
  pygame.display.update()
  
  clock.tick(100) #can only run under 120 fps properly
#pygame.quit() weird error, will fix later