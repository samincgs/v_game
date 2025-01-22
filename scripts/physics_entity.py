from .entity import Entity
from .utils import normalize


class PhysicsEntity(Entity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        self.velocity = [0, 0]
        self.velocity_normalization = [250, 250]
        
    def update(self, dt):
        r = super().update(dt)
        
        self.velocity[0] = normalize(self.velocity[0], self.velocity_normalization[0] * dt)
        self.velocity[1] = normalize(self.velocity[1], self.velocity_normalization[1] * dt)
        
        self.motion = self.velocity.copy()
        
        self.motion[0] *= dt
        self.motion[1] *= dt
                      
        last_collisions = self.collisions(self.game.world.tilemap, movement=self.motion)
        
        if last_collisions['bottom']:
            self.velocity[1] = 0
          
        self.velocity[1] = min(500, self.velocity[1] + dt * 700)
           
        return r