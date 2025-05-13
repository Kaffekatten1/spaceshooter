"""Definition for game classes."""
import pygame
import pygame_menu
import random

import spaceshooter.data_classes.colors as colors
import spaceshooter.helpers.misc_helpers as mh
from spaceshooter.data_classes.ship_classes import get_default_ship
from spaceshooter.data_classes.enemy_classes import get_default_enemy
from spaceshooter.data_classes.projectile_classes import ProjectileParent
from spaceshooter.data_classes.ship_classes import Ship
from spaceshooter.data_classes.parent_classes import PlayerParent

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
        self.isquitting = False

        self.nplayers = 1
        self.enemy_rate = 0.5

        self.clock = pygame.time.Clock()

        self.sound_on = True

        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()

        self.reset()

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
 
    def on_event(self, event):
        # Handle events
        if event.type == pygame.QUIT:
            self.isquitting = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.isrunning = False
            elif event.key == pygame.K_o:
                self.players.sprites()[0].cycle_level()
            elif event.key == pygame.K_p:
                if self.nplayers == 2:
                    self.players.sprites()[1].cycle_level()
            elif event.key == pygame.K_m:
                self.sound_on = not self.sound_on
        
    def on_loop(self):
        """Update game."""

        # Handle key press
        for player in self.players:
            player.key_press()

        # Handle movement
        self.all_sprites.update()

        # Kill sprites outside window
        g = 200
        for s in self.all_sprites:
            r = s.rect
            if r.right < -g or r.bottom < -g or r.left > self.screen_width + g or r.top > self.screen_height + g:
                s.kill()

        # Handle collisions
        G = pygame.sprite.Group(self.all_sprites.copy())
        for sprite1 in G:
            G.remove(sprite1)
            sprite2s = pygame.sprite.spritecollide(sprite1, G, False, mh.collide_if_not_self)
            if not sprite2s:
                continue
            for sprite2 in sprite2s:
                if isinstance(sprite1, ProjectileParent) and isinstance(sprite2, ProjectileParent):
                    continue

                if isinstance(sprite1, Ship) and isinstance(sprite2, Ship):
                    continue

                if isinstance(sprite1, ProjectileParent) and isinstance(sprite2, Ship):
                    continue

                if isinstance(sprite1, Ship) and isinstance(sprite2, ProjectileParent):
                    continue

                # print(f"Collision detected between sprites {sprite1.name} and {sprite2.name}")
                if isinstance(sprite1, ProjectileParent):
                    sprite1.parent.parent.score += 1
                sprite1.die()

                if isinstance(sprite2, ProjectileParent):
                    sprite2.parent.parent.score += 1
                sprite2.die()

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
        self.explosions.draw(self.screen)
        self.explosions.update()

        self.clock.tick()
        self.gametime += self.clock.get_time() / 1000.0
        
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
        if self.nplayers == 2:
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
        # Show menu
        menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

        menu.add.button('Play', self.on_start)
        menu.add.selector('Players :', [('ONE', 1), ('TWO', 2)], onchange=self.set_nplayers)
        menu.add.button('Quit', pygame_menu.events.EXIT)

        while not self.isquitting:
            pygame.mixer.music.load("spaceshooter/Sounds/Music/spaceshooter_theme_1.wav")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)

            menu.mainloop(self.screen)

    def set_nplayers(self, value, nplayers):
        self.nplayers = nplayers

    def on_start(self):
        # Run the game
        if self.on_init() == False:
            self.isrunning = False

        pygame.mixer.music.fadeout(1000)

        # Create players
        for ii in range(self.nplayers):
            ship = get_default_ship(ii + 1)
            ship.position.update(50, (ii + 1) * self.screen_height // (self.nplayers + 1))
            self.add_player(ship)

        # Create enemies
        nenemies = 3
        for ii in range(nenemies):
            enemy = get_default_enemy("Ufo", [self.screen_width - 100, (ii + 1) * self.screen_height // (nenemies + 1)])
            self.add_enemy(enemy)

        self.isrunning = True

        pygame.mixer.music.load("spaceshooter/Sounds/Music/spaceshooter_theme_4.wav")
        pygame.mixer.music.play(-1)
 
        # Main loop
        clock = pygame.time.Clock()
        enemy_countdown = 1 / self.enemy_rate
        while self.isrunning:
            # Handle events
            for event in pygame.event.get():
                self.on_event(event)
                
            enemy_countdown -= 1 / self.fps
            if enemy_countdown < 0:
                enemy_countdown = 1 / self.enemy_rate
                enemy = get_default_enemy("Ufo", [self.screen_width - 100, random.randint(100, self.screen_height - 100)])
                enemy.velocity.x = -100
                self.add_enemy(enemy)

            # Game mechanics
            self.on_loop()

            # Drawing
            self.on_render()

            # Limit to fps
            clock.tick(self.fps)

        pygame.mixer.music.fadeout(1000)

        self.reset()

        pygame.mixer.music.load("spaceshooter/Sounds/Music/spaceshooter_theme_1.wav")
        pygame.mixer.music.play(-1)
        # self.on_cleanup()

    def reset(self):
        """Reset game."""
        self.bg_x = 0
        self.bg_dx = 3
        self.gametime = 0

        for s in self.all_sprites:
            s.kill()

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

    def add_projectiles(self, plist):
        """Add multiple projectiles to game."""
        for p in plist:
            self.add_projectile(p)
