import pygame
import os
path = 'assets'

brushImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'brush.png')), (25,25))
clearImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'clear.png')), (25,25))
eraserImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'eraser.png')), (25,25))
dropperImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'dropper.png')), (25,25))
fillImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'fill.png')), (25,25))

zoomImage= pygame.transform.scale(pygame.image.load(os.path.join('assets','zoom.png')), (25,25))
gridImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'grid.png')), (25,25))
lineImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'line.png')), (25,25))
loadImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'load.jpg')), (25,25))
saveImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'save.png')), (25,25))
redoImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'redo.jpg')), (25,25))
undoImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'undo.png')), (25,25))

upImage = pygame.transform.scale(pygame.image.load(os.path.join('assets','arrow_up.png')), (25,25))
downImage = pygame.transform.scale(pygame.image.load(os.path.join('assets','arrow_down.png')), (25,25))

# flagImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'flag.png')), (25,25))
# helpImage = pygame.transform.scale(pygame.image.load(os.path.join(path,'help.png')), (25,25))
