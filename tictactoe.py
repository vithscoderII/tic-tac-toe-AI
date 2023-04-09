import pygame
import sys
import numpy as np
import random
import copy

from constant import *

# Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE')
screen.fill(BG_COLOR)

class PrintScreen:
    def __init__(self, name):
        self.name = name
        
class Board:
    def __init__(self):
        self.board = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.empty_sqrs = self.board
        self.marked_sqrs = 0

    def final_state(self, show=False):
        '''
            @return 0 if no win
            @return 1 if player 1 win
            @return 2 if player 2 win
        '''
        # verticle win
        for col in range(BOARD_COLS):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != 0:
                if show:
                    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    color = CIRCLE_COLOR if self.board[0][col] == 1 else CROSS_COLOR
                    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)
                return self.board[0][col]

        # horizontal win
        for row in range(BOARD_ROWS):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != 0:
                if show:
                    posY = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    color = CIRCLE_COLOR if self.board[row][0] == 1 else CROSS_COLOR
                    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)            
                return self.board[row][0]
            
        # desc diagonal win
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.board[1][1] == 1 else CROSS_COLOR
                    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)              
                return self.board[1][1]

        # asc diagonal win
        if self.board[2][0] == self.board[1][1] == self.board[0][2] != 0:
                if show:
                    color = CIRCLE_COLOR if self.board[1][1] == 1 else CROSS_COLOR
                    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)
                return self.board[1][1]            

        # no win
        return 0

    def mark_square(self, row, col, player):
        self.board[row][col] = player
        self.marked_sqrs += 1
    
    def avilable_square(self, row, col):
        return self.board[row][col] == 0
    
    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if self.avilable_square(row,col):
                    empty_sqrs.append((row, col))
        return empty_sqrs

    
    def isfull(self):
        return self.marked_sqrs == 9
    
    def isempty(self):
        return self.marked_sqrs == 0
        
class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def minmax(self, board, maximizing):
        # terminal cases
        case = board.final_state()

        # player 1
        if case == 1:
            return 1, None
        
        # player 2
        elif case == 2:
            return -1, None
        
        # draw
        elif board.isfull():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, 1)
                eval = self.minmax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            
            return max_eval, best_move
                
        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col, self.player)
                eval = self.minmax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
            
            return min_eval, best_move

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    def eval(self, main_board):
        if self.level == 0:
            # Random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # MinMax
            eval, move = self.minmax(main_board, False)
        
        print(f'AI has choosen to mark square pos at {move} with an evaluation of: {eval}')
        
        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1
        self.gamemode = 'ai' # pvp or ai
        self.running = True
        self.draw_lines()

    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_figure(row, col)
        self.next_turn()

    def draw_lines(self):
        screen.fill(BG_COLOR)
        # 1 horizontal line
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
        # 2 horizontal line
        pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
        # 1 vertical line
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
        # 2 vertical line
        pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    def next_turn(self):
        self.player = self.player % 2 + 1

    def draw_figure(self, row, col):
        if self.player == 1:
            #  draw circle
            pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            # draw cross
        elif self.player == 2:
            pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def restart(self):
        self.__init__()

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

def main():

    game = Game()
    board = game.board
    ai = game.ai

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # change game mode - g
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r - restart function
                if event.key == pygame.K_r:
                    game.restart()
                    board = game.board
                    ai = game.ai

                # 0 - random ai
                if event.key == pygame.K_0:
                    ai.level = 0

                # 1 - minmax ai
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX = event.pos[0] 
                mouseY = event.pos[1]

                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)

                if board.avilable_square(clicked_row, clicked_col) and game.running:
                    game.make_move(clicked_row, clicked_col)

                    if game.isover():
                        game.running = False

            if game.gamemode == 'ai' and game.player == ai.player and game.running:
                # update the screen
                pygame.display.update()

                # ai methood 
                row, col = ai.eval(board)
                game.make_move(row, col)

                if game.isover():
                    game.running = False
        
        pygame.display.update()

main()