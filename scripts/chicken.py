import random
import math

from scripts.physics_entity import PhysicsEntity
from scripts.item import create_item

class Chicken(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size, e_type='chicken')
        self.drops = [create_item(game, random.choice(['chicken_drumstick']), owner=None) for i in range(random.randint(0, 2))]

        # randomize animation cycle
        self.active_animation.update(random.random() * 10)

        # randomize direction
        self.flip[0] = random.choice([True, False])

    
    def create_particles(self):
        for i in range(12):
            vel = [random.uniform(-10, 0), random.uniform(-120, -60)]
            self.game.world.particle_manager.add_particle(game=self.game, pos=(self.pos[0] + random.random() * self.img.get_width(), self.center[1]), velocity=vel, p_type='feather', decay_rate=0, start_frame=random.randint(0, 4))
    
    def die(self):
        self.dead = True
        for i in range(32):
            angle = i / 16 * math.pi
            self.game.world.spark_manager.add_curved_spark(self.center, angle + random.random() / 5, speed=random.random() * 2 + 1, curve=0, scale=4, decay_rate=0.08)
            
        for item_drop in self.drops:
            self.game.world.entities.drop_item(self.pos.copy(), (1, 1), item_drop, velocity=(random.randint(0, 250) - 150, random.randint(0, 20) - 200))
        
        self.create_particles()
        