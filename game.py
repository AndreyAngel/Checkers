from checker import Checker
from board import Board

class Game(Checker, Board):

    def __init__(self):

        super().__init__()

    def start_game(self, cells):

        self.variants = []                      # варианты ходов одной шашки
        self.variants_all = []                  # все возможные варианты ходов на доске
        self.n = 0                              # номер нажатия на клетки одним игроком
        self.cells = cells                      # Математическая модель доски, содержащая клетки
        self.queue = 'white'                    # Очерёдность хода
        self.board = Board.create_board(self)   # Математическая модель доски, содежращая фигуры
        self.__arrangement_figures()            # Расстановка фигур
        self.all_variants()                     # считаются все варианты ходов на доске

    def get_coordinate(self):
        with open('coord.txt') as file:
            x, y = file.readline().split()
            print('Получение координат')
            self.click([int(x), int(y)])

    def __arrangement_figures(self):
        '''  Расстановка фигур '''

        '''  Белые '''
        for i in range(0, 7, 2):
            for j in range(3):
                if j % 2 == 0:
                    self.board[i][j] = Checker('white', [i, j])
                else:
                    self.board[i+1][j] = Checker('white', [i+1, j])

        ''' Чёрные '''
        for i in range(0, 7, 2):
            for j in range(7, 4, -1):
                if j % 2 == 0:
                    self.board[i][j] = Checker('black', [i, j])
                else:
                    self.board[i+1][j] = Checker('black', [i+1, j])

        print('Шашки расставлены')

    def click(self, locations):
        '''  Нажатие на фигуру '''
        if self.n == 0:  # первое нажатие
            # если клетка не пустая и цвет шашки совпадает цвету в очереди:
            if self.board[locations[0]][locations[1]] != 0 and self.board[locations[0]][locations[1]].color == self.queue:
                self.variants = []   # обнуление вариантов ходов одной шашки
                self.variants = self.board[locations[0]][locations[1]].variants_moves(self.board)   # заполнение списка возможных ходов

                # проверка совпадение вариантовы ходов выбранной шашки вариантам, возможным в игре в данный момент
                count = 0 # кол-во удалённых эелементов
                if not(self.variants in self.variants_all):
                    for i in range(len(self.variants)):
                        if self.variants[i-count][2] == []:
                            self.variants.pop(i-count)
                            count += 1
                print('Разрешённые варианты', self.variants)

                self.loc = locations  # координаты нажатой кетки
                self.n = 1
                Board.cell_illumination(self, 1, locations, self.cells, self.variants) # подстветка клетки

        elif self.n == 1:  # второе нажатие
            self.n = 0
            if locations == self.loc: # если координаты первого клика СОВПАДАЮТ с координатами второго
                self.variants = []    # обнуление вариантов ходов
                Board.cell_illumination(self, 0, locations, self.cells, self.variants)  # отключение подстветки

            else: # если координаты первого клика НЕ СОВПАДАЮТ с координатами второго
                try:
                    for i in self.variants:
                        if i[0] == locations[0] and i[1] == locations[1]:
                            # если координаты клика совпадают с одним из вариантов ходов
                            loc3 = i[2]  # координаты потенциальных врагов
                            
                    self.variants = []    # обнуление вариантов ходов
                    Board.cell_illumination(self, 0, locations, self.cells, self.variants)  # отключение подстветки
                    self.board[self.loc[0]][self.loc[1]].motion(self.board, locations, loc3, self.cells)  # ход
                    
                    self.__changing_queue()  # смена очереди хода
                    self.all_variants()      # считаются все варианты ходов на доске

                    if len(loc3) != 0: # если уничтожили врага, то автоматически происходит клик
                        self.n = 2
                        self.click(locations)
                        self.__changing_queue()

                except:
                    pass

        else:  # проверка второго хода подряд

            self.variants = []   # варианты ходов
            self.variants = self.board[locations[0]][locations[1]].variants_moves(self.board)  # заполнение списка возможных ходов
            self.loc = locations  # координаты нажатой кетки

            list_del = []  # список ходов, которые не приведут к уничтожению противника
            for i in self.variants:
                if i[2] == []: # если противника нет:
                    list_del.append(i)        

            for i in list_del:
                # удаление координат ход, которые не приведут к уничтожению противника, из списка возможных ходов
                self.variants.remove(i)

            if len(self.variants) != 0:  # если остались варианты ходов
                self.n = 1
                Board.cell_illumination(self, 1, locations, self.cells, self.variants) # подсветка клетки
            else:  # если нет возможных ходов
                self.n = 0
                self.__changing_queue()  # изменение очереди хода

    def __changing_queue(self):
        ''' Изменение очериди хода '''

        if self.queue == 'white':
            self.queue = 'black'
        else:
            self.queue = 'white'

    def all_variants(self):
        ''' Возвращает все возможные варианты ходов на доске '''

        flag = False
        flag2 = False
        self.variants_all = []
        for i in self.board:
            for j in i:
                if j != 0:   # если клетка не пустая
                    if j.color == self.queue:    # если цвет шашки совпадает с очередью хода
                        variant = j.variants_moves(self.board)
                        if flag == False:
                            self.variants_all.append(variant)
                        
                        for k in variant:
                            if k[2] != []:
                                flag = True
                                if flag2 == False:
                                    self.variants_all = []
                                    flag2 = True
                                self.variants_all.append(k)
        print('Все варианты на доске:', self.variants_all)
        return self.variants_all

    def __del__(self):
        print("delete game")
