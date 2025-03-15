import pygame
import random
import os
from PIL import Image
import io
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
TILE_SIZE = 48
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 64
GRAVITY = 0.8
JUMP_SPEED = -15
MOVE_SPEED = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Background:
    def __init__(self, image_path=None, is_earth=False):
        self.is_earth = is_earth
        if is_earth:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                # Get the actual width of the mountain image
                self.width = self.image.get_width()
                self.height = self.image.get_height()
                
                # Scale height to match screen height while maintaining aspect ratio
                scale_factor = SCREEN_HEIGHT / self.height
                new_width = int(self.width * scale_factor)
                self.image = pygame.transform.scale(self.image, (new_width, SCREEN_HEIGHT))
                self.width = new_width  # Update width after scaling
                
                # Set the world width to match the mountain width
                global WORLD_WIDTH
                WORLD_WIDTH = self.width
                
            except pygame.error as e:
                print(f"Could not load background image: {e}")
                self.fallback_background()
        else:
            self.fallback_background()
    
    def fallback_background(self):
        # For non-Earth planets or if image loading fails
        self.width = SCREEN_WIDTH * 3  # Make background 3 screens wide
        global WORLD_WIDTH
        WORLD_WIDTH = self.width
    
    def draw(self, screen, camera_x):
        if self.is_earth:
            # Draw mountain background with parallax for Earth
            parallax_x = camera_x * 0.5  # Mountains move at half speed
            rel_x = parallax_x % self.width
            screen.blit(self.image, (rel_x - self.width, 0))
            screen.blit(self.image, (rel_x, 0))
        else:
            # For other planets, just fill with black (space)
            screen.fill(BLACK)
            
            # Add some stars in the background
            for i in range(50):  # Draw 50 stars
                x = ((-camera_x * 0.2) + i * 100) % self.width  # Slow parallax for stars
                y = (i * 37) % SCREEN_HEIGHT  # Distribute stars vertically
                # Make stars twinkle by varying their brightness
                brightness = abs(math.sin(pygame.time.get_ticks() * 0.001 + i)) * 255
                color = (brightness, brightness, brightness)
                pygame.draw.circle(screen, color, (int(x), y), 1)

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.scroll_speed = MOVE_SPEED
        self.x = 0  # Store actual x position for parallax

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        self.x = -target.rect.centerx + SCREEN_WIDTH // 2
        
        # Limit scrolling to world boundaries
        self.x = min(0, self.x)  # Left boundary
        self.x = max(-(WORLD_WIDTH - SCREEN_WIDTH), self.x)  # Right boundary
        
        self.camera = pygame.Rect(self.x, 0, self.width, self.height)

class InfoButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = TILE_SIZE
        self.height = TILE_SIZE // 2
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))  # Red color
        
        # Add glow effect
        self.glow_images = []
        for i in range(5):
            glow_surf = pygame.Surface((self.width + i*4, self.height + i*4), pygame.SRCALPHA)
            alpha = 100 - i * 20
            pygame.draw.rect(glow_surf, (255, 50, 50, alpha), 
                           glow_surf.get_rect(), border_radius=5)
            self.glow_images.append(glow_surf)
        
        # Main button
        pygame.draw.rect(self.image, (200, 0, 0), 
                        pygame.Rect(2, 2, self.width-4, self.height-4), 
                        border_radius=5)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.cooldown = 0
        self.glow_index = 0
        self.glow_timer = 0
        self.player_on_button = False  # Track if player is on button

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1
        
        # Animate glow
        self.glow_timer += 1
        if self.glow_timer > 5:
            self.glow_timer = 0
            self.glow_index = (self.glow_index + 1) % len(self.glow_images)

