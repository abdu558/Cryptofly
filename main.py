import pygame, sys

pygame.init()
screen = pygame.display.set_mode((576,1024)) #screen


while True:
  for event in pygame.event.get():  #Looking for all event that are happening (clicking keys)
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  pygame.display.update()
