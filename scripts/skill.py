import random
import math

from scripts.item import Item

class Skill(Item):
    def __init__(self, game, owner, skill_name, tags=None):
        super().__init__(game, skill_name, owner, tags=tags + ['skill'])
        self.skill_name = skill_name
        
        self.max_count = 3
        self.count = self.max_count
        self.charge = 0
        self.charge_rate = 2
    
    @property
    def img(self):
        img = self.game.assets.misc[self.skill_name]
        return img
    
        
    def update(self, dt):
        if self.count < self.max_count:
            self.charge += dt
            if self.charge > self.charge_rate:
                self.count += 1
                self.charge = 0
                
                
    def use(self):
        if self.count:
            self.count -= 1

    def render(self, surf, offset=(0, 0)):
        pass
    
class DashSkill(Skill):
    def __init__(self, game, owner, skill_name, tags):
        super().__init__(game, owner, skill_name, tags)
        self.max_count = 3
        self.count = self.max_count
        self.charge = 0
        self.charge_rate = 2
        
        self.dash_force = 450
        self.dash_timer = 0
        self.dash_info = []
    
    def create_particles(self, color):
        for i in range(32):
            vel = [-100 + random.random() * 200, -100 + random.random() * 200]
            frame = 1 + random.random()
            self.game.world.particle_manager.add_particle(self.game, 'p', self.owner.center, vel, decay_rate=7 + random.random(), frame=frame, custom_color=color)

    def update(self, dt):
        super().update(dt)
        
        self.dash_timer = max(0, self.dash_timer - dt)
        if self.dash_timer:
            if random.randint(1, 3) == 1:
                self.dash_info.append({'pos': self.owner.pos.copy(), 'img': self.owner.img.copy()})
        else:
            if len(self.dash_info): # when it ends 
                self.create_particles((255, 255, 255))
            self.dash_info = []
        
        
    def use(self):
        if not self.dash_timer and self.count:
            self.dash_timer = 0.3
            self.owner.velocity[0] = math.cos(self.owner.aim_angle) * self.dash_force 
            self.owner.velocity[1] = math.sin(self.owner.aim_angle) * self.dash_force 
            self.create_particles((255, 255, 255))
                
        super().use()
                
    def render(self, surf, offset=(0, 0)):
        for dash in self.dash_info:
            img = dash['img']
            img.set_alpha(80)
            surf.blit(img, (dash['pos'][0] - offset[0], dash['pos'][1] - offset[1]))
            
            
SKILLS_MAP = {
    'dash': DashSkill
}