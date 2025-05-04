"""Definition for game classes."""
import math
import random
import pygame

import spaceshooter.data_classes.colors as colors
from spaceshooter.data_classes.ship_classes import get_default_ship

class SpaceshooterGame:
    """Spaceshooter game class."""
    def __init__(
            self, 
            name: str = "Spaceshooter", 
            screen_height: int = 600,
            screen_width: int = 800,
            background_filepath: str = "spaceshooter/Images/Backgrounds/Blue Nebula 1 - 1024x1024.png",
            fps: int = 30):
        """Initialize class."""
        self.name = name
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.background_filepath = background_filepath
        self.fps = fps
        self.score = 0
        self.text_color = colors.WHITE
        self.text_color_background = colors.BLACK
        
        self.background_image = None
        self.screen = None
        self.isrunning = False

        self.bg_x = 0
        self.bg_dx = 3

        self.clock = pygame.time.Clock()
        self.gametime = 0

        self.lives = 3

        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.on_init()

    @property
    def screen_size(self):
        """Return screen size."""
        return (self.screen_width, self.screen_height)
    
    def get_background_image(self):
        """Return background as image."""
        if self.background_filepath == "":
            return None
        
        return self.background_image if self.background_image is not None else pygame.image.load(self.background_filepath).convert()

    def on_init(self):
        """Initialize game."""
        pygame.init()
      
        # Set up the game window    
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption(self.name)

        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

        # Create players
        for ii in range(1, 3, 1):
            ship = get_default_ship(ii)
            ship.position.update(50, ii * self.screen_height // 3)
            self.add_player(ship)

        self.isrunning = True
 
    def on_event(self, event):
        # Handle events
        if event.type == pygame.QUIT:
            self.isrunning = False

        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            self.isrunning = False
        
    def on_loop(self):
        """Update game."""

        # Handle key press
        for player in self.players:
            player.key_press()

        # Handle movement
        self.all_sprites.update()


    def on_render(self):
        """Draw screen.""" 
        bg = self.get_background_image()
        bg_w = bg.get_width()
        if bg is None:
            self.screen.fill(colors.BLACK)
        else:
            self.screen.blit(bg, (self.bg_x, 0))
            self.screen.blit(bg, (self.bg_x + bg_w, 0))
            self.screen.blit(bg, (self.bg_x + 2 * bg_w, 0))

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        self.clock.tick()
        self.gametime += self.clock.get_time() /1000.0
        
        # Draw status text
        font = pygame.font.Font('freesansbold.ttf', 32)

        # Player 1
        p = self.players.sprites()[0]
        text = font.render(f"Score: {p.score}", True, self.text_color)
        textRect = text.get_rect()
        textRect.left = 0
        textRect.top = 0
        self.screen.blit(text, textRect)

        text = font.render(f"Lives: {p.lives}", True, self.text_color)
        textRect = text.get_rect()
        textRect.centerx = self.screen_width // 4
        textRect.top = 0
        self.screen.blit(text, textRect)

        # Player 2
        p = self.players.sprites()[1]
        text = font.render(f"Score: {p.score}", True, self.text_color)
        textRect = text.get_rect()
        textRect.right = self.screen_width
        textRect.top = 0
        self.screen.blit(text, textRect)
        
        text = font.render(f"Lives: {p.lives}", True, self.text_color)
        textRect = text.get_rect()
        textRect.centerx = self.screen_width - self.screen_width // 4
        textRect.top = 0
        self.screen.blit(text, textRect)

        # Game time
        text = font.render(f"Time: {int(self.gametime)}", True, self.text_color)
        textRect = text.get_rect()
        textRect.centerx = self.screen_width // 2 
        textRect.top = 0
        self.screen.blit(text, textRect)

        pygame.display.flip()

        # Update background position
        self.bg_x -= self.bg_dx
        if self.bg_x < -bg_w:
            self.bg_x = 0

    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        # Initialize game
        if self.on_init() == False:
            self.isrunning = False
 
        # Main loop
        clock = pygame.time.Clock()
        while self.isrunning:
            # Handle events
            for event in pygame.event.get():
                self.on_event(event)
                
            # Game mechanics
            self.on_loop()

            # Drawing
            self.on_render()

            # Limit to fps
            clock.tick(self.fps)

        self.on_cleanup()

    def add_player(self, player):
        """Add player to game."""
        player.parent = self
        self.all_sprites.add(player)
        self.players.add(player)

    def add_enemy(self, enemy):
        """Add enemy to game."""
        enemy.parent = self
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def add_projectile(self, projectile):
        """Add projectile to game."""
        self.all_sprites.add(projectile)
        self.projectiles.add(projectile)
