import math
import random
import os
import curses
import time

BEST_SCORE_FILE_NAME = "best_score"

BOARD_WIDTH = 10
BOARD_HEIGHT = 20

GAME_WINDOW_WIDTH = 2 * BOARD_WIDTH + 2
GAME_WINDOW_HEIGHT = BOARD_HEIGHT + 2

HELP_WINDOW_WIDTH = 19
HELP_WINDOW_HEIGHT = 7

STATUS_WINDOW_HEIGHT = 12
STATUS_WINDOW_WIDTH = HELP_WINDOW_WIDTH

TITLE_HEIGHT = 6

LEFT_MARGIN = 3

TITLE_WIDTH = FOOTER_WIDTH = 50


block_shapes = [
    # T Block
    [[0, 1, 0],
     [1, 1, 1]],
    # L Block
    [[1, 0],
     [1, 0],
     [1, 1]],
    # S Block
    [[0, 1, 1],
     [1, 1, 0]],
    # O Block
    [[1, 1],
     [1, 1]],
    # I Block
    [[1], [1], [1], [1]]
]

# def draw_non_tetris_title():
#     curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
#     curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLACK)
#     curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)
#     curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
#     curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
#     window = curses.newwin(TITLE_HEIGHT-1, TITLE_WIDTH, 1, LEFT_MARGIN)
#     i = random.randint(6, 10)
#     window.addstr(0, 4, "#####  ####  #####  ###    #   ####", curses.color_pair(i))
#     window.addstr(1, 4, "  #    #       #    #  #   #  #", curses.color_pair(i))
#     window.addstr(2, 4, "  #    ###     #    # #    #   ###", curses.color_pair(i))
#     window.addstr(3, 4, "  #    #       #    #  #   #      #", curses.color_pair(i))
#     window.addstr(4, 4, "  #    ####    #    #   #  #  ####", curses.color_pair(i))
#     window.refresh()
#     time.sleep(0.4)

