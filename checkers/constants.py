import pygame

#CONSTANTS - used thoughout the game code
#feel free to play around with these to change some settings


WIDTH, HEIGHT = 1000,1200 #width and height of created window

#Not implement properly, aimed to scale game based on changable window size
BASED_WIDTH,BASED_HEIGHT= 1000,1200 
HEIGHT_RATIO = BASED_HEIGHT/HEIGHT
WIDTH_RATIO = BASED_WIDTH/WIDTH
MEAN_RATIO = 1 
MAX_ROWS, MAX_COLS = 8,8

#depth of minimax for user hint
HINT_DEPTH = 3

#cap on ai depth limit, prevent game freezing to unplayable means, tho can be higher
AI_DEPTH_LIMIT = 10  
AI_DELAY = 100 #delay between moves for ai vs ai

#piece draw settings
PIECE_PADDING = 20 * MEAN_RATIO 
PIECE_BORDER = 2 * MEAN_RATIO

#padding above and below the board on screen
BOARD_Y_PADDING = 50 * MEAN_RATIO

#size of the gold border of the board
BOARD_BORDER_WIDTH =10 * MEAN_RATIO
BOARD_BORDER_HEIGHT =10 * MEAN_RATIO

#start of the padding, aka where on Y to draw the board
BOARD_Y_PADDING_START = 200 *MEAN_RATIO

#where does the border of the board starts Y
BOARD_START_Y = BOARD_Y_PADDING_START+BOARD_Y_PADDING

#where does the board start on the X
BOARD_START_X = 50 * MEAN_RATIO

#total size of each square in the board
SQUARE_SIZE =(WIDTH- (BOARD_BORDER_WIDTH*2)-(BOARD_START_X*2))//MAX_COLS

#the X and Y top left of the board inside the gold border
BOARD_START_INSIDE_X = BOARD_START_X+BOARD_BORDER_WIDTH
BOARD_START_INSIDE_Y = BOARD_START_Y+BOARD_BORDER_HEIGHT




#the X and Y of the bottom right of the board boarder
BOARD_END_Y = SQUARE_SIZE*MAX_ROWS+(2*BOARD_BORDER_HEIGHT)+BOARD_START_Y
BOARD_END_X = SQUARE_SIZE*MAX_COLS+(2*BOARD_BORDER_WIDTH)+BOARD_START_X

#the X and Y of the bottom right of the board, inside corner of the border
BOARD_END_INSIDE_X = BOARD_END_X-BOARD_BORDER_WIDTH
BOARD_END_INSIDE_Y = BOARD_END_Y-BOARD_BORDER_HEIGHT

#padding under the board border
BOARD_Y_PADDING_END = BOARD_END_Y+BOARD_Y_PADDING

#total size of the board
BOARD_SIZE_Y = BOARD_END_Y-BOARD_START_Y
BOARD_SIZE_X = BOARD_END_X-BOARD_START_X

#piece cosmetic values 
PIECE_RADIUS = SQUARE_SIZE//2 - PIECE_PADDING
PIECE_PADDING = 20 * MEAN_RATIO
PIECE_BORDER = 2 * MEAN_RATIO
PIECE_HIGHLIGHT_OFFSET = (15 * MEAN_RATIO)+ PIECE_RADIUS
PIECE_HIGHLIGHT_THICKNESS = int( 5* MEAN_RATIO)

#show move size
BOARD_DOT_SIZE = 15 * MEAN_RATIO


#color enum (ish). Color RED and White are also used as player values
class COLOR():
    RED = (220,20,0)
    BOARD_RED = (190,40,0)
    BLUE = (0,70,255)
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    GREY = (200,200,200)
    GREEN = (40,200,0)
    YELLOW = (255,190,0)
    DARK_GREY = (90,90,90)
    CYAN = (10,200,200)
    ORANGE = (200,100,10)

    def str(color): #to string to display the name of the color for displaying players
        if color ==COLOR.RED:
            return "RED"
        elif color == COLOR.WHITE:
            return "WHITE"
        else:
            return "NOT PLAYER"
        

        


#location of the crown image used by kings
IMG_CROWN =  pygame.transform.scale(pygame.image.load('checkers/assets/crown.png'),(45,25))