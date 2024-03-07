import pygame
from SudokuSolverProject import*
pygame.init()


class buttons():
    def __init__(self):
        self.fnt = pygame.font.SysFont("comicsansms", 20, True)
        self.fnt2 = pygame.font.SysFont("comicsansms", 125, True)
        self.ycord=(Window_Width+(Window_Hieght-Window_Width)/2)-30
        self.new4by4= pygame.Rect(10,self.ycord,110,60)       
        self.new4by4text= self.fnt.render("4x4",True,"White")
        self.new9by9= pygame.Rect(140,self.ycord,110,60)       
        self.new9by9text= self.fnt.render("9x9",True,"White")
        self.solve= pygame.Rect(270,self.ycord,110,60)       
        self.solvetext= self.fnt.render("SOLVE",True,"White")
        self.mistakes= pygame.Rect(400,self.ycord,180,60)  
        self.mistakestext= self.fnt.render(f"Mistakes: {Mainboard.mistake}",True,"Red")
        self.defe= pygame.Rect(50,150,500,300)       
        self.defetext= self.fnt2.render(f"Defeat",True,"Red")

    #draws all buttons on bottum of scree.    
    def draw_buttons(self,x,y):
        #print(x,y)
        self.mistakestext= self.fnt.render(f"Mistakes: {Mainboard.mistake}",True,"Red")
        self.draw_button(self.new4by4,self.new4by4text,x,y)
        self.draw_button(self.new9by9,self.new9by9text,x,y)
        self.draw_button(self.solve,self.solvetext,x,y)
        self.draw_button(self.mistakes,self.mistakestext,x,y)

    #draws indiviual buttons
    def draw_button(self,button,buttontext,x,y):
        textwidth=buttontext.get_width()
        buttonwidth=button.width
        xoffset=(buttonwidth-textwidth)/2
        if button.x <= x <= button.x+110 and button.y <= y <= button.y+60:
            pygame.draw.rect(window,(0,150,200),button)
        else:
            pygame.draw.rect(window,(0,200,200),button)
        window.blit(buttontext,(button.x+xoffset, button.y+15))

class UI(buttons):

    def __init__(self,Theboard,):
        super().__init__()
        self.Sudokuboard=Theboard
        self.gap=Window_Width/self.Sudokuboard.board_size
        self.selected=None

    #Draws Numnbers in the grid
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

    #draws the edges of the board
    def draw_edge(self):
        thickness=5
        pygame.draw.line(window, (0,0,0), (thickness/2,0), (thickness/2, Window_Width), thickness)
        pygame.draw.line(window, (0,0,0), (0,thickness/2), (Window_Width,thickness/2), thickness)
        pygame.draw.line(window, (0,0,0), (0,Window_Width), (Window_Width,Window_Width), thickness)
        pygame.draw.line(window, (0,0,0), (Window_Width-thickness/2,0), (Window_Width-thickness/2,Window_Width), thickness)

    #draw the grid
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

    #solves the board updates board every time it changes a value and pause breifly
    def solve_visually(self):
        current_cord = Mainboard.find_empty()
        pause=10 
        # return true if puzzle is fully solved
        if current_cord == None:
            return True 
        else:
            Mainboard.testboard[current_cord[0]][current_cord[1]]=0            
        for value in range (1,Mainboard.board_size+1):
            if Mainboard.is_valid(current_cord,value):
                Mainboard.board[current_cord[0]][current_cord[1]]=value
                self.selected=current_cord
                self.draw_mainboard()
                pygame.display.flip()
                pygame.time.delay(pause)                
                if self.solve_visually():
                    return True
                Mainboard.board[current_cord[0]][current_cord[1]] = 0
                self.selected=current_cord
                self.draw_mainboard()
                pygame.display.flip()
                pygame.time.delay(pause)
        return False

    #displays vicotry screen
    def victory(self):
        fnt = pygame.font.SysFont("comicsansms", 125, True)
        vic= pygame.Rect(50,150,500,300)
        victext= fnt.render(f"Victory!",True,"White")
        textwidth=victext.get_width()
        buttonwidth=vic.width
        xoffset=(buttonwidth-textwidth)/2       
        pygame.draw.rect(window,(0,175,200),vic)
        window.blit(victext,(vic.x+xoffset, vic.y+50))

    #displays defeat screen
    def defeat(self): 
        textwidth=self.defetext.get_width()
        buttonwidth=self.defe.width
        xoffset=(buttonwidth-textwidth)/2
        pygame.draw.rect(window,(0,0,0),self.defe)
        window.blit(self.defetext,(self.defe.x+xoffset, self.defe.y+50))

    #draws all elements of the board
    def draw_mainboard(self):
        window.fill((255,255,255))
        self.draw_edge()
        self.draw_grid()
        self.draw_nums(self.Sudokuboard.board)
        self.draw_nums(Mainboard.testboard,False,(150,150,150))
        if self.selected != None:
            MainUI.cube_glow(self.selected)
        if Mainboard.vict == True and Mainboard.lose == False:
            self.victory()
        elif Mainboard.lose == True:
            self.defeat()
        x,y = pygame.mouse.get_pos()
        self.draw_buttons(x,y)

    #highlights selected box
    def cube_glow(self,cord):
        gap=Window_Width/Mainboard.board_size
        pygame.draw.line(window, (255,0,0), (cord[1]*gap,cord[0]*gap), ((cord[1]+1)*gap,(cord[0])*gap), 5)
        pygame.draw.line(window, (255,0,0), (cord[1]*gap,cord[0]*gap), ((cord[1])*gap,(cord[0]+1)*gap), 5)
        pygame.draw.line(window, (255,0,0), ((cord[1]+1)*gap,(cord[0])*gap), ((cord[1]+1)*gap,(cord[0]+1)*gap), 5)
        pygame.draw.line(window, (255,0,0), ((cord[1])*gap,(cord[0]+1)*gap), ((cord[1]+1)*gap,(cord[0]+1)*gap), 5)







