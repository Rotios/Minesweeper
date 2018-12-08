import random

class Board:
    boardInitialized = False
    gameStarted = False
    mines = 0
    num_mines = 0
    board = []
    game_board = []
    _mine = "m"
    width = 0
    height = 0
    flags = set()
    discovered_mines = 0
    _flag = "f"

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
        return self.get_position(x, y) is self._mine

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
        for i in range(width):
            for j in range(height):
                b += str(board.get_position(i, j)) + " "
            b += "\n"
        print b

    def print_game_board(self):
        b = ""
        for i in range(width):
            for j in range(height):
                item = self.get_board_position(self.game_board, i, j)
                b += (str(item) if item is not None else "U") + " "
            b += "\n"
        print b

    def print_diff(self, solved_positions = []):
        good = 0
        bad = 0
        b = ""
        for i in range(self.width):
            for j in range(height):
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

class Solver:
    solved_positions = set()

    def solve_minesweeper(self, board):
        self.board = board
        self.choose_random_pos(board)

        old_items = []
        while not board.is_solved():
        # for i in range(1,20):
            board.print_diff()
            items = self.get_expandable_positions(board)
            old_items = items
            if not self.extract_positions(board, items):
                print "FAIL!"
                board.print_board()
                board.print_diff(self.solved_positions)
                return False

            if len(items) == len(old_items):

                for item in items:
                    if item not in old_items:
                        continue

                self.choose_random_pos(board)

            # self.update_other_positions(board)

        print "#################### SOLUTION ##################################"
        board.print_board()
        board.print_diff(self.solved_positions)
        board.print_game_board()
        return board.game_board

    def choose_random_pos(self, board):
        rand_x = random.randint(0, board.width - 1)
        rand_y = random.randint(0, board.height - 1)
        board.choose_position(rand_x, rand_y)
        board.print_board()
        board.print_game_board()

    def extract_positions(self, board, items):
        for x,y in items:
            if not self.updateItems(board, x, y, board.get_board_position(board.board,x,y)):
                print "FAIL",x,y
                return False

        return True

    def get_expandable_positions(self, board):
        items = []
        for x in range(0, board.width):
            for y in range(0, board.height):
                item = board.get_board_position(board.game_board, x, y)
                if item is not None and item != 0 and not board.is_flagged(x, y) and (x, y) not in self.solved_positions:
                    items.append((x, y))
        return items

    def updateItems(self,board,x,y, num_mines):
        undiscovered = []
        flagged = []
        for i in range(x - 1, x + 2):
            if i >= 0 and i < board.width:
                for j in range(y - 1, y + 2):
                    if j >= 0 and j < board.height:
                        item = board.get_board_position(board.game_board, i, j)
                        if item is None:
                            undiscovered.append((i, j))
                        elif board.is_flagged(i, j):
                            flagged.append((i, j))

        print "flags and undiscovered", (x,y),  len(flagged), len(undiscovered), num_mines

        if len(flagged) == num_mines:
            for i in range(x - 1, x + 2):
                if i >= 0 and i < board.width:
                    for j in range(y - 1, y + 2):
                        if j >= 0 and j < board.height:
                            item = board.get_board_position(board.game_board, i, j)
                            if item is None:
                                if not board.choose_position(i, j):
                                    print "FAILED", x, y, i, j, board.get_board_position(board.board, i, j)
                                    return False

                                board.print_game_board()
            self.solved_positions.add((x,y))

        elif len(flagged) + len(undiscovered) == num_mines:
            for mine_x, mine_y in undiscovered:
                board.add_flag(mine_x, mine_y)
                print x, y, "add flag ", mine_x, mine_y
            self.solved_positions.add((x,y))

        return True


    def extract_ones(self, board,x,y):
        undiscovered = []
        flagged = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                item = board.get_board_position(board.game_board, i, j)
                if item is None:
                    undiscovered.append((i, j))
                elif board.is_flagged(i,j):
                    flagged.append((i,j))

        if len(undiscovered) == 1 and len(flagged) == 0:
            mine_x, mine_y = undiscovered.pop()
            board.add_flag(mine_x, mine_y)
            print x,  y, "add flag ", mine_x, mine_y
            board.game_board[board.translate_pos(x, y)] = 0

        elif len(flagged) == 1:
            board.game_board[board.translate_pos(x, y)] = 0
            for i in range(x-1, x+2):
                for j in range(y-1,  y+2):
                    item = board.get_board_position(board.game_board, i, j)
                    if item is None:
                        if not board.choose_position(i,j):
                            print "FAILED"
                            return False

        print "Extracted Ones", x, y
        board.print_game_board()
        return True

    def expand_pos(self, x, y):
        return

    def is_same(self, stack1, stack2):
        if len(stack1) != len(stack2):
            return False

        for item in stack1:
            if item not in stack2:
                return False

        return True

if __name__ == '__main__':
    width = 24
    height = 24
    mines = 99
    board = Board()
    board.init_board(width, height, mines)
    board.print_game_board()
    solver = Solver()
    solver.solve_minesweeper(board)
