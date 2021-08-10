from checkers.board import Board  # imports
import pygame
from .constants import *
from .board import Board
from .button import Button


class Game:  # constructor, (is only used to create a game object)
    def __init__(self, win, minimax):
        self.minimax = minimax
        self.win = win

    def _init(self, turn, red_ai):  # private method, initialise values for game start, obtained options

        #building buttons (similar to menu)
        self.hint_button = Button(
            "Get Hint",
            (BOARD_END_X-100, 40),
            30,
            COLOR.BOARD_RED,
            func=self.suggest_a_move)

        self.forfeit_button = Button(
            "Forfeit",
            (BOARD_END_X-100, 140),
            30,
            COLOR.BOARD_RED,
            func=self.forfeit)

        self.winner_button = Button(
            "Main Menu",
            (WIDTH//2 - WIDTH//6+60, HEIGHT//4 - HEIGHT//20+60,),
            30,
            COLOR.BOARD_RED,
            func=self.clicked_winner_popup)

        self.show_hint = False  # if show hint been pressed
        self.last_move = None  # last move taken to be shown
        self.font = pygame.font.SysFont("Ariel", 32)  # font to be used
        self.selected = None  # current user selected piece
        self.board = Board()  # new board object
        self.turn = turn  # track of whose turn it is
        self.valid_moves = {}  # dict of all moves {piece : moves{move : skipped }}
        self.turn_counter = 1  # turn number
        self.red_ai = red_ai
        self.clicked_winner_box = True

    def new_game(self, turn=COLOR.RED, red_ai=False):  # run private _init
        self._init(turn, red_ai)

    #run per game tick, used to draw most major elements of the gui

    def game_play_update(self):
        self.board.draw(self.win)  # draw board
        self.draw_ai_move()  # draw prev ai move
        if self.selected:  # if piece selected
            # draw valid moves of selected piece
            self.draw_valid_moves(self.valid_moves[self.selected])
        elif self.turn == COLOR.RED and not self.red_ai:  # if red and not ai and not selected
            for piece in self.valid_moves.keys():  # draw blue circle on all movable pieces
                piece.draw_highlight(self.win, COLOR.BLUE)
        self.text_ui()  # draw text
        if self.show_hint:  # if hint, draw hint
          self.draw_hint()
        if self.selected:  # if selected (checked again for layering)
            self.selected.draw_highlight(self.win, COLOR.YELLOW)
        if not self.clicked_winner_box:  # if game winner window to show, draw window with text and button
            pygame.draw.rect(self.win, COLOR.GREY, (WIDTH//2 - WIDTH //
                             6, HEIGHT//4 - HEIGHT//20, WIDTH//3, HEIGHT//10))
            winner_label = self.font.render(
                "WINNER: " + COLOR.str(self.board.winner()), 20, COLOR.BLACK)
            self.win.blit(winner_label, (WIDTH//2 - WIDTH //
                          6+60, HEIGHT//4 - HEIGHT//20+10,))
            self.winner_button.draw(self.win)
        # draw other buttons
        self.hint_button.draw(self.win)
        self.forfeit_button.draw(self.win)
        pygame.display.update()  # update display

    def forfeit(self):  # forfeit current player
        self.board.forfeit(self.turn)

    def clicked_winner_popup(self):  # close game winner window
        self.clicked_winner_box = True

    # run get all valid moves, if none possible, forfeit
    def update_valid_moves(self):
        self.valid_moves = self.board.update_valid_moves(self.turn)
        # force human to forfeit if no moves possible
        if not self.valid_moves and self.turn == COLOR.RED and not self.red_ai:
            self.board.forfeit(self.turn)

    def select(self, row, col):  # select piece from given row and col
        if self.selected:  # if a piece is already selected run move instead
            result = self._move(row, col)
            # if move unsuccessful unselect and recall self (select new piece if invalid coords was own other piece)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)  # get piece at coords
        if piece != 0 and piece in self.valid_moves.keys():  # if piece is in valid moves
            self.selected = piece  # make piece selected
            return True  # new piece selected
        return False  # no new piece selected

    def deselect(self):  # reset shows on right click
        self.selected = None
        self.show_hint = False

    def _move(self, row, col):  # private, move piece to row and col
        piece = self.board.get_piece(row, col)  # get piece row and col
        # if piece is 0 and valid move
        if self.selected and piece == 0 and (row, col) in self.valid_moves[self.selected]:
            self.board.move(self.selected, row, col)  # run move in board
            skipped = self.valid_moves[self.selected][(
                row, col)]  # if pieces skipped
            if skipped:
                # remove pieces skipped
                self.board.remove(skipped, self.selected)
            self.change_turn()  # change turn
        else:
            return False  # if invalid selection, false
        return True

    # for each move in moves. "moves" here is all the moves of the selected piece
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move  # draw a yellow dot in the position of the moves
            pygame.draw.circle(self.win, COLOR.YELLOW, ((col * SQUARE_SIZE + SQUARE_SIZE//2) + BOARD_BORDER_WIDTH +
                               BOARD_START_X, (row * SQUARE_SIZE + SQUARE_SIZE//2)+BOARD_BORDER_HEIGHT+BOARD_START_Y), BOARD_DOT_SIZE)

    def change_turn(self):  # change turn, and reset values required
        self.show_hint = False
        self.selected = None
        self.turn_counter += 1
        if self.turn == COLOR.RED:

            self.turn = COLOR.WHITE
        else:
            self.turn = COLOR.RED

        self.valid_moves = {}  # empty valid moves

    def winner(self):  # return board winner
        return self.board.winner()

    # called by main when winner, creates own loop until winner button is clicked
    def winner_window(self):
        self.clicked_winner_box = False
        while not self.clicked_winner_box:  # while not clicked
            for event in pygame.event.get():  # allow user to still exit
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # check for click
                    self.winner_button.click(event)
            self.game_play_update()  # this will draw the game and the game window on top
        return True

    def get_board(self):  # return board
        return self.board

    def ai_move(self, board):  # update board to the ai move board (board after 1 move)
        self.board = board
        self.change_turn()

    def check_events(self, event):  # check for button clicks, called by main
        self.hint_button.click(event)
        self.forfeit_button.click(event)

    def text_ui(self):  # draw text, similar to menu class implementation
        #title text
        title_label = self.font.render("MINMAX CHECKERS GAME", 20, COLOR.BLACK)
        tile_rect = title_label.get_rect()
        self.win.blit(title_label, (WIDTH/2 - (tile_rect.width/2), 10))

        #Turn Counter
        turn_label = self.font.render(
            "Turn No: " + str(self.turn_counter), 20, COLOR.BLACK)
        self.win.blit(turn_label, (BOARD_START_X, 10 + tile_rect.height))

        #current player
        current_player_label = self.font.render(
            "Current player: " + COLOR.str(self.turn), 20, COLOR.BLACK)
        self.win.blit(current_player_label,
                      (BOARD_START_X, 10 + tile_rect.height*2))

    #set last move to be displayed
    def set_last_move(self, last_move):
        self.last_move = last_move

    #draws the ai prev move using skipped, new pos (move) and origin

    def draw_ai_move(self):
        if self.last_move:  # if last move stored
            origin, move, skip = self.last_move
            # prevent taken crash when player takes the piece which just moved, as Current_loc will no longer be a piece object but int ( 0 )
            current_loc = self.board.get_piece(move[0], move[1])

            if current_loc:  # show last move color in the color of piece
                color = current_loc.color
                self.board.get_piece(move[0], move[1]).draw_highlight(
                    self.win, color)  # draw highlight on piece which just moved
            else:
                color = COLOR.ORANGE  # debug color rarely show. due to 2 frames of drawing the taken piece last moves, which is overwitten straight after the other players turns
            pygame.draw.circle(self.win, color, ((origin.col * SQUARE_SIZE + SQUARE_SIZE//2) + BOARD_BORDER_WIDTH +
                               BOARD_START_X, (origin.row * SQUARE_SIZE + SQUARE_SIZE//2)+BOARD_BORDER_HEIGHT+BOARD_START_Y), BOARD_DOT_SIZE)

            for skipped in skip:  # draw a small circle showing jumps
                pygame.draw.circle(self.win, color, ((skipped.col * SQUARE_SIZE + SQUARE_SIZE//2) + BOARD_BORDER_WIDTH+BOARD_START_X,
                                   (skipped.row * SQUARE_SIZE + SQUARE_SIZE//2)+BOARD_BORDER_HEIGHT+BOARD_START_Y), BOARD_DOT_SIZE/2)

    def suggest_a_move(self):  # on click, run minimax for player, and return the move value
        self.hint = self.minimax.run_evaluation(
            self, HINT_DEPTH, COLOR.RED, COLOR.WHITE)[1][1]
        self.show_hint = True

    def draw_hint(self):  # draws the hinted move onto the board, the piece to move circled in green
        piece, move, skip = self.hint  # green dot for move to
        piece.draw_highlight(self.win, COLOR.GREEN)
        pygame.draw.circle(self.win, COLOR.GREEN, ((move[1] * SQUARE_SIZE + SQUARE_SIZE//2) + BOARD_BORDER_WIDTH +
                           BOARD_START_X, (move[0] * SQUARE_SIZE + SQUARE_SIZE//2)+BOARD_BORDER_HEIGHT+BOARD_START_Y), BOARD_DOT_SIZE)
