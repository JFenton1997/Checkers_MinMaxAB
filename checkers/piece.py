import pygame
from .constants import *

class Piece: #piece class constructor
    def __init__(self,row,col,color, king = False):
        self.row = row
        self.col = col
        self.color = color
        self.king = king
        self.x = 0
        self.y = 0
        self.get_window_pos() #cal pos to draw on window


    def get_window_pos(self): #get exact position on win to draw piece
        self.x = (SQUARE_SIZE * self.col + SQUARE_SIZE//2) + BOARD_BORDER_WIDTH+BOARD_START_X
        self.y = (SQUARE_SIZE * self.row + SQUARE_SIZE//2) + BOARD_BORDER_HEIGHT+BOARD_START_Y

    def make_king(self): #make self king 
        self.king = True

    def draw(self,win): #draw piece

        pygame.draw.circle(win,COLOR.GREY,(self.x,self.y),PIECE_RADIUS + PIECE_BORDER) #border outline
        pygame.draw.circle(win,self.color,(self.x,self.y),PIECE_RADIUS) #border fill

        pygame.draw.circle(win,COLOR.GREY,(self.x,self.y),PIECE_RADIUS/2 + PIECE_BORDER) #inner circle outline
        pygame.draw.circle(win,self.color,(self.x,self.y),PIECE_RADIUS/2) #inner circle

        if self.king: #if king add image of a crown on top of the piece
            win.blit(IMG_CROWN, (self.x- IMG_CROWN.get_width()//2, self.y - IMG_CROWN.get_height() //2 ))

    def draw_highlight(self,win,color): #draw a highlight around the piece (circle)
        pygame.draw.circle(win, color, (self.x,self.y),PIECE_HIGHLIGHT_OFFSET,PIECE_HIGHLIGHT_THICKNESS)# size, thickness

    

    def move(self,row,col): #move, update stored pos of piece
        self.row = row
        self.col = col
        self.get_window_pos()
    
    def __repr__(self): #to string method, for debugging
        return str("[" + str(self.row) + ":" + str(self.col)  + "]=> " +COLOR.str(self.color) + " K:" +str(self.king))