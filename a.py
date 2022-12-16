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
        self.squares = np.zeros((ROWS,COLS))
    
    def mark_sqr(self,row,col,player):
        self.squares[row][col] = player

    def empty_sqr(self,row,col):
        return self.squares[row][col] == 0
class Game:
    def __init__(self):
        self.board = Board()
        self.player = 1
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