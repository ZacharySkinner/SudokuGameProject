import pygame
from SudokuSolverProject import*
import time
pygame.init()

class UI():
    def __init__(self,Theboard):
        self.Sudokuboard=Theboard
        self.gap=Window_Width/self.Sudokuboard.board_size

    def draw_nums(self,board,bold=True,rgb=(0,0,0)):
        self.gap=Window_Width/self.Sudokuboard.board_size
        fontsize=int(self.gap*.5)

        for row in range(self.Sudokuboard.board_size):
            for column in range(self.Sudokuboard.board_size):
                if board[row][column] != 0:
                    fnt = pygame.font.SysFont("comicsansms", fontsize, bold)
                    text = fnt.render(f"{board[row][column]}", True, rgb)
                    text_width, text_height = fnt.size(f"{board[row][column]}")
                    xoffset=self.gap/2-text_width/2
                    yoffset=self.gap/2-text_height/2
                    window.blit(text,(xoffset+column*self.gap,yoffset+row*self.gap))

    def draw_edge(self):
        thickness=5
        pygame.draw.line(window, (0,0,0), (thickness/2,0), (thickness/2, Window_Width), thickness)
        pygame.draw.line(window, (0,0,0), (0,thickness/2), (Window_Width,thickness/2), thickness)
        pygame.draw.line(window, (0,0,0), (0,Window_Width), (Window_Width,Window_Width), thickness)
        pygame.draw.line(window, (0,0,0), (Window_Width-thickness/2,0), (Window_Width-thickness/2,Window_Width), thickness)

    def draw_grid(self):
        self.gap=Window_Width/self.Sudokuboard.board_size
        fontsize=int(self.gap*.5)
        offset=((Window_Width-(self.gap*(self.Sudokuboard.board_size-1)+fontsize))/2)-10
        for i in range (1,self.Sudokuboard.board_size):
            if i % self.Sudokuboard.box_size == 0 and i !=0:
                pygame.draw.line(window, (0,0,0), (i*self.gap,0), (i*self.gap, Window_Width), 5)
                pygame.draw.line(window, (0,0,0), (0,i*self.gap), (Window_Width, i*self.gap), 5)
            else:
                pygame.draw.line(window, (0,0,0), (i*self.gap,0), (i*self.gap, Window_Width), 1)
                pygame.draw.line(window, (0,0,0), (0,i*self.gap), (Window_Width, i*self.gap), 1)

    def victory(self):
        fnt = pygame.font.SysFont("comicsansms", 125, True)
        vic= pygame.Rect(50,150,500,300)       
        victext= fnt.render(f"Victory!",True,"White")
        pygame.draw.rect(window,(0,175,200),vic)
        window.blit(victext,(65, 200))

    def draw_mainboard(self):
        window.fill((255,255,255))
        self.draw_edge()
        self.draw_grid()
        self.draw_nums(self.Sudokuboard.board)
        self.draw_nums(Mainboard.testboard,False,(150,150,150))
        if selected != None:
            MainUI.cube_glow(selected)
        if Mainboard.vict == True:
            self.victory()
        x,y = pygame.mouse.get_pos()
        Butttons.draw_buttons(x,y)

    def cube_glow(self,cord):
        gap=Window_Width/Mainboard.board_size
        pygame.draw.line(window, (255,0,0), (cord[0]*gap,cord[1]*gap), ((cord[0]+1)*gap,(cord[1])*gap), 5)
        pygame.draw.line(window, (255,0,0), (cord[0]*gap,cord[1]*gap), ((cord[0])*gap,(cord[1]+1)*gap), 5)
        pygame.draw.line(window, (255,0,0), ((cord[0]+1)*gap,(cord[1])*gap), ((cord[0]+1)*gap,(cord[1]+1)*gap), 5)
        pygame.draw.line(window, (255,0,0), ((cord[0])*gap,(cord[1]+1)*gap), ((cord[0]+1)*gap,(cord[1]+1)*gap), 5)

class buttons():
    def __init__(self):
        self.fnt = pygame.font.SysFont("comicsansms", 20, True)
        self.ycord=(Window_Width+(Window_Hieght-Window_Width)/2)-30
        self.new4by4= pygame.Rect(10,self.ycord,110,60)       
        self.new4by4text= self.fnt.render("4x4",True,"White")
        self.new9by9= pygame.Rect(140,self.ycord,110,60)       
        self.new9by9text= self.fnt.render("9x9",True,"White")
        self.solve= pygame.Rect(270,self.ycord,110,60)       
        self.solvetext= self.fnt.render("SOLVE",True,"White")
    def draw_buttons(self,x,y):
        #print(x,y)
        self.draw_button(self.new4by4,self.new4by4text,x,y)
        self.draw_button(self.new9by9,self.new9by9text,x,y)
        self.draw_button(self.solve,self.solvetext,x,y)

    def draw_button(self,button,buttontext,x,y):
        textwidth=buttontext.get_width()
        buttonwidth=button.width
        xoffset=(buttonwidth-textwidth)/2
        if button.x <= x <= button.x+110 and button.y <= y <= button.y+60:
            pygame.draw.rect(window,(0,150,200),button)
        else:
            pygame.draw.rect(window,(0,200,200),button)
        window.blit(buttontext,(button.x+xoffset, button.y+15))

def initizlize():
    global Window_Width
    global Window_Hieght
    global window
    global Butttons
    global Mainboard
    global MainUI
    global run
    global selected
    Window_Width = 600
    Window_Hieght = 700
    window = pygame.display.set_mode((Window_Width, Window_Hieght))
    pygame.display.set_caption("Sudoku")
    Butttons = buttons()
    Mainboard = SodokuSolver()
    MainUI = UI(Mainboard)
    run=True
    selected=None


initizlize()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if Butttons.new4by4.collidepoint(event.pos):
                Mainboard.vict=False
                Mainboard.create_random(2)
                Mainboard.set_difficulty(0)
            elif Butttons.new9by9.collidepoint(event.pos):
                Mainboard.vict=False
                Mainboard.create_random(3)
                Mainboard.set_difficulty(32)
            elif Butttons.solve.collidepoint(event.pos):
                Mainboard.vict=False
                Mainboard.solve_board()
            else:
                gap=Window_Width/Mainboard.board_size
                x,y = pygame.mouse.get_pos()
                selected = (int(x//gap),int(y//gap))
                if selected[0]>=Mainboard.board_size or selected[1]>=Mainboard.board_size:
                    selected=None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                    Mainboard.hint()
            elif selected != None:
                if event.key == pygame.K_0:
                    Mainboard.sketch(0,selected)
                elif event.key == pygame.K_1:
                    Mainboard.sketch(1,selected)       
                elif event.key == pygame.K_2:
                    Mainboard.sketch(2,selected)
                elif event.key == pygame.K_3:
                    Mainboard.sketch(3,selected)
                elif event.key == pygame.K_4:
                    Mainboard.sketch(4,selected)
                elif event.key == pygame.K_5:
                    Mainboard.sketch(5,selected)
                elif event.key == pygame.K_6:
                    Mainboard.sketch(6,selected)
                elif event.key == pygame.K_7:
                    Mainboard.sketch(7,selected)
                elif event.key == pygame.K_8:
                    Mainboard.sketch(8,selected)
                elif event.key == pygame.K_9:
                    Mainboard.sketch(9,selected)
                elif event.key == pygame.K_RETURN:
                    print(f"UIiiii:{MainUI.Sudokuboard.board}\nMain:{Mainboard.board}")
                    Mainboard.sketch(999,selected)

    MainUI.draw_mainboard()
    pygame.display.flip()
pygame.quit()
