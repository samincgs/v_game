

class Camera:
    def __init__(self, game):
        self.game = game
        self.true_pos = [0, 0]
        self.target_pos = [0, 0]
        self.tracked_entity = None
        self.slowness = 40
    
    @property
    def pos(self):
        return (int(self.true_pos[0]), int(self.true_pos[1]))
    
    def smooth_approach(self, val, target, slowness):
        return val + (target - val) / slowness * min(self.game.window.dt * 60, slowness)
    
    def set_tracked_entity(self, entity):
        self.tracked_entity = entity
    
    def set_target(self, pos):
        self.target_pos = list(pos)
    
    def focus(self):
        if self.tracked_entity:
            self.true_pos = [self.tracked_entity.pos[0] - self.game.window.display.get_width() // 2, self.tracked_entity.pos[1] - self.game.window.display.get_height() // 2]
            
    def update(self):
        if self.tracked_entity:
            self.set_target((self.tracked_entity.pos[0] - self.game.window.display.get_width() // 2, self.tracked_entity.pos[1] - self.game.window.display.get_height() // 2))
        
        self.true_pos[0] = self.smooth_approach(self.true_pos[0], self.target_pos[0], self.slowness)
        self.true_pos[1] = self.smooth_approach(self.true_pos[1], self.target_pos[1], self.slowness)
        
        