import pygame
from pyautogui import size
from canvas import Grid
from colours import *
from slider import Slider
from tkinter import Tk,colorchooser
from button_images import brush_matrix_img,eraser_matrix_img,dropper_matrix_img,fill_matrix_img,save_matrix_image,load_matrix_image,clear_matrix_image
from button_images import grid_matrix_image,line_matrix_image
from buttons import Button,convert_matrix_to_img
from timer import Timer
import os

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

        clrs = [WHITE,absBlack,GREAY,BLACK,GREEN,TURTLEGREEN,VIOLET,ORANGE,CYAN,BLUE,PINK,YELLOW,AMBER,MAROON,OLIVE,TEAL,TRANSPARENT]
        self.row_items = row_items if row_items is not None else self.height//40
        self.col_items = col_items if col_items is not None else self.width//40
        
        self.padding_x ,self.padding_y = padding_x,padding_y

        row_gap = (self.height-self.padding_x) / self.row_items
        col_gap = (self.width-self.padding_y) / self.col_items

        # this is for correcting the position of the colour bar
        self._x = padding_x/2
        self._y = padding_y

        self.colours = [
            [colourButton(clrs[(row*self.col_items + col) if (row*self.col_items + col) < len(clrs) else len(clrs)-1],self._x+col * col_gap,self._y+self.position_y +row * row_gap,self.win )
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


def get_mouse_position(board):
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        return (y,x)


def main():  # sourcery no-metrics

    def click_events(event, board):
        if event.key == pygame.K_f:
            board.set_pen_type('fill')
        if event.key == pygame.K_e:
            board.set_pen_type('eraser')
        if event.key == pygame.K_n:
            board.set_pen_type('line')
        if event.key == pygame.K_p:
            board.set_pen_type('pen')

        if event.key == pygame.K_s:
            board.save()
        if event.key == pygame.K_l:
            board.load()
        if event.key == pygame.K_c:
            board.clear()
        if event.key == pygame.K_d:
            board.toggle_grid()

        if event.key == pygame.K_u:
            board.undo()

    # naming convention is a bit off

    # size of the screen from pyautogui
    screen_x,screen_y = size()
    # screen_x,screen_y = 1200,800
    pixel_x,pixel_y = 64,64
    screen_x,screen_y = screen_x//64,screen_y//64
    # screen_x,screen_y = screen_x//pixel_x,screen_y//pixel_y
    screen_x = min(8,screen_x,screen_y)
    screen_y = screen_x
    
    
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((620, 612))
    # WIN = pygame.display.set_mode((612, 612))

    pygame.display.set_caption('Art of Life')
    pygame_icon = pygame.image.load(os.path.join('assets','brush.png'))
    pygame.display.set_icon(pygame_icon)
    FPS = 60
    run = True

    board = Grid(cols = pixel_x, rows = pixel_y, width = 64*screen_x, height = 64*screen_y, WIN = WIN)
    clr_bar = colourBar(width = board.width,height = 100, position_x = 0, position_y = board.height, win = WIN)
    # clr_bar = colourBar(width = 200,height = 100, position_x = 0, position_y = board.height, win = WIN)

    slider = Slider(board.width+(WIN.get_width()-board.width)/2,550,WIN)

    surface = pygame.Surface((WIN.get_width()-board.width, WIN.get_height()))
    surface.fill((160,160,160))
    # pos_x = (WIN.get_width() - board.width - 40)/2 + board.width
    pos_x = 521
    pos_y =  20 -4
    spacing_y = 20

    row_items = 5

    # slider = Slider(521+20,550,WIN)

    buttons = []

    idx = 0
    # ! can't put lambda collectively because it also runs the function
    for i, func, val in [
        (brush_matrix_img,   lambda : board.set_pen_type('pen'),'pen'),
        (eraser_matrix_img,  lambda : board.set_pen_type('eraser'),'eraser'),
        (line_matrix_image,  lambda : board.set_pen_type('line'),'line'),
        (fill_matrix_img,    lambda : board.set_pen_type('fill'),'fill'),
        (dropper_matrix_img, lambda : board.set_pen_type('dropper'),'dropper'),
        (save_matrix_image,  lambda : board.save(), None),
        (load_matrix_image,  lambda : board.load(), None),
        (clear_matrix_image, lambda : board.clear(), None),
        (grid_matrix_image , lambda : board.toggle_grid(), None)]:
        idx += 1
        buttons.append(Button(color = (255,255,255),x = pos_x,y = pos_y, width= 40,height=40,text = convert_matrix_to_img(i),win = WIN,func = func))
        buttons[-1].val = val
        pos_y += 40 + spacing_y
        # indicies start from
        if idx >= row_items:
            pos_x += 40 + 10
            pos_y = 20 - 4
            idx = 0
        
    
    board.set_pen_type('pen')
    while run:
        if pygame.mouse.get_pressed()[0]:
            x,y = get_mouse_position(board)
            clr = clr_bar.clicked(pygame.mouse.get_pos())
            board.pen_size = int(slider.slideVal )
            if clr:
                board.pen_colour = clr
                if board.pen_type == 'eraser':
                        board.pen_type = 'pen'
            if board.clicked(x, y) != -1:
                # undo.append([cube.color for cube in board.cubes])
                pass

        # checks for right click
        elif pygame.mouse.get_pressed()[2] :
            x,y = get_mouse_position(board)
            if board.delete(x,y) == -1:
                clr_bar.change_colour(pygame.mouse.get_pos())
                i,j = clr_bar.selected_block
                if board.pen_colour != clr_bar.colours[i][j].colour:
                    board.pen_colour = clr_bar.colours[i][j].colour
                    if board.pen_type == 'eraser':
                        board.pen_type = 'pen'
        
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                click_events(event, board)

        # this take cares of border of button button no core functionality
        for button in buttons:
            if button.val == board.pen_type:
                button.clicked = True
            else:
                button.clicked = False

        # drawing objects
        WIN.blit(surface,(board.width,0))
        for btn in buttons:
            btn.update()
        board.pen_size = int(slider.slideVal)
        slider.update()
        pygame.display.update()
    pygame.quit()


if __name__ == '__main__' :
    main()