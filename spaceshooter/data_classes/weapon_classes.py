import math
import pygame

from spaceshooter.data_classes.parent_classes import WeaponParent
import spaceshooter.data_classes.projectile_classes as projectiles

class Laser(WeaponParent):
    """Laser weapon."""
    def __init__(self, **kwargs):
        """Initialize class."""
        super().__init__(
            fire_rate=1,
            projectile_initial_velocity=50,
            projectile_mass = 0,
            energy_cost=0,
            **kwargs
        )

    @property
    def delta_time(self):
        """Return time delta."""
        return 1.0 if self.parent is None or self.parent.parent.fps == 0 else 1.0 / self.parent.parent.fps

    def set_level(self, level):
        """Set weapon level."""
        if level == 1:
            self.nprojectiles = 1
            self.fire_rate = 1
        elif level == 2:
            self.nprojectiles = 1
            self.fire_rate = 2
        elif level == 3:
            self.nprojectiles = 3
            self.fire_rate = 2
        elif level == 4:
            self.nprojectiles = 3
            self.fire_rate = 5
        elif level == 5:
            self.nprojectiles = 5
            self.fire_rate = 7

        self.level = level

    def fire(self):
        """Fire weapon."""
        ship = self.parent

        plist = []
        momentum = self.nprojectiles * self.projectile_mass * self.projectile_initial_velocity
        energy = self.energy_cost

        # Check cooldown
        if self.cooldown > 0 or self.energy_cost > ship.energy:
            return plist, momentum, energy
        
        self.cooldown = 1 / (self.fire_rate * self.delta_time)

        px, py = ship.rect.center
        a = ship.angle
        px += (ship.radius + 30) * math.cos(a)
        py -= (ship.radius + 30) * math.sin(a)

        da = math.pi * 10 / 180
        a = ship.angle - self.nprojectiles // 2 * da
        for ii in range(self.nprojectiles):
            vx = self.projectile_initial_velocity / self.delta_time * math.cos(a)
            vy = - self.projectile_initial_velocity / self.delta_time * math.sin(a)

            plist.append(projectiles.LaserProjectile(
                parent=self,
                name=f"Laser pulse from {ship.name}",
                mass=self.projectile_mass,
                lifetime=3 / self.delta_time,
                health=1,
                height=7,
                width=30,
                radius=20,
                position=[px, py],
                velocity=[vx, vy],
                angle=a,
            ))

            a += da

        return plist, momentum, energy


class HomingMissile(WeaponParent):
    """Homing missile weapon."""
    def __init__(self, **kwargs):
        """Initialize class."""
        super().__init__(
            fire_rate=0.5,
            projectile_initial_velocity=20,
            projectile_mass=0,
            energy_cost=0,
            **kwargs
        )

    @property
    def delta_time(self):
        """Return time delta."""
        return 1.0 if self.parent is None or self.parent.parent.fps == 0 else 1.0 / self.parent.parent.fps

    def set_level(self, level):
        """Set weapon level."""
        if level == 1:
            self.nprojectiles = 1
            self.fire_rate = 0.5
        elif level == 2:
            self.nprojectiles = 1
            self.fire_rate = 1
        elif level == 3:
            self.nprojectiles = 2
            self.fire_rate = 1
        elif level == 4:
            self.nprojectiles = 2
            self.fire_rate = 1.5
        elif level == 5:
            self.nprojectiles = 3
            self.fire_rate = 1.5

        self.level = level

    def fire(self):
        """Fire weapon."""
        ship = self.parent

        plist = []
        momentum = self.projectile_mass * self.projectile_initial_velocity
        energy = self.energy_cost

        # Check cooldown
        if self.cooldown > 0 or self.energy_cost > ship.energy:
            return plist, momentum, energy
        
        self.cooldown = 1 / (self.fire_rate * self.delta_time)

        px0, py0 = ship.rect.center        

        da = math.pi * 135 / 180
        a = ship.angle - self.nprojectiles // 2 * da
        for ii in range(self.nprojectiles):
            px = px0 + (ship.radius + 30) * math.cos(a)
            py = py0 - (ship.radius + 30) * math.sin(a)

            vx = self.projectile_initial_velocity / self.delta_time * math.cos(a)
            vy = - self.projectile_initial_velocity / self.delta_time * math.sin(a)

            plist.append(projectiles.HomingMissileProjectile(
                parent=self,
                name=f"Homing missile from {ship.name}",
                mass=self.projectile_mass,
                lifetime=2 / self.delta_time,
                health=1,
                height=15,
                width=15,
                radius=15,
                position=[px, py],
                velocity=[vx, vy],
                angle=a,
                velocity_drag=0.1
            ))

            a += da

        return plist, momentum, energy
