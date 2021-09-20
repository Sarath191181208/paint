import pygame
class Slider():
    def __init__(self, posX : int = 200 , posY : int = 305,win = None , slider_width : int = 10, slider_height : int = 10, color : tuple = (210,210,210),fontSize=25, fontColor=(0, 0, 0)):
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
            pygame.draw.rect(self.win, (140,140,140), (self.drawPos[0]-self.slider_width/2, self.drawPos[1]-self.slider_height*3, self.slider_width, self.slider_height*7))
            self.win.blit(self.subsurface, (self.pos[0]-self.slider_width/2, self.pos[1]))
    
            self.slideVal = abs(6-self.Remap(-self.slider_height*3,self.slider_height*3,1,5,(self.pos[1]- self.drawPos[1])))
            pygame.draw.rect(self.win, (220,220,220), (self.drawPos[0]-10, self.drawPos[1]-self.slider_height*4-12, 20, 20))
            self.valMes = self.font.render(str(int(self.slideVal)), True, (30,30,30))
            self.win.blit(self.valMes, (self.drawPos[0]-self.valMes.get_width()/2, self.drawPos[1]-self.slider_height*4-self.valMes.get_height()/2))

    def is_hovering(self):
        threshold = 10
        return (
            pygame.mouse.get_pos()[0] > self.pos[0]-self.slider_width/2   -threshold      and 
            pygame.mouse.get_pos()[0] < self.pos[0]+self.slider_width/2   +threshold      and
            pygame.mouse.get_pos()[1] > self.pos[1]-self.slider_height/2  -threshold      and 
            pygame.mouse.get_pos()[1] < self.pos[1]+self.slider_height/2  +threshold      )

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            if self.is_hovering() or self.clicked:
                self.clicked = True
                self.pos[1] = max(self.drawPos[1]-self.slider_height*3, min(pygame.mouse.get_pos()[1], self.drawPos[1]+self.slider_height*3))
                clr  = (60, 80,180) 
        else:
            self.clicked = False
            clr =  (250, 250, 250)

        if clr != self.color:
            self.color = clr
            self.subsurface.fill(self.color)
        self.draw()


    def Remap(self,oldlow, oldhigh, newlow, newhigh, value):
        oldRange = (oldhigh - oldlow)
        newRange = (newhigh - newlow)
        return (((value - oldlow) * newRange) / oldRange) + newlow
