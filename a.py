import copy
import random
import pygame
import sys
import numpy as np

from constants import *

# initial pygame window
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))    # initialize values to 0
        self.empty_sqrs = self.squares # list of squares
        self.marked_sqrs = 0
    
    def mark_sqr(self,row,col,player):
        self.squares[row][col] = player
        self.marked_sqrs += 1   # to know when board is full

    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    # return 0 if no one won yet
    # return 1 if p1 wins
    # return 2 if p2 wins
    def final_state(self):
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:   # not equal to 0 means it is not empty   
                # if show:
                #     color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                #     iPos = (col * SQSIZE + SQSIZE // 2, 20)
                #     fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                #     pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col] # player number
        
        # horizonal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:   # not equal to 0 means it is not empty   
                # if show:
                #     color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                #     iPos = (20, row * SQSIZE + SQSIZE // 2)
                #     fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                #     pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # \ diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:   # not equal to 0 means it is not empty 
            # if show:
            #     color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
            #     iPos = (20, 20)
            #     fPos = (WIDTH - 20, HEIGHT - 20)
            #     pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # / diagonal win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            # if show:
            #     color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
            #     iPos = (20, HEIGHT - 20)
            #     fPos = (WIDTH - 20, 20)
            #     pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]
        
        # no win
        return 0

class AI:
    def __init__(self,level=1, player=2):   # default player is player 2
        self.level = level
        self.player = player

    def random_move(self,board):
        empty_sqrs = board.get_empty_sqrs() # get all the list of empty squares in the board
        index = random.randrange(0,len(empty_sqrs))

        return empty_sqrs[index]    # row, col

    # ai is going to minimize if maximize is false
    # ai is player 2
    def minimax(self,board,maximize):
        
        # check terminal case
        case = board.final_state()

        # p1 wins
        if case == 1:
            return 1, None  # eval, move
        
        # p2 wins
        # since ai is minimizing ai must return -1
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximize:
            max_eval = -1000
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            # loop each empty square
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)   # deep copy board so that main board will not be modified
                temp_board.mark_sqr(row,col,1)    # make move; 1 is p1
                eval = self.minimax(temp_board,False)[0]   # recursion part; True is the player move; 0 is the case 1,-1,0
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        #
        elif not maximize:
            min_eval = 1000
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            # loop each empty square
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)   # deep copy board so that main board will not be modified
                temp_board.mark_sqr(row,col,self.player)    # make move; self.player is ai 
                eval = self.minimax(temp_board,True)[0]   # recursion part; True is the player move; 0 is the case 1,-1,0
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.random_move(main_board) # row col
        else:
            # minmax algo
            eval, move = self.minimax(main_board,False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai'   # pvp or ai
        self.running = True # If game over, set to False
        self.show_lines()

    # create the lines of tic tac toe
    def show_lines(self):
        # vertical
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(WIDTH - SQSIZE,0),(WIDTH -SQSIZE, HEIGHT), LINE_WIDTH)

        #horizonal
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT - SQSIZE),(WIDTH,HEIGHT -SQSIZE), LINE_WIDTH)

    def draw_fig(self,row,col):
        if self.player == 1:
            # draw cross
            pos1 = (col * SQSIZE + OFFSET,row * SQSIZE + OFFSET)
            pos2 = (col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + SQSIZE - OFFSET)

            pos3 = (col * SQSIZE + OFFSET,row * SQSIZE + SQSIZE - OFFSET)
            pos4 = (col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + OFFSET)

            pygame.draw.line(screen,CROSS_COLOR,pos1,pos2, CROSS_WIDTH)
            pygame.draw.line(screen,CROSS_COLOR,pos3,pos4, CROSS_WIDTH)
            pass
        elif self.player == 2:
            # draw circle
            center = (col * SQSIZE + SQSIZE//2,row *SQSIZE + SQSIZE//2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    # change players
    def next_turn(self):
        self.player = self.player % 2 + 1



def main():
    # game object
    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            # check mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:

                # gets the equivalent position in the table self.squares
                pos = event.pos
                row = pos[1]//SQSIZE
                col = pos[0]//SQSIZE

                if board.empty_sqr(row,col):
                    board.mark_sqr(row,col,game.player)
                    game.draw_fig(row,col)
                    game.next_turn()
                    #print(board.squares)

        if game.gamemode == 'ai' and game.player == ai.player:
            # update screen
            pygame.display.update()  

            # ai functions
            row, col = ai.eval(board)

            board.mark_sqr(row,col,game.player)
            game.draw_fig(row,col)
            game.next_turn()



        pygame.display.update()  


main()