class InfoBubble(pygame.sprite.Sprite):
    def __init__(self, x, y, text, parent_button):
        super().__init__()
        self.font = pygame.font.Font(None, 32)
        self.full_text = text
        self.current_text = ""
        self.text_index = 0
        self.typing_speed = 2
        self.typing_timer = 0
        self.typing_delay = 1
        self.done_typing = False
        self.padding = 20
        self.border_radius = 15
        self.parent_button = parent_button
        
        # Calculate maximum width for text wrapping
        self.max_width = SCREEN_WIDTH // 2
        self.wrapped_text = self.wrap_text(self.full_text)
        
        # Create initial surface
        self.create_surface()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        
        # Fade in/out properties
        self.alpha = 0
        self.fade_speed = 5
        self.fade_in = True
        self.display_time = 90
        self.display_timer = 0
        self.active = True
        self.start_fade = False

    def wrap_text(self, text):
        words = text.split()
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = self.font.render(word + " ", True, BLACK)
            word_width = word_surface.get_width()
            
            if current_width + word_width <= self.max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width
        
        if current_line:
            lines.append(" ".join(current_line))
        
        return lines

    def create_surface(self):
        # Calculate required height for all lines
        line_height = self.font.get_linesize()
        total_height = (len(self.wrapped_text) * line_height) + (self.padding * 2)
        
        # Create surface
        self.image = pygame.Surface((self.max_width + self.padding * 2, total_height), pygame.SRCALPHA)
        
        # Draw background with gradient
        for i in range(3):
            alpha = 180 - (i * 30)
            pygame.draw.rect(self.image, (255, 255, 255, alpha),
                           self.image.get_rect(),
                           border_radius=self.border_radius-i)
        
        # Render current text
        y_offset = self.padding
        for i, line in enumerate(self.wrapped_text):
            if i * line_height > self.text_index * 2:
                break
            render_text = line[:max(0, self.text_index - i * len(line))]
            if render_text:
                text_surface = self.font.render(render_text, True, BLACK)
                self.image.blit(text_surface, (self.padding, y_offset))
            y_offset += line_height

    def update(self):
        if not self.active:
            return

        if self.fade_in and self.alpha < 255 and not self.start_fade:
            self.alpha = min(255, self.alpha + self.fade_speed)
        
        if not self.done_typing:
            self.typing_timer += 1
            if self.typing_timer >= self.typing_delay:
                self.typing_timer = 0
                self.text_index = min(self.text_index + self.typing_speed, 
                                    sum(len(line) for line in self.wrapped_text))
                if self.text_index >= sum(len(line) for line in self.wrapped_text):
                    self.done_typing = True
                self.create_surface()
        else:
            if not self.parent_button.player_on_button:
                self.start_fade = True
                
            if self.start_fade:
                self.display_timer += 1
                if self.display_timer >= self.display_time:
                    self.fade_in = False
                    self.alpha = max(0, self.alpha - self.fade_speed)
                    if self.alpha <= 0:
                        self.active = False
        
        self.image.set_alpha(self.alpha)

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Create base astronaut images for different states
        self.images = self.create_astronaut_sprites()
        self.current_image = self.images['idle']
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement variables
        self.change_x = 0
        self.change_y = 0
        self.platforms = None
        self.facing_right = True
        self.animation_timer = 0
        self.animation_frame = 0
        self.is_jumping = False
    
    def create_astronaut_sprites(self):
        sprites = {}
        
        # Colors
        WHITE = (255, 255, 255)
        GRAY = (180, 180, 180)
        DARK_GRAY = (100, 100, 100)
        VISOR = (100, 200, 255, 150)
        
        # Create base surfaces
        for state in ['idle', 'walk1', 'walk2', 'jump']:
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Draw helmet (circle)
            pygame.draw.circle(surf, WHITE, (self.width//2, self.height//3), self.width//3)
            
            # Draw visor
            visor_rect = pygame.Rect(self.width//3, self.height//4, self.width//3, self.height//4)
            pygame.draw.ellipse(surf, VISOR, visor_rect)
            pygame.draw.ellipse(surf, DARK_GRAY, visor_rect, 2)
            
            # Draw suit body
            suit_points = [
                (self.width//3, self.height//2),  # Left shoulder
                (self.width*2//3, self.height//2),  # Right shoulder
                (self.width*3//4, self.height*4//5),  # Right hip
                (self.width//4, self.height*4//5),  # Left hip
            ]
            pygame.draw.polygon(surf, WHITE, suit_points)
            
            # Draw legs
            if state == 'idle':
                # Standing straight
                pygame.draw.rect(surf, WHITE, (self.width//3, self.height*4//5, self.width//6, self.height//5))
                pygame.draw.rect(surf, WHITE, (self.width//2, self.height*4//5, self.width//6, self.height//5))
            elif state == 'walk1':
                # One leg forward, one back
                pygame.draw.rect(surf, WHITE, (self.width//4, self.height*4//5, self.width//6, self.height//5))
                pygame.draw.rect(surf, WHITE, (self.width*5//8, self.height*4//5, self.width//6, self.height//5))
            elif state == 'walk2':
                # Opposite leg positions
                pygame.draw.rect(surf, WHITE, (self.width*5//8, self.height*4//5, self.width//6, self.height//5))
                pygame.draw.rect(surf, WHITE, (self.width//4, self.height*4//5, self.width//6, self.height//5))
            elif state == 'jump':
                # Legs bent for jump
                pygame.draw.rect(surf, WHITE, (self.width//3, self.height*4//5, self.width//6, self.height//6))
                pygame.draw.rect(surf, WHITE, (self.width//2, self.height*4//5, self.width//6, self.height//6))
            
            # Add shading and details
            pygame.draw.circle(surf, GRAY, (self.width//2, self.height//3), self.width//3, 2)
            pygame.draw.lines(surf, GRAY, False, suit_points, 2)
            
            sprites[state] = surf
        
        return sprites

    def update(self):
        # Apply gravity
        self.change_y += GRAVITY
        
        # Move horizontally
        self.rect.x += self.change_x
        
        # Check for collisions horizontally
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right
        
        # Move vertically
        self.rect.y += self.change_y
        
        # Check for collisions vertically
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.is_jumping = False
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0
        
        # Update animation
        self.animation_timer += 1
        if self.animation_timer >= 10:  # Change frame every 10 game ticks
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 2
        
        # Update player image based on state
        if self.is_jumping:
            self.current_image = self.images['jump']
        elif self.change_x != 0:
            self.current_image = self.images['walk1'] if self.animation_frame == 0 else self.images['walk2']
        else:
            self.current_image = self.images['idle']
        
        # Flip image if facing left
        if not self.facing_right:
            self.image = pygame.transform.flip(self.current_image, True, False)
        else:
            self.image = self.current_image
    
    def jump(self):
        # Check if we're standing on a platform
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2
        
        if len(platform_hit_list) > 0:
            self.change_y = JUMP_SPEED
            self.is_jumping = True
    
    def go_left(self):
        self.change_x = -MOVE_SPEED
        self.facing_right = False
    
    def go_right(self):
        self.change_x = MOVE_SPEED
        self.facing_right = True
    
    def stop(self):
        self.change_x = 0

class PlanetPlatformer:
    def __init__(self, planet_name, planet_color, planet_info, background_color=(0, 0, 0)):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.planet_name = planet_name
        self.planet_color = planet_color
        self.planet_info = planet_info
        self.background_color = background_color
        
        # Load the background - only use mountains for Earth
        self.background = Background(
            os.path.join("assets", "mountainsfardetail.png"),
            is_earth=(planet_name == "Earth")
        )
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.info_buttons = pygame.sprite.Group()
        self.info_bubbles = pygame.sprite.Group()

        # Create the player (reusing the Player class from earth_platformer.py)
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.player.platforms = self.platforms
        self.all_sprites.add(self.player)

        # Create camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the level
        self.create_level()

    def create_level(self):
        # Create ground - a flat line of colored blocks
        ground_y = SCREEN_HEIGHT - TILE_SIZE
        for x in range(0, WORLD_WIDTH + TILE_SIZE, TILE_SIZE):
            platform = Platform(x, ground_y, TILE_SIZE, TILE_SIZE, self.planet_color)
            self.platforms.add(platform)
            self.all_sprites.add(platform)
        
        # Add info buttons along the ground
        button_spacing = WORLD_WIDTH // (len(self.planet_info) + 1)
        for i in range(len(self.planet_info)):
            x = (i + 1) * button_spacing
            button = InfoButton(x, SCREEN_HEIGHT - TILE_SIZE)
            self.info_buttons.add(button)
            self.all_sprites.add(button)

    def check_button_collisions(self):
        # Reset all buttons' player_on_button status
        for button in self.info_buttons:
            button.player_on_button = False
            
        # Check for new collisions
        for button in self.info_buttons:
            if pygame.sprite.collide_rect(self.player, button):
                button.player_on_button = True
                if button.cooldown == 0:
                    button.cooldown = 30
                    
                    # Immediately remove any existing info bubbles
                    for bubble in self.info_bubbles:
                        bubble.kill()
                    self.info_bubbles.empty()
                    
                    # Create new info bubble
                    index = list(self.info_buttons).index(button)
                    bubble = InfoBubble(
                        self.player.rect.centerx,
                        200,
                        self.planet_info[index],
                        button
                    )
                    self.info_bubbles.add(bubble)
                    self.all_sprites.add(bubble)

    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    elif event.key == pygame.K_ESCAPE:
                        return True

            # Get the current keyboard state
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.go_left()
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.go_right()
            if not (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_a] or keys[pygame.K_d]):
                self.player.stop()

            # Update
            self.all_sprites.update()
            self.camera.update(self.player)
            self.check_button_collisions()

            # Draw
            self.screen.fill(self.background_color)
            
            # Draw the mountain background with parallax
            self.background.draw(self.screen, self.camera.x)
            
            # Draw button glow effects first
            for button in self.info_buttons:
                if button.cooldown > 0:
                    button_pos = self.camera.apply(button)
                    glow_image = button.glow_images[button.glow_index]
                    glow_rect = glow_image.get_rect(center=button_pos.center)
                    self.screen.blit(glow_image, glow_rect)
            
            # Draw all sprites
            for sprite in self.all_sprites:
                if isinstance(sprite, InfoBubble):
                    bubble_pos = sprite.rect.copy()
                    bubble_pos.centerx = SCREEN_WIDTH // 2
                    self.screen.blit(sprite.image, bubble_pos)
                else:
                    sprite_pos = self.camera.apply(sprite)
                    self.screen.blit(sprite.image, sprite_pos)

            pygame.display.flip()
            self.clock.tick(60)

        return True 