#class that takes sudoku board and solves
#Class assumes that the input sudoku board has total boxes = number of rows = number of columns = integer that is a perfect square
import random
class SodokuSolver:
    def __init__(self,Puzzle_Board=[[1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]]):
        self.board = Puzzle_Board
        self.board_size = len(self.board) #contains number of row and columns assumes there is same num of row/columns
        self.box_size = int(self.board_size ** 0.5) #contains the demensions of the boxes
        self.found=0
        self.testboard = self.create_empty(self.box_size)
        self.solution = Puzzle_Board
        self.vict=False
        self.lose=False
        self.mistake=0
    # prints out board in terminal
    def print_sudoku_board(self):
        board_size=len(self.board)
        for i in range(self.board_size):
            if (i != 0 and i % (self.box_size) == 0):
                for j in range(self.board_size):
                    print("- - ",end="")
                print("")
            for k in range(self.board_size):
                if (k == self.board_size-1):
                    print(f" {self.board[i][k]} \n",end="")
                elif (k != 0 and k % (self.box_size) == 0):
                    print(f" | {self.board[i][k]} ",end="")
                else:
                    print(f" {self.board[i][k]} ",end="")
        print("Printed^\n")

    #adds number to self.solution to track what player is considering in a square
    def sketch(self,value,cord):
        if(value == 999):
            if (self.testboard[cord[0]][cord[1]] == self.solution[cord[0]][cord[1]]):
                self.board[cord[0]][cord[1]] = self.testboard[cord[0]][cord[1]]
                self.testboard[cord[0]][cord[1]] = 0
            else:
                if self.testboard[cord[0]][cord[1]] != 0:
                    self.mistake += 1
        else:
            if self.board[cord[0]][cord[1]]==0 and value<=self.board_size:
                if (self.testboard[cord[0]][cord[1]]*10)+value>self.board_size:
                    self.testboard[cord[0]][cord[1]]=value
                else:
                    self.testboard[cord[0]][cord[1]]=(self.testboard[cord[1]][cord[0]]*10)+value
        if self.find_empty() == None:
            self.vict=True   
        if self.mistake>=5:
            self.lose=True
    #return cord of first empty square in self.board returns in row,column form
    def find_empty(self):
        for i in range (self.board_size):
            for j in range (self.board_size):
                if self.board[i][j] == 0 :
                    return(i,j)
        return None
    
    #sets self.board and self.solution to board of sopesified size size is size of boxes in board so size 2 is 4x4 board
    def create_empty(self,size):
        board=[]
        self.board_size = int(size*size) #contains number of row and columns assumes there is same num of row/columns
        self.box_size = size #contains the demensions of the boxes
        for i in range (self.board_size):
            temp=[]
            for k in range (self.board_size):
                temp.append(0)
            board.append(temp)
        
        return board
    
    #checks if a value=num is valid in a specific cordinate cord is in Row,Column form
    def is_valid(self, cord, num):
        #checks the Column
        for i in range(self.board_size):
            if  (i != cord[0] and self.board[i][cord[1]] == num):
                return False

        #checks the Row    
        for i in range(self.board_size):
            if  (i != cord[1] and self.board[cord[0]][i] == num):
                return False
        
        #checks box
        box_cord_x = cord[1] // self.box_size
        box_cord_y = cord[0] // self.box_size
        for column in range(box_cord_x*self.box_size, box_cord_x*self.box_size+self.box_size):
            for row in range(box_cord_y*self.box_size, box_cord_y*self.box_size+self.box_size):
                if (((row,column) != cord) and (self.board[row][column]==num)):
                    return False
        return True
    
    #Fills the first empty box in self.board in with the correct number
    def hint(self):
        cord=self.find_empty()
        if cord!=None:
            self.board[cord[0]][cord[1]]=self.solution[cord[0]][cord[1]]
            self.testboard[cord[0]][cord[1]]=0
    
    #Solve self.board using backtracking
    def solve_board(self):
        current_cord = self.find_empty() 
        
        # return true if puzzle is fully solved
        if current_cord == None:
            return True 
        else:
            self.testboard[current_cord[0]][current_cord[1]]=0      
        for value in range (1,self.board_size+1):
            if self.is_valid(current_cord,value):
                self.board[current_cord[0]][current_cord[1]]=value                
                if self.solve_board():
                    return True
                self.board[current_cord[0]][current_cord[1]] = 0
        return False
    
    #sets self.solution adn self.board to a random solved board of spesified size
    def create_random(self,size):
        self.board=self.create_empty(size) 
        self.testboard = self.create_empty(self.box_size)
        self.vict=False
        self.lose=False
        self.mistake=0      
        self.fill_random()
        self.solution=[]
        for row in range(len(self.board)):
            temp=[]
            for column in range(len(self.board)):
                temp.append(self.board[row][column])
            self.solution.append(temp)
        return True

    #Used to fill in an empty board with random numbers resulting in a solved board with numnbers randomized
    def fill_random(self):       
        current_cord = self.find_empty() 
        valuelist = []
        for i in range (1,self.board_size+1):
            valuelist.append(i)
        random.shuffle(valuelist)
        if current_cord == None:
            return True       
        for value in valuelist:
            if self.is_valid(current_cord,value):
                self.board[current_cord[0]][current_cord[1]]=value
                if self.fill_random():
                    return True
                self.board[current_cord[0]][current_cord[1]] = 0
        return False
    
    #Uses Backtracking to return weather or not self.board currently has only 1 solution return boolean
    def only_one(self,initial=False):
        current_cord = self.find_empty()
        if initial == True:
            self.found = 0
            if current_cord == None:
                return True
        if current_cord == None:
            self.found += 1 
            if self.found>1:
                return True   
            else:
                return False
               
        for value in range (1,self.board_size+1):
            if self.is_valid(current_cord,value):
                self.board[current_cord[0]][current_cord[1]]=value
                if self.only_one():
                    self.board[current_cord[0]][current_cord[1]] = 0
                    if initial == True:
                        return False
                    else:
                        return True
                self.board[current_cord[0]][current_cord[1]] = 0
        if initial == True and self.found == 1:
            return True
        return False
        
    #removes givens from a board until givens while making sure the board only has 1 solutioon 
    #will loop through all givens in random order until givens<=difficulty or until loop has gone through all givens
    def set_difficulty(self,difficulty):
        nonemptyboxes=[]
        givens=0 #givens is how many givens remain on board
        test=0 # tracks how many givens we have tried to remove
        for row in range(self.board_size):
            for column in range(self.board_size):
                if self.board[row][column] != 0:
                    nonemptyboxes.append([row,column])
                    givens += 1
        random.shuffle(nonemptyboxes)


        for cordinate in nonemptyboxes:
            temp = self.board[cordinate[0]][cordinate[1]]
            self.board[cordinate[0]][cordinate[1]]=0

            testing = self.only_one(True)
            test+=1

            if testing == False:
                self.board[cordinate[0]][cordinate[1]]=temp
            else:
                #print(cordinate)
                givens -= 1
                if givens <= difficulty:
                    return True
        return False                      


