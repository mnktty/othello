#!/usr/bin/env python

__author__ = 'mnktty'


"""An othello play environment. Written in simplest possible Python to make it
understandable to a 14 year old. 

The board is organized as a 8x8 list of lists. Positions are taken as - row,
column - from stdin. 
"""

EMPTY, WHITE, BLACK = '.', 'W', 'B'     # positions

def withinBoard(r, c):
    """ Check if a r, c position falls within the board
    >>> withinBoard(2, 2)
    True
    >>> withinBoard(0, 2)
    False
    >>> withinBoard(8, 8)
    True
    >>> withinBoard(8, 9)
    False
    >>> withinBoard(1, 1)
    True
    """
    return (r in range(1, 9) and c in range(1, 9))

def neighbours(r, c):
    """Get valid neighbour squares for a given co-ordinate. Any neighbour within
    the Euclidean distance is valid
    
    >>> neighbours(1, 2)
    [(1, 1), (1, 3), (2, 1), (2, 2), (2, 3)]
    >>> neighbours(8, 8)
    [(7, 7), (7, 8), (8, 7)]
    >>> neighbours(1, 1)
    [(1, 2), (2, 1), (2, 2)]
    >>> neighbours(3, 3)
    [(2, 2), (2, 3), (2, 4), (3, 2), (3, 4), (4, 2), (4, 3), (4, 4)]

    """
    neighbours = [(r-1, c-1), (r-1, c), (r-1, c+1),
                  (r, c-1), (r, c+1),
                  (r+1, c-1), (r+1, c), (r+1, c+1)]
    # filter out neighbours that are outside the board - e.g. in case of (8,8)
    neighbours = [(r, c) for (r, c) in neighbours if withinBoard(r, c)]
    return neighbours

def rightRow(r, c):
    """
    >>> rightRow(5, 4)
    [(5, 4), (5, 5), (5, 6), (5, 7), (5, 8)]
    """
    x = [r, ] * (9-c)
    y = range(c, 9)
    return zip(x, y)

def leftRow(r, c):
    """
    >>> leftRow(5, 4)
    [(5, 4), (5, 3), (5, 2), (5, 1)]
    """
    x = [r, ] * c
    y = range(c, 0, -1)
    return zip(x, y)

def upperColumn(r, c):
    """
    >>> upperColumn(5, 4)
    [(5, 4), (4, 4), (3, 4), (2, 4), (1, 4)]
    >>> upperColumn(6, 4)
    [(6, 4), (5, 4), (4, 4), (3, 4), (2, 4), (1, 4)]
    
    """
    x = range(r, 0, -1)
    y = [c, ] * r
    return zip(x, y)

def lowerColumn(r, c):
    """
    >>> lowerColumn(5, 4)
    [(5, 4), (6, 4), (7, 4), (8, 4)]
    """
    x = range(r, 9)
    y = [c, ] * (9-r)
    return zip(x, y)

def upperSlash(r, c):
    """
    >>> upperSlash(6 ,3)
    [(6, 3), (7, 2), (8, 1)]
    >>> upperSlash(3, 4)
    [(3, 4), (4, 3), (5, 2), (6, 1)]
    >>> upperSlash(2, 2)
    [(2, 2), (3, 1)]
    >>> upperSlash(1, 1)
    [(1, 1)]
    >>> upperSlash(8, 8)
    [(8, 8)]
    >>> upperSlash(1, 8)
    [(1, 8), (2, 7), (3, 6), (4, 5), (5, 4), (6, 3), (7, 2), (8, 1)]
    """
    upper_x = range(r, 9, 1)
    upper_y = range(c, 0, -1)
    return zip(upper_x, upper_y)

def lowerSlash(r, c):
    """
    >>> lowerSlash(6 ,3)
    [(6, 3), (5, 4), (4, 5), (3, 6), (2, 7), (1, 8)]
    >>> lowerSlash(3, 4)
    [(3, 4), (2, 5), (1, 6)]
    >>> lowerSlash(2, 2)
    [(2, 2), (1, 3)]
    >>> lowerSlash(1, 1)
    [(1, 1)]
    >>> lowerSlash(8, 8)
    [(8, 8)]
    >>> lowerSlash(1, 8)
    [(1, 8)]
    """
    lower_x = range(r, 0, -1)
    lower_y = range(c, 9, 1)
    return zip(lower_x, lower_y)

def upperBackslash(r, c):
    """
    >>> upperBackslash(6, 3)
    [(6, 3), (5, 2), (4, 1)]
    >>> upperBackslash(2, 2)
    [(2, 2), (1, 1)]
    >>> upperBackslash(1, 8)
    [(1, 8)]
    >>> upperBackslash(1, 1)
    [(1, 1)]
    """
    upper_x = range(r, 0, -1)
    upper_y = range(c, 0, -1)
    return zip(upper_x, upper_y)
    
