import pygame
from pyautogui import size
from canvas import Grid
from colours import *
from slider import Slider
from tkinter import Tk,colorchooser
from button_images import brush_matrix_img,eraser_matrix_img,dropper_matrix_img,fill_matrix_img,save_matrix_image,load_matrix_image
from buttons import Button,convert_matrix_to_img
pygame.init()

def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)

class colourBar():
    def __init__(self,
            width:int = 0 , height:int = 0,
            position_x : int = 0 , position_y : int = 0,
            win = None,
            row_items : int = None , col_items :int = None,
            padding_x : int = 30, padding_y : int = 20
            ) -> None:

        self.width,self.height = width,height
        self.position_x,self.position_y = position_x,position_y

        self.win = win

        self.surface = pygame.Surface((self.width,self.height))
        self.color = (160,160,160)
        self.surface.fill(self.color)

        clrs = [absBlack,WHITE,GREAY,BLACK,GREEN,TURTLEGREEN,VIOLET,ORANGE,CYAN,BLUE,PINK,YELLOW,AMBER,MAROON,OLIVE,TEAL]
        self.row_items = row_items if row_items is not None else self.height//40
        self.col_items = col_items if col_items is not None else self.width//40
        
        self.padding_x ,self.padding_y = padding_x,padding_y

        row_gap = (self.height-self.padding_x) / self.row_items
        col_gap = (self.width-self.padding_y) / self.col_items

        # this is for correcting the position of the colour bar
        self._x = padding_x/2
        self._y = padding_y

        self.colours = [
            [colourButton(clrs[(row*self.col_items + col)%len(clrs)],self._x+col * col_gap,self._y+self.position_y +row * row_gap,self.win )
            for row in range(self.row_items)]
                for col in range(self.col_items)]

        self.selected_block = (0,0)

        self.draw()

    def draw(self):
        self.win.blit(self.surface,(self.position_x,self.position_y))
        for row in self.colours:
            for button in row:
                button.draw()
        i,j = self.selected_block

        self.colours[i][j].stroke()
        pygame.display.update()

    def find_pos(self,pos):
        x,y = pos

        y -= self.position_y
        x -= self.position_x

        row_gap = (self.height-self.padding_x) / self.row_items
        col_gap = (self.width-self.padding_y) / self.col_items

        y -= self._y
        x -= self._x

        x,y = x//col_gap,y//row_gap

        return int(x),int(y)

    def clicked(self,pos):
        x,y = self.find_pos(pos)
        if y >= self.row_items or x >= self.col_items or y < 0 or x < 0:
            return 0
        self.selected_block = (x,y)
        self.colours[x][y].stroke()
        self.draw()
        return self.colours[x][y].colour

    def change_colour(self,pos):
        win = Tk()
        win.withdraw()
        x,y = self.find_pos(pos)
        if y >= self.row_items or x >= self.col_items or y < 0 or x < 0:
            return -1
        color_code = colorchooser.askcolor(title ="Choose color")
        if color_code[0] is None:
            return
        print(color_code)
        self.colours[x][y].colour = color_code[0]
        self.selected_block = (x,y)
        self.colours[x][y].stroke()
        self.draw()


class colourButton():
    def __init__(self,colour,x,y,win) -> None:
        self.colour = colour
        self.win = win
        self.x,self.y =  x,y

    def draw(self):
        pygame.draw.rect(self.win, self.colour, pygame.Rect(self.x, self.y, 20, 20))
    
    def stroke(self):
        pygame.draw.rect(self.win, (0,0,0), pygame.Rect(self.x, self.y, 20, 20),3)
        pygame.display.update()

class Container:
    def __init__(self,width,height,x,y,WIN) -> None:
        self.width,self.height = width,height
        self.x,self.y = x,y 
        self.surface = pygame.Surface((width,height))
        self.surface.fill((160,160,160))
        self.win = WIN
        self.childern = []
        self.just_hovering= False
        self.selected = None
        self.draw()

    def draw(self):
        self.win.blit(self.surface,(self.x,self.y))
        for child in self.childern:
            if self.selected == child:
                child.draw()
    def is_hovering(self):
        pos = pygame.mouse.get_pos()
        return (
            pos[0] > self.x
            and pos[1] > self.y
        )

    def update(self):
        for child in self.childern:
            child.update()
        if self.is_hovering() and pygame.mouse.get_pressed()[0]:
            self.clicked()
    def clicked(self):
        global actions
        for child in self.childern:
            if child.clicked == True and child != self.selected:
                self.selected.clicked = False
                self.selected = child



def get_mouse_position(board):
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        return (y,x)