def initizlize():
    global Window_Width
    global Window_Hieght
    global window
    global Mainboard
    global MainUI
    global run
    Window_Width = 600
    Window_Hieght = 700    
    window = pygame.display.set_mode((Window_Width, Window_Hieght))
    pygame.display.set_caption("Sudoku")   
    Mainboard = SodokuSolver()
    MainUI = UI(Mainboard)
    run=True
    Mainboard.create_random(3)
    Mainboard.set_difficulty(35)


initizlize()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if MainUI.new4by4.collidepoint(event.pos):
                Mainboard.create_random(2)
                Mainboard.set_difficulty(0)
            elif MainUI.new9by9.collidepoint(event.pos):
                Mainboard.create_random(3)
                Mainboard.set_difficulty(32)
            elif MainUI.solve.collidepoint(event.pos):
                Mainboard.solve_board()
            elif MainUI.mistakes.collidepoint(event.pos):
                Mainboard.vict=False
                Mainboard.lose=False
            else:
                gap=Window_Width/Mainboard.board_size
                x,y = pygame.mouse.get_pos()
                MainUI.selected = (int(y//gap),int(x//gap))
                if MainUI.selected[0]>=Mainboard.board_size or MainUI.selected[1]>=Mainboard.board_size:
                    MainUI.selected=None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                    Mainboard.hint()
            elif event.key == pygame.K_SPACE:
                    MainUI.solve_visually()   
            elif MainUI.selected != None:
                if event.key == pygame.K_0:
                    Mainboard.sketch(0,MainUI.selected)
                elif event.key == pygame.K_1:
                    Mainboard.sketch(1,MainUI.selected)       
                elif event.key == pygame.K_2:
                    Mainboard.sketch(2,MainUI.selected)
                elif event.key == pygame.K_3:
                    Mainboard.sketch(3,MainUI.selected)
                elif event.key == pygame.K_4:
                    Mainboard.sketch(4,MainUI.selected)
                elif event.key == pygame.K_5:
                    Mainboard.sketch(5,MainUI.selected)
                elif event.key == pygame.K_6:
                    Mainboard.sketch(6,MainUI.selected)
                elif event.key == pygame.K_7:
                    Mainboard.sketch(7,MainUI.selected)
                elif event.key == pygame.K_8:
                    Mainboard.sketch(8,MainUI.selected)
                elif event.key == pygame.K_9:
                    Mainboard.sketch(9,MainUI.selected)
                elif event.key == pygame.K_RETURN:
                    Mainboard.sketch(999,MainUI.selected)
                 

    MainUI.draw_mainboard()
    pygame.display.flip()
pygame.quit()
