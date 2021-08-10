from checkers.game import Game #import classes from checkers to run
import pygame #import pygame
from checkers.constants import *
from checkers.game import Game
from checkers.menu import *

from checkers.minimax import Minimax

FPS = 60 #setting frame rate of clock ticks

WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #Create game window
pygame.display.set_caption('Minimax')

def get_row_col_from_mouse(pos): #Utility method to get the mouse pos if the mouse is located inside the board, and return the clicked row and col
    x, y = pos
    if x >= BOARD_START_INSIDE_X and x <= BOARD_END_INSIDE_X and y >= BOARD_START_INSIDE_Y and y <= BOARD_END_INSIDE_Y: #if inside board
        row = (y-BOARD_START_INSIDE_Y)//SQUARE_SIZE 
        col = (x-BOARD_START_INSIDE_X)//SQUARE_SIZE
        # print((row, col)) 
        return int(row), int(col) #return coords (casted as ints preventing bug, floor div returning a float)
    return -1, -1 #if click wasnt in board


def game_loop(game, minimax, options): #runs the entire sequence
    ai_depth,ai_random_error,red_start,red_ai  = options # get options to be used
    if red_start: #set starting player
        start_player = COLOR.RED
    else:
        start_player = COLOR.WHITE
    game.new_game(start_player) #create new game
    game.update_valid_moves() #get all valid moves for next player (only need to be run once at turn start)
    while True:
        if game.turn == COLOR.WHITE: #white always Minimax
            if red_ai: #add delay if its two AI, allowing the user to observe the game
                pygame.time.delay(AI_DELAY) 
            value, move = minimax.run_evaluation( 
                game, ai_depth, COLOR.WHITE, COLOR.RED, ai_random_error)
                #run evaluation, returning final evaluation value and move = board, move                
            if move: #if move found
                try:
                    game.set_last_move(move[1]) #show move on board
                    game.ai_move(move[0]) #update board to include move
                    game.update_valid_moves() #update valid moves for the next player
                except: # [FIXED] when only a board is returned and not a move, so move[1] breaks, normally caused from no possible move in forfeit position  - here for debug
                    print("INVALID RETURNED MOVE BUG")
        
        if game.winner() != None: #check for winner after move, if so end game
            break

        if game.turn == COLOR.RED and red_ai: #same logic as white, this only runs if red is to Minimax as well
            pygame.time.delay(AI_DELAY) 
            value, move = minimax.run_evaluation(
            game, ai_depth, COLOR.RED, COLOR.WHITE, ai_random_error)
            if move:
                try:
                    game.set_last_move(move[1])
                    game.ai_move(move[0])
                    game.update_valid_moves()
                except:
                    print("INVALID RETURNED MOVE BUG")
                    game.board.forfeit(game.turn)
            
        if game.winner() != None:
            break

        for event in pygame.event.get(): #user control loop 
            if event.type == pygame.QUIT: #close game if quit is press (x  on game window)
                return False
            if not red_ai: #if red is human player
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #on left click

                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    if row != -1 and col != -1: # if click in board, run select. -1,-1 is used insted of just a check since 0,0 is a col and row
                        game.select(row, col)

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: #on right click, deselect
                    game.deselect()

            game.check_events(event) #run button checks in game class

        game.game_play_update() #run game update which handles drawing
    #print(game.board.winner()) # if winner
    #print(COLOR.str(game.board.winner()))
    run = game.winner_window() #display winner window
    return run




def main(): #program start
    run = True #run game while true
    pygame.font.init() #initialise font module of pygame
    clock = pygame.time.Clock() #get game clock
    minimax = Minimax() #initialise classes
    game = Game(WIN, minimax)
    menu = Menu(WIN)

    while run: 
        clock.tick(FPS) #tick clock per iteration
        for event in pygame.event.get(): #check for quit
            if event.type == pygame.QUIT:
                run = False
        # Menu loop
        run , options= menu.menu_loop() #run menu loop (display main menu), options are return to pass to game
        

        # Game loop
        if run: 
            run = game_loop(game, minimax, options) #run game loop once menu loop stopped

    pygame.quit() #exit game


main() #run main
