'''
Joshua V. Esguerra
170 - WX3L
MinMax Algorithm


Reference:
https://github.com/AlejoG10/python-tictactoe-ai-yt
'''

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
    def final_state(self, show=False):
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]

        # horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        # desc diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # asc diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, CROSS_WIDTH)
            return self.squares[1][1]

        # no win yet
        return 0

class AI:
    def __init__(self, player=2,level=1):   # default player is player 2
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
        # checks current state of the board if match to a final_state
        case = board.final_state()

        # p1 wins
        # if maximizing return 1
        if case == 1:
            return 1, None  # eval, move
        
        # p2 wins
        # since ai is minimizing ai must return -1
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        # starts here if ai is player number 1
        if maximize:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            # loop each empty square
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)   # deep copy board so that main board will not be modified
                #if self.player == 2:
                temp_board.mark_sqr(row,col,1)    # make move; 1 is p1
                # else:
                #     temp_board.mark_sqr(row,col,2)
                eval = self.minimax(temp_board, False)[0]   # recursion part; True is the player move; 0 is the case 1,-1,0
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        # starts here if ai is player number 2
        elif not maximize:
            min_eval = 1000
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            # loop each empty square
            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)   # deep copy board so that main board will not be modified
                # if self.player == 2:
                temp_board.mark_sqr(row,col,self.player)    # make move; self.player is ai 
                # else:
                #     temp_board.mark_sqr(row,col,1) 
                # switches to the max
                eval = self.minimax(temp_board, True)[0]   # recursion part; True is the player move; 0 is the case 1,-1,0
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
            #if self.player == 2:
            eval, move = self.minimax(main_board,False)
            # else:
            #     eval, move = self.minimax(main_board,True)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')
        return move

class Game:
    def __init__(self,player,ai_player):
        self.board = Board()
        self.ai = AI()
        self.player = player
        self.gamemode = 'ai'   # pvp or ai
        self.running = True # If game over, set to False
        self.show_lines()
        self.ai_player = ai_player

    # create the lines of tic tac toe
    def show_lines(self):
        # to clear initial screen
        screen.fill(BG_COLOR)
        # vertical
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(WIDTH - SQSIZE,0),(WIDTH -SQSIZE, HEIGHT), LINE_WIDTH)

        #horizonal
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT - SQSIZE),(WIDTH,HEIGHT -SQSIZE), LINE_WIDTH)

    def draw_fig(self,row,col):
        if self.ai_player == 1:
            if self.player == 2:
                # draw cross
                pos1 = (col * SQSIZE + OFFSET,row * SQSIZE + OFFSET)
                pos2 = (col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + SQSIZE - OFFSET)

                pos3 = (col * SQSIZE + OFFSET,row * SQSIZE + SQSIZE - OFFSET)
                pos4 = (col * SQSIZE + SQSIZE - OFFSET,row * SQSIZE + OFFSET)

                pygame.draw.line(screen,CROSS_COLOR,pos1,pos2, CROSS_WIDTH)
                pygame.draw.line(screen,CROSS_COLOR,pos3,pos4, CROSS_WIDTH)
                pass
            elif self.player == 1:
                # draw circle
                center = (col * SQSIZE + SQSIZE//2,row *SQSIZE + SQSIZE//2)
                pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
        else:
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

    # if ai will make turn first
    # make player 2 then 1
    # def next_turn_user(self):
    #     self.player =  2
    
    # def next_turn_ai(self):
    #     self.player =  1
    
    # change game mode
    def change_gamemode(self):
        if self.gamemode == 'pvp':
            self.gamemode = 'ai'
        else:
            self.gamemode = 'pvp'

    def reset(self):
        self.__init__()

    def isdone(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()



def main():
    # get input from user
    player_number = input("Player 1 or Player 2? Choose [1] or [2]\n")
    pnum = int(player_number)
    if pnum == 2:
        ai_num = 1
    else:
        ai_num = 0
    # game object
    game = Game(pnum,ai_num)
    #game = Game()
    board = game.board
    ai = game.ai

    run = 0
    first = 0


    while True:
        #if int(player_number) == 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # G - gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()
                
                # choose ai level
                # Press - 0
                if event.key == pygame.K_0:
                    ai.level = 0
                # Press - 1
                if event.key == pygame.K_1:
                    ai.level = 1

                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

            # check mouse event
            if event.type == pygame.MOUSEBUTTONDOWN:

                # gets the equivalent position in the table self.squares
                pos = event.pos
                row = pos[1]//SQSIZE
                col = pos[0]//SQSIZE

                if board.empty_sqr(row,col) and game.running:
                    # make move
                    # board.mark_sqr(row,col,game.player)
                    # game.draw_fig(row,col)
                    # game.next_turn()
                    game.move(row, col)

                    print(game.board)
                    
                    # check if game is done to prevent errors
                    if game.isdone():
                        game.running = False

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            # update screen
            pygame.display.update()  

            # ai functions
            row, col = ai.eval(board)

            # make move
            # board.mark_sqr(row,col,ai.player)
            # game.draw_fig(row,col)
            # game.next_turn()
            game.move(row, col)
            

            # check if game is done to prevent errors
            if game.isdone():
                game.running = False

        pygame.display.update()  

main()