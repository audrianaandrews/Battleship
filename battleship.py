import sys
import os
import random
import time
from board import Board
from computerAI import ComputerAI
import copy

class Battleship(object):
    '''Game of Battleship.'''

    def __init__(self):
        '''(Battleship) -> None
        Battleship constructor.'''

        self.board_size = 0
        self.fits_ships = False
        self.not_attacked = False
        self.mode = ""
        self.board1 = None
        self.board2 = None

    def play(self):
        print("Welcome to Battleship\n")

        self.want_instructions()
        self.clear_screen()

        print("Welcome to Battleship\n")

        print("These are the game modes available:\n")
        print("h: for Human vs Human \nc: for Easy Computer vs Human")
        print("a: for Hard Computer vs Human")
        self.choose_mode()

        self.choose_board_size()
        print("\n")

        print("These are the ships available:\n")
        self.print_ships_available()
        print("\n")

        while self.fits_ships == False:
            self.board1.aircraft = self.num_of_ships("aircraft carriers")
            self.board2.aircraft = self.board1.aircraft

            self.board1.battleship = self.num_of_ships("battleships")
            self.board2.battleship = self.board1.battleship

            self.board1.submarine = self.num_of_ships("submarines")
            self.board2.submarine = self.board1.submarine

            self.board1.patrol = self.num_of_ships("patrol boats")
            self.board2.patrol = self.board1.patrol

            if self.board1.aircraft == 0 and self.board2.submarine == 0 and \
               self.board2.patrol == 0\
               and self.board2.battleship == 0:
                print("You must enter at least one for one of the type of",)
                print("ships.")
                print("\n")
            else:
                self.place_ships(self.board1)
                self.place_ships(self.board2)

                if self.fits_ships == False:
                    print("The board can't fit your ships.",)
                    print("Please choose a different amount.\n")

        if self.mode == "h":
            while self.board1.done == False and self.board2.done == False:
                self.clear_screen()
                if self.board1.turn_over == True:
                    self.human_move("Player 1", self.board1, \
                                                self.board2)
                elif self.board2.turn_over == True:
                    self.human_move("Player 2", self.board2, \
                                                self.board1)

        elif self.mode == "c":
            while self.board1.done == False and self.board2.done == False:
                if self.board1.turn_over == True:
                    self.clear_screen()
                    self.human_move("Player 1", self.board1, self.board2)
                elif self.board2.turn_over == True:
                    while self.not_attacked == False:
                        row = random.randint(0, (self.board_size - 1))
                        column = random.randint(0, (self.board_size - 1))
                        if self.board2.shots_taken[row][column] == " ":
                            self.not_attacked = True
                    self.board2.check_if_hit(row, column, self.board1, \
                                                 'The computer')
                    self.not_attacked = False
                    if self.board2.done == True:
                        self.clear_screen()
                        self.board2.display_board()
                        print("The computer won...")
                        self.board1.turn_over = False
                        self.board1.done == True
                    else:
                        self.board2.turn_over = False
                        self.board1.turn_over = True
        else:
            computer = ComputerAI(self.board2, self.board1)
            while self.board1.done == False and self.board2.done == False:
                if self.board1.turn_over == True:
                    self.clear_screen()
                    self.human_move("Player 1", self.board1, self.board2)
                elif self.board2.turn_over == True:
                    computer.computer_move()
                    computer.not_attacked = False
                    if self.board2.done == True:
                        self.clear_screen()
                        self.board2.display_board()
                        print("The computer won...")
                        self.board1.turn_over = False
                        self.board1.done == True
                    else:
                        self.board2.turn_over = False
                        self.board1.turn_over = True
                pass

    def want_instructions(self):
        '''(Battlefield)->None
        Asks user if they want to see instructions for game.'''

        try:
            instruct = \
                input("Would you like to see the instructions(y or n)? ")
            print("\n")
            if instruct == "y" or instruct == "n":
                if instruct == "y":
                    instructions = open("instructions.txt")
                    for line in instructions:
                        print(line,)
                    input("\n\nPress Enter to continue.")
                else:
                    pass
            else:
                raise Exception
        except Exception:
            self.instructions()

    def human_move(self, player, player_board, other_board):
        '''(Battleship, str, Board, Board) -> None
        Take user's input, input into Board dictionaries and display updated
        game board to screen. Then check to see if player has won.'''

        print("Enemy's board | %s's board:\n" % (player))
        player_board.display_board()
        try:
            row, column = input("Please enter coordinates (y x):").split()
            player_board.check_if_hit(row, column, other_board, player)
        except Exception:
            player_board.check_if_hit('b', 'a', player_board, player)
        self.clear_screen()
        print("Enemy's board | %s's board\n" % (player))
        player_board.display_board()

        if player_board.done == True:
            self.clear_screen()
            player_board.display_board()
            print(player + " Wins!")
            other_board.turn_over = False
            other_board.done == True
        else:
            player_board.turn_over = False
            other_board.turn_over = True
        pass

    def choose_mode(self):
        '''(Battlefield) -> None
        Take user's input to decide which version of game to play.'''

        try:
            self.mode = input("Please choose a mode to play: ")
            if self.mode == "h" or self.mode == "c" or self.mode == "a":
                pass
            else:
                raise Exception
        except Exception:
            self.choose_mode()

    def choose_board_size(self):
        '''(Battlefield) -> None
        Take user input to decide size of gameboard.'''

        try:
            self.board_size = \
                int(input("\nPlease enter the size of board: "))
            if self.board_size < 2 or \
               (isinstance(self.board_size, int) == False):
                raise Exception
            else:
                self.board1 = Board(self.board_size)
                self.board1.create_board()
                self.board2 = Board(self.board_size)
                self.board2.create_board()
        except Exception:
                print("Please enter a number greater than 1.")
                self.choose_board_size()

    def print_ships_available(self):
        '''(Battlefield) -> str
        Print to the screen the types of ships and their lengths.'''

        ships_available = [("Type", "Size"), \
                          ("aircraft carrier", "5"),\
                          ("battleship", "4"),\
                          ("submarine", "3"),\
                          ("patrol boat", "2")]

        for x, y in ships_available:
            length_x = len(ships_available[1][0])
            length_y = len(ships_available[0][1])

            sys.stdout.write("[" + x + (" " * (length_x - len(x))) + "]")
            sys.stdout.write("[" + y + (" " * (length_y - len(y))) + "]\n")

    def num_of_ships(self, ship_type):
        '''(Battlefield, str) -> int
        Take user input to assign int to a variable that decides how many of a
        ship the user will have.'''

        try:
            amount = input("Please enter the amount of %s you'd like: " \
                               % (ship_type))
            amount = int(amount)
            amount += 0
            return amount
        except Exception:
            print("Please enter a number.")
            amount = self.num_of_ships(ship_type)
            return amount

    def place_ships(self, board):
        '''(Battlefield, Board) -> None
        Randomly assign player ships.'''

        board.backup_board = copy.deepcopy(board.whole_board)
        sys.setrecursionlimit(1000)
        try:
            for ship in range(board.aircraft):
                board.place_ships(5)

            for ship in range(board.battleship):
                board.place_ships(4)

            for ship in range(board.submarine):
                board.place_ships(3)

            for ship in range(board.patrol):
                board.place_ships(2)
            self.fits_ships = True
        except RuntimeError:
            board.whole_board = copy.deepcopy(board.backup_board)
            self.fits_ships = False

    def clear_screen(self):
        '''Clear python screen.'''

        print("\n")
        time.sleep(1.5)
        if os.name == "posix":
        # Unix/Linux/MacOS/BSD/etc
            os.system('clear')
        elif os.name in ("nt", "dos", "ce"):
        # DOS/Windows
            os.system('CLS')
        pass


def play_again():
    '''(None) -> str
    Take user input and return str to determine if user will play game again.
    '''

    try:
        replay = input("Would you like to play again?(y or n): ")
        if replay == "y" or replay == "n":
            return replay
        else:
            raise Exception
    except Exception:
        print("Please enter y or n.")
        play_again()
        return replay

if __name__ == "__main__":
    replay = "y"
    while replay == "y":
        battleship = Battleship()
        battleship.clear_screen()
        battleship.play()
        print("\n")
        replay = play_again()
