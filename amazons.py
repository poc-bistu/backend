import numpy as np

# 我们规定 0 为没有棋子
# 我们规定 1 为先手方 A
# 我们规定 2 为后手方 B
# 我们规定 3 为先手方障碍 A
# 我们规定 4 为后手方障碍 B


class Amazons(object):
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
        playerResult = self.__gameStatus()

        return changedBoard, playerResult

    # 获取历史信息

    def history(self):
        return self.__history

    # 引入棋局

    def imports(self, history):
        self.__history = history
        self.__globalBoard = history['boardlist'][0]


    # 判断胜负的私有函数

    def __gameStatus(self):
        reshapeBoard = self.__globalBoard.reshape(self.__height, self.__width)
        print(reshapeBoard)
        # 定义玩家A 和 B 四个棋子状态
        statusA = [True, True, True, True]
        statusB = [True, True, True, True]

        # 首先判断是否有棋子在四个角上，并汇总双方棋子
        corner = {'A': None, 'B': None, 'C': None, 'D': None}
        corner['A'] = reshapeBoard[0, 0]
        corner['B'] = reshapeBoard[0, 9]
        corner['C'] = reshapeBoard[9, 9]
        corner['D'] = reshapeBoard[9, 0]
        cornerResult = [0, 0, 0]
        if corner['A'] == 1:
            cornerResult[0] = reshapeBoard[0, 1]
            cornerResult[1] = reshapeBoard[1, 0]
            cornerResult[2] = reshapeBoard[1, 1]
            if cornerResult[0] != 0 and cornerResult[1] != 0 and cornerResult[2] != 0:
                for i in range(4):
                    if statusA[i] == True:
                        statusA[i] = False
                        break
        if corner['A'] == 2:
            cornerResult[0] = reshapeBoard[0, 1]
            cornerResult[1] = reshapeBoard[1, 0]
            cornerResult[2] = reshapeBoard[1, 1]
            if cornerResult[0] != 0 and cornerResult[1] != 0 and cornerResult[2] != 0:
                for i in range(4):
                    if statusB[i] == True:
                        statusB[i] = False
                        break

        if corner['B'] == 1:
            cornerResult[0] = reshapeBoard[0, 8]
            cornerResult[1] = reshapeBoard[1, 8]
            cornerResult[2] = reshapeBoard[1, 9]
            if cornerResult[0] != 0 and cornerResult[1] != 0 and cornerResult[2] != 0:
                for i in range(4):
                    if statusA[i] == True:
                        statusA[i] = False
                        break
        if corner['B'] == 2:
            cornerResult[0] = reshapeBoard[0, 8]
            cornerResult[1] = reshapeBoard[1, 8]
            cornerResult[2] = reshapeBoard[1, 9]
            if cornerResult[0] != 0 and cornerResult[1] != 0 and cornerResult[2] != 0:
                for i in range(4):
                    if statusB[i] == True:
                        statusB[i] = False
                        break

        if corner['C'] == 1:
            cornerResult[0] = reshapeBoard[8, 9]
            cornerResult[1] = reshapeBoard[8, 8]
            cornerResult[2] = reshapeBoard[9, 8]
            if cornerResult[0] != 0 and cornerResult[1] != 0 and cornerResult[2] != 0:
                for i in range(4):
                    if statusA[i] == True:
                        statusA[i] = False
                        break
        if corner['C'] == 2:
            cornerResult[0] = reshapeBoard[8, 9]
            cornerResult[1] = reshapeBoard[8, 8]
            cornerResult[2] = reshapeBoard[9, 8]
            if cornerResult[0] != 0 and cornerResult[1] != 0 and cornerResult[2] != 0:
                for i in range(4):
                    if statusB[i] == True:
                        statusB[i] = False
                        break

        if corner['D'] == 1:
            cornerResult[0] = reshapeBoard[8, 0]
            cornerResult[1] = reshapeBoard[8, 1]
            cornerResult[2] = reshapeBoard[9, 1]
            if cornerResult[0] != 0 and cornerResult[1] != 0 and cornerResult[2] != 0:
                for i in range(4):
                    if statusA[i] == True:
                        statusA[i] = False
                        break
        if corner['D'] == 2:
            cornerResult[0] = reshapeBoard[8, 0]
            cornerResult[1] = reshapeBoard[8, 1]
            cornerResult[2] = reshapeBoard[9, 1]
            if cornerResult[0] != 0 and cornerResult[1] != 0 and cornerResult[2] != 0:
                for i in range(4):
                    if statusB[i] == True:
                        statusB[i] = False
                        break

        # 判断边界点的棋子
        '''
            我们规定上边界为A，顺时针顺序为A，B，C，D
                       A
                 _____________
                 |           |
            D    |           |     B
                 |           |
                 |___________|
                 
                       C
        '''
        border = {'A': [], 'B': [], 'C': [], 'D': []}
        zone = [1, 2, 3, 4, 5, 6, 7, 8]

        for i in zone:
            border['A'].append(reshapeBoard[0, i])
        for i in zone:
            border['B'].append(reshapeBoard[i, 9])
        for i in zone:
            border['C'].append(reshapeBoard[9, i])
        for i in zone:
            border['D'].append(reshapeBoard[i, 0])

        for i in range(8):
            # 先从边界A开始
            keyResult = [0, 0, 0, 0, 0]
            if border['A'][i] == 1:
                keyResult[0] = reshapeBoard[0, i]
                keyResult[1] = reshapeBoard[1, i]
                keyResult[2] = reshapeBoard[1, i+1]
                keyResult[3] = reshapeBoard[1, i+2]
                keyResult[4] = reshapeBoard[0, i+2]
                if(     keyResult[0] != 0 and keyResult[1] != 0 and keyResult[2] != 0
                        and keyResult[3] != 0 and keyResult[4] != 0):
                    for k in range(4):
                        if statusA[k] == True:
                            statusA[k] = False
                            break
            if border['A'][i] == 2:
                keyResult[0] = reshapeBoard[0, i]
                keyResult[1] = reshapeBoard[1, i]
                keyResult[2] = reshapeBoard[1, i+1]
                keyResult[3] = reshapeBoard[1, i+2]
                keyResult[4] = reshapeBoard[0, i+2]
                if(     keyResult[0] != 0 and keyResult[1] != 0 and keyResult[2] != 0
                        and keyResult[3] != 0 and keyResult[4] != 0):
                    for k in range(4):
                        if statusB[k] == True:
                            statusB[k] = False
                            break

            # 然后是边界B
            if border['B'][i] == 1:
                keyResult[0] = reshapeBoard[i, 9]
                keyResult[1] = reshapeBoard[i, 8]
                keyResult[2] = reshapeBoard[i+1, 8]
                keyResult[3] = reshapeBoard[i+2, 8]
                keyResult[4] = reshapeBoard[i+2, 9]

                if(     keyResult[0] != 0 and keyResult[1] != 0 and keyResult[2] != 0
                        and keyResult[3] != 0 and keyResult[4] != 0):
                    for k in range(4):
                        if statusA[k] == True:
                            statusA[k] = False
                            break
            if border['B'][i] == 2:
                keyResult[0] = reshapeBoard[i, 9]
                keyResult[1] = reshapeBoard[i, 8]
                keyResult[2] = reshapeBoard[i+1, 8]
                keyResult[3] = reshapeBoard[i+2, 8]
                keyResult[4] = reshapeBoard[i+2, 9]
                if(     keyResult[0] != 0 and keyResult[1] != 0 and keyResult[2] != 0
                        and keyResult[3] != 0 and keyResult[4] != 0):
                    for k in range(4):
                        if statusB[k] == True:
                            statusB[k] = False
                            break

            # 然后是边界C
            if border['C'][i] == 1:
                keyResult[0] = reshapeBoard[9, i]
                keyResult[1] = reshapeBoard[8, i]
                keyResult[2] = reshapeBoard[8, i+1]
                keyResult[3] = reshapeBoard[8, i+2]
                keyResult[4] = reshapeBoard[9, i+2]
                if(     keyResult[0] != 0 and keyResult[1] != 0 and keyResult[2] != 0
                        and keyResult[3] != 0 and keyResult[4] != 0):
                    for k in range(4):
                        if statusA[k] == True:
                            statusA[k] = False
                            break
            if border['C'][i] == 2:
                keyResult[0] = reshapeBoard[9, i]
                keyResult[1] = reshapeBoard[8, i]
                keyResult[2] = reshapeBoard[8, i+1]
                keyResult[3] = reshapeBoard[8, i+2]
                keyResult[4] = reshapeBoard[9, i+2]
                if(     keyResult[0] != 0 and keyResult[1] != 0 and keyResult[2] != 0
                        and keyResult[3] != 0 and keyResult[4] != 0):
                    for k in range(4):
                        if statusB[k] == True:
                            statusB[k] = False
                            break

            # 然后是边界D
            if border['D'][i] == 1:
                keyResult[0] = reshapeBoard[i, 0]
                keyResult[1] = reshapeBoard[i, 1]
                keyResult[2] = reshapeBoard[i+1, 1]
                keyResult[3] = reshapeBoard[i+2, 1]
                keyResult[4] = reshapeBoard[i+2, 0]
                if(     keyResult[0] != 0 & keyResult[1] != 0 and keyResult[2] != 0
                        and keyResult[3] != 0 and keyResult[4] != 0):
                    for k in range(4):
                        if statusA[k] == True:
                            statusA[k] = False
                            break
            if border['D'][i] == 2:
                keyResult[0] = reshapeBoard[9, i]
                keyResult[1] = reshapeBoard[8, i]
                keyResult[2] = reshapeBoard[8, i+1]
                keyResult[3] = reshapeBoard[8, i+2]
                keyResult[4] = reshapeBoard[9, i+2]
                if(     keyResult[0] != 0 and keyResult[1] != 0 and keyResult[2] != 0
                        and keyResult[3] != 0 and keyResult[4] != 0):
                    for k in range(4):
                        if statusB[k] == True:
                            statusB[k] = False
                            break

        '''
            下面是除边界以外的全部点
        '''
        innerResult = [0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(8):
            for j in range(8):
                # 玩家A的情况
                if reshapeBoard[i+1, j+1] == 1:
                    innerResult[0] = reshapeBoard[i, j]
                    innerResult[1] = reshapeBoard[i, j+1]
                    innerResult[2] = reshapeBoard[i, j+2]
                    innerResult[3] = reshapeBoard[i+1, j]
                    innerResult[4] = reshapeBoard[i+1, j+2]
                    innerResult[5] = reshapeBoard[i+2, j]
                    innerResult[6] = reshapeBoard[i+2, j+1]
                    innerResult[7] = reshapeBoard[i+2, j+2]
                    if(     innerResult[0] != 0 and innerResult[1] != 0 and innerResult[2] != 0
                            and innerResult[3] != 0 and innerResult[4] != 0 and innerResult[5] != 0
                            and innerResult[6] != 0 and innerResult[7] != 0):
                        for k in range(4):
                            if statusA[k] == True:
                                statusA[k] = False
                                break
                # 玩家B的情况
                if reshapeBoard[i+1, j+1] == 2:
                    innerResult[0] = reshapeBoard[i, j]
                    innerResult[1] = reshapeBoard[i, j+1]
                    innerResult[2] = reshapeBoard[i, j+2]
                    innerResult[3] = reshapeBoard[i+1, j]
                    innerResult[4] = reshapeBoard[i+1, j+2]
                    innerResult[5] = reshapeBoard[i+2, j]
                    innerResult[6] = reshapeBoard[i+2, j+1]
                    innerResult[7] = reshapeBoard[i+2, j+2]
                    if(     innerResult[0] != 0 and innerResult[1] != 0 and innerResult[2] != 0
                            and innerResult[3] != 0 and innerResult[4] != 0 and innerResult[5] != 0
                            and innerResult[6] != 0 and innerResult[7] != 0):
                        for k in range(4):
                            if statusB[k] == True:
                                statusB[k] = False
                                break
        # playerA = True 则为A赢了 PlayerB = True 则为B赢了
        playerA = False
        playerB = False

        countA = 0
        countB = 0
        for i in statusA:
            if i == False:
                countA += 1

        for i in statusB:
            if i == False:
                countB += 1
        if countA == 4:
            playerB = True

        if countB == 4:
            playerA = True

        # 开始返回胜利的玩家
        if playerA == True and playerB == False:
            return 'A'
        elif playerB == True and playerB == False:
            return 'B'
        elif playerA == True and playerB == True:
            return 'TIE'
        elif playerA == False and playerB == False:
            return None

'''
def main():
    board = Amazons(10, 10)

    while True:
        player = input("player:")
        itemFromX = int(input("fromX:"))
        itemFromY = int(input("fromY:"))
        itemToX = int(input("toX:"))
        itemToY = int(input("toY:"))
        itemType = int(input("type:"))
        a = board.fire(player, {'from': [itemFromX, itemFromY], 'to': [itemToX, itemToY]}, itemType)
        print(a)
        #board.gameStatus()


if __name__ == '__main__':
    main()


'''
