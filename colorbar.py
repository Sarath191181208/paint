import pygame 
from colours import * 
from tkinter import Tk,colorchooser

class ColourBar():
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

        clrs = [BLACK,WHITE,absBlack,GREAY,GREEN,TURTLEGREEN,VIOLET,ORANGE,CYAN,BLUE,PINK,YELLOW,AMBER,MAROON,OLIVE,TEAL,TRANSPARENT]
        self.row_items = row_items if row_items is not None else self.height//40
        self.col_items = col_items if col_items is not None else self.width//40
        
        self.padding_x ,self.padding_y = padding_x,padding_y

        row_gap = (self.height-self.padding_x) / self.row_items
        col_gap = (self.width-self.padding_y) / self.col_items

        # this is for correcting the position of the colour bar
        self._x = padding_x/2
        self._y = padding_y

        self.colours = [
            [ColourButton(clrs[(row*self.col_items + col) if (row*self.col_items + col) < len(clrs) else len(clrs)-1],self._x+col * col_gap,self._y+self.position_y +row * row_gap,self.win )
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

    def is_hovering(self):
        pos = pygame.mouse.get_pos()
        return (
            pos[0] > self.position_x
            and pos[0] < self.position_x + self.width
            and pos[1] > self.position_y
            and pos[1] < self.position_y + self.height
        )


class ColourButton():
    def __init__(self,colour,x,y,win) -> None:
        self.colour = colour
        self.win = win
        self.x,self.y =  x,y

    def draw(self):
        pygame.draw.rect(self.win, self.colour, pygame.Rect(self.x, self.y, 20, 20))
    
    def stroke(self):
        pygame.draw.rect(self.win, (0,0,0), pygame.Rect(self.x, self.y, 20, 20),3)
        pygame.display.update()
