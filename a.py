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
                if self.empty_sqr(row,col) == 0:
                    empty_sqrs.append((row,col))
        return empty_sqrs

    # return 0 if no one won yet
    # return 1 if p1 wins
    # return 2 if p2 wins
    def final_state(self):
        # vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:   # not equal to 0 means it is not empty   
                return self.squares[0][col]     # this is the player number
        
        # horizonal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][0] == self.squares[row][0] != 0:   # not equal to 0 means it is not empty   
                return self.squares[row][0]     # this is the player number

        # \ diagonal win
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:   # not equal to 0 means it is not empty 
            return self.squares[1][1]

        # / diagonal win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:   # not equal to 0 means it is not empty 
            return self.squares[1][1]
        
        # no win
        return 0


class Game:
    def __init__(self):
        self.board = Board()
        # self.ai = AI()
        self.player = 1
        self.gamemode = 'pvp'   # pvp or ai
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
                    print(board.squares)


        pygame.display.update()  


main()