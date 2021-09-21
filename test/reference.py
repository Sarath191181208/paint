import pygame
class Slider():
    def __init__(self, posX : int = 200 , posY : int = 305,win = None,start = 1,end = 5 , step = 1,default_value = 50 , slider_width : int = 10, slider_height : int = 30, color : tuple = (210,210,210),fontSize=25, fontColor=(0, 0, 0)):
        stp = (((start+end-1)/2)-default_value)*((start/end)*slider_height*6)
        self.pos = [posX, posY-stp]
        self.drawPos = posX , posY
        # self.drawPos = self.pos.copy()
        self.slider_width, self.slider_height = slider_width, slider_height
        self.background_color = color
        self.color = (210, 210, 210)
        self.subsurface = pygame.Surface((self.slider_width, self.slider_height))
        self.subsurface.fill(self.color)
        self.font = pygame.font.SysFont(None,fontSize)
        self.clicked = False
        self.start,self.end = start,end
        self.step = step
        self.slideVal = 0
        self.win = win
        
        self.draw()
    def draw(self):
        new_val = self.Remap(-self.slider_height*3,self.slider_height*3,self.start,self.end,(self.pos[1]- self.drawPos[1]))
        new_val -= new_val%self.step
        if abs(new_val) < self.start :
            new_val = self.start
        # toggle to disable always refresh
        # if self.slideVal != new_val:
        self.slideVal = int(abs(new_val))
        self.valMes = self.font.render(str(self.slideVal), True, (30,30,30))
        pygame.draw.rect(self.win, (220,220,220), ((self.drawPos[0]-self.slider_width/2)-15, self.drawPos[1]-self.slider_height*3.5-10, self.slider_width+30, self.slider_height*7+20))
        # border
        stroke = 3
        pygame.draw.rect(self.win, (120,120,120), ((self.drawPos[0]-self.slider_width/2)-15-stroke, self.drawPos[1]-self.slider_height*3.5-10-stroke, self.slider_width+30+stroke*2, self.slider_height*7+20+stroke*2),stroke)
        # text
        self.win.blit(self.valMes, (self.drawPos[0]+self.slider_width/2-self.valMes.get_width()/2+43, self.drawPos[1]+self.valMes.get_height()/2))
        # slider rectangle
        pygame.draw.rect(self.win, (140,140,140), (self.drawPos[0]-self.slider_width/2, self.drawPos[1]-self.slider_height*3.5, self.slider_width, self.slider_height*7))
        # slider
        self.win.blit(self.subsurface, (self.pos[0]-self.slider_width/2, self.pos[1]-self.slider_height/2))
    
    def is_hovering(self):
        threshold = 10
        return (
            pygame.mouse.get_pos()[0] > self.pos[0]-self.slider_width/2   -threshold      and 
            pygame.mouse.get_pos()[0] < self.pos[0]+self.slider_width/2   +threshold      and
            pygame.mouse.get_pos()[1] > self.pos[1]-self.slider_height/2  -threshold      and 
            pygame.mouse.get_pos()[1] < self.pos[1]+self.slider_height/2  +threshold      )

    def update(self):

        if (self.is_hovering() or self.clicked) and pygame.mouse.get_pressed()[0]:
            self.clicked = True
            self.pos[1] = max(self.drawPos[1]-self.slider_height*3, min(pygame.mouse.get_pos()[1], self.drawPos[1]+self.slider_height*3))
            # self.pos[1] += self.slider_height/2
            clr  = (60, 80,180) 
        else:
            self.clicked = False
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

    def set_val(self,val):
        if val < self.start or val > self.end:
            return
        stp = (((self.start+self.end-1)/2)-val)*((self.start/self.end)*self.slider_height*6)
        self.pos[1] = self.drawPos[1] - stp


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((540, 600))
    pygame.display.set_caption('slider')
    FPS = 20
    clock.tick(FPS)
    WIN.fill((220,200,220))
    slider = Slider(200,200,WIN,start=1,end=100,step=5)

    run = True
    while run:
        WIN.fill((220,200,220))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        slider.draw()
        slider.update()
    pygame.quit()
