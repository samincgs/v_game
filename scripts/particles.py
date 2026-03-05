import pygame
import math
import random

import scripts.pgtools as pt

from scripts.pgtools.utils import glow_blit, outline

class ParticleManager(pt.ParticleManager):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.grass_particles = []
        self.destruction_particles = []

    def add_particle(self, *args, **kwargs):
        self.particles.append(Particle(*args, **kwargs))
        
    def add_death_particle(self, *args, **kwargs):
        self.destruction_particles.append(DestructionParticle(*args, **kwargs))
    
    def environment_particles(self):
        # leaf particles
        leaf_extract = ('foliage', (0, 1))
        for tree in self.game.world.tilemap.extract(leaf_extract, keep=True):
            # if the tree is visible on the players screen
            if (self.game.world.camera.pos[0] <=  tree['pos'][0] + self.game.world.tilemap.tiles['foliage'][1].get_width() <= (self.game.world.camera.pos[0] + self.game.window.display.get_width())) or (self.game.world.camera.pos[0] <=  tree['pos'][0] <= (self.game.world.camera.pos[0] + self.game.window.display.get_width())):
                r = pygame.Rect(tree['pos'][0] + 9, tree['pos'][1] + 8, 44, 17)
                if random.randint(0, 1500) < (r.width - r.height):
                    pos = [r.x + random.random() * r.width, r.y + random.random() * r.height]
                    color = (random.randint(100, 150), random.randint(80, 130), random.randint(10, 50))
                    self.particles.append(Particle(self.game, pos, velocity=[random.randint(-60, -35), random.randint(35, 50)], p_type='leaf', start_frame=random.randint(0, 1), custom_color=color, decay_rate=1.4))
            
        # grass particles    
        visible_screen = self.game.world.camera.get_visible_screen
        tile_size = self.game.world.tilemap.tile_size
        player = self.game.world.entities.player
        for y in visible_screen[1]:
            for x in visible_screen[0]:
                tile_loc = (x, y)
                if tile_loc in self.game.world.grass_manager.grass:
                    px_pos = (tile_loc[0] * tile_size, tile_loc[1] * tile_size)
                    if player.rect.collidepoint(px_pos):
                        if random.random() < 0.02 and player.last_movement[0] != 0:
                            grass_tile = self.game.world.grass_manager.grass[tile_loc]
                            img = grass_tile.grass_assets[random.choice(grass_tile.grass_variants)]
                            color = None
                            for i in range(random.randint(3, 7)):
                                while True:
                                    img_color_loc = (random.randint(0, img.get_width() - 1), random.randint(0, img.get_height() - 1))
                                    color = img.get_at(img_color_loc)
                                    if color != (0, 0, 0, 255):
                                        break 
                                self.particles.append(Particle(self.game, (player.center[0], player.rect.bottom), [random.uniform(-50, 50), random.uniform(-80, -50)], 'p', start_frame=random.choice([4, 4, 5]), custom_color=color, decay_rate=0.4, gravity=random.uniform(140, 200), terminal_velocity=200))
                                
    def update(self, dt):   
        for particle in self.destruction_particles.copy():
            kill = particle.update(dt)
            if kill:
                self.destruction_particles.remove(particle)
                
        for particle in self.particles.copy():
            kill = particle.update(dt)
            if kill:
                self.particles.remove(particle)
        
        self.environment_particles()
        

    def render(self, surf, offset=(0, 0)):
        for particle in self.destruction_particles:
            particle.render(surf, offset=offset)
    
        for particle in self.particles:
            particle.render(surf, offset=offset)
            

