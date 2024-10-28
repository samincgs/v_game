from scripts.window import Window
from scripts.input_manager import InputManager
from scripts.asset_manager import AssetManager
from scripts.world import World
from scripts.renderer import Renderer

class Game:
    def __init__(self):
        self.window = Window(self)
        self.input = InputManager(self)
        self.assets = AssetManager()
        self.world = World(self)
        self.renderer = Renderer(self)
        
    def update(self):
        while True:
            self.input.update()
            self.world.update()
            self.renderer.render()
            self.window.create()
    
    def run(self):
        self.update()
        
        
if __name__ == '__main__':
    Game().run()