def lowerBackslash(r, c):
    """
    >>> lowerBackslash(6, 3)
    [(6, 3), (7, 4), (8, 5)]
    >>> lowerBackslash(2, 2)
    [(2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]
    >>> lowerBackslash(1, 8)
    [(1, 8)]
    >>> lowerBackslash(1, 1)
    [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8)]
    """
    lower_x = range(r, 9, 1)
    lower_y = range(c, 9, 1)
    return zip(lower_x, lower_y)


class Board:
    def __init__(self, player = 'B'):
        """Setup 8 X 8 board. Each position is called a square. Center squares
        are B and W"""
        self.layout = [['0', '1', '2', '3', '4', '5', '6', '7', '8'],
                       ['1', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['2', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['3', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['4', '.', '.', '.', 'B', 'W', '.', '.', '.'],
                       ['5', '.', '.', '.', 'W', 'B', '.', '.', '.'],
                       ['6', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['7', '.', '.', '.', '.', '.', '.', '.', '.'],
                       ['8', '.', '.', '.', '.', '.', '.', '.', '.']]

        self.player = player            # first player by default is black

    def show(self):
        "Show the board"
        for row in self.layout:
            print ' '.join(row)
        print 'OTHELLO: Player {0}, please play your move - as r, c'.format(self.player)

    def flipPlayer(self, whites = 0, blacks = 0):
        "Adjust scores and give turn to other player"
        # TODO: adjust scores
        self.player = 'W' if self.player == 'B' else 'B'

    def isEmpty(self, r, c):
        "Check if a position is empty or not"
        return self.layout[r][c] == EMPTY

    def canPlayAt(self, r, c):
        """A position can be played ONLY if it is within the board, is empty,
        and if a neighbour is filled.
        
        >>> b = Board()
        >>> b.canPlayAt(4, 3)
        True
        >>> b.canPlayAt(6, 4)
        True
        >>> b.canPlayAt(6, 2)
        False
        
        """
        if (withinBoard(r, c) and not self.isEmpty(r, c)):
            return False
        ns = neighbours(r, c)
        # Get status of neighbours - filled or not. At least one should be
        # filled
        filled = [not self.isEmpty(x, y) for (x, y) in ns]
        return True in filled

    def truncateToBound(self, seq):
        """Truncate sequence lengths to co-ordinates is bounded by the current
        player's pieces. If a row, column or diagonal is fed to this function,
        it assumes the first entry to be played square, finds the square which
        is the farthest this player's piece and truncates it at that point
        """
        end = 0
        for (x, y) in seq:
            if self.layout[x][y] == EMPTY: # empty field,
                break                      # no point in continuing
            elif self.layout[x][y] == self.player:
                end = seq.index((x, y)) # bound reached
        return seq[:end] if end else []

    def longestSequence(self, r, c):
        """Figure out the longest sequence of squares (among rows, columns and
        diagonals) which are bounded by the current player's pieces, on current
        insertion.
        """
        sequences = [leftRow(r, c), rightRow(r, c),
                     upperColumn(r, c), lowerColumn(r, c),
                     upperSlash(r, c), lowerSlash(r, c),
                     upperBackslash(r, c), lowerBackslash(r, c)]
        sequences = [self.truncateToBound(s) for s in sequences]
        sizes = [len(s) for s in sequences]
        longest = max(sizes)
        return sequences[sizes.index(longest)]

    def flip(self, r, c):
        """Insert at square, flip squares based on this insertion, change counts
        for each player and give turn to other player"""
        self.layout[r][c] = self.player # actual insertion

        # flip squares along longest bound
        for (x, y) in self.longestSequence(r, c):
            self.layout[x][y] = self.player
            
        self.flipPlayer();
        self.show()                     # do not forget to print the board
        
class Othello:
    def __init__(self):
        self.board = Board()
        self.board.show()

    def accept(self):
        "Accept square position as r, c co-ordinate from player"
        spec = raw_input().split(',')
        return spec
    
    def validate(self):
        while(True):
            try:
                r, c = self.accept()
                r, c = int(r), int(c)
                if not (r in range(9) and c in range(9)):
                    print "Invalid input, enter again"
                    continue
                else:
                    return r, c
            except(ValueError):
                print "Invalid input, enter again"
                continue

    def play(self):
        try:
            while (True):
                r, c = self.validate()
                if not self.board.canPlayAt(r, c):
                    continue
                self.board.flip(r, c)
        except KeyboardInterrupt:
            print "OTHELLO: Aborting game, goodbye"


def playOthello():
    oc = Othello()
    oc.play()


if __name__ == '__main__':
    import doctest
    # enable this to unit test all code
    # doctest.testmod()
    playOthello()

# eof
