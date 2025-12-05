from scripts.entity import Entity
import scripts.pgtools as pt


class PhysicsEntity(Entity, pt.PhysicsEntity):
    def __init__(self, game, pos, size, e_type):
        super().__init__(game, pos, size, e_type)
        
        self.gravity = 600
        self.terminal_velocity = 400
        self.horizontal_normalization = 250
        
    def update(self, dt):
        r = super().update(dt)
        
        self.velocity[0] = pt.utils.normalize(self.velocity[0], self.horizontal_normalization * dt)
        self.velocity[1] = min(self.terminal_velocity, self.velocity[1] + dt * self.gravity)
        
        self.frame_movement[0] = self.velocity[0] * dt
        self.frame_movement[1] = self.velocity[1] * dt
        
        self.physics_movement(self.game.world.tilemap, self.frame_movement)
        
        return r
        