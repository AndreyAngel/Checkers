class Checker():
    '''  Шашка '''
    def __init__(self, color = 'black', locations = [0, 0], variants = []):
        
        self.color = color
        self.locations = locations
        self.status = 0
        self.variants = []
        self.x = locations[0]
        self.y = locations[1]
        

    def motion(self, board, loc2, loc3, cells):
        ''' Ход '''

        x, y = self.x, self.y # координаты шашки

        board[loc2[0]][loc2[1]], board[x][y] = board[x][y], 0  # обновление мат. модели доcки
        if loc3 != [] and loc3 != None: # если рядом были патенциальные противники
            for i in loc3:

                board[i[0]][i[1]].x = None
                board[i[0]][i[1]].y = None

                board[i[0]][i[1]] = 0   # обновление мат. модели доcки
                cells[i[0]][i[1]].background_normal = ''   # обновление мат. модели доски, содержащей клетки
        
        # обновление математической модели доски
        cells[loc2[0]][loc2[1]].background_normal = cells[x][y].background_normal
        cells[x][y].background_normal = ''

        if board[loc2[0]][loc2[1]].color == 'white': # если ход сделали белые
            if loc2[1] == 7:  # если прошли в дамки
                board[loc2[0]][loc2[1]].status = 1
                cells[loc2[0]][loc2[1]].background_normal = 'templates/missis_white.jpg'

        else:  # если ход сделали чёрные
            if loc2[1] == 0:  # если прошли в дамки
                board[loc2[0]][loc2[1]].status = 1
                cells[loc2[0]][loc2[1]].background_normal = 'templates/missis_black.png'

        self.x = loc2[0]
        self.y = loc2[1]

    def variants_moves(self, board):
        '''  Варианты ходов '''
        variants = []   # список вариантов возможных ходов
        x, y = self.x, self.y  # координаты нажатой клетки

        if board[x][y].status == 0: # если не дамка

            if board[x][y].color == 'white':    # если ходят чёрные
                
                try:
                    ''' вправо вверх '''
                    if board[x+1][y+1]==0 and x+1<=7 and y+1<=7: # если клетка пустая, и не вышли за пределы доски
                        variants.append((x+1, y+1, []))  # добавление варианта хода
                    elif board[x+1][y+1]!=0 and board[x+1][y+1].color != board[x][y].color:  # если клетка непустая, и на ней враг
                        if board[x+2][y+2]==0 and x+2<=7 and y+2<=7: # если клетка за врагом путая, и не вышли за пределы доски
                            variants.append((x+2, y+2, [[x+1, y+1]]))  # добавление варианта хода
                except:
                    pass
                
                try:
                    ''' влево вверх '''
                    if board[x-1][y+1]==0 and x-1>=0 and y+1<=7:
                        variants.append((x-1, y+1, []))
                    elif board[x-1][y+1]!=0 and board[x-1][y+1].color != board[x][y].color:
                        if board[x-2][y+2]==0 and x-2>=0 and y+2<=7:
                            variants.append((x-2, y+2, [[x-1, y+1]]))
                except:
                    pass

                try:
                    ''' влево вниз '''
                    if board[x-1][y-1]!=0 and board[x-1][y-1].color != board[x][y].color:
                        if board[x-2][y-2]==0 and x-2>=0 and y-2>=0:
                            variants.append((x-2, y-2, [[x-1, y-1]]))
                except:
                    pass

                try:
                    ''' вправо вниз '''
                    if board[x+1][y-1]!=0 and board[x+1][y-1].color != board[x][y].color:
                        if board[x+2][y-2]==0 and x+2<=7 and y-2>=0:
                            variants.append((x+2, y-2, [[x+1, y-1]]))
                except:
                    pass


            else:   # если ходят былые
                try:
                    ''' вправо вниз '''
                    if board[x+1][y-1]==0 and x+1<=7 and y-1>=0:
                        variants.append((x+1, y-1, []))
                    elif board[x+1][y-1]!=0 and board[x+1][y-1].color != board[x][y].color:
                        if board[x+2][y-2]==0 and x+2<=7 and y-2>=0:
                            variants.append((x+2, y-2, [[x+1, y-1]]))
                except:
                    pass

                try:
                    ''' влево вниз '''
                    if board[x-1][y-1]==0 and x-1>=0 and y-1>=0:
                        variants.append((x-1, y-1, []))
                    elif board[x-1][y-1]!=0 and board[x-1][y-1].color != board[x][y].color:
                        if board[x-2][y-2]==0 and x-2>=0 and y-2>=0:
                            variants.append((x-2, y-2, [[x-1, y-1]]))
                except:
                    pass

                try:
                    ''' влево вверх '''
                    if board[x-1][y+1]!=0 and board[x-1][y+1].color != board[x][y].color:
                        if board[x-2][y+2]==0 and x-2>=0 and y+2<=7:
                            variants.append((x-2, y+2, [[x-1, y+1]]))
                except:
                    pass

                try:
                    ''' вправо вверх '''
                    if board[x+1][y+1]!=0 and board[x+1][y+1].color != board[x][y].color:
                        if board[x+2][y+2]==0 and x+2<=7 and y+2<=7:
                            variants.append((x+2, y+2, [[x+1, y+1]]))
                except:
                    pass

        else:   # если дамка

            from copy import deepcopy
            self.loc_enemy = []  # список координат врагов
            n = 1  # длина пути от дамки

            ''' влево и вниз '''
            while True:
                if x-n>=0 and x-n<=7 and y-n>=0 and y-n<=7: # если в пределах доски
                    if board[x-n][y-n] == 0:  # если клетка путсая
                        variants.append((x-n, y-n, self.loc_enemy))  # добавление варианта хода
                    else:  # елси клетка занята
                        if board[x-n-1][y-n-1] == 0:  # если клетка за шашкой свободна
                            if board[x-n][y-n].color != board[x][y].color:  # если шашка - враг
                                cop = deepcopy(self.loc_enemy)  # копироавние списка врагов
                                self.loc_enemy = [] # обнуление списка врагов
                                for i in cop:
                                    self.loc_enemy.append(i)
                                self.loc_enemy.append([x-n, y-n])  # добавление координат нового врага
                            else:  # если шашка - союзник
                                n = 1
                                self.loc_enemy = []  # обнуление списка врагов
                                break
                        else:  # если клетка за шашкой занята
                            n = 1
                            self.loc_enemy = []  # обнуление списка врагов
                            break
                else: # если вышли за пределы доски
                    n = 1
                    self.loc_enemy = []  # обнуление списка врагов
                    break
                n += 1

            ''' вправо и вниз '''
            while True:
                if x+n>=0 and x+n<=7 and y-n>=0 and y-n<=7:
                    if board[x+n][y-n] == 0:
                        variants.append((x+n, y-n, self.loc_enemy))
                    elif x+n+1 <= 7:
                        if board[x+n+1][y-n-1] == 0:
                            if board[x+n][y-n].color != board[x][y].color:
                                cop = deepcopy(self.loc_enemy)
                                self.loc_enemy = []
                                for i in cop:
                                    self.loc_enemy.append(i)
                                self.loc_enemy.append([x+n, y-n])
                            else:
                                n = 1
                                self.loc_enemy = []
                                break
                        else:
                            n = 1
                            self.loc_enemy = []
                            break
                    else:
                        n = 1
                        self.loc_enemy = []
                        break
                else:
                    n = 1
                    self.loc_enemy = []
                    break
                n += 1

            ''' влево и вверх '''
            while True:
                if x-n>=0 and x-n<=7 and y+n>=0 and y+n<=7:
                    if board[x-n][y+n] == 0:
                        variants.append((x-n, y+n, self.loc_enemy))
                    elif y+n+1 <= 7:
                        if board[x-n-1][y+n+1] == 0:
                            if board[x-n][y+n].color != board[x][y].color:
                                cop = deepcopy(self.loc_enemy)
                                self.loc_enemy = []
                                for i in cop:
                                    self.loc_enemy.append(i)
                                self.loc_enemy.append([x-n, y+n])
                            else:
                                n = 1
                                self.loc_enemy = []
                                break
                        else:
                            n = 1
                            self.loc_enemy = []
                            break
                    else:
                        n = 1
                        self.loc_enemy = []
                        break
                else:
                    n = 1
                    self.loc_enemy = []
                    break
                n += 1

            ''' вправо и вверх '''
            while True:
                if x+n>=0 and x+n<=7 and y+n>=0 and y+n<=7:
                    if board[x+n][y+n] == 0:
                        variants.append((x+n, y+n, self.loc_enemy))
                    elif x+n+1 <= 7 and y+n+1 <= 7:
                        if board[x+n+1][y+n+1] == 0:
                            if board[x+n][y+n].color != board[x][y].color:
                                cop = deepcopy(self.loc_enemy)
                                self.loc_enemy = []
                                for i in cop:
                                    self.loc_enemy.append(i)
                                self.loc_enemy.append([x+n, y+n])
                            else:
                                self.loc_enemy = []
                                break
                        else:
                            self.loc_enemy = []
                            break
                    else:
                        self.loc_enemy = []
                        break
                else:
                    self.loc_enemy = []
                    break
                n += 1
        print('Прощитаны варианты ходов')
        print(variants)
        self.variants = variants
        return variants