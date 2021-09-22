import pygame
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename,asksaveasfilename

class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400,WIN = None):
        self.rows = cols
        self.cols = rows
        self.cubes = [
            [Cube(i, j, width, height, self.cols, self.rows,WIN)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.draw_grid = False
        self.width = width
        self.height = height
        self.win = WIN
        self.surface = pygame.Surface((self.width,self.height))
        self.draw()
        self.availableFormats = [("All files", "*.*"),("Portable Network Graphics", "*.png"), ("JPEG", "*.jpg"), ("GIF", "*.gif")]
        BLACK = (60,60,60)
        self.pen_colour = BLACK
        self.pen_size = 1
        self.pen_type = 'pen'

        self.start = None
        self.end = None

        self.undo_states = []
        self.undo_states.append([[cube.color for cube in row] for row in self.cubes ][:])
        self.redo_states = []

    def draw(self):
        # self.win.blit(self.surface,(0,0))
                # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw()
        if self.draw_grid:
            row_gap = self.width / self.rows
            col_gap = self.height / self.cols

            for i in range(self.rows+1):
                pygame.draw.line(self.win, (40,40,40), (0, i*row_gap),(self.height, row_gap*i))
            for i in range(self.cols+1):
                pygame.draw.line(self.win, (40,40,40), (i*col_gap, 0), (col_gap*i, self.width))


        pygame.display.update()

    def clicked(self,i,j):
        if type(i) is not int or type(j) is not int:
            return -1
        if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
            return -1

        if self.pen_type == 'fill':
            self.fill(i,j)
            self.draw()
            return
        elif self.pen_type == 'line':
            self.draw_line((i,j))
            self.draw()
            return
        elif self.pen_type == 'eraser':
            self.delete(i,j)
            self.draw()
            return
        elif self.pen_type == 'dropper':
            self.pen_colour = self.cubes[i][j].color
            time.sleep(0.15)
            self.pen_type = 'pen'
            return

        # reseting the line tool
        if self.start is not None and self.end is None:
            self.start = None

        for x in range(max(0,i-self.pen_size+1),min(i+self.pen_size,self.rows)):
            for y in range(max(0,j-self.pen_size+1),min(j+self.pen_size,self.cols)):
                self.cubes[x][y].color = self.pen_colour
        self.draw()

    def delete(self,i,j):
        if type(i) is not int or type(j) is not int:
            return -1
        if i < 0 or i >= self.rows or j < 0 or j >= self.cols:
            return -1
        for x in range(max(0,i-self.pen_size+1),min(i+self.pen_size,self.rows)):
            for y in range(max(0,j-self.pen_size+1),min(j+self.pen_size,self.cols)):
                self.cubes[x][y].color = (255,255,255)
        self.draw()

    def fill(self,x,y):
        if x < 0 or x >= self.rows or y < 0 or y >= self.cols:
            return -1
        neighbours = []
        block_colour = self.cubes[x][y].color
        if block_colour == self.pen_colour:
            return
        def cube_nbrs(x,y):
            # DOWN
            if x < self.rows-1  and self.cubes[x + 1][y].color  == block_colour:
                neighbours.append(self.cubes[x + 1][y])

            # UP

            if x > 0 and self.cubes[x - 1][y].color  == block_colour:  
                neighbours.append(self.cubes[x - 1][y])

            # RIGHT
            if y < self.rows-1 and self.cubes[x][y + 1].color  == block_colour:
                neighbours.append(self.cubes[x][y + 1])

            # LEFT
            if y > 0 and self.cubes[x][y - 1].color  == block_colour:
                neighbours.append(self.cubes[x][y - 1])
        cube_nbrs(x,y)
        while(neighbours):
            latest = neighbours.pop()
            latest.color = self.pen_colour
            cube_nbrs(latest.row,latest.col)
        self.draw()
        return True
    
    def clear(self):
        for row in self.cubes:
            i = 0 
            for cube in row:
                if i == 7:
                    pygame.display.update()
                    i = 0
                i += 1
                cube.reset()
                cube.draw()
        self.draw_grid = False
        self.draw()
        self.undo_redo_reset()

    def save(self):

        window = Tk()
        window.withdraw()
        name = asksaveasfilename(title="Save File",defaultextension='.png', filetypes=self.availableFormats)
        # check if a file exists
        if name == '' or name is None :
            return

        size = (self.width,self.height)
        pos = (0,0)
        image = pygame.Surface(size)       
        toggle = False
        if self.draw_grid:
            self.draw_grid = False
            self.draw()
            toggle = True

        image.blit(self.win,(0,0),(pos,size))

        if toggle:
            self.draw_grid = True
            self.draw()
        pygame.image.save(image,name)

    def load(self):
        window = Tk()
        window.withdraw()
        path =  askopenfilename(title="Open File", filetypes=self.availableFormats)
        if path == '' or path is None:
            return
            
        img = pygame.transform.scale(pygame.image.load(path), (self.rows,self.cols))
        self.undo_redo_reset()

        for i in range(self.rows):
            for j in range(self.cols):
                # for images there are 4 channels and we only need 3 4th channel is for opacity
                self.cubes[i][j].color = tuple(img.get_at((j,i))[0:3])

        self.draw()

    def draw_line(self,pos):

        if self.start is None:
            self.start = self._extracted_from_draw_line_3(pos)

        elif self.end is None:
            self.end = self._extracted_from_draw_line_3(pos)

            # ||||
            i = min(self.start.row,self.end.row)
            while i < max(self.start.row,self.end.row):
                i += 1
                self.cubes[i][self.start.col].color = self.pen_colour

            # this is to avoid a point being missed
            if self.end.row< self.start.row:
                self.cubes[self.end.row][self.start.col].color = self.pen_colour

            # ----
            i = min(self.start.col,self.end.col)
            while i < max(self.start.col,self.end.col):
                i += 1
                self.cubes[self.end.row][i].color = self.pen_colour
            
            self.draw()
            self.start = self.end
            self.end = None
            return True

    def  _extracted_from_draw_line_3(self, pos):
        result = self.cubes[pos[0]][pos[1]]
        result.clicked(self.pen_colour)
        return result

    def save_state(self):
        temp = [[cube.color for cube in row] for row in self.cubes ][:]
        if len(self.undo_states) > 1:
            if temp != self.undo_states[-1]:
                self.undo_states.append(temp)
        else:
            self.undo_states.append(temp)

    def undo(self):
        if len(self.undo_states) < 2:
            return

        present_state = self.undo_states.pop()
        self.redo_states.append(present_state)
        state = self.undo_states[-1]

        for i,row in enumerate(state):
            for j,clr in enumerate(row):
                self.cubes[i][j].color = clr
        self.draw()

    def redo(self):
        if len(self.redo_states) <1:
            return

        state = self.redo_states.pop()
        self.undo_states.append(state)

        for i,row in enumerate(state):
            for j,clr in enumerate(row):
                self.cubes[i][j].color = clr
        self.draw()

    def set_pen_type(self,pen_type):
        if pen_type is None:
            print('pen_type can"t be None')
            return
        self.pen_type = pen_type
    
    def toggle_grid(self):
        self.draw_grid = not self.draw_grid
        self.draw()

    def undo_redo_reset(self):
        self.undo_states = [] 
        self.redo_states = []

class ZoomDisplay():
    def __init__(self,x = 0, y = 0, width = 50, height = 50, win = None) -> None:
        self.x,self.y = x,y
        self.width, self.height = width, height
        self.rows,self.cols = 5,5
        self.win = win
        self.cubes =  [
            [Cube(i, j, width, height, 5, 5, win, x = self.x, y=self.y)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.zoom = True

    def draw(self):
        for row in self.cubes:
            for cube in row:
                cube.draw()

    def update(self,board):
        x, y = pygame.mouse.get_pos()
        gap = board.width // board.rows
        y //= gap
        x //= gap

        if (x < 0 or x >= board.rows or y < 0 or y >= board.cols) or not self.zoom:
            for row in self.cubes:
                for cube in row:
                    cube.color = (255,255,255)
            self.draw()
            return 

        i, j = y, x

        a = 0
        for x in range(max(0,i-self.rows//2),min(i+self.rows//2+1,board.rows)):
            b = 0
            for y in range(max(0,j-self.cols//2),min(j+self.cols//2 +1,board.cols)):
                self.cubes[a][b].color = board.cubes[x][y].color
                b += 1
            a += 1

        self.draw()

    def toggle_zoom(self):
        self.zoom = not self.zoom

    def is_hovering(self) -> bool:
        #Pos is the mouse position or a tuple of (x,y) coordinates
        pos = pygame.mouse.get_pos()
        return (
            pos[0] > self.x
            and pos[0] < self.x + self.width
            and pos[1] > self.y
            and pos[1] < self.y + self.height
        )

class Cube():
    def __init__(self,row, col, width, height, cols, rows,win, x = 0, y = 0):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.centerFactor = 10
        self.win = win
        WHITE = (255,255,255)
        self.color = WHITE
        self.x, self.y = x, y 

    def draw(self):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        pygame.draw.rect(self.win, self.color, pygame.Rect(x+self.x, y+self.y, colGap, rowGap))

    def reset(self):
        WHITE = (255,255,255)
        self.color = WHITE

    def clicked(self,colour):
        self.color = colour
        self.draw()
        pygame.display.update()

    def delete(self):
        WHITE = (255,255,255)
        self.clicked(WHITE)
    
