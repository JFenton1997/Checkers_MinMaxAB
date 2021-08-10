import random #random to run random number gen check to proc mistake
from copy import deepcopy #deep copy used to copy entire object as new object, and not by reference

from .constants import *


class Minimax: 

    def __init__(self): #base constructor
        self.p_count = 0
        self.se_Count = 0
        self.de_count = 0
        self.random_error_chance=0

    def run_evaluation(self, game, depth,max_player, min_player, random_error_chance = 0): #run evaluation, game obj, depth to do, random_error_chance, for error to occur
        print("\n"+ str(COLOR.str(max_player))+ " is THINKING......")
        self.p_count = 0 #for evaluating the search
        self.se_count = 0
        self.de_count = 0
        self.random_error_chance =random_error_chance 
        board = game.board #get current board
        value, best_move = self._minimax(board, depth, True, max_player, min_player, game, float('-inf'), float('inf')) #run minimax (start with max player), alpha and beta values at end
        print("se_count = " +str(self.se_count))
        print("de_count = " +str(self.de_count))
        print("p_count = " +str(self.p_count))
        print("MOVE: " + str(best_move[1]))
        return value, best_move

    def _minimax(self, board, depth, is_max_player, max_player, min_player, game, alpha, beta):
        if depth == 0 or board.winner() != None: #if winner or end of tree depth return score with no best move
            self.se_count +=1           
            return board.evaluate(max_player), (board,None)
        self.de_count += 1
        if is_max_player: #if max player
            best_score = float('-inf') 
            best_move = None 
            moves =self._get_all_moves(board,max_player) #get all possible moves
            if not moves: #if no moves are returned, then end and return current board (player cant move)
                board.forfeit(max_player) #make player forfeit
                return board.evaluate(max_player), (board,None)
            for move in moves: #for each move found
                current_score = self._minimax(move[0], depth-1, False,max_player, min_player,game,alpha,beta)[0] #run minimax for min player and get score
                current_score = self._random_error_check(current_score) #check for error proc, changing score
                best_score = max(best_score, current_score) #compare score and update
                if best_score == current_score: #if new score 
                    best_move = move #update best to move currently being checked
                alpha = max(current_score, alpha) #update alpha
                if alpha >= beta: #prune 
                    self.p_count += 1
                    break
            return best_score, best_move #return score and best_move


        else:
            best_score = float('inf') #exactly same for min player
            best_move = None
            moves = self._get_all_moves(board,min_player)
            if not moves:
                board.forfeit(min_player)               
                return board.evaluate(max_player), (board,None)
            for move in moves:
                current_score = self._minimax(move[0], depth-1, True,max_player,min_player, game, alpha, beta)[0] #run minimax for max player
                current_score = self._random_error_check(current_score)
                best_score = min(best_score, current_score)
                if best_score == current_score:
                    best_move = move
                beta = min(current_score,beta)
                if alpha >= beta:
                    self.p_count += 1
                    break
            return best_score, best_move






    def _simulate_move(self,piece, move, board, skip): #update board, running move given
        board.move(piece, move[0], move[1]) #row , col
        if skip: #if piece been jumped 
            board.remove(skip, piece)
        return board

    def _get_all_moves(self,board, color): #get all possible moves from a board for player
        moves = []
        all_valid_moves = board.update_valid_moves(color) #get all moves from board
        for piece,valid_moves in all_valid_moves.items(): #for each moves {Piece : move} 
            for move, skip in valid_moves.items(): #for each move valid_moves = {new pos: [skipped]}
                temp_board = deepcopy(board) #create a new object which is a exact copy of the current board (not assigned by reference but by value )
                temp_piece = temp_board.get_piece(piece.row, piece.col) #get piece to be moved on new copy board
                new_board = self._simulate_move(temp_piece,move, temp_board, skip) #simulate move and return new board outcome
                moves.append((new_board, (piece,move,skip))) #add to moves 
        return moves

    def _random_error_check(self,evaluation_value): #check for random error
        if self.random_error_chance == 0: #if 0, just return correct value
            return evaluation_value
        rand_val = random.randint(1,100) #get a value between 1 and 100
        if rand_val <= self.random_error_chance: #if proc chance given is less than random value
            return random.randint(-200,200) #evaluation value (current_score) becomes a random value between -200 and 200 (simulating major misjudgment)
        else: 
            return evaluation_value #return normal move
