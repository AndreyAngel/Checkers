from tkinter import W
from kivy.uix.button import Button

class Cell(Button):
    ''' клетка '''
    def __init__(self, x=None, y=None, background_color='#deb887', background_normal = '', **kwargs):

        super().__init__(background_color=background_color, background_normal=background_normal, on_release = kwargs['on_release'])
        self.a = x
        self.b = y

    def on_press(self):
        ''' Нажатие на клетку '''

        # запись координат клика
        with open('coord.txt', W) as file:
            file.write(f'{self.a} {self.b}')
        print('Отправка координат')



class Board(Cell):
    ''' доска '''
    def __init__(self):

        super().__init__()
        self.color1 = 'black'
        self.color2 = 'white'
        self.last_click = []  # координаты следущего возможного клика

    def create_board(self):
        '''  Создание математической модели доски '''
        print('Доска создана')
        return [[0]*8 for _ in range(8)]

    def cell_illumination(self, status, locations, cells, variants):
        ''' Подстветка клетки '''

        if variants != []:
            if status == 1:
                # включить подсветку
                print('Клетка подсвечена')
                self.last_click = [locations, variants]

                cells[locations[0]][locations[1]].background_color = 'green'

                for i in variants:
                    cells[i[0]][i[1]].background_color = 'green'
                    try:
                        for j in i[2]:
                            cells[j[0]][j[1]].background_color = 'red'
                    except:
                        pass
                    

        if status == 0:
            # отключить подстветку
            print('Подсветка отключена')
            cells[self.last_click[0][0]][self.last_click[0][1]].background_color = '#dd3cd'

            for i in self.last_click[1]:
                cells[i[0]][i[1]].background_color = '#dd3cd'
                try:
                    for j in i[2]:
                        cells[j[0]][j[1]].background_color = '#dd3cd'
                except:
                    pass
    
    def __del__(self):
        print("delete board")