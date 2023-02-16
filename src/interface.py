from kivy.uix.button import Button
from kivy import Config

Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'resizable', 1)

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from board import Cell
from game import Game


class GameApp(App):

    def build(self):

        ''' Представление интерфеса (окна) '''

        self.title = "Шашки"

        self.interface = BoxLayout(orientation = 'vertical') # интерфейс
        self.toolbar = BoxLayout(size_hint = (1, 0.1)) # панель инструментов
        self.game_board = GridLayout(cols = 8, rows = 8) # доска

        self.board = [] # инициализация математической модели доски

        self.color1 = '#deb887' #светлый
        self.color2 = '#dd3cd'  #тёмный

        print('Окно создано')

        self.create_board()

        self.interface.add_widget(self.game_board)
        self.interface.add_widget(self.toolbar)

        self.toolbar.add_widget(Button(text = 'Готов!', on_press = lambda x: self.start()))
        self.toolbar.add_widget(Button(text = 'Заново', on_press = lambda x: self.start_over()))

        return self.interface

    def create_board(self):
        
        ''' Создание экземпляров класса Клетка и рассатановка шашек по клеткам '''

        self.cells = [[0]*8 for _ in range(8)] # математическая модель доски, содержащая экземпляры клеток

        for i in range(7, -1, -1):
            for j in range(8):

                if i % 2 == 0 and j % 2 == 0:
                    if i == 6:
                        cell = Cell(j, i, self.color2, 'templates/checker_black.jpg', on_release = lambda x: self.release())
                    elif i == 0 or i == 2:
                        cell = Cell(j, i, self.color2, 'templates/checkers_white.png', on_release = lambda x: self.release())
                    else:
                        cell = Cell(j, i, self.color2, on_release = lambda x: self.release())

                elif i % 2 != 0 and j % 2 != 0:
                    if i == 7 or i == 5:
                        cell = Cell(j, i, self.color2, 'templates/checker_black.jpg', on_release = lambda x: self.release())
                    elif i == 1:
                        cell = Cell(j, i, self.color2, 'templates/checkers_white.png', on_release = lambda x: self.release())
                    else:
                        cell = Cell(j, i, self.color2, on_release = lambda x: self.release())

                else:
                    cell = Cell(j, i, on_release = lambda x: self.release())

                self.game_board.add_widget(cell)
                self.cells[j][i] = cell
        print('Доска создана')

    def start(self):
        ''' начало игры '''
        print('Запуск игры')
        self.MyGame = Game()
        self.MyGame.start_game(self.cells)

    def start_over(self):
        ''' начать заново '''

        # удаление старой игры
        del self.MyGame
        self.game_board.clear_widgets()

        # создание новой игры
        self.create_board()
        self.MyGame = Game()
        self.MyGame.start_game(self.cells)

    def release(self):
        try:
            print('Отправка сигнала о нажатии кнопки')
            self.MyGame.get_coordinate()
        except:
            pass