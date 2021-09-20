import cv2
import pygame

def play_vedio(path,dimensions = (600,400)):
    cap = cv2.VideoCapture('trail.mp4')
    success, img = cap.read()
    shape = img.shape[1::-1]
    wn = pygame.display.set_mode(dimensions)
    clock = pygame.time.Clock()

    while success:
        clock.tick(60)
        success, img = cap.read()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                success = False
        wn.blit(pygame.transform.scale(pygame.image.frombuffer(img.tobytes(), shape, "BGR"),dimensions), (0, 0))
        pygame.display.update()

    pygame.quit()
