import random
class Board:
    def __init__(self):
        self.boardInitialized = False
        self.gameStarted = False
        self.mines = 0
        self.num_mines = 0
        self.board = []
        self.game_board = []
        self._mine = "m"
        self.width = 0
        self.height = 0
        self.flags = set()
        self.discovered_mines = 0
        self._flag = "f"

    def init_board(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines

        if not self.boardInitialized:
            for x in range(width):
                for y in range(self.height):
                    self.board.append(0)
                    self.game_board.append(None)

            self.boardInitialized = True

    def create_board(self, chosen_x, chosen_y):
        mines = self.mines

        if self.boardInitialized:
            for x in range(self.width):
                while self.mines:
                    rand = random.randint(0, self.width*self.height)
                    x = rand / self.width - 1
                    y = rand % self.height
                    pos = self.translate_pos(x,y)
                    if self.board[pos] is not self._mine:
                        self.board[pos] = self._mine
                        self.mines-=1
                        self.num_mines+=1

            for x in range(self.width):
                for y in range(self.height):
                    position = self.translate_pos(x, y)
                    # print "positions", x, y, position, self.get_position(x,y)
                    if self.board[position] is not self._mine:
                        for i in range(x - 1, x + 2):
                            if i >= 0 and i < self.width:
                                for j in range(y - 1, y + 2):
                                    if j >= 0 and j < self.height and not (i == x and j == y):
                                        # print "check ", x, y, i, j

                                        if self.get_position(i, j) is self._mine:
                                            self.board[position] += 1
            self.gameStarted = True

    def delete_board(self):
        self.board = []
        self.boardInitialized = False

    def get_position(self, x, y):
        if x * y < len(self.board):
            return self.board[self.translate_pos(x, y)]

        return None

    def get_board_position(self, board, x, y):
        if x * y < len(board):
            return board[self.translate_pos(x, y)]

        return None

    def is_mine(self, x, y):
        return self.get_position(x, y) == self._mine

    def translate_pos(self, x, y):
        return x * self.width + y

    def choose_position(self, pos_x, pos_y):
        if not self.gameStarted:
            self.create_board(pos_x, pos_y)

        if self.is_mine(pos_x, pos_y):
            return False

        if self.get_board_position(self.game_board, pos_x, pos_y) is None:
            item = self.get_board_position(self.board, pos_x, pos_y)
            if item == 0:
                self.reveal_positions(pos_x, pos_y)
            else:
                self.game_board[self.translate_pos(pos_x, pos_y)] = item

        return True

    def reveal_positions(self, pos_x, pos_y):
        stack = []
        self.game_board[self.translate_pos(pos_x, pos_y)] = self.get_board_position(self.board, pos_x, pos_y)

        for x in range(pos_x - 1, pos_x + 2, 1):
            if x >= 0 and x < self.width:
                for y in range(pos_y - 1, pos_y + 2):

                    if y >= 0 and y < self.height:
                        if x != pos_x and y != pos_y:
                            stack.append((x, y))

        while len(stack):
            new_pos = stack.pop()
            pos_x = new_pos[0]
            pos_y = new_pos[1]
            for x in range(pos_x - 1, pos_x + 2):

                if x >= 0 and x < self.width:
                    for y in range(pos_y - 1, pos_y + 2):
                        if y >= 0 and y < self.height:
                            item = self.get_board_position(self.board, x, y)

                            game_board_item = self.get_board_position(self.game_board, x, y)
                            if item is not self._mine and not (x == pos_x and y == pos_y) and game_board_item is None:
                                pos = self.translate_pos(x, y)

                                self.game_board[pos] = self.board[pos]

                                if item == 0:
                                    stack.append((x, y))

    def add_flag(self, x, y):
        self.flags.add((x, y))
        self.game_board[self.translate_pos(x, y)] = self._flag
        self.discovered_mines += 1

    def is_flagged(self, x, y):
        return (x, y) in self.flags

    def print_board(self):
        b = ""
        for i in range(self.width):
            for j in range(self.height):
                b += str(self.get_position(i, j)) + " "
            b += "\n"
        print b

    def print_game_board(self):
        b = ""
        for i in range(self.width):
            for j in range(self.height):
                item = self.get_board_position(self.game_board, i, j)
                b += (str(item) if item is not None else "U") + " "
            b += "\n"
        print b

    def print_diff(self, solved_positions = []):
        good = 0
        bad = 0
        b = ""
        for i in range(self.width):
            for j in range(self.height):
                item = self.get_board_position(self.board, i, j)
                game = self.get_board_position(self.game_board, i, j)
                if game is None:
                    b += "U "
                elif game is self._flag and item is self._mine:
                    b += "Y "
                    good+=1
                elif game is self._flag and item is not self._mine:
                    b += "N "
                    bad+=1
                else:
                    b+=(str(game) if (i,j) not in solved_positions else "S") + " "
            b += "\n"

        print b
        print "Correct flags = ", good, "Incorrect Flags = ", bad

    def is_solved(self):
        if len(self.flags) != self.num_mines:
            print "FLAGS and num mines do not match"
            return False

        for x,y in self.flags:
            if not self.get_board_position(self.board, x, y) == self._mine:
                print "found a flag that is not correct"
                return False

        return True

