import random

from scripts.physics_entity import PhysicsEntity

class Chicken(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, e_type='chicken')

        # randomize animation cycle
        self.active_animation.update(random.random() * 10)

        # randomize direction
        self.flip[0] = random.choice([True, False])

    
    def create_particles(self, color):
        for i in range(32):
            vel = [-100 + random.random() * 200, -100 + random.random() * 200]
            frame = 1 + random.random()
            self.game.world.particle_manager.add_particle(self.game, 'feather', self.center, vel, decay_rate=7 + random.random(), frame=frame)

    
    def die(self):
        self.create_particles((255, 255, 255))

        super().die()