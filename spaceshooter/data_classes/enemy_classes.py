"""Define ship class."""
import math
import numpy as np
from pygame.math import Vector2
from typing import List
import pygame

import spaceshooter.data_classes.colors as colors
import spaceshooter.helpers.misc_helpers as mh
from spaceshooter.data_classes.parent_classes import PlayerParent
import spaceshooter.data_classes.weapon_classes as weapons
import spaceshooter.data_classes.explosion_classes as explosions

class Enemy(PlayerParent):
    """Enemy class."""
    def __init__(self, **kwargs):
        """Initialize class."""
        super().__init__(**kwargs)

        self.image0 = pygame.transform.scale(pygame.image.load("spaceshooter/Images/Enemies/enemy_default.png").convert(), (self.width, self.height))
        self.image0.set_colorkey(colors.WHITE)
        self.rect = self.image0.get_rect()

        # Set position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.image, self.rect = mh.rot_center(self.image0, self.angle_deg, self.rect.x, self.rect.y)

        # Weapons
        self.primary_weapon = weapons.Laser(parent=self)
        self.secondary_weapon = weapons.HomingMissile(parent=self)

    @property
    def angle_deg(self):
        """Return angle in degrees."""
        return 180 * self.angle / math.pi

    def move_left(self):
        """Move ship left."""
        self.position[0] = max(0, self.position[0] - self.velocity_max * self.delta_time)

    def move_right(self):
        """Move ship right."""
        self.position[0] = min(self.parent.screen_width - self.width, self.position[0] + self.velocity_max * self.delta_time)
        
    def move_up(self):
        """Move ship up."""
        self.position[1] = max(0, self.position[1] - self.velocity_max * self.delta_time)

    def move_down(self):
        """Move ship down."""
        self.position[1] = min(self.parent.screen_height - self.height, self.position[1] + self.velocity_max * self.delta_time)
        
    def fire_primary(self):
        """Fire primary weapon"""
        self.fire_weapon(self.primary_weapon)

    def fire_secondary(self):
        """Fire secondary weapon"""
        self.fire_weapon(self.secondary_weapon)

    def fire_weapon(self, weapon):
        """Fire weapon."""
        if weapon is None:
            return

        plist, momentum, energy = weapon.fire()
        if len(plist) == 0:
            return

        self.parent.add_projectiles(plist)

        v1 = self.velocity
        n = Vector2(math.cos(self.angle), -math.sin(self.angle))
        v2 = v1 - n * momentum / self.mass
        self.velocity.update(v2)

        self.energy -= energy

    def update(self):
        """Update sprite location"""
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.image, self.rect = mh.rot_center(self.image0, self.angle_deg, self.rect.x, self.rect.y)

        self.update_counters()

    def update_counters(self):
        """Update counters."""
        if self.primary_weapon is not None:
            self.primary_weapon.update_counters()
        
        if self.secondary_weapon is not None:
            self.secondary_weapon.update_counters()
    
    def die(self):
        """Kill the sprite."""
        exp = explosions.Explosion(self.position.x, self.position.y)
        self.parent.explosions.add(exp)
        self.kill()

class Ufo(Enemy):
    """Ufo enemy."""
    def __init__(self, **kwargs):
        """Initialize class."""
        if "angle" not in kwargs:
            kwargs["angle"] = math.pi

        super().__init__(**kwargs)

        self.image = pygame.transform.scale(pygame.image.load("spaceshooter/Images/Enemies/ufo.png").convert(), (self.width, self.height))
        self.image.set_colorkey(colors.WHITE)
        self.rect = self.image.get_rect()

    def die(self):
        """Kill the sprite."""
        exp = explosions.Explosion(self.position.x, self.position.y)
        self.parent.explosions.add(exp)
        self.kill()


def get_default_enemy(subtype: str = "Ufo", position: Vector2|List = [0, 0]):
    """Generate an enemy with default settings."""
    #enemy = eval(subtype)
    enemy = Ufo()

    enemy.name = f"Enemy ({subtype})"
    enemy.position.update(position)
    
    return enemy