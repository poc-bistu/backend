import numpy as np

# 我们规定 0 为没有棋子
# 我们规定 1 为先手方 A
# 我们规定 2 为后手方 B
# 我们规定 3 为先手方障碍 A
# 我们规定 4 为后手方障碍 B


class Amazons():
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

        # Start 下棋规则

        '''
            说明：
            chessX 是 行坐标
            chessY 是 列坐标
            enableLocation* 在八个方向可以下棋的位置
            enabelLocation 是八个方向汇总在一起可以下的位置
            flag* 是分别在八个方向有阻挡棋子的开始和结束位置
            count* 是统计出当前每个enabelLocation*的成员数量
        '''
        chessX = itemfromH
        chessY = itemfromV
        enableLocationX = []
        enableLocationY = []
        enableLocationP = []
        enableLocationN = []
        flagX = {'start': None, 'end': None}
        flagY = {'start': None, 'end': None}
        flagP = {'start': None, 'end': None}
        flagN = {'start': None, 'end': None}
        countX, countY, countP, countN = 0, 0, 0, 0

        '''
            首先需要用两个for循环，遍历出当前棋子位置，在八个方向上允许下棋的所有位置
            包括中间有格挡棋子的情况
        '''
        for i in range(10):
            for j in range(10):

                if i == chessX and j != chessY:
                    if reshapeBoard[i, j] == 0:
                        enableLocationX.append((i, j,))
                        countX += 1
                    else:
                        # if j != chessX and i != chessY:
                        if j < chessY:
                            flagX['start'] = countX
                        elif j > chessY:
                            if flagX['end'] == None:
                                flagX['end'] = countX
                if j == chessY and i != chessX:
                    if reshapeBoard[i, j] == 0:
                        enableLocationY.append((i, j,))
                        countY += 1
                    else:
                        if i < chessX:
                            flagY['start'] = countY
                        elif i > chessX:
                            if flagY['end'] == None:
                                flagY['end'] = countY
                if chessX + chessY == i + j and (chessX != i and chessY != j):
                    if reshapeBoard[i, j] == 0:
                        enableLocationP.append((i, j,))
                        countP += 1
                    else:
                        if i < chessX:
                            flagP['start'] = countP
                        elif i > chessX:
                            if flagP['end'] == None:
                                flagP['end'] = countP

                if chessX - chessY == i - j and (chessX != i and chessY != j):
                    if reshapeBoard[i, j] == 0:
                        enableLocationN.append((i, j,))
                        countN += 1
                    else:
                        if i < chessX:
                            flagN['start'] = countN
                        elif i > chessX:
                            if flagN['end'] == None:
                                flagN['end'] = countN
        '''
            通过刚才记录的有棋子的flag标记，开始删除跳过这个棋子的所有位置
        '''
        if flagX['end'] != None:
            for i in range(len(enableLocationX) - flagX['end']):
                enableLocationX.pop()

        if flagX['start'] != None:
            if flagX['start'] == 1:
                flagX['start'] += 1
            for i in range(flagX['start']):
                enableLocationX.pop(0)

        if flagY['end'] != None:
            for i in range(len(enableLocationY) - flagY['end']):
                enableLocationY.pop()

        if flagY['start'] != None:
            if flagY['start'] == 1:
                flagY['start'] += 1
            for i in range(flagY['start']):
                enableLocationY.pop(0)

        if flagP['end'] != None:
            for i in range(len(enableLocationP) - flagP['end']):
                enableLocationP.pop()

        if flagP['start'] != None:
            if flagP['start'] == 1:
                flagP['start'] += 1
            for i in range(flagP['start']):
                enableLocationP.pop(0)

        if flagN['end'] != None:
            for i in range(len(enableLocationN) - flagN['end']):
                enableLocationN.pop()

        if flagN['start'] != None:
            if flagN['start'] == 1:
                flagN['start'] += 1
            for i in range(flagN['start']):
                enableLocationN.pop(0)

            # 最后将整个可以放置为位置整合在一个list中
        enableLocation = enableLocationX + enableLocationY + enableLocationP + enableLocationN
        # End 棋盘规则

        # 然后判断是否可以放在这个地方
        flag = 0
        for (i, j) in enableLocation:
            if i == itemtoH and j == itemtoV:
                flag = 1
                break

        if flag == 0:
            raise RuntimeError


        # player = A itemtype = 0
        if player == 'A' and itemtype == 0:
            reshapeBoard[itemfromH, itemfromV] = 0
            reshapeBoard[itemtoH, itemtoV] = 1
        elif player == 'A' and itemtype == 1:
            # reshapeBoard[itemfromH, itemfromV] = 0
            reshapeBoard[itemtoH, itemtoV] = 3
        elif player == 'B' and itemtype == 0:
            reshapeBoard[itemfromH, itemfromV] = 0
            reshapeBoard[itemtoH, itemtoV] = 2
        elif player == 'B' and itemtype == 1:
            # reshapeBoard[itemfromH, itemfromV] = 0
            reshapeBoard[itemtoH, itemtoV] = 4
        else:
            pass

        changedBoard = np.asarray(reshapeBoard, dtype=int)
        self.__globalBoard = changedBoard

        # 然后将下棋步骤保存在history

        self.__history['boardlist'].insert(0, changedBoard.reshape(-1))
        self.__history['movelist'].insert(0, location)

        #然后进行胜负的判断

        return changedBoard, None

    # 获取历史信息

    def history(self):
        return self.__history

    # 引入棋局

    def imports(self, history):
        self.__history = history


def main():
    board = Amazons(10, 10)

    while True:
        player = input("player:")
        itemFromX = int(input("fromX:"))
        itemFromY = int(input("fromY:"))
        itemToX = int(input("toX:"))
        itemToY = int(input("toY:"))
        itemType = int(input("type:"))
        board.fire(player, {'from': [itemFromX, itemFromY], 'to': [itemToX, itemToY]}, itemType)

if __name__ == '__main__':
    main()
