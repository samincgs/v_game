from scripts.window import Window
from scripts.input import Input
from scripts.assets import Assets

class Game:
    def __init__(self):
        self.window = Window(self)
        self.input = Input(self)
        self.assets = Assets()
        
    def update(self):
        while True:
            self.input.update()
            self.window.create()
    
    def run(self):
        self.update()
        
        
if __name__ == '__main__':
    Game().run()