class Particle(pt.Particle):
    def __init__(self, game, pos, velocity, p_type, gravity=0, terminal_velocity=None, decay_rate=0.1, start_frame=0, custom_color=None, custom_func=None, physics=None, damping=(0.8, -0.7), glow=None, glow_radius=None, scale=1, grass_effect=(1, 3)):
        super().__init__(game, pos, velocity, p_type, decay_rate, start_frame, custom_color, custom_func, physics, damping, glow, glow_radius)
        self.spawn = True
        self.terminal_velocity = terminal_velocity
        self.grass_effect = grass_effect
        self.wind_force = 0
        self.scale = scale
        self.gravity = gravity
        self.phase = random.uniform(0, math.pi * 2)
        self.timer = 0
        
    def update(self, dt):    
        if not self.physics:
            self.velocity[1] += self.gravity * dt
            if self.terminal_velocity:
                self.velocity[1] = min(self.velocity[1], self.terminal_velocity)
            self.pos[0] += self.velocity[0] * dt
            self.pos[1] += self.velocity[1] * dt
        else:
            # horizontal collision
            hit = False
            self.pos[0] += self.velocity[0] * dt
            if self.physics.tile_collide(self.pos):
                self.velocity[0] *= -0.7
                self.velocity[1] *= 0.8
                hit = True
            # vertical collision
            self.pos[1] += self.velocity[1] * dt
            if self.physics.tile_collide(self.pos):
                self.velocity[0] *= 0.8
                self.velocity[1] *= -0.7
                hit = True
            if hit:
                self.pos[0] += self.velocity[0] * dt * 2
                self.pos[1] += self.velocity[1] * dt * 2
        
        if self.type in ['shells', 'mag']:
            self.velocity[1] += 300 * dt
            abs_motion = abs(self.velocity[1]) + abs(self.velocity[0])
            if abs_motion > 20:
                self.rotation += 20 * dt * abs_motion
        elif self.type == 'leaf':
            # TODO: fix sin wave
            self.pos[0] += math.sin(self.frame * 0.76) * 0.21
        elif self.type == 'feather':
            self.timer += dt            
            
            self.velocity[1] = min(150, self.velocity[1] + 100 * dt)
            self.pos[0] += math.sin(self.game.world.master_clock * 2 + self.phase) * 1.1
            
        force_point = (self.rect.centerx, self.rect.bottom)
        self.game.world.grass_manager.apply_bend(force_point, self.grass_effect[0], self.grass_effect[1])   
        
        self.frame += self.decay_rate * dt
        self.frame = min(self.frame, len(self.active_animation.images))
        if self.frame >= len(self.active_animation.images):
            self.despawn = True
        
        if self.timer > 5:
            self.despawn = True
        
        return self.despawn
    
    def render(self, surf, offset=(0,0)):
        img = self.img
        render_pos = (self.pos[0] - img.get_width() // 2 - offset[0], self.pos[1] - img.get_height() // 2 - offset[1] + 1)
        if self.scale != 1:
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
        if self.custom_color:
            img = pt.utils.palette_swap(img, (255, 255, 255), self.custom_color)
            img.set_colorkey((0, 0, 0))
        if self.rotation:
            img = pygame.transform.rotate(img, self.rotation)
        if self.outline:
            outline(surf, img, render_pos, self.outline)
        surf.blit(img, render_pos)
        if self.glow:
            glow_blit(surf, (self.pos[0] - offset[0] - self.glow_radius, self.pos[1] - offset[1] - self.glow_radius), self.glow_radius, self.glow)
        

class DestructionParticle:
    def __init__(self, game, img, pos, rot, rot_speed, decay_rate, velocity, duration=3, physics=None):
        self.game = game
        self.img = img
        self.pos = list(pos)
        self.rotation = rot
        self.rotation_speed = rot_speed
        self.velocity = list(velocity)
        self.physics = physics
        self.rotation = 0
        self.duration = duration
        self.decay_rate = decay_rate
        
    def update(self, dt):
        
        self.pos[0] += self.velocity[0] * dt
        self.pos[1] += self.velocity[1] * dt
        
        self.velocity[1] = min(300, self.velocity[1] + dt * 500)
        
        self.rotation += self.rotation_speed * dt 

        self.duration -= max(self.decay_rate * dt, 0)
        if self.duration <= 0:
            return self.duration

    
    def render(self, surf, offset=(0, 0)):
        img = self.img.copy()
        if self.rotation:
            img = pygame.transform.rotate(self.img, self.rotation)
        surf.blit(img, (self.pos[0] - self.img.get_width() // 2 - offset[0], self.pos[1] - self.img.get_height() // 2 - offset[1]))
             

            
     
                       