def main():  # sourcery no-metrics

    undo = [] 
    redo  = []

    def click_events(event, board,container):
        if event.key == pygame.K_f:
            board.pen_type = 'fill'
        if event.key == pygame.K_e:
            board.pen_type = 'eraser'
        if event.key == pygame.K_s:
            board.save()
        if event.key == pygame.K_l:
            board.load()
        if event.key == pygame.K_n:
            board.pen_type = 'line'
        if event.key == pygame.K_p:
            board.pen_type = 'pen'
        if event.key == pygame.K_d:
            board.draw_grid = not board.draw_grid
            board.draw()
        if event.key == pygame.K_u:
            if len(undo) != 0:
                print('undo')
                redo.append(undo.pop())
                for i,row in enumerate(redo[-1]):
                    for j,color_val in enumerate(redo[-1][i]):
                        board.cubes[i][j] = color_val
                board.draw()
                pygame.display.update()
        # if event.key == pygame.K_r:
        #     if len(redo) != 0:
        #         undo.append(redo.pop())
        #         board.cubes = undo[-1]
        #         board.draw()
        # pygame.display.update()
            
        for child in container.childern:
            if child.val == board.pen_type:
                child.clicked = True
                container.selected.clicked = False
                container.selected = child

    # naming convention is a bit off
    # this denotes the dimensions of image

    # size of the screen from pyautogui
    screen_x,screen_y = size()
    pixel_x,pixel_y = 128,128
    screen_x,screen_y = screen_x//64,screen_y//64
    # screen_x,screen_y = screen_x//pixel_x,screen_y//pixel_y
    screen_x = min(8,screen_x,screen_y)
    screen_y = screen_x
    
    
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((570, 612))

    pygame.display.set_caption('Art of Life')
    pygame_icon = pygame.image.load('assets/brush.png')
    pygame.display.set_icon(pygame_icon)
    FPS = 20
    run = True

    board = Grid(cols = pixel_x, rows = pixel_y, width = 64*screen_x, height = 64*screen_y, WIN = WIN)
    clr_bar = colourBar(width = board.width,height = 100, position_x = 0, position_y = board.height, win = WIN)
    # clr_bar = colourBar(width = 200,height = 100, position_x = 0, position_y = board.height, win = WIN)
    
    container = Container(width=WIN.get_width()-board.width,height=WIN.get_height(),x = board.width,y = 0,WIN = WIN)
    slider = Slider(board.width+(WIN.get_width()-board.width)/2,550,WIN)
    
    # container.childern.append(slider)
    pos_x = board.width
    pos_y =  20
    # pos_y = slider.slider_height*7+WIN.get_width() - board.width + 20
    
    for i,val in [(brush_matrix_img,'brush'),(eraser_matrix_img,'eraser'),(dropper_matrix_img,'line'),(fill_matrix_img,'fill')]:
        container.childern.append(Button(color = (255,255,255),x = (WIN.get_width() - board.width - 40)/2 + board.width,y = pos_y-4, width= 40,height=40,text = convert_matrix_to_img(i),win = WIN))
        container.childern[-1].val = val
        pos_y += 40 + 20

    buttons = []
    save_button = Button(color = (255,255,255),x = (WIN.get_width() - board.width - 40)/2 + board.width,y = pos_y-4, width= 40,height=40,text = convert_matrix_to_img(save_matrix_image),win = WIN)
    buttons.append(save_button)
    pos_y += 40 + 20
    load_button = Button(color = (255,255,255),x = (WIN.get_width() - board.width - 40)/2 + board.width,y = pos_y-4, width= 40,height=40,text = convert_matrix_to_img(load_matrix_image),win = WIN)
    buttons.append(load_button)

    container.selected = container.childern[0]
    container.childern[0].clicked =True

    while run:
        if pygame.mouse.get_pressed()[0]:
            x,y = get_mouse_position(board)
            clr = clr_bar.clicked(pygame.mouse.get_pos())
            board.pen_size = int(slider.slideVal )
            if clr:
                board.pen_colour = clr
            if board.clicked(x, y) != -1:
                undo.append([cube.color for cube in board.cubes])

        # checks for right click
        elif pygame.mouse.get_pressed()[2]:
            x,y = get_mouse_position(board)
            if board.delete(x,y) == -1:
                clr_bar.change_colour(pygame.mouse.get_pos())
            else:
                undo.append([cube.color for cube in board.cubes])
        board.pen_type = container.selected.val
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                click_events(event, board,container)
            if save_button.clicked:
                save_button.clicked = False
                board.save()
            if load_button.clicked:
                load_button.clicked = False
                board.load()
        for btn in buttons :
            btn.update()
        slider.update()
        container.update()

    pygame.quit()


if __name__ == '__main__' :
    main()