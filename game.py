import numpy
import random


class Game:
    # 2048 游戏类，使用numpy 矩阵运算
    # 使用幂指数作为元素，0表示空格，默认规则下最大取值为17（2^17）
    def __init__(self, width: int = 4, height: int = 4):
        self.width: int = width
        self.height: int = height
        self.board: numpy.ndarray = numpy.zeros((self.width, self.height))
        self.score: int = 0
        self.choice: list = [1, 2]
        self.generate_new_number(random.choice(self.choice))

    def __str__(self):
        string_value = ""
        for y in range(self.height):
            for x in range(self.width):
                string_value += f"|{str(int(self.board[x, y])):^5}"
            string_value += "|\n"
        return string_value

    def set_board(self, board: numpy.ndarray):
        self.board = board

    def random(self):
        # 随机生成棋盘，默认生成随机数，随机数取值范围在0-16之间，0表示空格
        self.board = numpy.random.randint(0, 10, size=(self.width, self.height))

    def generate_new_number(self, number: int = 1) -> bool:
        # 在随机的空位生成指定的数字，默认生成1（2^1）
        empty = numpy.where(self.board == 0)
        if len(empty[0]) == 0:
            return False
        else:
            x = random.randint(0, len(empty[0]) - 1)
            self.board[empty[0][x], empty[1][x]] = number
            return True

    def board_merge_left(self):
        # 合并但不移动，按照从左往右，从上到下的顺序遍历，以保证不二次合并
        # 指定的元素从自身向右搜索相同的元素，如果找到则自身+1，对应位置变为0，更新分数，更新棋盘
        for y in range(self.height):
            for x in range(self.width):
                if self.board[x, y] == 0:
                    continue
                search_x = x + 1
                while search_x < self.width:
                    if self.board[x, y] == self.board[search_x, y]:
                        self.board[x, y] += 1
                        self.score = self.count_score()
                        self.board[search_x, y] = 0
                    elif self.board[search_x, y] != 0:
                        break
                    search_x += 1

    def count_score(self) -> int:
        # 统计棋盘上所有元素的幂指数之和，即棋盘分数
        return sum([2 ** i for i in self.board.flatten()])

    def element_left(self, x_index: int, y_index: int, moved: bool = False) -> bool:
        # 只移动，不合并
        if x_index == 0:
            return moved
        if self.board[x_index - 1, y_index] == 0:
            self.board[x_index - 1, y_index], self.board[x_index, y_index] = self.board[x_index, y_index], 0
            # 递归直到无法移动
            return self.element_left(x_index - 1, y_index, True)
        return moved

    def border_left(self) -> bool:
        # 只移动，不合并
        moved = False
        for y in range(self.height):
            for x in range(1, self.width):
                if self.element_left(x, y):
                    moved = True
        return moved

    def move_left(self) -> bool:
        before = self.board.copy()
        # 合并
        self.board_merge_left()
        # 移动
        self.border_left()
        if numpy.array_equal(before, self.board):
            return False
        else:
            return True

    def move(self, direction: int = 0) -> bool:
        """
        0: 左
        1: 下
        2: 右
        3: 上
        :param direction:
        :return:
        """
        before = self.board.copy()
        # 旋转
        self.board = numpy.rot90(self.board, direction)
        # 并全部化归为左移操作
        self.move_left()
        # 旋转回来
        self.board = numpy.rot90(self.board, 4 - direction)
        if numpy.array_equal(before, self.board):
            return False
        else:
            self.generate_new_number(random.choice(self.choice))
            return True

    def copy(self):
        new = Game(self.width, self.height)
        new.set_board(self.board.copy())
        return new

    def is_over(self) -> bool:
        # 如果有0，则游戏未结束
        if 0 in self.board.flatten():
            return False
        else:
            for play in range(4):
                if self.copy().move(play):
                    return False
        return True


if __name__ == "__main__":
    game = Game()
    print(game)
    while True:
        if not game.move(int(input("请输入移动方向："))):
            print("游戏结束")
            break
        print(game)
        print(game.score)
