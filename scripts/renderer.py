from scripts.background import Background
from scripts.gui import GUI


class Renderer:
    def __init__(self, game):
        self.game = game
        
        self.background = Background(game)
        self.gui = GUI(game)

    def render(self):
        surf = self.game.window.display
                  
        # self.background.update()
        # self.background.render(surf)
    
        self.game.world.render(surf)
        self.gui.render(surf)
        
        
            
        
        