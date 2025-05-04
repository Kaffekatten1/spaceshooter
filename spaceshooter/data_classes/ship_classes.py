"""Define ship class."""
import math
import numpy as np
from pygame.math import Vector2
from typing import List
import pygame

import spaceshooter.data_classes.colors as colors
from spaceshooter.data_classes.parent_classes import PlayerParent

class Ship(PlayerParent):
    """Ship class."""
    def __init__(self, boost_acceleration: float = 0, lives: int = 3, **kwargs):
        """Initialize class."""
        super().__init__(**kwargs)

        self.boost_acceleration = boost_acceleration

        self.image = pygame.transform.scale(pygame.image.load("spaceshooter/Images/Ships/ship_default.png").convert(), (self.width, self.height))
        self.image.set_colorkey(colors.WHITE)
        self.rect = self.image.get_rect()

        # Set position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.lives = lives
        self.score = 0

        # Weapons
        self.primary_weapon = None  #Laser(parent=self)
        self.secondary_weapon = None  #HomingMissile(parent=self)

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

        projectile, momentum, energy = weapon.fire()
        if projectile is None:
            return

        self.parent.add_projectile(projectile)

        v1 = self.velocity
        n = Vector2(math.cos(self.angle), -math.sin(self.angle))
        v2 = v1 - n * momentum / self.mass
        self.velocity.update(v2)

        self.energy -= energy

    def update(self):
        """Update sprite location"""
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]

        self.update_counters()

    def update_counters(self):
        """Update counters."""
        if self.primary_weapon is not None:
            self.primary_weapon.update_counters()
        
        if self.secondary_weapon is not None:
            self.secondary_weapon.update_counters()
    
    def die(self):
        """Kill the sprite."""
        self.kill()


def get_default_ship(player:int = 1):
    """Generate a ship with default settings."""
    ship = Ship(
        name = f"Player {player}",
        height = 35,
        width = 35,
        radius = 35,
        mass = 1,
        velocity_max = 300
        )

    if player == 1:
        ship.control_dict = {
            pygame.K_a: ship.move_left,
            pygame.K_d: ship.move_right,
            pygame.K_w: ship.move_up,
            pygame.K_s: ship.move_down,
            pygame.K_LSHIFT: ship.fire_primary,
            pygame.K_LCTRL: ship.fire_secondary,
        }
    else:
        ship.control_dict = {
            pygame.K_LEFT: ship.move_left,
            pygame.K_RIGHT: ship.move_right,
            pygame.K_UP: ship.move_up,
            pygame.K_DOWN: ship.move_down,
            pygame.K_RETURN: ship.fire_primary,
            pygame.K_RSHIFT: ship.fire_secondary,
        }

    return ship