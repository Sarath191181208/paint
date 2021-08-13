WHITE = (215, 215, 215)
GREAY = (70, 70, 70)
BLACK = (0, 0, 0)
BLUE = (10, 40, 100)
checksClr = BLUE
boardClr = WHITE
txtClr = GREAY
class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400,WIN = None):
        self.rows = cols
        self.cols = rows
        self.cubes = [
            [Cube(0, i, j, width, height, self.cols, self.rows,WIN)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.width = width
        self.height = height
        self.win = WIN
        self.surface = pygame.Surface((self.width,self.height))
        self.draw()
    def draw(self, win = None):
        self.win.blit(self.surface,(0,0))
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw()
        thick = 1
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*rowGap),(self.height, rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*colGap, 0), (colGap*i, self.width))
        pygame.display.update()
    def updateAt(self, value, i, j, win):
        self.cubes[i][j].value = value
        self.draw()
class Cube():
    def __init__(self, value, row, col, width, height, cols, rows,win):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.centerFactor = 10
        self.win = win
    def draw(self):
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        if (self.col % 2) == (self.row % 2) :
            pygame.draw.rect(self.win, checksClr, pygame.Rect(x, y, colGap, rowGap))
        if self.value == 1:
        #   newImg = pygame.transform.scale(queenImg, (int(colGap-self.centerFactor), int(rowGap-self.centerFactor)))
        #   win.blit(newImg, (x+self.centerFactor/2, y+self.centerFactor/2))
            fnt = pygame.font.SysFont('comicsans', 40)
            text = fnt.render('Q', 1, txtClr)
            self.win.blit(text, (x + (colGap/2 - text.get_width()/2),
                        y + (rowGap/2 - text.get_height()/2))) 