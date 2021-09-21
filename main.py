from val_nav import ValNav
import pygame
from pyautogui import size
from tkinter import Tk
# from button_matrices import brush_matrix_img,eraser_matrix_img,dropper_matrix_img,fill_matrix_img,save_matrix_image,load_matrix_image,clear_matrix_image
# from button_matrices import grid_matrix_image,line_matrix_image, flag_matrix_image,undo_matrix_image,redo_matrix_image
from tkinter import messagebox
import os

from canvas import Grid, ZoomDisplay
# from slider import Slider
from buttons import Button
from colorbar import ColourBar
from timer import Timer
from colours import *
from button_images import *
pygame.init()

class PositionTracker():
    def __init__(self,x = 0 , y = 0 , win = None ) -> None:
        self.x,self.y = x,y
        self.win = win
        self.x_pos,self.y_pos = "",""
    
    def draw(self):
        text = PYtxt(f"X : {self.x_pos}")
        self.win.blit(text,(self.x-text.get_width()/2,self.y))
        text = PYtxt(f"Y : {self.y_pos}")
        self.win.blit(text,(self.x-text.get_width()/2+50,self.y))

    def update_pos(self,pos):
        self.x_pos,self.y_pos = pos
    
    def update(self):
        self.draw()


def PYtxt(txt: str, fontSize: int = 14, font: str = 'arial', fontColour: tuple = (0, 0, 0)):
    font = pygame.font.match_font(
            font, bold=False, italic=False)
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


def get_mouse_position(board):
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap
        if x < 0 or x >= board.rows or y < 0 or y >= board.cols:
            return "",""
        return (y,x)


