import pygame, sys,random

def draw_floor():
    screen.blit(floor_surface,(floor_x_position,900))
    screen.blit(floor_surface,(floor_x_position+576,900))

def create_pipe():
    random_pipe_position = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700,random_pipe_position))
    top_pipe =pipe_surface.get_rect(midbottom=(700,random_pipe_position-300))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=1024:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True) #flip in y not x direction
            screen.blit(flip_pipe,pipe)

def check_collison(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    return True
pygame.init()
screen = pygame.display.set_mode((576,1024)) #screen
clock = pygame.time.Clock() # this just helps limit frame rate

# variables
gravity = 0.25
bird_movement = 0
game_active = True

bg_surface = pygame.image.load('assets/background-day.png').convert() # convert just makes it better to run
bg_surface =  pygame.transform.scale2x(bg_surface) #double the size of the image upscales

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_position = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale2x(bird_surface)
bird_rect = bird_surface.get_rect(center = (100,512))

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT #triggered by timer
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400,600,800] #position of pipes


while True:
  for event in pygame.event.get():  #Looking for all event that are happening (clicking keys)
    if event.type == pygame.QUIT: #or game_active== False:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and game_active:
            bird_movement = 0 #disables gravity momentarily 
            bird_movement -= 12
        if event.key == pygame.K_SPACE and game_active == False:
            game_active =True
            pipe_list.clear()
            bird_rect.clear = (100,512)
            bird_movement=0
    if event.type == SPAWNPIPE:
        pipe_list.extend(create_pipe())

  # This block is being always redrawn....
  screen.blit(bg_surface,(0,0))
  if game_active:
    bird_movement += gravity # increasing number
    bird_rect.centery += bird_movement
    screen.blit(bird_surface,bird_rect)
    game_active = check_collison(pipe_list)
    # Pipes
    pipe_list = move_pipes(pipe_list)
    draw_pipes(pipe_list)
  #Floor
  floor_x_position -=1
  # This just has two floors and when floor is too far off, change in x axis
  draw_floor()
  if floor_x_position <= - 576:
      floor_x_position = 0
   # puts a surface on another surface
  pygame.display.update()
  clock.tick(120) #can only run under 120 fps