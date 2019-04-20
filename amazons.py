import numpy as np

# 我们规定 0 为没有棋子
# 我们规定 1 为先手方 A
# 我们规定 2 为后手方 B
# 我们规定 3 为先手方障碍 A
# 我们规定 4 为后手方障碍 B


class Amazons(Exception):
    def __init__(self, width=10, height=10):
        board = np.zeros([height, width], dtype=int)
        # 初始化先手方棋子位置
        board[0, 3] = 1
        board[0, 6] = 1
        board[3, 0] = 1
        board[3, 9] = 1
        # 初始化后手方棋子位置
        board[6, 0] = 2
        board[9, 3] = 2
        board[9, 6] = 2
        board[6, 9] = 2
        self.__globalBoard = board
        self.__width = width
        self.__height = height
        self.__history = {'boardlist': [board.reshape(-1)], 'movelist': [{'from': None, 'to': None}]}

    # 获取棋盘情况

    def getBoard(self):
        return self.__globalBoard.reshape(-1)
        # return self.__globalBoard

    # 下棋操作

    def fire(self, player, location, itemtype):
        # 我们规定itemtype=0 为棋子
        # 我们规定itemtype=1 为障碍

        reshapeBoard = self.__globalBoard.reshape(self.__height, self.__width)

        # 将 from to 搞出来
        itemfromV = location['from'][0] - 1
        itemfromH = location['from'][1] - 1
        itemtoV = location['to'][0] - 1
        itemtoH = location['to'][1] - 1

        # 首先判断目标位置是否存在棋子
        target = reshapeBoard[itemtoV, itemtoH]
        if target != 0:
            raise RuntimeError

        # 然后判断他是否越过障碍
        

        # player = A itemtype = 0
        if player == 'A' and itemtype == 0:
            reshapeBoard[itemfromV, itemfromH] = 0
            reshapeBoard[itemtoV, itemtoH] = 1
        elif player == 'A' and itemtype == 1:
            reshapeBoard[itemfromV, itemfromH] = 0
            reshapeBoard[itemtoV, itemtoH] = 3
        elif player == 'B' and itemtype == 0:
            reshapeBoard[itemfromV, itemfromH] = 0
            reshapeBoard[itemtoV, itemtoH] = 2
        elif player == 'B' and itemtype == 1:
            reshapeBoard[itemfromV, itemfromH] = 0
            reshapeBoard[itemtoV, itemtoH] = 4
        else:
            pass

        changedBoard = np.asarray(reshapeBoard, dtype=int)
        self.__globalBoard = changedBoard

        # 然后将下棋步骤保存在history

        self.__history['boardlist'].insert(0, changedBoard.reshape(-1))
        self.__history['movelist'].insert(0, location)

        return changedBoard, None

    # 获取历史信息

    def history(self):
        return self.__history

    # 引入棋局

    def imports(self, history):
        self.__history = history


def main():
    board = Amazons(10, 10)
    # print(board.getBoard())
    board.fire('A', {'from': [1, 4], 'to': [1, 7]}, 0)
    # print(board.getBoard())
    # print(board.history())


if __name__ == '__main__':
    main()
