"""
                        TETRIS
This file implements all the basic functionality of the popular game named
tetris.

Available moves -
a - Move left
d - Move right
w - Rotate left
s - Rotate right
f - Fix the shape into the board
q - Quit the game inbetween


In each iteration a new shape appear on the top of the board. You can perform
multiple moves to roate the shape or move it to the lef or right. Once you
satisfy with the shape location you can fix it on the shape and next shape will
appear on the top of the board.

The game would be finish if the shape you have put on the borad do not fit on
on it.

"""
import os
import random


class Tetris(object):
    _shape = ('straight', 'square', 'n-shape',  'L-shape',  '7-shape')
    _shape_map = {
        _shape[0]: [[1,1,1,1]],
        _shape[1]: [[1,1],[1,1]],
        _shape[2]: [[0,1], [1,1], [1,0]],
        _shape[3]: [[1,0], [1,0], [1,1]],
        _shape[4]: [[0,1], [0,1], [1,1]]
    }
    _next_shape = None
    _board = []

    def __init__(self, board_size):
        """
        Intialize the class object with the given borad size.

        Args:
            board_size: Dimension of the borad.
        """
        self.board_size = board_size
        self.CreateBoard()

    def CreateBoard(self):
        """
        Intialize the borad with empty cells(i.e all zeros).
        """
        for i in range(self.board_size):
            self._board.append([])
            for j in range(self.board_size):
                if j == 0 or j == self.board_size-1 or i == self.board_size-1:
                    self._board[i].append(1)
                else:
                    self._board[i].append(0)

    def RenderBoard(self):
        """
        Renders the board as print '*' for filled cells and blank as empty
        cells
        """
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self._board[i][j] == 1:
                    print '*',
                else:
                    print ' ',
            print ''

    def GetNextshape(self):
        """
        Gets the next shape from the given shape at random basis, also fix
        its intial position on the board by setting the left. """
        self._next_shape = self._shape_map[self._shape[random.randint(0,len(self._shape)-1)]]
        width = Tetris.GetWidthOfShape(self._next_shape)
        self.left = (self.board_size - width)/2


    def ShowNextShape(self):
        """ shows the next shape on the top of the borad."""
        shape_length = len(self._next_shape)
        for i in range(shape_length):
            for j in range(self.left):
                print ' ',
            for k in self._next_shape[i]:
                if k == 1:
                    print '*',
                else:
                    print ' ',
            print ''


    def RotateLeft(self):
        """Rotates the shape to the left."""
        next_shape = map(lambda x: list(x),zip(*self._next_shape))[::-1]
        if Tetris.IsValid(self.board_size, self.left, next_shape):
            self._next_shape = next_shape



    def RotateRight(self):
        """Rotates the shape to the right."""
        next_shape = map(lambda x: list(x),zip(*self._next_shape[::-1]))
        if Tetris.IsValid(self.board_size, self.left, next_shape):
            self._next_shape = next_shape

    def MoveRight(self):
        """Move the shape one cell right from the current cell."""
        if Tetris.IsValid(self.board_size, self.left + 1, self._next_shape):
            self.left +=1



    def MoveLeft(self):
        """Move the shape one cell left from the current cell."""
        if Tetris.IsValid(self.board_size, self.left - 1, self._next_shape):
            self.left -=1



    def GetAppropriateRow(self):
        """
        Finds the first appropriate row that is a row contains the empty cells
        for the shape and returns.
        """
        width = Tetris.GetWidthOfShape(self._next_shape)
        height = len(self._next_shape)
        row_index = self.board_size - 1
        while(row_index >= height):
            sub_board = self._board[row_index - height:row_index]
            for i in range(len(self._next_shape)):
                if 2 in [x + y for x, y in zip(self._next_shape[i], sub_board[i][self.left:self.left+width])]:
                        break
            else:
                return row_index
            row_index -= 1
        return False



    def UpdateBoard(self):
        """ Merge the shape with the board."""
        width = Tetris.GetWidthOfShape(self._next_shape)
        row = self.GetAppropriateRow()
        if row:
            for shape_row in self._next_shape[::-1]:
                row -= 1
                self._board[row][self.left:self.left+width] = [x + y for x, y in zip(shape_row, self._board[row][self.left:self.left+width])]
            self.RenderBoard()
            return True
        else:
            return False


    def ChooseAction(self, input_str):
        action_map = {
                'a': self.MoveLeft,
                'd': self.MoveRight,
                'w': self.RotateLeft,
                's': self.RotateRight,
                'f': self.UpdateBoard
        }

        if input_str in action_map.keys():
            return action_map[input_str]


    @staticmethod
    def IsValid(board_size, left, shape):
        """
        Checks the move for valid move that is after performing the move
        shape should not go outside the borad. """
        width = Tetris.GetWidthOfShape(shape)
        if left <= board_size - width - 1 and left >= 1:
            return True
        return False

    @staticmethod
    def GetWidthOfShape(shape):
        """
        Returns no of columns in the shape.
        e.g.
            *
            *
            **
        for L-shape its width would be 2.
        """
        count = 0
        for i in zip(*shape):
            if sum(i) >= 1:
                count += 1
        return count


def main():
    tetris_obj = Tetris(12)
    next_move = None
    is_continue = True
    while True:
        tetris_obj.GetNextshape()
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print "\n\n\n**********************Tetris**********************\n\n\n"
            tetris_obj.ShowNextShape()
            print '\n\n'
            tetris_obj.RenderBoard()
            next_move = raw_input('Enter next move to change shape or f to fix - ')
            if next_move == 'q':
                break

            valid_move = tetris_obj.ChooseAction(next_move)

            if valid_move:
                is_continue = valid_move()

            if next_move == 'f':
                break
        if next_move == 'q':
            is_quit = raw_input('Do you want to quit. - ')
            if is_quit == 'y':
                print "Play Again!! BYE !!"
                break
        if not is_continue:
            print "Dude Your Game is Over!!!!!!"
            break


if __name__ == '__main__':
    main()

