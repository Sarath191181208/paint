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
# WIN.blit(text, (x + (colGap/2 - text.get_width()/2),
#                 y + (rowGap/2 - text.get_height()/2)))
class Slider(object):
    def __init__(self,text="Button", posX : int = 200 , posY : int = 305, slider_width : int = 10, slider_height : int = 20, color : tuple = (210,210,210),fontSize=25, fontColor=(0, 0, 0)):
        self.pos = [posX, posY]
        self.drawPos = self.pos.copy()
        self.slider_width, self.slider_height = slider_width, slider_height
        self.background_color = color
        self.color = (210, 210, 210)
        self.text, self.fontSize, self.fontColor = text, fontSize, fontColor
        self.subsurface = pygame.Surface((self.slider_width, self.slider_height))
        self.subsurface.fill(self.color)
        self.font = pygame.font.SysFont(None, self.fontSize)
        self.mes = self.font.render(self.text, True, self.fontColor)
        self.clicked = False
        self.slideVal = 0
        self.draw()
    def draw(self):
            self.slideVal = self.Remap(-60,60,1,5,(self.pos[0]- self.drawPos[0]))
            # back ground colour
            pygame.draw.rect(WIN, self.background_color, (self.drawPos[0]-100, self.drawPos[1]-30, 180, 60))
            pygame.draw.rect(WIN, (140,140,140), (self.drawPos[0]-60, self.drawPos[1]+self.slider_height/3, 120, self.slider_height/2))

            self.valMes = self.font.render(str(int(self.slideVal)), True, (30,30,30))
            WIN.blit(self.valMes, (self.drawPos[0]-85, self.drawPos[1]+3))

            WIN.blit(self.subsurface, (self.pos[0]-self.slider_width/2, self.pos[1]))
            WIN.blit(self.mes, (self.drawPos[0]-90, self.drawPos[1]-25))
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
            S_brushSize.pos[0] = max(S_brushSize.drawPos[0]-60, min(pygame.mouse.get_pos()[0], S_brushSize.drawPos[0]+60))
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
S_brushSize = Slider()

while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    S_brushSize.update()
pygame.quit()