def main():  # sourcery no-metrics

    def click_events(event, board):
        def lengths():
            print('undo : ',len(board.undo_states))
            print('redo : ',len(board.redo_states))

            print()

        # --------------------------------------------------------------------------

        if event.key == pygame.K_f:
            board.set_pen_type('fill')
        if event.key == pygame.K_e:
            board.set_pen_type('eraser')
        if event.key == pygame.K_l:
            board.set_pen_type('line')
        if event.key == pygame.K_p:
            board.set_pen_type('pen')
        # if event.key == pygame.k_d:
        #     board.set_pen_type('dropper')

        if event.key == pygame.K_s:
            board.save()
        if event.key == pygame.K_o:
            board.load()
        if event.key == pygame.K_c:
            board.clear()
        if event.key == pygame.K_g:
            board.toggle_grid()

        if event.key == pygame.K_z:
            board.undo()
            lengths()
            board.draw()
        if event.key == pygame.K_y:
            board.redo()
            lengths()
            board.draw()
        if event.key == pygame.K_SPACE:
            board.save_state()

        # ------------------------------------------------------------------
        if event.key == pygame.K_TAB:
            lengths()

    # naming convention is a bit off
    def create_buttons(buttons):
        pos_x = 521
        pos_y =  80
        spacing_y = 20

        row_items = 6
        idx = 0
        # ! can't put lambda collectively because it also runs the function
    
        for img, func, val in [
            (brushImage,   lambda : board.set_pen_type('pen'),'pen'),
            (eraserImage,  lambda : board.set_pen_type('eraser'),'eraser'),
            (lineImage,    lambda : board.set_pen_type('line'),'line'),
            (fillImage,    lambda : board.set_pen_type('fill'),'fill'),
            (dropperImage, lambda : board.set_pen_type('dropper'),'dropper'),
            (saveImage,    lambda : board.save(), 'save'),
            (loadImage,    lambda : board.load(), 'load'),
            (gridImage ,   lambda : board.toggle_grid(), 'grid'),
            (undoImage,    lambda : board.undo(),'undo'),
            (redoImage ,   lambda : board.redo(),'redo'),
            (zoomImage,    lambda : zoom_dis.toggle_zoom(),'toggle_zoom'),
            (clearImage,   lambda : board.clear(), 'clear'),
            ]:
            idx += 1
            buttons.append(Button(color = (255,255,255),x = pos_x,y = pos_y, width= 40,height=40,text = img,win = WIN,func = func))
            # buttons.append(Button(color = (255,255,255),x = pos_x,y = pos_y, width= 40,height=40,text = convert_matrix_to_img(i),win = WIN,func = func))
            buttons[-1].val = val
            pos_y += 40 + spacing_y
            # indicies start from
            if idx >= row_items:
                pos_x += 40 + 10
                pos_y = 80
                idx = 0
    # size of the screen from pyautogui
    screen_x,screen_y = size()
    # screen_x,screen_y = 1200,800
    pixel_x,pixel_y = 512,512
    screen_x,screen_y = screen_x//64,screen_y//64
    # screen_x,screen_y = screen_x//pixel_x,screen_y//pixel_y
    screen_x = min(8,screen_x,screen_y)
    screen_y = screen_x
    
    
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((620, 612))

    pygame.display.set_caption('Art of Life')
    pygame_icon = pygame.image.load(os.path.join('assets','brush.png'))
    pygame.display.set_icon(pygame_icon)
    FPS = 60
    run = True

    board = Grid(cols = pixel_x, rows = pixel_y, width = 64*screen_x, height = 64*screen_y, WIN = WIN)
    clr_bar = ColourBar(width = board.width,height = 100, position_x = 0, position_y = board.height, win = WIN)
    zoom_dis = ZoomDisplay(x = 513,y = 512, width= 105 , height=100, win = WIN)

    # surface to draw widgets on
    widgets_surface = pygame.Surface((WIN.get_width()-board.width, WIN.get_height()))
    widgets_surface.fill((160,160,160))

    buttons = []
    create_buttons(buttons)

    board.set_pen_type('pen')

    # place holder variables for undo
    just_pressed = False
    undo_timer = Timer(0.05)
    
    # widgets
    pos_tracker  = PositionTracker(x = 540 , y = 60 , win = WIN)
    val_nav  = ValNav(x = 566, y = 470, win = WIN, max = 5)

    while run:
        # left click check
        if pygame.mouse.get_pressed()[0]:
            just_pressed = True
            x,y = get_mouse_position(board)
            clr = clr_bar.clicked(pygame.mouse.get_pos())
            board.pen_size = int(val_nav.val)

            if clr:
                board.pen_colour = clr
                if board.pen_type == 'eraser':
                        board.pen_type = 'pen'
            if board.clicked(x, y) != -1:
                undo_timer.start_timer()
                pass
        else:
            if just_pressed and not undo_timer.start:
                board.save_state()
                just_pressed = False

        # checks for right click
        if pygame.mouse.get_pressed()[2]:
            x,y = get_mouse_position(board)
            if board.delete(x,y) == -1:
                clr_bar.change_colour(pygame.mouse.get_pos())
                i,j = clr_bar.selected_block
                if board.pen_colour != clr_bar.colours[i][j].colour:
                    board.pen_colour = clr_bar.colours[i][j].colour
                    if board.pen_type == 'eraser':
                        board.pen_type = 'pen'

        # keyboard event handler
        pos_tracker.update_pos(get_mouse_position(board))
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                root = Tk()
                root.withdraw()
                reply = messagebox.askokcancel("Question","Do you like to save the file ?")
                if reply:
                    board.save()
                run = False

            if event.type == pygame.KEYDOWN:
                click_events(event, board)

        # drawing/updating objects
        WIN.blit(widgets_surface,(board.width,0))
        val_nav.update()
        pos_tracker.update()
        undo_timer.update()
        zoom_dis.update(board)
        for btn in buttons:
            btn.update()
            if btn.is_hovering():
                WIN.blit(PYtxt(str(btn.val)),(522,25))
            if btn.val == board.pen_type:
                btn.clicked = True
            else:
                btn.clicked = False

        if zoom_dis.is_hovering():
            WIN.blit(PYtxt("zoom display"),(522,25))
            
        if val_nav.is_hovering():
            WIN.blit(PYtxt("brush size"),(522,25))
        if clr_bar.is_hovering():
            WIN.blit(PYtxt("Left click to select ",9),(522,14))
            WIN.blit(PYtxt("Right to modify",9),(522,25))

        pygame.display.update()
    pygame.quit()


if __name__ == '__main__' :
    main()