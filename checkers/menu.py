from checkers.button import Button #imports
from checkers.constants import *
import pygame #import pygame
import functools #functools used to pass methods with paramters to objects 
class Menu:

    def __init__(self, win): #constructor
        self.title_font = pygame.font.SysFont("Ariel", 50) #set fonts
        self.font = pygame.font.SysFont("Ariel", 34)
        self.win = win
        self.ai_depth =3 #initial option values
        self.ai_random_error = 5
        self.red_ai = False 
        self.red_start = True
        self.game_start = False
        self.build_buttons() #run constructors for buttons
        

      

    def build_buttons(self): #build buttons, => (text, location, font size,color, function to run on click )
        #dec depth
        self.dec_depth = Button(
        "- ",
        (BOARD_START_INSIDE_X+20, BOARD_START_INSIDE_Y + 50),
        30,
        COLOR.BOARD_RED,
        func= functools.partial(self.change_ai_depth,-1))

        #inc depth
        self.inc_depth = Button(
        "+",
        (BOARD_START_INSIDE_X+120, BOARD_START_INSIDE_Y + 50),
        30,
        COLOR.GREEN,
        func= functools.partial(self.change_ai_depth,1))

        #ai random error  dec 
        self.ai_error_dec = Button(
        "- ",
        (BOARD_START_INSIDE_X+210, BOARD_START_INSIDE_Y + 50),
        30,
        COLOR.BOARD_RED,
        func= functools.partial(self.change_ai_error,-1))

        #ai random error inc
        self.ai_error_inc = Button(
        "+",
        (BOARD_START_INSIDE_X+330, BOARD_START_INSIDE_Y + 50),
        30,
        COLOR.GREEN,
        func= functools.partial(self.change_ai_error,1))

        #toggle for starting player
        self.toggle_start_player = Button(
        "     TOGGLE     ",
        (BOARD_START_INSIDE_X+440, BOARD_START_INSIDE_Y + 50),
        30,
        COLOR.RED,
        func= functools.partial(self.change_red_start))

        #toggle for red Minmax player
        self.toggle_red_ai = Button(
        "     TOGGLE     ",
        (BOARD_START_INSIDE_X+690, BOARD_START_INSIDE_Y + 50),
        30,
        COLOR.RED,
        func= functools.partial(self.change_red_ai))

        #start game button
        self.start_game_but = Button(
        "     START GAME     ",
        (WIDTH//2-150, BOARD_START_INSIDE_Y + 150),
        30,
        COLOR.BOARD_RED,
        func= functools.partial(self.start_game))

    #start game
    def start_game(self):
        self.game_start = True


    #change starting player, on click, flip value and change color of button accordingly
    def change_red_start(self):
        button = self.toggle_start_player
        if self.red_start:
            self.red_start = False
            button.change_color(COLOR.GREY)
        else:
            self.red_start = True
            button.change_color(COLOR.RED)

      #change red minimax player, on click, flip value and change color of button accordingly  
    def change_red_ai(self):
        button = self.toggle_red_ai
        if self.red_ai:
            self.red_ai = False
            button.change_color(COLOR.RED)
        else:
            self.red_ai = True
            button.change_color(COLOR.GREEN)


    #change ai_depth option by value, within a range 
    def change_ai_depth(self,value):
            self.ai_depth += value
            self.ai_depth = min(self.ai_depth, AI_DEPTH_LIMIT)
            self.ai_depth = max(1, self.ai_depth)

    #change ai_error option by value, within a range 
    def change_ai_error(self,value):
        self.ai_random_error += value
        self.ai_random_error = min(self.ai_random_error, 100)
        self.ai_random_error = max(0, self.ai_random_error)

    #run draw on each button
    def draw_buttons(self):
        self.inc_depth.draw(self.win)
        self.dec_depth.draw(self.win)
        self.ai_error_inc.draw(self.win)
        self.ai_error_dec.draw(self.win)
        self.toggle_start_player.draw(self.win)
        self.toggle_red_ai.draw(self.win)
        self.start_game_but.draw(self.win)

    #run click on each button
    def check_button_click(self,event):
        self.inc_depth.click(event)
        self.dec_depth.click(event)
        self.ai_error_inc.click(event)
        self.ai_error_dec.click(event)
        self.toggle_start_player.click(event)
        self.toggle_red_ai.click(event)
        self.start_game_but.click(event)


    #draw entire menu (uses a lot of code from board)
    def draw_menu(self):
        self.win.fill(COLOR.BLACK)
        pygame.draw.rect(self.win,COLOR.GREY,(0,0,WIDTH,BOARD_Y_PADDING_START))
        pygame.draw.rect(self.win,COLOR.YELLOW,(BOARD_START_X,BOARD_START_Y,BOARD_SIZE_X,BOARD_SIZE_Y))


        pygame.draw.rect(self.win,COLOR.DARK_GREY,(BOARD_BORDER_WIDTH+BOARD_START_X,BOARD_BORDER_HEIGHT+BOARD_START_Y, SQUARE_SIZE*MAX_COLS,SQUARE_SIZE*MAX_ROWS))
        for row in range(MAX_ROWS):
            for col in range(row % 2, MAX_COLS, 2):#x,y, size W, size H
                pygame.draw.rect(self.win,COLOR.GREY,((row*SQUARE_SIZE)+BOARD_START_X+BOARD_BORDER_WIDTH,BOARD_START_Y+(col*SQUARE_SIZE)+BOARD_BORDER_WIDTH,SQUARE_SIZE,SQUARE_SIZE))
        self.draw_buttons() #draw buttons
 
        

        self.text_ui() #draw text
        pygame.display.update() #update display

    #draw all text, text works by creating a surface object containing text, then drawing the surface to the window using blit (works similar to draw)
    #taking =>  blit(surface, (x,y))
    def text_ui(self):
        #title text
        title_label = self.title_font.render("MINIMAX CHECKERS GAME", 50, COLOR.BLACK)  
        tile_rect = title_label.get_rect() 
        self.win.blit(title_label, (WIDTH/2 - (tile_rect.width/2), 50))
        
        #depth text
        depth_label = self.font.render("AI DEPTH", 20, COLOR.BLACK)
        self.win.blit(depth_label, (BOARD_START_INSIDE_X+20,BOARD_START_INSIDE_Y + 20))
        #depth value
        depth_count = self.title_font.render(str(self.ai_depth), 20, COLOR.BLACK)
        self.win.blit(depth_count, (BOARD_START_INSIDE_X+55,BOARD_START_INSIDE_Y + 55))

        #error text
        error_label = self.font.render("AI ERROR", 20, COLOR.BLACK)
        self.win.blit(error_label, (BOARD_START_INSIDE_X+220,BOARD_START_INSIDE_Y + 20))
        #error value
        error_count = self.title_font.render(str(self.ai_random_error) + "%", 20, COLOR.BLACK)
        self.win.blit(error_count, (BOARD_START_INSIDE_X+245,BOARD_START_INSIDE_Y + 55))

        #start turn text
        start_label = self.font.render("STARTING COLOR", 20, COLOR.BLACK)
        self.win.blit(start_label, (BOARD_START_INSIDE_X+420,BOARD_START_INSIDE_Y + 20))

        #red ai text
        red_ai_label = self.font.render("AI RED(Green=on)", 20, COLOR.BLACK)
        self.win.blit(red_ai_label, (BOARD_START_INSIDE_X+670,BOARD_START_INSIDE_Y + 20))

    #menu loop, run until quit or game start
    def menu_loop(self):     
        self.game_start = False   
        while not self.game_start:
            self.draw_menu() #draw menu
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False, None #return to main loop to exit program
                self.check_button_click(event) #check all buttons for click
        return True, (self.ai_depth,self.ai_random_error,self.red_start,self.red_ai ) #return (run) and options
