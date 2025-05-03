"""Definition for game classes."""
import math
import random
import pygame
import spaceshooter.data_classes.colors as colors
# from astroids.data_classes.projectile_classes import LaserProjectile
# import astroids.helpers.misc_helpers as mh
# import astroids.helpers.physics_helper as ph
# from astroids.data_classes.ship_class import get_default_ship
# from astroids.data_classes.astroid_class import get_default_astroid


class GameParent:
    """Parent to all games."""
    def __init__(
            self, 
            name: str = "", 
            screen_height: int = 600,
            screen_width: int = 800,
            background_filepath: str = "",
            fps: int = 30):
        """Initialize class."""
        self.name = name
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.background_filepath = background_filepath
        self.fps = fps
        

        self.background_image = None
        self.screen = None
        self.isrunning = False

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

        # font = pygame.font.Font('freesansbold.ttf', 16)
        # text = font.render("Score: 000, Energy: 000, Health: 000", True, colors.WHITE)
        # text_rect = text.get_rect()
        # text_rect.left = 0
        # text_rect.top = 0
        # self.font = font
        # self.text_rect = text_rect

        self.isrunning = True
 
    def on_event(self, event):
        # Handle events
        if event.type == pygame.QUIT:
            self.isrunning = False
        
    def on_loop(self):
        """Update game."""

        # Handle key press
        for player in self.players:
            player.key_press()

        # Handle movement
        self.all_sprites.update()

        # Update counters
        # for sprite in self.players.sprites():
        #     sprite.update_counters()

        # Handle collisions
        # G = pygame.sprite.Group(self.all_sprites.copy())
        # for sprite1 in G:
        #     G.remove(sprite1)
        #     sprite2s = pygame.sprite.spritecollide(sprite1, G, False, mh.collide_if_not_self)
        #     if not sprite2s:
        #         continue
        #     for sprite2 in sprite2s:
        #         if isinstance(sprite1, LaserProjectile) and isinstance(sprite2, LaserProjectile):
        #             continue

        #         # print(f"Collision detected between sprites {sprite1.name} and {sprite2.name}")
        #         ph.calculate_collision(sprite1, sprite2)
        #         ph.calculate_damage(sprite1, sprite2)
            
    def on_render(self):
        """Draw screen.""" 
        bg = self.get_background_image()
        if bg is None:
            # self.screen.fill(colors.WHITE)
            self.screen.fill(colors.BLACK)
        else:
            self.screen.blit(bg, (0, 0))

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # player = self.players.sprites()[0]
        # text = self.font.render(f"Score: {player.score:03d}, Energy: {int(player.energy):03d}, Health: {player.health:03d}", True, colors.WHITE)
   
        # self.screen.blit(text, self.text_rect)

        pygame.display.flip()

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

class SpaceshooterGame(GameParent):
    """Spaceshooter game class."""
    def __init__(self):
        """Initialize class."""
        super().__init__(
            name = "Spaceshooter",
            #background_filepath="astroids/Images/background.jpeg"
            )

        # Create players
        # ship = get_default_ship()
        # ship.position[0] = self.screen_width // 5
        # ship.position[1] = self.screen_height // 5
        # self.add_player(ship)

        # # Create astroids
        # for ii in range(3):
        #     astroid = get_default_astroid()

        #     pos = [
        #         (1 + ii) * self.screen_width // 4,
        #         random.randrange(self.screen_height // 3, 2 * self.screen_height // 3)
        #     ]
        #     angle = math.pi * (2 * random.random() - 1)
        #     vel = astroid.velocity_max * random.random()

        #     astroid.position[0] = pos[0]
        #     astroid.position[1] = pos[1]
        #     astroid.velocity[0] = vel * math.cos(angle)
        #     astroid.velocity[1] = vel * math.sin(angle)
        #     astroid.angle_velocity = astroid.angle_velocity_max * (2 * random.random() - 1)
        
        #     # Add the astroid to the list of astroids
        #     self.add_enemy(astroid)

