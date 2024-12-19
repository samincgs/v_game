from scripts.window import Window
from scripts.input import Input
from scripts.assets import Assets
from scripts.world import World
from scripts.renderer import Renderer

class Game:
    def __init__(self):
        self.window = Window(self)
        self.input = Input(self)
        self.assets = Assets()
        self.renderer = Renderer(self) 
        self.world = World(self)

    def run(self):
        while True: 
            self.input.update()
            self.renderer.render()
            self.world.update()
            self.window.create()
            
if __name__ == '__main__':
    Game().run() 