import random
import math

from .spark import CurvedSpark

class Skill:
    def __init__(self, game, owner, skill_name):
        self.game = game
        self.owner = owner
        self.skill_name = skill_name
        
        self.max_amount = 3
        self.amount = self.max_amount
        self.charge = 0
        self.charge_rate = 2
    
    @property
    def img(self):
        dash_img = self.game.assets.misc[self.skill_name]
        return dash_img
    
        
    def update(self, dt):
        if self.amount < self.max_amount:
            self.charge += dt
            if self.charge > self.charge_rate:
                self.amount += 1
                self.charge = 0
                
                
    def use(self):
        if self.amount:
            self.amount -= 1
        
    
                
    def render(self, surf, offset=(0, 0)):
        pass
    
class DashSkill(Skill):
    def __init__(self, game, owner, skill_name):
        super().__init__(game, owner, skill_name)
        self.max_amount = 3
        self.amount = self.max_amount
        self.charge = 0
        self.charge_rate = 2
        
        self.dash_timer = 0
        self.dash_info = []
    
    def update(self, dt):
        super().update(dt)
        
        self.dash_timer = max(0, self.dash_timer - dt)
        
        if self.dash_timer:
            self.game.world.spark_manager.sparks.append(CurvedSpark([self.owner.center[0], self.owner.center[1] + 9], math.pi + self.owner.aim_angle, random.randint(1,10) / 10, random.randint(-40, 40) / 100, scale=1, decay_rate=random.randint(10, 20) / 100))
            if random.randint(1, 3) == 1:
                self.dash_info.append({'pos': self.owner.pos.copy(), 'img': self.owner.img.copy()})
        else:
            self.dash_info = []
        
    def use(self):
        if not self.dash_timer and self.amount:
            self.dash_timer = 0.2
            self.owner.velocity[0] = math.cos(self.owner.aim_angle) * 450 
            self.owner.velocity[1] = math.sin(self.owner.aim_angle) * 450 
            for i in range(12):
                self.game.world.spark_manager.sparks.append(CurvedSpark(self.owner.center.copy(), math.pi + self.owner.aim_angle + random.uniform(-math.pi / 6, math.pi / 6), random.randint(30,80) / 10, random.randint(-10, 10) / 100, scale=2, decay_rate=random.randint(40, 70) / 100))
                
        super().use()
                
    def render(self, surf, offset=(0, 0)):
        for dash in self.dash_info:
            img = dash['img']
            img.set_alpha(45)
            surf.blit(img, (dash['pos'][0] - offset[0], dash['pos'][1] - offset[1]))