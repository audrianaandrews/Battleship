import random
import sys
import os


class Board(object):
    '''Create board for Battlefield game.'''

    def __init__(self, board_size):
        '''(Board, int) -> None
        Board constructor.'''

        self.board_size = board_size
        self.whole_board = {}
        self.backup_board = {}
        self.done = False
        self.player_ships = {}
        self.shots_taken = {}
        self.ship_number = 1
        self.square_size = " " * (len(str(self.board_size - 1)))
        self.row_order = []
        self.turn_over = True

        self.aircraft = 0
        self.battleship = 0
        self.submarine = 0
        self.patrol = 0

    def create_board(self):
        '''(Board) -> None
        Create user board in two dictionaries self.whole_board and
        self.shots_taken.'''

        board = []

        for y in range(self.board_size):
            board.append(str(y))
        self.whole_board[self.square_size] = board
        self.shots_taken[self.square_size] = board
        self.row_order.append(self.square_size)

        for x in range(self.board_size):
            self.whole_board[x] = []
            self.shots_taken[x] = []
            self.row_order.append(x)
            for j in range(self.board_size):
                self.whole_board[x].append(self.square_size)
                self.shots_taken[x].append(self.square_size)

    def display_board(self):
        '''(Board) -> None
        Print dictionaries self.shots_taken and self.whole_board to screen as
        the game board.'''

        s = ""

        for key in self.row_order:
            s += "[" + str(key) + (" " * (len(self.square_size) - \
                                         len(str(key)))) + "]"

            for row in self.shots_taken[key]:
                s += "[" + row + (" " * (len(str(self.board_size - 1)) - \
                                         (len(row)))) + "]"

            s += "\t[" + str(key) + (" " * (len(self.square_size) - \
                                           len(str(key)))) + "]"

            for row in self.whole_board[key]:
                s += "[" + row + (" " * (len(str(self.board_size - 1)) - \
                                         (len(row)))) + "]"

            sys.stdout.write(s + "\n")
            sys.stdout.flush()
            s = ""

    def place_ships(self, ship_size):
        '''(Board, int) -> Nonetype
        Randomly place ships in dictionary self.whole_board.'''

        buttons_made = 0
        L = ["vertical", "horizontal"]
        random.shuffle(L)
        row = random.randint(0, (self.board_size - 1))
        column = random.randint(0, (self.board_size - 1))

        self.player_ships[self.ship_number] = []

        #place ship in a column
        if L[0] == "vertical":
            for y in range(ship_size):
                try:
                    if self.whole_board[row][column] != self.square_size:
                        raise IndexError
                    else:
                        if y == 0:
                            self.whole_board[row][column] = "^"
                        elif y == (ship_size - 1):
                            self.whole_board[row][column] = "v"
                        else:
                            self.whole_board[row][column] = "*"
                        self.player_ships[self.ship_number].\
                            append((row, column))
                        buttons_made += 1
                        row += 1
                        if row == self.board_size:
                            raise IndexError
                except IndexError:
                    if buttons_made == 1:
                        self.whole_board[row - buttons_made][column] = \
                            self.square_size
                    else:
                        for but in range(1, buttons_made + 1):
                            self.whole_board[row - but][column] = \
                                self.square_size
                    self.place_ships(ship_size)
                    return

        #place ship in a row
        else:
            for y in range(ship_size):
                try:
                    if self.whole_board[row][column] != self.square_size:
                        raise IndexError
                    else:
                        if y == 0:
                            self.whole_board[row][column] = "<"
                        elif y == (ship_size - 1):
                            self.whole_board[row][column] = ">"
                        else:
                            self.whole_board[row][column] = "*"
                        self.player_ships[self.ship_number].\
                            append((row, column))
                        buttons_made += 1
                        column += 1
                except IndexError:
                    if buttons_made == 1:
                        self.whole_board[row][(column) - buttons_made] = \
                            self.square_size
                    else:
                        for but in range(1, buttons_made + 1):
                            self.whole_board[row][(column) - but] = \
                                self.square_size
                    self.place_ships(ship_size)
                    return
        self.ship_number += 1

    def check_if_hit(self, row, column, other_player, player):
        '''(int, int, Board, str) -> Nonetype
        Input str row and int column as indexes in self.whole_board to see if
        space is occupied by other player's ship.'''

        try:
            column = int(column)
            row = int(row)
            if self.shots_taken[row][column] != self.square_size:
                print("You've already attacked this spot.")
                raise Exception
            user_entry = (row, column)
            ships = other_player.player_ships.keys()
            for ship in ships:
                ship_coordinates = other_player.player_ships[ship]
                for coordinates in ship_coordinates:
                    if user_entry == coordinates:
                        self.shots_taken[row][column] = \
                            other_player.whole_board[row][column]
                        other_player.whole_board[row][column] = "H"
                        ship_coordinates.remove(coordinates)
                        if ship_coordinates == []:
                            del other_player.player_ships[ship]
                            ships_left = len(other_player.player_ships.keys())
                            if ships_left > 0:
                                print(player + " has sunk a ship, only", \
                                  ships_left, "to go!")
                                print("\n")
                            if other_player.player_ships == {}:
                                self.done = True
                        return
            self.shots_taken[row][column] = "M"
            other_player.whole_board[row][column] = "M"
            return
        except Exception:
            try:
                row, column = input("Please enter valid coordinates: ").\
                    split()
                self.check_if_hit(row, column, other_player, player)
            except Exception:
                self.check_if_hit('a', 'b', other_player, player)
        pass

if __name__ == "__main__":
    pass
