import pygame
from widgets.buttons import Button
from widgets.button_images import upImage, downImage

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

class CustomBtn(Button):
    def update(self):
        self.timer.update()

        if self.is_hovering():
            if pygame.mouse.get_pressed()[0] and not self.timer.start:
                self.clicked = True
                self.function()
                self.timer.start_timer()
            else:
                self.clicked = False
            self.draw(1)
        else:
            self.clicked = False
            self.draw()
        return super().update()

class ValNav():
    def __init__(self, x = 50 , y = 50 , win = None, max = 10 , min = 1 , step = 1) -> None:
        self.x,self.y = x,y
        self.win = win
        self.val = 3
        increase_btn_img = pygame.transform.rotate(upImage,-90)
        translate = 20        
        self.increase_btn = CustomBtn(x = self.x + translate ,y = self.y , width= 25 , height= 25 , text = increase_btn_img,win = self.win,func = lambda : self.increase_val())
        decrease_btn_img = pygame.transform.rotate(downImage,-90)        
        self.decrease_btn = CustomBtn(x = self.x - translate - 25 ,y = self.y , width= 25 , height= 25 , text = decrease_btn_img,win = self.win,func= lambda : self.decrease_val())
        self.step = step
        self.max, self.min = max, min 
        self.draw()

    def draw(self):
        text = PYtxt(str(self.val))
        self.win.blit(text,(self.x - (text.get_width()/2),self.y))

    def update(self):
        self.draw()
        self.increase_btn.update()
        self.decrease_btn.update()


    def is_hovering(self) -> bool:
        #Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pygame.mouse.get_pos()
        return (
            pos[0] > self.x - 50
            and pos[0] < self.x + 50
            and pos[1] > self.y - 5
            and pos[1] < self.y + 40
        )
    def increase_val(self):
        if self.val < self.max:
            self.val += self.step
    def decrease_val(self):
        if self.val > self.min:
            self.val -= self.step

if __name__ == "__main__":
        
    pygame.init()
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((540, 600))
    pygame.display.set_caption('')
    FPS = 60

    num_slider = ValNav(win = WIN)
    run = True
    while run:
        WIN.fill((220,220,220))
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        num_slider.update()
        pygame.display.update()
    pygame.quit()