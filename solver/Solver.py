import random
class Solver:
    solved_positions = set()

    def solve_minesweeper(self, board):
        self.board = board
        self.choose_random_pos(board)
        board.print_diff()

        old_items = []
        while not board.is_solved():
            board.print_diff()
            items = self.get_expandable_positions(board)

            if not self.extract_positions(board, items):
                print "FAIL!"
                board.print_board()
                board.print_diff(self.solved_positions)
                return False

            if len(items) == len(old_items):
                
                print("Checking if a random position must be chosen.", items, old_items)
                must_choose_rand = True
                
                for item in items:
                    if item not in old_items:
                        print("A new position was found. Will expand this next.")
                        must_choose_rand = False
                        break
                
                if must_choose_rand:
                    print("Choosing a new random position.")
                    if not self.choose_random_pos(board):
                        board.print_board()
                        board.print_diff(self.solved_positions)
                        return False
            old_items = items

        print "#################### SOLUTION ##################################"
        board.print_board()
        board.print_diff(self.solved_positions)
        board.print_game_board()
        return board.game_board

    def choose_random_pos(self, board):
        rand_x = random.randint(0, board.width - 1)
        rand_y = random.randint(0, board.height - 1)
        if not board.choose_position(rand_x, rand_y):
            print("Fail! Mine chosen at position ", (rand_x, rand_y))
            return False
        board.print_board()
        board.print_game_board()
        return True

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
