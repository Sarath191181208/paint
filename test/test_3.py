import pygame
pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption('')
FPS = 20
def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)
# self.win.blit(PYtxt('Solved'), (20, 560) -> position)
# pygame.display.update()
# self.win.blit(text, (x + (colGap/2 - text.get_width()/2),
#                 y + (rowGap/2 - text.get_height()/2)))
class Slider(object):
    def __init__(self, posX : int = 200 , posY : int = 305,win = None , slider_width : int = 10, slider_height : int = 20, color : tuple = (210,210,210),fontSize=25, fontColor=(0, 0, 0)):
        self.pos = [posX, posY]
        self.drawPos = self.pos.copy()
        self.slider_width, self.slider_height = slider_width, slider_height
        self.background_color = color
        self.color = (210, 210, 210)
        self.subsurface = pygame.Surface((self.slider_width, self.slider_height))
        self.subsurface.fill(self.color)
        self.font = pygame.font.SysFont(None,fontSize)
        self.clicked = False
        self.slideVal = 0
        self.win = win
        self.draw()
    def draw(self):
            if self.slideVal != self.Remap(-60,60,1,5,(self.pos[1]- self.drawPos[1])):
                self.slideVal = self.Remap(-60,60,1,5,(self.pos[1]- self.drawPos[1]))
                pygame.draw.rect(self.win, (220,220,220), (self.drawPos[0]-10, self.drawPos[1]-self.slider_height*4-12, 20, 20))
                self.valMes = self.font.render(str(int(self.slideVal)), True, (30,30,30))
                self.win.blit(self.valMes, (self.drawPos[0]-self.valMes.get_width()/2, self.drawPos[1]-self.slider_height*4-self.valMes.get_height()/2))
            
            
            pygame.draw.rect(self.win, (140,140,140), (self.drawPos[0]-self.slider_width/2, self.drawPos[1]-self.slider_height*3, self.slider_width, self.slider_height*7))
            self.win.blit(self.subsurface, (self.pos[0]-self.slider_width/2, self.pos[1]))
            pygame.display.update()
    def update(self):

        if pygame.mouse.get_pressed()[0]:
            threshold = 10
            self.clicked =  (
            pygame.mouse.get_pos()[0] > self.pos[0]-self.slider_width/2   -threshold      and 
            pygame.mouse.get_pos()[0] < self.pos[0]+self.slider_width/2   +threshold      and
            pygame.mouse.get_pos()[1] > self.pos[1]-self.slider_height/2  -threshold      and 
            pygame.mouse.get_pos()[1] < self.pos[1]+self.slider_height/2  +threshold      )
        else:
            self.clicked = False

        if self.clicked:
            S_brushSize.pos[1] = max(S_brushSize.drawPos[1]-60, min(pygame.mouse.get_pos()[1], S_brushSize.drawPos[1]+60))
            clr  = (60, 80,180) 
        else:
            clr =  (250, 250, 250)

        if clr != self.color:
            self.color = clr
            self.subsurface.fill(self.color)
            self.draw()
        if self.clicked:
            self.draw()

    def Remap(self,oldlow, oldhigh, newlow, newhigh, value):
        oldRange = (oldhigh - oldlow)
        newRange = (newhigh - newlow)
        return (((value - oldlow) * newRange) / oldRange) + newlow

run = True
S_brushSize = Slider(win = WIN)

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    S_brushSize.update()
pygame.quit()