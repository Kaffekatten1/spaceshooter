import pygame

import spaceshooter.data_classes.colors as colors

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            image = pygame.image.load(f"spaceshooter/Images/Animations/exp{num}.png")
            # image.set_colorkey(colors.WHITE)
            image = pygame.transform.scale(image, (35, 35))
            self.images.append(image)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()