def draw_tetris_title():
    curses.init_pair(10, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
    for i in range(6,11):
        window = curses.newwin(TITLE_HEIGHT-1, TITLE_WIDTH-3, 1, 3)
        window.addstr(0, 4, "#####  ####  #####  ###    #   ####", curses.color_pair(i))
        window.addstr(1, 4, "  #    #       #    #  #   #  #", curses.color_pair(i))
        window.addstr(2, 4, "  #    ###     #    # #    #   ###", curses.color_pair(i))
        window.addstr(3, 4, "  #    #       #    #  #   #      #", curses.color_pair(i))
        window.addstr(4, 4, "  #    ####    #    #   #  #  ####", curses.color_pair(i))
        window.refresh()
        time.sleep(0.2)

def _burn_animation(row):
    # window = curses.newwin(1, BOARD_WIDTH*2 , TITLE_HEIGHT+row+1, LEFT_MARGIN+1)
    for i in range(1,BOARD_WIDTH+1):
        window = curses.newwin(1, 2 , TITLE_HEIGHT+row+1, LEFT_MARGIN-1+2*i)
        curses.init_pair(12, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(13, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
        curses.init_pair(14, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(15, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(16, curses.COLOR_BLUE, curses.COLOR_BLUE)
        window.bkgd(' ', curses.color_pair(random.randint(12, 16)))
        window.refresh() 
        time.sleep(0.02)

class Board:
    """Board representation"""
    draw_tetris_title

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = None
        self.lines = None
        self.best_score = None
        self.level = None

    def start(self, menulevel):
        """Start game"""

        self.board = self._get_new_board()

        self.current_block_pos = None
        self.current_block = None
        self.next_block = None

        self.game_over = False
        self.score = 0
        self.lines = 0
        self.level = menulevel
        self.best_score = self._read_best_score()

        self._place_new_block()

    def is_game_over(self):
        """Is game over"""
        return self.game_over

    def rotate_block(self):
        rotated_shape = list(map(list, zip(*self.current_block.shape[::-1])))

        if self._can_move(self.current_block_pos, rotated_shape):
            self.current_block.shape = rotated_shape

    def move_block(self, direction):
        """Try to move block"""
        pos = self.current_block_pos
        if direction == "left":
            new_pos = [pos[0], pos[1] - 1]
        elif direction == "right":
            new_pos = [pos[0], pos[1] + 1]
        elif direction == "down":
            new_pos = [pos[0] + 1, pos[1]]
        else:
            raise ValueError("wrong directions")

        if self._can_move(new_pos, self.current_block.shape):
            self.current_block_pos = new_pos
        elif direction == "down":
            self._land_block()
            self._burn()
            self._place_new_block()


    def drop(self):
        """Move to very very bottom"""

        i = 1
        while self._can_move((self.current_block_pos[0] + 1, self.current_block_pos[1]), self.current_block.shape):
            i += 1
            self.move_block("down")

        self._land_block()
        self._burn()
        self._place_new_block()

    def _get_new_board(self):
        """Create new empty board"""

        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def _place_new_block(self):
        """Place new block and generate the next one"""

        if self.next_block is None:
            self.current_block = self._get_new_block()
            self.next_block = self._get_new_block()
        else:
            self.current_block = self.next_block
            self.next_block = self._get_new_block()

        size = Block.get_size(self.current_block.shape)
        col_pos = math.floor((self.width - size[1]) / 2)
        self.current_block_pos = [0, col_pos]

        if self._check_overlapping(self.current_block_pos, self.current_block.shape):
            self.game_over = True
            self._save_best_score()
        else:
            self.score += 5

    def _land_block(self):
        """Put block to the board and generate a new one"""

        size = Block.get_size(self.current_block.shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if self.current_block.shape[row][col] == 1:
                    self.board[self.current_block_pos[0] + row][self.current_block_pos[1] + col] = 1

    def _burn(self):
        """Remove matched lines"""
        tetris = 0
        for row in range(self.height):
            if all(col != 0 for col in self.board[row]):
                for r in range(row, 0, -1):
                    self.board[r] = self.board[r - 1]
                self.board[0] = [0 for _ in range(self.width)]
                self.score += 100
                self.lines += 1
                if self.lines % 10 == 0:
                    self.level += 1
                tetris = tetris + 1
                if tetris in range(1,5):
                    _burn_animation(row)
        if tetris == 4:
            draw_tetris_title()
            
    def _check_overlapping(self, pos, shape):
        """If current block overlaps any other on the board"""

        size = Block.get_size(shape)
        for row in range(size[0]):
            for col in range(size[1]):
                if shape[row][col] == 1:
                    if self.board[pos[0] + row][pos[1] + col] == 1:
                        return True
        return False

    def _can_move(self, pos, shape):
        """Check if move is possible"""

        size = Block.get_size(shape)
        if pos[1] < 0 or pos[1] + size[1] > self.width \
                or pos[0] + size[0] > self.height:
            return False

        return not self._check_overlapping(pos, shape)

    def _save_best_score(self):
        X = []
        """Saves scores to file"""
        with open (BEST_SCORE_FILE_NAME+".txt", 'a') as file:
            file.close()
        with open(BEST_SCORE_FILE_NAME+".txt", "r+") as file:
            
            X.append(self.score)
            for line in file:
                X.append(int(line))
            X.sort(reverse=True)
            file.close()
        with open (BEST_SCORE_FILE_NAME+".txt", 'w') as file:
            for i in X:
                file.write(str(i) + "\n")
            
    @staticmethod
    def _read_best_score():
        """Read best score from file"""
        if os.path.exists(f"./{BEST_SCORE_FILE_NAME}.txt"):
            with open(BEST_SCORE_FILE_NAME+".txt") as file:
                return int(file.readline())
        return 0

    @staticmethod
    def _get_new_block():
        """Get random block"""

        block = Block(random.randint(0, len(block_shapes) - 1))

        # flip it randomly
        if random.getrandbits(1):
            block.flip()

        return block


class Block:
    """Block representation"""

    def __init__(self, block_type):
        self.shape = block_shapes[block_type]
        self.color = block_type + 1

    def flip(self):
        self.shape = list(map(list, self.shape[::-1]))

    def _get_rotated(self):
        return list(map(list, zip(*self.shape[::-1])))

    def size(self):
        """Get size of the block"""

        return self.get_size(self.shape)

    @staticmethod
    def get_size(shape):
        """Get size of a shape"""

        return [len(shape), len(shape[0])]
