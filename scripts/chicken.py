import random

from scripts.physics_entity import PhysicsEntity

class Chicken(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, e_type='chicken')

        # randomize animation cycle
        self.active_animation.update(random.random() * 10)

        # randomize direction
        self.flip[0] = random.choice([True, False])

    
    def create_particles(self):
        for i in range(12):
            vel = [random.uniform(-10, 0), random.uniform(-200, -130)]
            self.game.world.particle_manager.add_particle(game=self.game, pos=(self.pos[0] + random.random() * self.img.get_width(), self.center[1]), velocity=vel, p_type='feather', decay_rate=0, start_frame=random.randint(0, 4))
    
    def die(self):
        super().die()
        self.create_particles()
        