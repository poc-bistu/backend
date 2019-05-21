from surakarta import game
import numpy as np


class Surakarta(object):
    # 初始化棋盘
    def __init__(self):
        self.__width = 6
        self.__height = 6

        # 初始化一个苏拉卡尔塔棋盘的Game类
        self.__game = game.Game(-1)

        # 扩展的历史棋盘信息
        self.__history = None

    # 获取棋盘的情况
    def getBoard(self):
        tempBoard = self.__game.get_board()
        board = np.zeros((6, 6), dtype=int)
        for chesses in tempBoard:
            for chess in chesses:
                if chess.camp == -1:
                    board[chess.x][chess.y] = 1
                elif chess.camp == 0:
                    board[chess.x][chess.y] = 0
                else:
                    board[chess.x][chess.y] = 2

        return board.reshape(-1)

    # 重排列棋盘
    def reshapeBoard(self, board):
        returnBoard = np.zeros((6, 6), dtype=int)
        for chesses in board:
            for chess in chesses:
                if chess.camp == -1:
                    returnBoard[chess.x][chess.y] = 1
                elif chess.camp == 0:
                    returnBoard[chess.x][chess.y] = 0
                else:
                    returnBoard[chess.x][chess.y] = 2

        return returnBoard.reshape(-1)

    # 下棋操作
    def fire(self, player, location):
        self.__game.do_move(location)
        board = self.getBoard()
        win_status = self.__game.has_winner()
        winner = None
        if win_status[0] == True:
            if win_status[1] == -1:
                winner = 'A'
            else:
                winner = 'B'
        else:
            pass

        return board, winner

    # 获取历史棋局
    def history(self):
        tempHistory = self.__game.get_history()
        # 首先将tempHistory反向排序
        tempHistory.reverse()

        # 创建一个空的historyList
        historyList = []
        for item in tempHistory:
            tempData = {'boardlist': None, 'movelist': {'from': None, 'to': None},
                        'other':{'board':None ,'camp': None, 'red_num': None, 'blue_num': None, 'chess_num': None}}
            tempData['boardlist'] = self.reshapeBoard(item['board'])
            tempData['movelist']['from'] = (item['from_x'], item['from_y'])
            tempData['movelist']['to'] = (item['to_x'], item['to_y'])
            tempData['other']['camp'] = item['camp']
            tempData['other']['red_num'] = item['red_num']
            tempData['other']['blue_num'] = item['blue_num']
            tempData['other']['chess_num'] = item['chess_num']
            tempData['other']['board'] = item['board']

            historyList.append(tempData)

    # 回滚棋局
    def rollBack(self, step=1):
        for i in range(step):
            self.__game.cancel_move()

        return self.getBoard()

    # 导入历史棋局
    def imports(slef, history: list):
        board_record = []
        game_info = []

        history.reverse()
        for item in history:
            board_record.append({
            "board": item['other']['board'],
            "camp": item['other']['camp'],
            "red_num": item['other']['red_num'],
            "blue_num": item['other']['blue_num'],
            "chess_num": item['other']['chess_num'],
            "from_x": item['movelist']['from'][0],
            "from_y": item['movelist']['from'][1],
            "to_x": item['movelist']['to'][0],
            "to_y": item['movelist']['to'][1]
        })
            game_info.append({
            "board": item['other']['board'],
            "camp": item['other']['camp'],
            "red_num": item['other']['red_num'],
            "blue_num": item['other']['blue_num']
        })










