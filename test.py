import numpy as np


def main():
    board = np.zeros([10, 10], dtype=int)

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

    # 首先计算上下左右 四个方向的
    chessX = 0
    chessY = 5
    enableLocationX = []
    enableLocationY = []
    enableLocationP = []
    enableLocationN = []

    for i in range(10):
        for j in range(10):

            if i == chessX and j != chessY:
                if j < chessY and board[i, j] == 0:
                    enableLocationX.append((i, j,))
                elif j < chessY and board[i, j] != 0:
                    enableLocationX.clear()


            if j == chessX and i != chessY:
                if board[i, j] == 0:
                    enableLocationY.append((i, j, ))
            if chessX + chessY == i + j and (chessX != i and chessY != j):
                if board[i, j] == 0:
                    enableLocationP.append((i, j, ))
            if chessX - chessY == i - j and (chessX != i and chessY != j):
                if board[i, j] == 0:
                    enableLocationN.append((i, j, ))
    print(enableLocationX, enableLocationY, enableLocationP, enableLocationN)

if __name__ == '__main__':
    main()
