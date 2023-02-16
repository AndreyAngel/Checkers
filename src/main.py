from interface import GameApp
from kivy import Config

Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'resizable', 1)

if __name__ == "__main__":
    A = GameApp()
    A.run()