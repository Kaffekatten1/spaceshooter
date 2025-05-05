"""Definition of parent classes for all custom sprites."""
import math
from pathlib import Path
import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
from typing import List, Tuple

# %% Top-level parent
class SpriteParent(Sprite):
    """Top-level parent class"""
    def __init__(
            self, 
            parent = None,
            name: str = "",
            height: int = 30,
            width: int = 30,
            radius: float = 30
            ):
        """Initialize class."""
        super().__init__()

        self.parent = parent
        self.name = name
        self.height = height
        self.width = width
        self.radius = radius


class MovableSprite(SpriteParent):
    """Parent class defining movement properties."""
    def __init__(
            self, 
            mass: float = 1, 
            position: List[float]|Vector2 = [0, 0], 
            velocity: List[float]|Vector2 = [0, 0], 
            velocity_max: float = 10,
            velocity_drag: float = 0,
            angle: float = 0, 
            angle_velocity: float = 0,
            angle_velocity_max: float = 0,
            angle_velocity_drag: float = 0,
            health : int = 100,
            **kwargs
            ):
        """Initialize class."""
        super().__init__(**kwargs)

        self.mass = mass

        self.position = Vector2(position)
        self.velocity = Vector2(velocity)
        self.velocity_max = velocity_max

        self.angle = angle
        self.angle_velocity = angle_velocity
        self.angle_velocity_max = angle_velocity_max

        self.velocity_drag = velocity_drag
        self.angle_velocity_drag = angle_velocity_drag

        self.health = health


class PlayerParent(MovableSprite):
    """Parent class for player."""
    def __init__(
            self, 
            acceleration: float = 0.05,
            angle_acceleration: float = 0.005,
            energy: int = 100,
            energy_regen: int = 1,
            score: int = 0,
            control_dict: dict = {},
            **kwargs
            ):
        """Initialize class."""
        super().__init__(**kwargs)

        self.acceleration = acceleration
        self.angle_acceleration = angle_acceleration
        self.energy = energy
        self.energy_regen = energy_regen
        self.score = score
        self.control_dict = control_dict


    @property
    def delta_time(self):
        """Return time delta."""
        return 1.0 if self.parent is None or self.parent.fps == 0 else 1.0 / self.parent.fps

    def key_press(self):
        """React to key press."""
        # Get pressed keys
        keys = pygame.key.get_pressed()

        for key, action in self.control_dict.items():
            # Check if key is relevant
            if keys[key]:
                action()
            
class WeaponParent(pygame.sprite.Sprite):
    """Parent class for weapons."""
    def __init__(
            self, 
            parent = None,
            name: str = "", 
            fire_rate: float = 1, 
            damage: int = 1, 
            energy_cost: int = 1, 
            projectile_mass: float = 1,
            projectile_initial_velocity: float = 1, 
            projectile_final_velocity: float = 5,
            level: int = 1,
            nprojectiles: int = 1):
        """Initialize class."""
        super().__init__()

        self.parent = parent
        self.name = name
        self.fire_rate = fire_rate
        self.damage = damage
        self.energy_cost = energy_cost
        self.projectile_mass = projectile_mass
        self.projectile_initial_velocity = projectile_initial_velocity
        self.projectile_final_velocity = projectile_final_velocity
        self.level = level
        self.nprojectiles = nprojectiles

        self.cooldown = 0

    def update_counters(self):
        """Update counters."""
        self.cooldown = max(0, self.cooldown - 1)

    
    def fire(self) -> Tuple:
        """Fire weapon."""
        projectile = None
        momentum = self.projectile_mass * self.projectile_initial_velocity
        energy = self.energy_cost

        # Check cooldown
        if self.cooldown > 0:
            return projectile, momentum, energy
        
        print("Pew pew")
        self.cooldown = 1 / (self.fire_rate * self.delta_time)
        return projectile, momentum, energy

class ProjectileParent(MovableSprite):
    """Projectile parent class."""
    def __init__(
            self,
            initial_velocity: float = 1,
            final_velocity: float = 5,
            damage: int = 1,
            lifetime: int = 1,
            **kwargs):
        """Initialize class."""
        super().__init__(**kwargs)

        self.initial_velocity = initial_velocity
        self.final_velocity = final_velocity
        self.damage = damage
        self.lifetime = lifetime

