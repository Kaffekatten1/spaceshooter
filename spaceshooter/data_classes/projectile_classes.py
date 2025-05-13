import math
import pygame
from pygame.math import Vector2

import spaceshooter.data_classes.colors as colors
from spaceshooter.data_classes.parent_classes import ProjectileParent
import spaceshooter.helpers.misc_helpers as mh

class LaserProjectile(ProjectileParent):
    """Laser projectile."""
    def __init__(self, **kwargs):
        """Initialize class."""
        super().__init__(self, **kwargs)

        self.image0 = pygame.transform.scale(pygame.image.load("spaceshooter/Images/Projectiles/laser.png").convert(), (self.width, self.height))
        self.image0.set_colorkey(colors.WHITE)
        self.rect = self.image0.get_rect()

        # Set position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.image, self.rect = mh.rot_center(self.image0, self.angle_deg, self.rect.x, self.rect.y)

    @property
    def delta_time(self):
        """Return time delta."""
        return 1.0 if self.parent is None  else self.parent.delta_time
    
    @property
    def angle_deg(self):
        """Return angle in degrees."""
        return 180 * self.angle / math.pi


    def update(self):
        """Update sprite location"""
        # Get properties
        p = self.position
        v = self.velocity
        vd = self.velocity_drag

        a = self.angle
        av = self.angle_velocity
        avd = self.angle_velocity_drag

        dt = self.delta_time

        # Apply drag
        v1 = v * (1 - vd)
        if abs(v1[0]) < 0.001:
            v1[0] = 0
        if abs(v1[1]) < 0.001:
            v1[1] = 0

        av1 = av * (1 - avd)
        if abs(av1) < 0.001:
            av1 = 0

        # Calculate new position
        p1 = p + v * dt

        # Calculate new angle
        a1 = (a + av1 * dt) % (2 * math.pi)

        # Assign
        self.position.update(p1)
        self.velocity.update(v1) 
        self.angle = a1
        self.angle_velocity = av1

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.image, self.rect = mh.rot_center(self.image0, self.angle_deg, self.rect.x, self.rect.y)

        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

    
    def die(self):
        """Kill the sprite."""
        self.kill()


class HomingMissileProjectile(ProjectileParent):
    """Homing missile projectile."""
    def __init__(self, **kwargs):
        """Initialize class."""
        super().__init__(self, **kwargs)

        self.kill_sound = pygame.mixer.Sound("spaceshooter/Sounds/Weapons/Boom!.wav")

        self.image0 = pygame.transform.scale(pygame.image.load("spaceshooter/Images/Projectiles/missile.png").convert(), (self.width, self.height))
        self.image0.set_colorkey(colors.WHITE)
        self.rect = self.image0.get_rect()

        # Set position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.image, self.rect = mh.rot_center(self.image0, self.angle_deg, self.rect.x, self.rect.y)

        self.target = None
        self.targeting_time = 0.5 / self.delta_time


    @property
    def delta_time(self):
        """Return time delta."""
        return 1.0 if self.parent is None  else self.parent.delta_time
    
    @property
    def angle_deg(self):
        """Return angle in degrees."""
        return 180 * self.angle / math.pi


    def update(self):
        """Update sprite location"""
        # Get properties
        p = self.position
        v = self.velocity
        vd = self.velocity_drag

        a = self.angle
        av = self.angle_velocity
        avd = self.angle_velocity_drag

        dt = self.delta_time

        if self.target is not None:
            ut = (self.target.position - self.position).normalize()
            self.angle = a = math.atan2(-ut.y, ut.x)
            v += 100 * ut

        # Apply drag
        v1 = v * (1 - vd)
        if abs(v1[0]) < 0.001:
            v1[0] = 0
        if abs(v1[1]) < 0.001:
            v1[1] = 0

        av1 = av * (1 - avd)
        if abs(av1) < 0.001:
            av1 = 0

        # Calculate new position
        p1 = p + v * dt

        # Calculate new angle
        a1 = (a + av1 * dt) % (2 * math.pi)

        # Assign
        self.position.update(p1)
        self.velocity.update(v1) 
        self.angle = a1
        self.angle_velocity = av1

        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.image, self.rect = mh.rot_center(self.image0, self.angle_deg, self.rect.x, self.rect.y)

        self.targeting_time -= 1
        if self.targeting_time <= 0:
            # Select target
            targets = self.parent.parent.parent.enemies
            if len(targets) > 0:
                pos = self.position
                self.target = min([t for t in targets], key=lambda t: pos.distance_to(t.position))
                # print(f"{self.name} acquired target: {self.target.name}")
            
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

    
    def die(self):
        """Kill the sprite."""
        self.kill()
        if self.parent.parent.parent.sound_on:
            pygame.mixer.Sound.play(self.kill_sound)