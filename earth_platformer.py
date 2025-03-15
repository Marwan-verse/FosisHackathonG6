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
BLUE = (100, 149, 237)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)

class Background:
    def __init__(self, image_path):
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
            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.image.fill((135, 206, 235))  # Sky blue color
            self.width = SCREEN_WIDTH
    
    def draw(self, screen, camera_x):
        # Calculate parallax effect (mountains move slower than the player)
        parallax_x = camera_x * 0.5  # Mountains move at half speed
        
        # Calculate how much of the image we need to show
        rel_x = parallax_x % self.width
        
        # Draw first part of the background
        screen.blit(self.image, (rel_x - self.width, 0))
        # Draw second part to fill the gap
        screen.blit(self.image, (rel_x, 0))

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

class Tree(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)

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
        self.parent_button = parent_button  # Reference to the button that created this bubble
        
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
        self.display_time = 90  # Reduced to 1.5 seconds (90 frames at 60 FPS)
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
            if i * line_height > self.text_index * 2:  # Adjust multiplier to match typing speed
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
            # Start fading out if player has left the button
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

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.load_animations()
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 150  # Slowed down animation speed for better visibility
        self.state = "idle"
        
        # Set up initial image and rect
        self.image = self.animations["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.change_x = 0
        self.change_y = 0
        self.platforms = None
        self.score = 0
        self.lives = 3
        self.facing_right = True
        self.jumping = False

    def load_animations(self):
        self.animations = {
            "idle": [],
            "running": [],
            "jump": []
        }
        
        # Load all animations
        animation_files = {
            "idle": "player_idle.gif",
            "running": "player_running.gif",
            "jump": "player_jump.gif"
        }
        
        for anim_name, filename in animation_files.items():
            try:
                # Open the GIF file
                gif = Image.open(os.path.join("assets", "animations", filename))
                
                # Process all frames in the GIF
                frame_count = 0
                while True:
                    try:
                        gif.seek(frame_count)
                        # Convert PIL image to pygame surface
                        frame_str = gif.convert('RGBA').tobytes()
                        frame_size = gif.size
                        frame_surface = pygame.image.fromstring(frame_str, frame_size, 'RGBA')
                        
                        # Scale the frame to match player size
                        frame_surface = pygame.transform.scale(frame_surface, (PLAYER_WIDTH, PLAYER_HEIGHT))
                        
                        # Make the background transparent (assuming white or near-white is the background)
                        frame_array = pygame.surfarray.pixels3d(frame_surface)
                        white_pixels = (frame_array[..., 0] > 250) & (frame_array[..., 1] > 250) & (frame_array[..., 2] > 250)
                        frame_array[white_pixels] = [0, 0, 0]
                        del frame_array  # Release the surface lock
                        
                        # Convert to surface with alpha
                        alpha_surface = frame_surface.convert_alpha()
                        # Make white pixels transparent
                        pixel_array = pygame.surfarray.pixels_alpha(alpha_surface)
                        pixel_array[white_pixels] = 0
                        del pixel_array  # Release the surface lock
                        
                        self.animations[anim_name].append(alpha_surface)
                        frame_count += 1
                    except EOFError:
                        break
                
                # If no frames were loaded, create a fallback
                if frame_count == 0:
                    fallback = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
                    fallback.fill((0, 0, 255, 128))  # Semi-transparent blue
                    self.animations[anim_name] = [fallback]
                    
            except Exception as e:
                print(f"Error loading animation {filename}: {e}")
                # Create fallback surface
                fallback = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
                fallback.fill((0, 0, 255, 128))  # Semi-transparent blue
                self.animations[anim_name] = [fallback]

    def update(self):
        # Update animation frame
        now = pygame.time.get_ticks()
        if now - self.animation_timer > self.animation_speed:
            self.animation_timer = now
            if len(self.animations[self.state]) > 0:  # Make sure we have frames to animate
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
                current_anim = self.animations[self.state][self.current_frame]
                
                # Flip the image if facing left
                if not self.facing_right:
                    self.image = pygame.transform.flip(current_anim, True, False)
                else:
                    self.image = current_anim

        # Gravity
        self.change_y += GRAVITY

        # Horizontal movement
        self.rect.x += self.change_x

        # Keep player within world bounds
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH

        # Check for collision with platforms
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right

        # Vertical movement
        self.rect.y += self.change_y

        # Check for collision with platforms
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.jumping = False
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            self.change_y = 0

        # Update animation state
        if self.jumping:
            self.state = "jump"
        elif self.change_x != 0:
            self.state = "running"
        else:
            self.state = "idle"

    def jump(self):
        if not self.jumping:
            self.change_y = JUMP_SPEED
            self.jumping = True
            self.state = "jump"
            self.current_frame = 0
            self.animation_timer = pygame.time.get_ticks()

    def go_left(self):
        self.change_x = -MOVE_SPEED
        self.facing_right = False
        if not self.jumping:
            self.state = "running"

    def go_right(self):
        self.change_x = MOVE_SPEED
        self.facing_right = True
        if not self.jumping:
            self.state = "running"

    def stop(self):
        self.change_x = 0
        if not self.jumping:
            self.state = "idle"
            self.current_frame = 0
            self.animation_timer = pygame.time.get_ticks()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class EarthPlatformer:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        # Earth facts that will appear in bubbles
        self.earth_facts = [
            "Earth is the third planet from the Sun",
            "Earth's atmosphere is 78% nitrogen",
            "Earth's core temperature is as hot as the Sun's surface",
            "Earth's magnetic field protects us from solar radiation",
            "70% of Earth's surface is covered by oceans",
            "Earth is the only known planet with liquid water on its surface",
            "Earth's atmosphere creates a greenhouse effect",
            "Earth completes one rotation every 24 hours",
            "Earth's ozone layer blocks harmful UV radiation",
            "Earth has one natural satellite - the Moon",
            "Earth's gravity keeps everything on its surface",
            "Earth's tilt creates our seasons",
            "Earth is 4.54 billion years old",
            "Earth is the densest planet in our solar system",
            "Earth's atmosphere extends about 100 km up"
        ]
        
        # Load the background first
        self.background = Background(os.path.join("assets", "mountainsfardetail.png"))
        
        # Load the Earth floor texture
        try:
            self.floor_image = pygame.image.load(os.path.join("assets", "Earth floor.png")).convert_alpha()
            self.floor_image = pygame.transform.scale(self.floor_image, (TILE_SIZE, TILE_SIZE))
            
            # Load tree texture
            self.tree_image = pygame.image.load(os.path.join("assets", "tree.png")).convert_alpha()
            tree_width = int(TILE_SIZE * 3)
            tree_height = int(TILE_SIZE * 4)
            self.tree_image = pygame.transform.scale(self.tree_image, (tree_width, tree_height))
        except pygame.error as e:
            print(f"Could not load textures: {e}")
            self.floor_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            self.floor_image.fill(GREEN)
            self.tree_image = None
        
        # Earth information paragraphs
        self.earth_info = [
            "Earth's atmosphere is a complex system that protects all life. The atmosphere is 78% nitrogen and 21% oxygen, with small amounts of other gases. The ozone layer, a special part of the atmosphere, blocks harmful UV radiation from reaching the surface. This protective shield extends about 100 kilometers into space.",
            
            "Earth's surface is a dynamic landscape shaped by powerful forces. 70% is covered by oceans containing liquid water, a unique feature in our solar system. The remaining 30% consists of continents with mountains, forests, and deserts. This diverse environment supports millions of species.",
            
            "Earth's core is an incredible powerhouse. Its temperature matches the Sun's surface at about 5,400°C. This molten core generates a magnetic field that protects us from harmful solar radiation and helps some animals navigate. The core's heat also drives plate tectonics and volcanic activity.",
            
            "Earth's daily and yearly cycles create our familiar patterns of life. It completes one rotation every 24 hours, giving us day and night. The planet's 23.5-degree tilt causes our seasons as we orbit the Sun. One orbit takes 365.25 days, which is why we have leap years.",
            
            "Earth's gravity, averaging 9.8 m/s², keeps everything grounded. This force holds our atmosphere in place, keeps the oceans in their basins, and helps maintain the Moon's orbit. The Moon, Earth's only natural satellite, influences our tides and helps stabilize Earth's tilt."
        ]
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.trees = pygame.sprite.Group()
        self.info_buttons = pygame.sprite.Group()
        self.info_bubbles = pygame.sprite.Group()

        # Create the player
        self.player = Player(100, SCREEN_HEIGHT - 150)
        self.player.platforms = self.platforms
        self.all_sprites.add(self.player)

        # Create camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Create the level
        self.create_level()

    def create_level(self):
        # Create ground - a flat line of Earth floor blocks
        ground_y = SCREEN_HEIGHT - TILE_SIZE
        for x in range(0, WORLD_WIDTH + TILE_SIZE, TILE_SIZE):
            platform = Platform(x, ground_y, TILE_SIZE, TILE_SIZE, self.floor_image)
            self.platforms.add(platform)
            self.all_sprites.add(platform)

        # Add trees at semi-random positions along the entire world width
        num_trees = WORLD_WIDTH // 400
        tree_positions = [i * 400 + random.randint(-100, 100) for i in range(num_trees)]
        
        for x in tree_positions:
            if self.tree_image and 0 <= x <= WORLD_WIDTH:
                tree = Tree(x, ground_y, self.tree_image)
                self.trees.add(tree)
                self.all_sprites.add(tree)
        
        # Add info buttons along the ground
        button_spacing = WORLD_WIDTH // (len(self.earth_info) + 1)
        for i in range(len(self.earth_info)):
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
                if button.cooldown == 0:  # Only check cooldown, not pressed state
                    button.cooldown = 30  # Reduced cooldown to 0.5 seconds (30 frames at 60 FPS)
                    
                    # Immediately remove any existing info bubbles
                    for bubble in self.info_bubbles:
                        bubble.kill()  # Remove from all sprite groups
                    self.info_bubbles.empty()  # Clear the info_bubbles group
                    
                    # Create new info bubble
                    index = list(self.info_buttons).index(button)
                    bubble = InfoBubble(
                        self.player.rect.centerx,
                        200,  # Fixed height in sky
                        self.earth_info[index],
                        button  # Pass the button reference
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
            self.screen.fill((135, 206, 235))  # Sky blue background
            
            # Draw the mountain background with parallax
            self.background.draw(self.screen, self.camera.x)
            
            # Draw button glow effects first (behind other sprites)
            for button in self.info_buttons:
                if button.cooldown > 0:  # Show glow effect during cooldown
                    button_pos = self.camera.apply(button)
                    glow_image = button.glow_images[button.glow_index]
                    glow_rect = glow_image.get_rect(center=button_pos.center)
                    self.screen.blit(glow_image, glow_rect)
            
            # Draw all sprites with camera offset
            for sprite in self.all_sprites:
                if isinstance(sprite, InfoBubble):
                    # Special handling for info bubbles to keep them on screen
                    bubble_pos = sprite.rect.copy()
                    bubble_pos.centerx = SCREEN_WIDTH // 2
                    self.screen.blit(sprite.image, bubble_pos)
                else:
                    sprite_pos = self.camera.apply(sprite)
                    self.screen.blit(sprite.image, sprite_pos)

            pygame.display.flip()
            self.clock.tick(60)

        return True 