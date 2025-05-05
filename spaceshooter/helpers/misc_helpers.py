"""Definition for miscellaneous helper functions."""
import pygame

def rot_center(image, angle, x, y):
    """Rotate image around center."""
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

def collide_if_not_self(sprite1, sprite2):
    """Detect collision between unequal sprites."""
    if sprite1 == sprite2:
        return False
    
    return pygame.sprite.collide_mask(sprite1, sprite2)