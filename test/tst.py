import pygame
pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption('')
FPS = 20
def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)
# WIN.blit(PYtxt('Solved'), (20, 560) -> position)
# pygame.display.update()
# win.blit(text, (x + (colGap/2 - text.get_width()/2),
#                 y + (rowGap/2 - text.get_height()/2)))

class MenuItem:

    def __init__(self,width,height,rel_x,rel_y,win,x,y,button) -> None:

        self.width,self.height = width,height
        self.x,self.y = x,y
        self.rel_x,self.rel_y = rel_x,rel_y
        self.button = button
        self.items = []

        self.surface = pygame.Surface((self.width,self.height))
        self.surface.fill((240,240,240))
        self.win = win
        self.draw()

    def draw(self):
        self.win.blit(self.surface,(self.x+self.rel_x,self.y+self.rel_y))
        self.button.draw()
        pygame.display.update()



class Button():
    def __init__(self, color, x,y,width,height, text='',win= None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.win = win
        self.surface = pygame.Surface((self.width+4,self.height+4))
        self.surface.fill(self.color)
        
        self.draw()

    def draw(self,outline=None):
        #Call this method to draw the button on the screen
        self.win.blit(self.surface,(self.x-2,self.y-2))
        if outline:
            pygame.draw.rect(self.win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(self.win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font_size = (self.width//len(self.text))*2
            font = pygame.font.SysFont('comicsans', font_size)
            text = font.render(self.text, 1, (0,0,0))
            self.win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        pygame.display.update()

    def isOver(self) -> bool:
        #Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pygame.mouse.get_pos()
        return (
            pos[0] > self.x
            and pos[0] < self.x + self.width
            and pos[1] > self.y
            and pos[1] < self.y + self.height
        )
    def update(self):
        self.win.fill((255,255,255))
        if self.isOver():
            self.draw(1)
        else:
            self.draw()

# item = MenuItem(width = 200,height = 200,rel_x = 0, rel_y = 30,win = WIN,x = 50, y =0)
btn = Button(color = (200,255,255), x = 100, y = 100, width = 100, height = 50, text = "button",win = WIN)

run = True
while run:

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    btn.update()
pygame.quit()