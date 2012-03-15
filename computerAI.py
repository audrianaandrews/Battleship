from queue import Queue
import random


class ComputerAI(object):
    '''Harder version of Computer player that does more than attack
    randomly.'''

    def __init__(self, board, other_board):
        '''(ComputerAI, Board, Board) -> None
        ComputerAI constructor.'''

        self.west = None
        self.east = None
        self.north = None
        self.south = None
        self.board = board
        self.other_board = other_board
        self.move = None
        self.miss = False
        self.not_attacked = False
        self.north_end = False
        self.south_end = False
        self.west_end = False
        self.east_end = False
        self.vertical_queue = Queue()
        self.horizontal_queue = Queue()
        pass

    def computer_move(self):
        '''(ComputerAI) -> None
        Determine where computer player will attack the game board.'''

        '''if there are items in queue self.vertical_queue, dequeue each item
        for every turn the computer has'''
        if not self.vertical_queue.is_empty():
            while (self.north_end == False or self.south_end == False) and \
                  self.miss == False:
                value = self.vertical_queue.dequeue()
                if self.board.shots_taken[value[0]][value[1]] == \
                   self.board.square_size:
                    self.board.check_if_hit(value[0], value[1], \
                                            self.other_board, 'The computer')
                    if self.board.shots_taken[value[0]][value[1]] == "^":
                        '''If move made by computer reveals that the top or
                        bottom of a ship is in a column, set boolean self.north
                        or boolean self.south to True. If move made by computer
                        reveals that it nothing was in space then boolean
                        self.miss will be set to True.'''
                        self.north_end = True
                        if self.south_end == True:
                            self.move = None
                    elif self.board.shots_taken[value[0]][value[1]] == "v":
                        self.south_end = True
                        if self.north_end == True:
                            self.move = None
                    elif self.board.shots_taken[value[0]][value[1]] == "M":
                        self.miss = True
                    else:
                        return
                else:
                    pass
            self.north_end = False
            self.south_end = False
            self.miss = False
            self.vertical_queue = Queue()
        elif not self.horizontal_queue.is_empty():
            '''if there are items in queue self.horizontal_queue, dequeue each
            item for every turn the computer has'''
            while (self.west_end == False or self.east_end == False) and \
                  self.miss == False:
                value = self.horizontal_queue.dequeue()
                if self.board.shots_taken[value[0]][value[1]] == \
                   self.board.square_size:
                    '''If move made by computer reveals that the left or right
                    of a ship is in a column, set boolean self.west or boolean
                    self.east to True. If move made by computer reveals that it
                    nothing was in space then boolean self.miss will be set to
                    True.'''
                    self.board.check_if_hit(value[0], value[1], \
                                            self.other_board, 'The computer')
                    if self.board.shots_taken[value[0]][value[1]] == "<":
                        self.west_end = True
                        if self.east_end == True:
                            self.move = None
                    elif self.board.shots_taken[value[0]][value[1]] == ">":
                        self.east_end = True
                        if self.west_end == True:
                            self.move = None
                    elif self.board.shots_taken[value[0]][value[1]] == "M":
                        self.miss = True
                    else:
                        return
                else:
                    pass
            self.west_end = False
            self.east_end = False
            self.miss = False
            self.horizontal_queue = Queue()
        elif self.move == None:
            #if no random move has been assigned to self.move
            while self.not_attacked == False:
                #choose random coordinates for the computer to attack
                row = random.randint(0, (self.board.board_size - 1))
                column = random.randint(0, (self.board.board_size - 1))
                if self.board.shots_taken[row][column] == \
                   self.board.square_size:
                    self.not_attacked = True
            self.board.check_if_hit(row, column, self.other_board, \
                                    'The computer')
            self.move = (row, column)
            ''''If random coordinate is the end of a ship a queue is created
            leading away from ship part. If it's not an end, a coordinate is
            created one square away in each direction from the random
            coordinate.'''
            if self.board.shots_taken[row][column] == "^":
                self.north_end = True
                self.create_queue(row, column, "south")
            elif self.board.shots_taken[row][column] == "v":
                self.south_end = True
                self.create_queue(row, column, "north")
            elif self.board.shots_taken[row][column] == "<":
                self.west_end = True
                self.create_queue(row, column, "east")
            elif self.board.shots_taken[row][column] == ">":
                self.east_end = True
                self.create_queue(row, column, "west")
            elif self.board.shots_taken[row][column] == "*":
                self.create_coordinates(row, column)
        #if self.move is not either end of a ship
        elif self.board.shots_taken[self.move[0]][self.move[1]] == "*":
            '''Check if coordinate to north, south, east, west has been
            created. If one has been created and it is the end of a ship , the
            respective boolean variable is set to True. Otherwise a queue is
            created going in that direction, then that coordinate is set to
            None.'''
            if self.north != None:
                self.board.check_if_hit(self.north[0], self.north[1], \
                                        self.other_board, 'The computer')
                if self.board.shots_taken[self.north[0]][self.north[1]] == "^":
                    self.north_end = True
                elif self.board.shots_taken[self.north[0]][self.north[1]] == \
                     "M":
                    pass
                else:
                    self.create_queue(self.north[0], self.north[1], "north")
                self.north = None
            elif self.south != None:
                self.board.check_if_hit(self.south[0], self.south[1], \
                                        self.other_board, 'The computer')
                if self.board.shots_taken[self.south[0]][self.south[1]] == "v":
                    self.south_end = True
                elif self.board.shots_taken[self.south[0]][self.south[1]] == \
                     "M":
                    pass
                else:
                    self.create_queue(self.south[0], self.south[1], "south")
                self.south = None
            elif self.east != None:
                self.board.check_if_hit(self.east[0], self.east[1], \
                                        self.other_board, 'The computer')
                if self.board.shots_taken[self.east[0]][self.east[1]] == ">":
                    self.east_end = True
                elif self.board.shots_taken[self.east[0]][self.east[1]] == "M":
                    pass
                else:
                    self.create_queue(self.east[0], self.east[1], "east")
                self.east = None
            elif self.west != None:
                self.board.check_if_hit(self.west[0], self.west[1], \
                                        self.other_board, 'The computer')
                if self.board.shots_taken[self.west[0]][self.west[1]] == "<":
                    self.west_end = True
                elif self.board.shots_taken[self.west[0]][self.west[1]] == "M":
                    pass
                else:
                    self.create_queue(self.west[0], self.west[1], "west")
                self.west = None
            else:
                self.move = None
                self.computer_move()
        else:
            self.move = None
            self.north_end = False
            self.south_end = False
            self.west_end = False
            self.east_end = False
            self.miss = False
            self.computer_move()

    def create_queue(self, row, column, direction):
        '''(ComputerAI, int, int, str) -> None
        Add to values to queues heading in the direction given in str
        direction.'''

        if direction == 'south':
            for x in range(row + 1, self.board.board_size):
                self.vertical_queue.enqueue((x, column))
        elif direction == 'north':
            x = row - 1
            while x >= 0:
                self.vertical_queue.enqueue((x, column))
                x -= 1
        elif direction == 'east':
            for x in range(column + 1, self.board.board_size):
                self.horizontal_queue.enqueue((row, x))
        elif direction == 'west':
            x = column - 1
            while x >= 0:
                self.horizontal_queue.enqueue((row, x))
                x -= 1
        pass

    def create_coordinates(self, row, column):
        '''(ComputerAI, int, int) -> None
        Create coordinates to the north, south, east and west of the coordinate
        given by int row and int column.'''

        if (row + 1) < self.board.board_size:
            if self.board.shots_taken[row + 1][column] == \
                   self.board.square_size:
                self.south = (row + 1, column)
            else:
                pass
        if (row - 1) >= 0:
            if self.board.shots_taken[row - 1][column] == \
                               self.board.square_size:
                self.north = (row - 1, column)
            else:
                pass
        if (column + 1) < self.board.board_size:
            if self.board.shots_taken[row][column + 1] == \
                               self.board.square_size:
                self.east = (row, column + 1)
        if (column - 1) >= 0:
            if self.board.shots_taken[row][column - 1] == \
                               self.board.square_size:
                self.west = (row, column - 1)
            else:
                pass
