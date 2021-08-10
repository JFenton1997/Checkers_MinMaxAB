import pygame #import pygame
from pygame import constants
from .constants import *
from .piece import Piece

class Board: 
    def __init__(self): #board constructor, set up starting values
        self.board = []
        self.red_left = 12
        self.white_left = 12
        self.red_kings = 0
        self.white_kings = 0
        self.create_board() #create board
    

    #Drawing the board on the window
    def draw_squares(self, win):
        win.fill(COLOR.BLACK)
        pygame.draw.rect(win,COLOR.GREY,(0,0,WIDTH,BOARD_Y_PADDING_START)) #using constants to cal location of rects to create gui
        pygame.draw.rect(win,COLOR.YELLOW,(BOARD_START_X,BOARD_START_Y,BOARD_SIZE_X,BOARD_SIZE_Y))
        pygame.draw.rect(win,COLOR.BLACK,(BOARD_BORDER_WIDTH+BOARD_START_X,BOARD_BORDER_HEIGHT+BOARD_START_Y, SQUARE_SIZE*MAX_COLS,SQUARE_SIZE*MAX_ROWS))
        for row in range(MAX_ROWS):
            for col in range(row % 2, MAX_COLS, 2):#alternate red per col based on row % 2, thus row 1 = col 1,3,5,7 and row 2 = col 0,2,4,6
                pygame.draw.rect(win,COLOR.BOARD_RED,((row*SQUARE_SIZE)+BOARD_START_X+BOARD_BORDER_WIDTH,BOARD_START_Y+(col*SQUARE_SIZE)+BOARD_BORDER_WIDTH,SQUARE_SIZE,SQUARE_SIZE))

    def evaluate(self, max_player): #Heuristic evaluation function
        if max_player == COLOR.WHITE: #if white
            eval = self.white_left- self.red_left + self.white_kings *0.7 - self.red_kings* 0.5 #base score on piece and king delta to other player
            for piece in self.get_all_pieces(COLOR.WHITE): #for all white pieces
                if not piece.king: #if not king
                    eval+= piece.row * 0.01 #promote movement toward row 7 => to king
                    if piece.row == 0: #if on own base row, promote staying, to defend
                        eval+= 0.06
                else:  #if king
                    for op_piece in self.get_all_pieces(COLOR.RED):#get all opponent pieces
                        row_diff = abs(piece.row - op_piece.row) #delta row 
                        col_diff = abs(piece.col - op_piece.col) #delta col
                        eval += 0.01 - 0.01 * (row_diff +col_diff) #gain up to 0.01 propositional to distance to opponent pieces > promote attacking once a king
        else:
            eval = self.red_left- self.white_left + self.red_kings *0.7 - self.white_kings* 0.5 #same as white but for red 
            for piece in self.get_all_pieces(COLOR.RED):
                if not piece.king:
                    eval+= (7-piece.row) * 0.01 #so 7-row num instead
                    if piece.row == 7:
                        eval+= 0.06
                else: 
                    for op_piece in self.get_all_pieces(COLOR.WHITE):
                        row_diff = abs(piece.row - op_piece.row)
                        col_diff = abs(piece.col - op_piece.col)
                        eval += 0.01 - 0.01 * (row_diff +col_diff)

        return eval



    def get_all_pieces(self, color): #get all pieces for given player
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece) 
        return pieces #return list of pieces

    def move(self, piece,row,col):#swap position with position
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col] ,self.board[piece.row][piece.col] # old, new = new ,old  (quick swap in python)
        piece.move(row,col) #run move in piece, updating its pos it stored
        if row == MAX_ROWS-1 or row ==0: #if on base line
            if not piece.king: #not a king
                piece.make_king() #make king
                if piece.color == COLOR.WHITE:#change count
                    self.white_kings +=1
                else:
                    self.red_kings +=1

    def get_piece(self,row,col): #get piece from row and col
            return self.board[row][col] 


    def create_board(self):# using a 2D array to create the board [ROW][COL]
        for row in range(MAX_ROWS): #for each row
            self.board.append([]) #each list is a col
            for col in range(MAX_COLS): #for each col
                if col % 2 == ((row +1)%2): # per row, the col will shift. col 1 will hit row 0,2,4 and col2 will hit 1,3,5 ect 
                    if row < 3: #if top 3 rows
                        self.board[row].append (Piece(row= row, col= col, color=COLOR.WHITE)) #add white piece
                        
                    elif row> 4:
                        self.board[row].append (Piece(row= row, col= col, color=COLOR.RED ))  #add red piece
                    else:
                        self.board[row].append(0) #if not piece location, add '0', the empty representation in the state space
                else:
                    self.board[row].append(0) #if not piece location, add '0', the empty representation in the state space

    def draw(self,win): #draw the board, win
        self.draw_squares(win)  #draw squares 
        for row in range(MAX_ROWS): #draw pieces, for each row
            for col in range(MAX_COLS): #for col
                piece = self.board[row][col] #run draw if no empty
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces, moved_piece):#remove pieces
        for piece in pieces: # for each piece to be remove (skipped)
            if piece != 0: #if not a null skip
                if piece.color == COLOR.RED: #remove piece from count
                    self.red_left -= 1
                if piece.color == COLOR.WHITE: 
                    self.white_left -=1

            if piece.king and not moved_piece.king:#might need update
                moved_piece.make_king()
                if piece.color == COLOR.WHITE:
                    self.red_kings +=1
                    self.white_kings -= 1

                else:
                    self.white_kings +=1
                    self.red_kings -=1
            else:
                if piece.color == COLOR.WHITE:
                    self.white_kings -= 1

                else:
                    self.red_kings -=1

                
            #set piece to 0, removing it from the board
            self.board[piece.row][piece.col] = 0
    
    def winner(self): #check for a winner, if there is, return winner
        if self.red_left <= 0:
            return COLOR.WHITE
        elif self.white_left <=0:
            return COLOR.RED
        else:
            return None

    def forfeit(self, turn): #called when no move or button click. make player lose 
        if turn == COLOR.RED:
            self.red_left = 0
        else:
            self.white_left = 0

    def update_valid_moves(self, turn): #get all possible moves
        pieces = self.get_all_pieces(turn) #for all pieces of current player (turn)
        all_attacking_moves = {} #store attacking moves - returned if any
        all_possible_moves = {} #store possible 
        valid_moves={} 
        for piece in pieces:#for each piece 
            possible_moves = self.get_possible_piece_moves(piece) #get possible moves of piece
            if possible_moves: #if any
                possible_attacking_moves = {key: value for key, value in possible_moves.items() if value} #for each possible move returned, add all moves which a skipped value (attacking)
                all_possible_moves[piece] = possible_moves #append possible moves to all possible moves, piece to be key
                if possible_attacking_moves: #if a possible attacking move found
                    all_attacking_moves[piece] = possible_attacking_moves #add to all_attacking moves
        if all_attacking_moves: #if all possible attacking moves contain a move, return attacking 
            valid_moves = all_attacking_moves
        else:
            valid_moves = all_possible_moves #else return all normal moves 
        return valid_moves
        
                 

    def get_possible_piece_moves(self, piece): #get all possible moves a piece
        moves = {}
        left = piece.col -1 #define left
        right = piece.col +1 #define right
        row = piece.row 

        if piece.color == COLOR.RED or piece.king: #check forward (+1 row movement )
            moves.update(self._traverse_left(row -1, max(row-3,-1),-1,piece.color,left))
            moves.update(self._traverse_right(row -1, max(row-3,-1),-1,piece.color,right))

        if piece.color == COLOR.WHITE or piece.king: #check back (-1 row movement )
            moves.update(self._traverse_left(row +1, min(row+3, MAX_ROWS),1,piece.color,left))
            moves.update(self._traverse_right(row +1, min(row+3,MAX_ROWS),1,piece.color,right))
        
        return moves #return all possible moves

    def _traverse_left(self,start, stop, step , color, left, skipped =[]): 
        moves = {}
        enemy_piece_visit = []
        for r in range(start,stop,step): #r = steps taken, eg from start 1, stop 3, step 1, r = 1,2,3
            if left < 0: #if hit left wall
                break
                
            current = self.board[r][left] #current is square currently looked at
            if current == 0: #if empty square (no piece)
                if skipped and not enemy_piece_visit: #true if after jump and local squares are empty (prevents jumps followed by a normal move)
                    break
                elif skipped: #if skipped, and has a visited piece 
                    moves[(r,left)] = enemy_piece_visit + skipped  #add skipped piece with piece visited (2nd or 3rd jump) with key of current
                else:
                    moves[(r,left)] = enemy_piece_visit  #add piece to skipped (1st jump)  with key of current
                
                if enemy_piece_visit: #if enemy been visited and looking at empty space 
                    if step == -1: #update row
                        row = max(r-3,0)
                    else:
                        row = min(r+3, MAX_ROWS)
                    #re run for next jump
                    moves.update(self._traverse_left(r+step,row,step,color,left-1,skipped=skipped + enemy_piece_visit)) 
                    moves.update(self._traverse_right(r+step,row,step,color,left+1,skipped=skipped + enemy_piece_visit))
                break
            elif current.color == color:
                break

            else: #if piece is opposing color, add to last
                    enemy_piece_visit = [current]

            left -= 1
        return moves

    def _traverse_right(self,start, stop, step , color, right, skipped =[]):# exact same as left for right 
        moves = {}
        enemy_piece_visit = []
        for r in range(start,stop,step):
            if right >= MAX_COLS:
                break
                
            current = self.board[r][right]
            if current == 0:
                if skipped and not enemy_piece_visit:
                    break
                elif skipped:
                    moves[(r,right)] = enemy_piece_visit + skipped
                else:
                    moves[(r,right)] = enemy_piece_visit
                
                if enemy_piece_visit:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3, MAX_ROWS)
                    
                    moves.update(self._traverse_left(r+step,row,step,color,right-1,skipped= skipped +enemy_piece_visit))
                    moves.update(self._traverse_right(r+step,row,step,color,right+1,skipped=skipped +enemy_piece_visit))
                break
            elif current.color == color:
                break

            else:
                enemy_piece_visit = [current]

            right += 1
        return moves