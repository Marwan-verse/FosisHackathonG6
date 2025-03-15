import pygame
import math
import sys
from random import randint, choice, random
import time
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 1200
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Explorer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
STAR_COLORS = [(255, 255, 255), (200, 200, 255), (255, 200, 200), (255, 255, 200)]

# Add after other constants
ASSETS_DIR = "assets"  # Create this directory to store your pixel art images

# Game constants
BULLET_SPEED = 10
ASTEROID_SPEED_MIN = 1
ASTEROID_SPEED_MAX = 3
MAX_ASTEROIDS = 5
ASTEROID_SPAWN_RATE = 0.02  # 2% chance per frame to spawn new asteroid
BULLET_LIFETIME = 60  # frames

# Planet data with extended information
planets = {
    "Sun": {
        "color": (255, 200, 50),  # Bright yellow
        "radius": 40,
        "orbit": 0,
        "speed": 0,
        "image": "sun.png",
        "info": [
            "The Sun - Our Star",
            "Temperature: 5,500°C (surface)",
            "Age: 4.6 billion years",
            "Type: Yellow Dwarf Star",
            "Contains 99.86% of solar system's mass",
            "Powered by nuclear fusion"
        ]
    },
    "Mercury": {
        "color": (169, 169, 169),  # Grey
        "radius": 10,
        "orbit": 100,
        "speed": 0.02,
        "image": "Murcury.png",  # Changed from "mercury.png" to "Murcury.png"
        "info": [
            "Mercury - The Smallest Planet",
            "Temperature: -180°C to 430°C",
            "No moons",
            "Closest planet to the Sun",
            "Year length: 88 Earth days",
            "No atmosphere"
        ]
    },
    "Venus": {
        "color": (255, 198, 73),  # Yellow-orange
        "radius": 15,
        "orbit": 150,
        "speed": 0.015,
        "image": "venus.png",  # Add your pixel art filenames here
        "info": [
            "Venus - The Hottest Planet",
            "Temperature: 462°C",
            "Rotates backwards",
            "Similar size to Earth",
            "Thick atmosphere of CO2",
            "No moons"
        ]
    },
    "Earth": {
        "color": (100, 149, 237),  # Cornflower blue
        "radius": 18,
        "orbit": 200,
        "speed": 0.01,
        "image": "earth.png",  # Add your pixel art filenames here
        "info": [
            "Earth - Our Home Planet",
            "Temperature: -88°C to 58°C",
            "One moon",
            "Only known planet with life",
            "71% covered by water",
            "24-hour day cycle"
        ]
    },
    "Mars": {
        "color": (205, 127, 50),  # Rusty red
        "radius": 14,
        "orbit": 250,
        "speed": 0.008,
        "image": "mars.png",  # Add your pixel art filenames here
        "info": [
            "Mars - The Red Planet",
            "Temperature: -140°C to 20°C",
            "Two moons: Phobos and Deimos",
            "Has the largest volcano in the solar system",
            "Possible future human colony",
            "Year length: 687 Earth days"
        ]
    },
    "Jupiter": {
        "color": (255, 198, 73),  # Sandy yellow
        "radius": 40,
        "orbit": 320,
        "speed": 0.005,
        "image": "jupiter.png",  # Add your pixel art filenames here
        "info": [
            "Jupiter - The Largest Planet",
            "Temperature: -110°C (cloud top)",
            "79 known moons",
            "Great Red Spot is a giant storm",
            "More than twice the mass of all other planets combined",
            "Year length: 12 Earth years"
        ]
    },
    "Saturn": {
        "color": (238, 232, 205),  # Pale yellow
        "radius": 35,
        "orbit": 400,
        "speed": 0.003,
        "image": "saturn.png",  # Add your pixel art filenames here
        "info": [
            "Saturn - The Ringed Planet",
            "Temperature: -178°C",
            "82 confirmed moons",
            "Famous for its beautiful rings",
            "Could float in water (if there was a big enough pool)",
            "Year length: 29.5 Earth years"
        ]
    },
    "Uranus": {
        "color": (173, 216, 230),  # Light blue
        "radius": 25,
        "orbit": 470,
        "speed": 0.002,
        "image": "uranus.png",  # Add your pixel art filenames here
        "info": [
            "Uranus - The Sideways Planet",
            "Temperature: -224°C",
            "27 known moons",
            "Rotates on its side",
            "First planet discovered by telescope",
            "Year length: 84 Earth years"
        ]
    },
    "Neptune": {
        "color": (0, 0, 139),  # Dark blue
        "radius": 24,
        "orbit": 520,
        "speed": 0.001,
        "image": "neptune.png",  # Add your pixel art filenames here
        "info": [
            "Neptune - The Windy Planet",
            "Temperature: -214°C",
            "14 known moons",
            "Strongest winds in the solar system",
            "The most distant planet",
            "Year length: 165 Earth years"
        ]
    }
}

class Star:
    def __init__(self):
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)
        self.size = random() * 2
        self.color = choice(STAR_COLORS)
        self.twinkle_speed = random() * 0.1
        self.brightness = random()
        self.flash_chance = 0.005  # Chance to start flashing
        self.is_flashing = False
        self.flash_brightness = 0
        
    def update(self):
        # Regular twinkling
        self.brightness = abs(math.sin(time.time() * self.twinkle_speed))
        
        # Random flashing
        if not self.is_flashing and random() < self.flash_chance:
            self.is_flashing = True
            self.flash_brightness = 2.0  # Start with bright flash
            
        if self.is_flashing:
            self.flash_brightness *= 0.9  # Fade out
            if self.flash_brightness < 0.1:
                self.is_flashing = False
        
    def draw(self, screen):
        # Combine regular brightness with flash brightness
        final_brightness = min(self.brightness + self.flash_brightness, 2.0)
        color = [min(255, c * final_brightness) for c in self.color]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.size))

class Planet:
    def __init__(self, name, data):
        self.name = name
        self.color = data["color"]
        self.radius = data["radius"]
        self.orbit = data["orbit"]
        self.speed = data["speed"]
        self.angle = randint(0, 360)
        self.x = 0
        self.y = 0
        
        # Add rotation properties
        self.rotation_angle = 0
        self.rotation_speed = 0.5  # Degrees per frame, adjust for faster/slower rotation
        
        # Load planet image if available
        self.image = None
        self.original_image = None  # Store the original image for rotation
        if "image" in data:
            try:
                image_path = os.path.join(ASSETS_DIR, data["image"])
                if os.path.exists(image_path):
                    self.original_image = pygame.image.load(image_path).convert_alpha()
                    # Scale image to match planet size
                    self.original_image = pygame.transform.scale(
                        self.original_image, 
                        (self.radius * 2, self.radius * 2)
                    )
                    self.image = self.original_image.copy()
            except pygame.error:
                print(f"Could not load image for {name}")
        
        self.tilt_factor = 0.5
        self.trail = []
        self.trail_length = 50
        self.rotation = 0

    def update(self):
        self.angle += self.speed
        
        # Calculate position with tilt effect
        base_x = math.cos(self.angle) * self.orbit
        base_y = math.sin(self.angle) * self.orbit
        
        # Apply perspective transformation
        self.x = WIDTH // 2 + base_x
        self.y = HEIGHT // 2 + (base_y * self.tilt_factor)  # Compress y-coordinate for tilt effect
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

        # Update rotation
        self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
        if self.original_image:
            self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)

    def draw(self, screen):
        # Draw orbit trail
        if len(self.trail) > 2:
            trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail)))
                pygame.draw.line(trail_surface, (*self.color, alpha),
                               self.trail[i], self.trail[i + 1], 2)
            screen.blit(trail_surface, (0, 0))

        # Draw tilted orbit
        rect = pygame.Rect(
            WIDTH//2 - self.orbit, 
            HEIGHT//2 - (self.orbit * self.tilt_factor),
            self.orbit * 2, 
            self.orbit * 2 * self.tilt_factor
        )
        pygame.draw.ellipse(screen, (*self.color, 30), rect, 1)

        # Draw planet glow
        glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        for r in range(self.radius + 10, self.radius - 2, -2):
            alpha = int(100 * (r / (self.radius + 10)))
            pygame.draw.circle(glow_surface, (*self.color, alpha),
                             (self.radius * 2, self.radius * 2), r)
        
        screen.blit(glow_surface, 
                   (self.x - self.radius * 2, self.y - self.radius * 2))

        if self.image:
            # Get the rect of the rotated image
            rect = self.image.get_rect()
            # Center the rect on the planet's position
            rect.center = (self.x, self.y)
            # Draw rotated planet image
            screen.blit(self.image, rect)
        else:
            # Draw default planet circle and details
            planet_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(planet_surface, self.color,
                             (self.radius, self.radius), self.radius)
            
            # Add surface details for gas giants
            if self.name in ["Jupiter", "Saturn"]:
                for i in range(-self.radius, self.radius, 4):
                    stripe_color = (min(255, self.color[0] + 20),
                                  min(255, self.color[1] + 20),
                                  min(255, self.color[2] + 20))
                    pygame.draw.line(planet_surface, stripe_color,
                                   (0, self.radius + i),
                                   (self.radius * 2, self.radius + i), 2)
            
            screen.blit(planet_surface, (self.x - self.radius, self.y - self.radius))

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.lifetime = BULLET_LIFETIME
        self.size = 3
        self.bounces = 0  # Track number of bounces
        self.max_bounces = 3  # Maximum number of bounces before disappearing

    def update(self):
        # Update position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.lifetime -= 1
        
        # Check for wall collisions and bounce
        if self.x <= 0 or self.x >= WIDTH:
            self.angle = 180 - self.angle  # Reverse horizontal direction
            self.bounces += 1
            # Add slight random angle variation on bounce
            self.angle += random() * 10 - 5
        
        if self.y <= 0 or self.y >= HEIGHT:
            self.angle = -self.angle  # Reverse vertical direction
            self.bounces += 1
            # Add slight random angle variation on bounce
            self.angle += random() * 10 - 5
        
        # Keep angle in range 0-360
        self.angle = self.angle % 360
        
        # Reduce speed slightly with each bounce
        if self.bounces > 0:
            self.speed = max(BULLET_SPEED * (0.8 ** self.bounces), 3)

    def draw(self, screen):
        # Draw bullet with color based on bounce count
        color = (
            min(255, 255 - self.bounces * 30),  # Reduce red
            min(255, 255 - self.bounces * 30),  # Reduce yellow
            min(255, self.bounces * 50)         # Add blue
        )
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

class Asteroid:
    def __init__(self):
        # Spawn from edge of screen
        if random() < 0.5:
            self.x = 0 if random() < 0.5 else WIDTH
            self.y = randint(0, HEIGHT)
        else:
            self.x = randint(0, WIDTH)
            self.y = 0 if random() < 0.5 else HEIGHT
        
        self.size = randint(15, 30)
        self.speed = random() * (ASTEROID_SPEED_MAX - ASTEROID_SPEED_MIN) + ASTEROID_SPEED_MIN
        # Angle towards center of screen with some randomness
        target_x = WIDTH//2 + randint(-200, 200)
        target_y = HEIGHT//2 + randint(-200, 200)
        self.angle = math.degrees(math.atan2(target_y - self.y, target_x - self.x))
        self.rotation = 0
        self.rotation_speed = random() * 2 - 1  # Random rotation speed
        
        # Create irregular shape
        self.points = []
        num_points = randint(6, 10)
        for i in range(num_points):
            angle = i * (360 / num_points)
            distance = self.size * (0.8 + random() * 0.4)
            self.points.append((
                math.cos(math.radians(angle)) * distance,
                math.sin(math.radians(angle)) * distance
            ))

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        self.rotation += self.rotation_speed

    def draw(self, screen):
        # Rotate and translate points
        rotated_points = []
        for x, y in self.points:
            # Rotate
            rot_x = x * math.cos(math.radians(self.rotation)) - y * math.sin(math.radians(self.rotation))
            rot_y = x * math.sin(math.radians(self.rotation)) + y * math.cos(math.radians(self.rotation))
            # Translate
            rotated_points.append((rot_x + self.x, rot_y + self.y))
        
        # Draw asteroid
        pygame.draw.polygon(screen, (169, 169, 169), rotated_points, 2)

    def check_collision(self, x, y, size):
        return math.sqrt((self.x - x)**2 + (self.y - y)**2) < self.size + size

class Comet:
    def __init__(self):
        # Determine spawn position (from edges only)
        if random() < 0.5:
            self.x = 0 if random() < 0.5 else WIDTH
            self.y = randint(0, HEIGHT)
        else:
            self.x = randint(0, WIDTH)
            self.y = 0 if random() < 0.5 else HEIGHT
        
        # Increased speed range (was 1-3, now 3-6)
        self.speed = random() * 3 + 3  # Speed between 3 and 6
        
        # Calculate target point avoiding middle area
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        avoid_radius = 200  # Radius of area to avoid around center
        
        while True:
            target_x = randint(0, WIDTH)
            target_y = randint(0, HEIGHT)
            # Check if target is too close to center
            dist_to_center = math.sqrt((target_x - center_x)**2 + (target_y - center_y)**2)
            if dist_to_center > avoid_radius:
                break
        
        # Calculate angle towards target
        self.angle = math.degrees(math.atan2(target_y - self.y, target_x - self.x))
        
        # Trail properties
        self.trail = []
        self.trail_length = 20
        self.size = random() * 2 + 1  # Comet size between 1 and 3

    def update(self):
        # Update position
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed
        
        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > self.trail_length:
            self.trail.pop(0)

    def draw(self, screen):
        # Draw trail with fade effect
        if len(self.trail) > 2:
            for i in range(len(self.trail) - 1):
                alpha = int(255 * (i / len(self.trail)))
                pygame.draw.line(screen, (255, 255, 255, alpha),
                               self.trail[i], self.trail[i + 1], 2)
        
        # Draw comet head
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), int(self.size))

class Rocket:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 4  # Changed from HEIGHT // 2 to HEIGHT // 4
        self.angle = 0
        self.speed = 0
        self.acceleration = 0.1
        self.max_speed = 5
        self.size = 20
        self.thrust = False
        self.particles = []
        self.thrust_start_time = 0
        self.fire_colors = [
            (255, 69, 0),    # Red-Orange
            (255, 165, 0),   # Orange
            (255, 215, 0),   # Yellow
            (255, 255, 255)  # White (core)
        ]
        
        # Load rocket images for different stages
        try:
            self.stage1_image = pygame.image.load(os.path.join(ASSETS_DIR, "Rocket-Stage1.png")).convert_alpha()
            self.stage2_image = pygame.image.load(os.path.join(ASSETS_DIR, "Rocket-Stage2.png")).convert_alpha()
            self.stage3_image = pygame.image.load(os.path.join(ASSETS_DIR, "Rocket-Stage3.png")).convert_alpha()
            
            # Scale all images to match rocket size
            self.stage1_image = pygame.transform.scale(self.stage1_image, (self.size * 2, self.size * 2))
            self.stage2_image = pygame.transform.scale(self.stage2_image, (self.size * 2, self.size * 2))
            self.stage3_image = pygame.transform.scale(self.stage3_image, (self.size * 2, self.size * 2))
            
            self.current_image = self.stage1_image
        except pygame.error as e:
            print(f"Could not load rocket images: {e}")
            self.stage1_image = None
            self.stage2_image = None
            self.stage3_image = None
        
        self.bullets = []
        self.shoot_cooldown = 0
        self.shoot_delay = 10  # Frames between shots

    def update(self, keys):
        # Rotation with both arrow keys and A/D
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += 5

        # Shooting
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if keys[pygame.K_SPACE] and self.shoot_cooldown == 0:
            self.bullets.append(Bullet(self.x, self.y, self.angle))
            self.shoot_cooldown = self.shoot_delay
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.lifetime <= 0 or bullet.bounces >= bullet.max_bounces:
                self.bullets.remove(bullet)

        # Forward thrust with both UP and W
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            if not self.thrust:
                self.thrust_start_time = time.time()
                self.thrust = True
            self.speed = min(self.speed + self.acceleration, self.max_speed)
            
            # Add new fire particles
            back_x = self.x - math.cos(math.radians(self.angle)) * self.size
            back_y = self.y - math.sin(math.radians(self.angle)) * self.size
            
            # Add multiple particles per frame
            for _ in range(5):
                spread_angle = self.angle + randint(-20, 20)  # Random spread
                speed = random() * 5 + 5  # Original speed range
                size = random() * 3 + 1   # Original size range
                color = choice(self.fire_colors)
                
                self.particles.append({
                    'x': back_x,
                    'y': back_y,
                    'dx': -math.cos(math.radians(spread_angle)) * speed,
                    'dy': -math.sin(math.radians(spread_angle)) * speed,
                    'size': size,
                    'color': color,
                    'life': 20,  # Original life
                    'fade_rate': random() * 0.1 + 0.05  # Original fade rate
                })
        
        # Backward thrust with DOWN and S
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if not self.thrust:
                self.thrust_start_time = time.time()
                self.thrust = True
            self.speed = max(self.speed - self.acceleration, -self.max_speed)
            
            # Add reverse thrust particles
            front_x = self.x + math.cos(math.radians(self.angle)) * self.size
            front_y = self.y + math.sin(math.radians(self.angle)) * self.size
            
            # Add multiple particles for reverse thrust
            for _ in range(5):
                spread_angle = self.angle + 180 + randint(-20, 20)
                speed = random() * 3 + 3  # Reduced speed range
                size = random() * 1.5 + 0.5   # Smaller size range
                color = choice(self.fire_colors)
                
                self.particles.append({
                    'x': front_x,
                    'y': front_y,
                    'dx': math.cos(math.radians(spread_angle)) * speed,
                    'dy': math.sin(math.radians(spread_angle)) * speed,
                    'size': size,
                    'color': color,
                    'life': 15,  # Shorter life
                    'fade_rate': random() * 0.15 + 0.1  # Faster fade
                })
        else:
            self.thrust = False
            self.thrust_start_time = 0
            # Apply drag to gradually slow down
            if abs(self.speed) > 0:
                self.speed *= 0.98  # Gradual slowdown
                if abs(self.speed) < 0.1:  # Stop completely if very slow
                    self.speed = 0

        # Movement
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        # Screen wrapping
        self.x = self.x % WIDTH
        self.y = self.y % HEIGHT

        # Update particles
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= particle['fade_rate']
            particle['size'] = max(0.1, particle['size'] - 0.1)
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)

        # Draw particles first (behind rocket)
        for particle in self.particles:
            alpha = int(255 * (particle['life'] / 20))  # Back to original life value
            color = (*particle['color'], alpha)
            
            # Create a surface for the glowing particle
            size = int(particle['size'] * 4)  # Original glow size multiplier
            particle_surf = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Draw multiple circles for glow effect
            for radius in range(int(particle['size'] * 2), 0, -1):  # Original glow radius
                glow_alpha = int(alpha * (radius / (particle['size'] * 2)))
                pygame.draw.circle(
                    particle_surf,
                    (*particle['color'], glow_alpha),
                    (size//2, size//2),
                    radius
                )
            
            # Draw the particle
            screen.blit(
                particle_surf,
                (int(particle['x'] - size//2), int(particle['y'] - size//2))
            )

        # Draw rocket image based on stage
        if self.stage1_image and self.stage2_image and self.stage3_image:
            # Determine current stage
            if not self.thrust:
                self.current_image = self.stage1_image
            else:
                thrust_duration = time.time() - self.thrust_start_time
                if thrust_duration < 2:
                    self.current_image = self.stage2_image
                else:
                    self.current_image = self.stage3_image
            
            # Rotate image
            rotated_image = pygame.transform.rotate(self.current_image, -self.angle - 90)
            # Get rect for centered drawing
            rect = rotated_image.get_rect(center=(self.x, self.y))
            screen.blit(rotated_image, rect)
        else:
            # Fallback to original triangle drawing if images not available
            points = [
                (self.x + math.cos(math.radians(self.angle)) * self.size,
                 self.y + math.sin(math.radians(self.angle)) * self.size),
                (self.x + math.cos(math.radians(self.angle + 140)) * self.size,
                 self.y + math.sin(math.radians(self.angle + 140)) * self.size),
                (self.x + math.cos(math.radians(self.angle + 220)) * self.size,
                 self.y + math.sin(math.radians(self.angle + 220)) * self.size)
            ]
            pygame.draw.polygon(screen, WHITE, points)

class InfoScreen:
    def __init__(self, planet_name, info):
        self.planet_name = planet_name
        self.info = info
        self.font_title = pygame.font.Font(None, 48)
        self.font_info = pygame.font.Font(None, 36)

    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw title
        title = self.font_title.render(self.info[0], True, WHITE)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))

        # Draw info lines
        for i, line in enumerate(self.info[1:], 1):
            text = self.font_info.render(line, True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 100 + i * 40))

        # Draw exit instruction
        exit_text = self.font_info.render("Press ESC to return to space", True, WHITE)
        screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT - 100))

class QuizScreen:
    def __init__(self, planet_name):
        self.font = pygame.font.Font(None, 36)
        self.planet_name = planet_name
        self.show_correct_answer = False
        self.options = {
            'answer1': {'rect': pygame.Rect(WIDTH//4 - 150, HEIGHT//2 - 100, 300, 50), 'color': (100, 100, 200)},
            'answer2': {'rect': pygame.Rect(WIDTH*3//4 - 150, HEIGHT//2 - 100, 300, 50), 'color': (100, 100, 200)},
            'answer3': {'rect': pygame.Rect(WIDTH//4 - 150, HEIGHT//2 + 50, 300, 50), 'color': (100, 100, 200)},
            'answer4': {'rect': pygame.Rect(WIDTH*3//4 - 150, HEIGHT//2 + 50, 300, 50), 'color': (100, 100, 200)},
            'back': {'rect': pygame.Rect(WIDTH//2 - 100, HEIGHT - 60, 200, 40), 'color': (100, 100, 200)}
        }
        self.questions = {
            "Mercury": [
                {
                    "question": "What is Mercury's position from the Sun?",
                    "answers": ["First", "Second", "Third", "Fourth"],
                    "correct": 0
                },
                {
                    "question": "How long is a year on Mercury?",
                    "answers": ["88 Earth days", "225 Earth days", "365 Earth days", "687 Earth days"],
                    "correct": 0
                },
                {
                    "question": "What is Mercury's surface temperature range?",
                    "answers": ["-180°C to 430°C", "-50°C to 100°C", "0°C to 100°C", "-100°C to 200°C"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Mercury have?",
                    "answers": ["None", "One", "Two", "Three"],
                    "correct": 0
                },
                {
                    "question": "What is Mercury named after?",
                    "answers": ["Roman messenger god", "Greek war god", "Norse thunder god", "Egyptian sun god"],
                    "correct": 0
                },
                {
                    "question": "What is Mercury's atmosphere like?",
                    "answers": ["Almost none", "Thick and cloudy", "Thin but breathable", "Mostly hydrogen"],
                    "correct": 0
                }
            ],
            "Venus": [
                {
                    "question": "What is Venus's most notable feature?",
                    "answers": ["Ring System", "Great Red Spot", "Thick Atmosphere", "Ice Caps"],
                    "correct": 2
                },
                {
                    "question": "Why is Venus so hot?",
                    "answers": ["Greenhouse effect", "Close to Sun", "Volcanic activity", "Core temperature"],
                    "correct": 0
                },
                {
                    "question": "What direction does Venus rotate?",
                    "answers": ["Backwards", "Forwards", "Doesn't rotate", "Sideways"],
                    "correct": 0
                },
                {
                    "question": "What is Venus's surface temperature?",
                    "answers": ["462°C", "100°C", "250°C", "350°C"],
                    "correct": 0
                },
                {
                    "question": "What is Venus often called?",
                    "answers": ["Earth's twin", "Red Planet", "Gas Giant", "Ice Planet"],
                    "correct": 0
                },
                {
                    "question": "What makes up most of Venus's atmosphere?",
                    "answers": ["Carbon dioxide", "Nitrogen", "Oxygen", "Hydrogen"],
                    "correct": 0
                }
            ],
            "Earth": [
                {
                    "question": "How many moons does Earth have?",
                    "answers": ["None", "One", "Two", "Three"],
                    "correct": 1
                },
                {
                    "question": "What makes Earth unique in our solar system?",
                    "answers": ["Known life", "Has water", "Has atmosphere", "Has a moon"],
                    "correct": 0
                },
                {
                    "question": "What percentage of Earth is covered by water?",
                    "answers": ["51%", "61%", "71%", "81%"],
                    "correct": 2
                },
                {
                    "question": "How long is Earth's day cycle?",
                    "answers": ["12 hours", "24 hours", "36 hours", "48 hours"],
                    "correct": 1
                },
                {
                    "question": "What is Earth's core made of?",
                    "answers": ["Iron and nickel", "Rock and magma", "Gold and silver", "Ice and rock"],
                    "correct": 0
                },
                {
                    "question": "What protects Earth from solar radiation?",
                    "answers": ["Magnetic field", "Atmosphere", "Ozone layer", "All of these"],
                    "correct": 3
                }
            ],
            "Mars": [
                {
                    "question": "What gives Mars its red color?",
                    "answers": ["Iron Oxide", "Methane", "Sulfur", "Carbon Dioxide"],
                    "correct": 0
                },
                {
                    "question": "What is the name of Mars's largest volcano?",
                    "answers": ["Olympus Mons", "Mount Everest", "Mauna Kea", "Valles Marineris"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Mars have?",
                    "answers": ["Two", "One", "Three", "None"],
                    "correct": 0
                },
                {
                    "question": "What is Mars's year length in Earth days?",
                    "answers": ["687", "365", "550", "825"],
                    "correct": 0
                },
                {
                    "question": "What is the largest canyon on Mars called?",
                    "answers": ["Valles Marineris", "Grand Canyon", "Hellas Basin", "Argyre Planitia"],
                    "correct": 0
                },
                {
                    "question": "What evidence suggests Mars once had water?",
                    "answers": ["Dried riverbeds", "Blue color", "Cloud formations", "Plant fossils"],
                    "correct": 0
                }
            ],
            "Jupiter": [
                {
                    "question": "What is Jupiter's most famous feature?",
                    "answers": ["Ice Caps", "Great Red Spot", "Ring System", "Water Oceans"],
                    "correct": 1
                },
                {
                    "question": "What type of planet is Jupiter?",
                    "answers": ["Gas giant", "Rocky planet", "Ice giant", "Dwarf planet"],
                    "correct": 0
                },
                {
                    "question": "How many known moons does Jupiter have?",
                    "answers": ["79", "50", "63", "92"],
                    "correct": 0
                },
                {
                    "question": "How long is Jupiter's year in Earth years?",
                    "answers": ["12", "8", "15", "20"],
                    "correct": 0
                },
                {
                    "question": "What is Jupiter's Great Red Spot?",
                    "answers": ["A storm", "A volcano", "A crater", "An ocean"],
                    "correct": 0
                },
                {
                    "question": "Which moon of Jupiter might have life?",
                    "answers": ["Europa", "Io", "Ganymede", "Callisto"],
                    "correct": 0
                }
            ],
            "Saturn": [
                {
                    "question": "What is Saturn most famous for?",
                    "answers": ["Great Red Spot", "Blue Color", "Ring System", "High Temperature"],
                    "correct": 2
                },
                {
                    "question": "What are Saturn's rings made of?",
                    "answers": ["Ice and rock", "Gas clouds", "Metal debris", "Liquid hydrogen"],
                    "correct": 0
                },
                {
                    "question": "How many confirmed moons does Saturn have?",
                    "answers": ["82", "63", "45", "95"],
                    "correct": 0
                },
                {
                    "question": "What is unique about Saturn's density?",
                    "answers": ["Could float in water", "Heaviest planet", "Densest atmosphere", "Solid core"],
                    "correct": 0
                },
                {
                    "question": "Which is Saturn's largest moon?",
                    "answers": ["Titan", "Enceladus", "Mimas", "Rhea"],
                    "correct": 0
                },
                {
                    "question": "How wide are Saturn's rings?",
                    "answers": ["175,000 miles", "50,000 miles", "100,000 miles", "25,000 miles"],
                    "correct": 0
                }
            ],
            "Uranus": [
                {
                    "question": "What is unique about Uranus's rotation?",
                    "answers": ["Very Fast", "Rotates Backwards", "Rotates on its Side", "Doesn't Rotate"],
                    "correct": 2
                },
                {
                    "question": "What type of planet is Uranus?",
                    "answers": ["Ice giant", "Gas giant", "Rocky planet", "Dwarf planet"],
                    "correct": 0
                },
                {
                    "question": "How many known moons does Uranus have?",
                    "answers": ["27", "15", "32", "21"],
                    "correct": 0
                },
                {
                    "question": "What is Uranus's temperature?",
                    "answers": ["-224°C", "-180°C", "-150°C", "-200°C"],
                    "correct": 0
                },
                {
                    "question": "What gives Uranus its blue-green color?",
                    "answers": ["Methane gas", "Water ice", "Ammonia clouds", "Hydrogen"],
                    "correct": 0
                },
                {
                    "question": "Who discovered Uranus?",
                    "answers": ["William Herschel", "Galileo Galilei", "Johannes Kepler", "Edwin Hubble"],
                    "correct": 0
                }
            ],
            "Neptune": [
                {
                    "question": "What is Neptune known for?",
                    "answers": ["Strongest Winds", "Highest Temperature", "Most Moons", "Closest to Sun"],
                    "correct": 0
                },
                {
                    "question": "How fast are Neptune's strongest winds?",
                    "answers": ["2,100 km/h", "1,200 km/h", "800 km/h", "1,500 km/h"],
                    "correct": 0
                },
                {
                    "question": "How many known moons does Neptune have?",
                    "answers": ["14", "8", "21", "17"],
                    "correct": 0
                },
                {
                    "question": "How long is Neptune's year in Earth years?",
                    "answers": ["165", "120", "200", "150"],
                    "correct": 0
                },
                {
                    "question": "What is Neptune's largest moon?",
                    "answers": ["Triton", "Nereid", "Naiad", "Thalassa"],
                    "correct": 0
                },
                {
                    "question": "What makes Neptune blue?",
                    "answers": ["Methane gas", "Water ice", "Nitrogen", "Hydrogen"],
                    "correct": 0
                }
            ],
            "Sun": [
                {
                    "question": "What type of star is the Sun?",
                    "answers": ["Yellow Dwarf", "Red Giant", "White Dwarf", "Neutron Star"],
                    "correct": 0
                },
                {
                    "question": "How long does it take sunlight to reach Earth?",
                    "answers": ["8 minutes", "2 minutes", "30 minutes", "1 second"],
                    "correct": 0
                },
                {
                    "question": "What is the Sun's core temperature?",
                    "answers": ["15 million °C", "5,500 °C", "1 million °C", "100,000 °C"],
                    "correct": 0
                },
                {
                    "question": "What process powers the Sun?",
                    "answers": ["Nuclear Fusion", "Nuclear Fission", "Chemical Burning", "Solar Wind"],
                    "correct": 0
                },
                {
                    "question": "What is the Sun's outermost layer called?",
                    "answers": ["Corona", "Photosphere", "Chromosphere", "Core"],
                    "correct": 0
                },
                {
                    "question": "What percentage of the solar system's mass is in the Sun?",
                    "answers": ["99.86%", "75%", "85%", "95%"],
                    "correct": 0
                }
            ]
        }
        self.used_questions = []
        self.get_new_question()
        self.result = None
        self.result_timer = 0
        self.rocket_reset_position = False
        self.stars = [(randint(0, WIDTH), randint(0, HEIGHT), random() * 2, choice(STAR_COLORS)) 
                     for _ in range(100)]

    def get_new_question(self):
        available_questions = [q for q in self.questions[self.planet_name] 
                             if q not in self.used_questions]
        if not available_questions:  # If all questions have been used, reset
            self.used_questions = []
            available_questions = self.questions[self.planet_name]
        
        self.current_question = choice(available_questions)
        self.used_questions.append(self.current_question)

    def check_answer(self, rocket_rect):
        if self.result is not None:
            if self.result_timer <= 0:
                if self.show_correct_answer:  # If we were showing the correct answer
                    self.get_new_question()
                    self.show_correct_answer = False
                else:  # If answer was wrong and we haven't shown correct answer yet
                    self.show_correct_answer = True
                    self.result_timer = 180  # Show correct answer for 3 seconds
                self.result = None  # Reset result state
            return None

        for i, (key, data) in enumerate(self.options.items()):
            if key != 'back' and rocket_rect.colliderect(data['rect']):
                if i == self.current_question['correct']:
                    self.result = True
                    self.result_timer = 60  # Show success message for 1 second
                    self.get_new_question()  # Immediately get new question
                else:
                    self.result = False
                    self.result_timer = 120  # Show wrong answer message for 2 seconds
                self.rocket_reset_position = True  # Reset position for both correct and wrong answers
                return None
            elif key == 'back' and rocket_rect.colliderect(data['rect']):
                return 'back'
        return None

    def draw(self, screen, rocket):
        # Draw background
        screen.fill(BLACK)
        
        # Draw stars
        for x, y, size, color in self.stars:
            star_x = (x - rocket.x/16) % WIDTH
            star_y = (y - rocket.y/16) % HEIGHT
            brightness = 0.7 + (math.sin(time.time() * 2 + x * y) * 0.3)
            star_color = tuple(int(c * brightness) for c in color)
            pygame.draw.circle(screen, star_color, (int(star_x), int(star_y)), size)

        # Draw question
        question_surface = self.font.render(self.current_question["question"], True, WHITE)
        question_rect = question_surface.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(question_surface, question_rect)

        # Draw answer options
        for i, (key, data) in enumerate(self.options.items()):
            if key == 'back':
                text = "BACK"
            else:
                text = self.current_question["answers"][i]
            
            # Determine button color
            button_color = data['color']
            if self.show_correct_answer and i == self.current_question['correct']:
                button_color = (100, 255, 100)  # Green for correct answer
            
            # Draw button with glow
            glow_rect = data['rect'].inflate(8, 8)
            for g in range(3):
                glow_alpha = 100 - g * 30
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surface, (*button_color, glow_alpha), 
                               glow_surface.get_rect(), border_radius=10)
                screen.blit(glow_surface, glow_rect.topleft)
            
            # Draw main button
            button_surface = pygame.Surface((data['rect'].width, data['rect'].height), pygame.SRCALPHA)
            pygame.draw.rect(button_surface, (*button_color, 200), 
                           button_surface.get_rect(), border_radius=8)
            screen.blit(button_surface, data['rect'].topleft)
            
            # Draw text
            text_surface = self.font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=data['rect'].center)
            screen.blit(text_surface, text_rect)

        # Draw result if there is one
        if self.result is not None:
            if self.result:
                result_text = "Congratulations! Correct Answer!"
                color = (100, 255, 100)
            else:
                result_text = "Wrong Answer!"
                color = (255, 100, 100)
            
            result_surface = self.font.render(result_text, True, color)
            result_rect = result_surface.get_rect(center=(WIDTH//2, HEIGHT//3))
            screen.blit(result_surface, result_rect)
            
            self.result_timer -= 1
            if self.result_timer <= 0:
                self.result = None

    def reset_rocket(self, rocket):
        rocket.x = WIDTH // 2  # Center horizontally
        rocket.y = HEIGHT * 3 // 4  # Changed from HEIGHT // 2 to HEIGHT * 3 // 4
        rocket.speed = 0
        self.rocket_reset_position = False

class SpaceExplorer:
    def __init__(self):
        self.planets = [Planet(name, data) for name, data in planets.items() if name != "Sun"]
        self.stars = [Star() for _ in range(200)]
        self.rocket = Rocket()
        self.asteroids = []
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        self.current_info_screen = None
        self.current_quiz_screen = None
        self.cooldown = 0
        self.planet_view = False
        self.current_planet = None
        self.transition_alpha = 0
        self.planet_view_stars = [(randint(0, WIDTH), randint(0, HEIGHT), random() * 2, choice(STAR_COLORS)) 
                                for _ in range(150)]
        self.surface_details = []
        self.options = {
            'facts': {'rect': pygame.Rect(20, 20, 100, 40), 'color': (100, 200, 100)},
            'quiz': {'rect': pygame.Rect(WIDTH - 120, 20, 100, 40), 'color': (200, 100, 100)},
            'back': {'rect': pygame.Rect(WIDTH//2 - 100, HEIGHT - 60, 200, 40), 'color': (100, 100, 200)}
        }
        
        # Add sun image loading
        try:
            self.sun_image = pygame.image.load(os.path.join(ASSETS_DIR, "sun.png")).convert_alpha()
            # Scale the sun image (reduced size from 150 to 100)
            self.sun_image = pygame.transform.scale(self.sun_image, (100, 100))
            self.use_sun_image = True
            self.sun_rotation = 0
            self.sun_rotation_speed = 0.1
        except pygame.error as e:
            print(f"Could not load sun image: {e}")
            self.use_sun_image = False
        
        # Add menu state and font
        self.in_menu = True
        self.menu_font = pygame.font.Font(None, 74)
        self.menu_alpha = 0
        self.alpha_direction = 1
        
        # Replace launch button with galaxy particles
        self.launch_button = {
            'rect': pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 50, 300, 80),
            'color': (100, 100, 200),
            'hover': False
        }
        self.comets = []
        self.comet_spawn_timer = 0
        
        # Add development button with increased width
        self.dev_button = {
            'rect': pygame.Rect(WIDTH//2 - 200, HEIGHT//2 + 150, 400, 80),  # Increased width from 300 to 400
            'color': (100, 200, 100),
            'hover': False
        }
        
        # Add development mode properties
        self.in_dev_mode = False
        self.history_images = []
        self.current_image_index = 0
        
        # Load history images
        history_dir = "history"
        if os.path.exists(history_dir):
            for file in os.listdir(history_dir):
                if file.endswith(".jpg"):
                    try:
                        img_path = os.path.join(history_dir, file)
                        img = pygame.image.load(img_path)
                        # Scale image to fit screen while maintaining aspect ratio
                        img_ratio = img.get_width() / img.get_height()
                        if img_ratio > WIDTH / HEIGHT:
                            new_width = WIDTH
                            new_height = int(WIDTH / img_ratio)
                        else:
                            new_height = HEIGHT
                            new_width = int(HEIGHT * img_ratio)
                        img = pygame.transform.scale(img, (new_width, new_height))
                        self.history_images.append(img)
                    except pygame.error as e:
                        print(f"Could not load image {file}: {e}")

    def reset_rocket_position(self):
        if not self.planet_view:
            # Position rocket in the upper middle of the solar system screen
            self.rocket.x = WIDTH // 2
            self.rocket.y = HEIGHT // 4  # Changed from HEIGHT // 2 to HEIGHT // 4
        else:
            if self.current_quiz_screen:
                # Position rocket in the upper middle for quiz
                self.rocket.x = WIDTH // 2
                self.rocket.y = HEIGHT // 4  # Changed from HEIGHT // 2 to HEIGHT // 4
            else:
                # Position rocket on the planet screen
                self.rocket.x = WIDTH // 2
                self.rocket.y = HEIGHT // 4  # Changed from HEIGHT - 100 to HEIGHT // 4
        self.rocket.speed = 0
        self.cooldown = 30

    def check_collisions(self):
        if not self.planet_view:
            # First check collision with Sun (changed radius from 60 to 40)
            distance_to_sun = math.sqrt(
                (self.rocket.x - WIDTH//2)**2 + 
                (self.rocket.y - HEIGHT//2)**2
            )
            if distance_to_sun < 40 + self.rocket.size:  # Changed from 60 to 40
                return Planet("Sun", planets["Sun"])
            
            # Then check other planets
            for planet in self.planets:
                distance = math.sqrt(
                    (self.rocket.x - planet.x)**2 + 
                    (self.rocket.y - planet.y)**2
                )
                if distance < planet.radius + self.rocket.size:
                    return planet
        return None

    def enter_planet_view(self, planet):
        self.planet_view = True
        self.current_planet = planet
        self.transition_alpha = 255
        self.rocket.x = WIDTH // 2
        self.rocket.y = HEIGHT // 4
        self.rocket.speed = 0
        
        # Generate persistent surface details for this planet
        planet_radius = self.current_planet.radius * 8
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        self.surface_details = []
        for _ in range(40):
            angle = random() * 2 * math.pi
            distance = random() * planet_radius
            x = math.cos(angle) * distance
            y = math.sin(angle) * distance
            radius = randint(5, 15)
            shade = randint(-30, 30)
            self.surface_details.append((x, y, radius, shade))

    def exit_planet_view(self):
        self.planet_view = False
        self.current_planet = None
        self.transition_alpha = 0
        self.reset_rocket_position()

    def check_option_collisions(self):
        if not self.planet_view:
            return None
        
        rocket_rect = pygame.Rect(self.rocket.x - self.rocket.size, 
                                self.rocket.y - self.rocket.size,
                                self.rocket.size * 2, 
                                self.rocket.size * 2)
        
        for option, data in self.options.items():
            if rocket_rect.colliderect(data['rect']):
                return option
        return None

    def draw_option_button(self, screen, rect, text, color):
        # Draw button background with glow
        glow_rect = rect.inflate(8, 8)
        for i in range(3):
            glow_alpha = 100 - i * 30
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*color, glow_alpha), 
                           glow_surface.get_rect(), border_radius=10)
            screen.blit(glow_surface, glow_rect.topleft)
        
        # Draw main button
        button_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*color, 200), 
                        button_surface.get_rect(), border_radius=8)
        screen.blit(button_surface, rect.topleft)
        
        # Draw text
        text_surface = self.large_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)

    def update_space_objects(self):
        # Update comets
        self.comet_spawn_timer -= 1
        if self.comet_spawn_timer <= 0 and len(self.comets) < 3:
            if random() < 0.05:
                self.comets.append(Comet())
                self.comet_spawn_timer = randint(120, 240)
        
        # Update existing comets
        for comet in self.comets[:]:
            comet.update()
            if (comet.x < -50 or comet.x > WIDTH + 50 or 
                comet.y < -50 or comet.y > HEIGHT + 50):
                self.comets.remove(comet)
        
        # Update asteroids
        if len(self.asteroids) < MAX_ASTEROIDS and random() < ASTEROID_SPAWN_RATE:
            self.asteroids.append(Asteroid())

        for asteroid in self.asteroids[:]:
            asteroid.update()
            
            # Check collision with bullets
            for bullet in self.rocket.bullets[:]:
                if asteroid.check_collision(bullet.x, bullet.y, bullet.size):
                    if asteroid in self.asteroids:
                        self.asteroids.remove(asteroid)
                    if bullet in self.rocket.bullets:
                        self.rocket.bullets.remove(bullet)
                    break
            
            # Remove asteroids that are far off screen
            if (asteroid.x < -100 or asteroid.x > WIDTH + 100 or 
                asteroid.y < -100 or asteroid.y > HEIGHT + 100):
                if asteroid in self.asteroids:
                    self.asteroids.remove(asteroid)

    def draw_planet_screen(self, screen):
        # Draw a space background
        screen.fill(BLACK)

        # Draw background stars with slower movement
        for x, y, size, color in self.planet_view_stars:
            star_x = (x - self.rocket.x/8) % WIDTH
            star_y = (y - self.rocket.y/8) % HEIGHT
            brightness = 0.7 + (math.sin(time.time() * 2 + x * y) * 0.3)
            star_color = tuple(int(c * brightness) for c in color)
            pygame.draw.circle(screen, star_color, (int(star_x), int(star_y)), size)

        # Draw comets and asteroids
        for comet in self.comets:
            comet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

        # Special handling for Sun view
        if self.current_planet.name == "Sun":
            if self.use_sun_image:
                self.draw_sun()  # Use the existing sun drawing method
            else:
                # Fallback to basic sun drawing if image isn't available
                center_x = WIDTH // 2
                center_y = HEIGHT // 2
                pygame.draw.circle(screen, YELLOW, (center_x, center_y), 60)
        else:
            # Regular planet drawing code
            planet_radius = self.current_planet.radius * 8
            center_x = WIDTH // 2
            center_y = HEIGHT // 2

            # Draw planet glow/atmosphere with smoother gradient
            for radius in range(planet_radius + 20, planet_radius - 2, -1):
                alpha = int(20 * (radius - planet_radius + 2) / 22)
                glow_color = (*self.current_planet.color, alpha)
                pygame.draw.circle(screen, glow_color, (center_x, center_y), radius)

            # Draw main planet body
            pygame.draw.circle(screen, self.current_planet.color, (center_x, center_y), planet_radius)

            # Draw persistent surface details
            for x, y, radius, shade in self.surface_details:
                color = tuple(max(0, min(255, c + shade)) for c in self.current_planet.color)
                pygame.draw.circle(screen, color, 
                                 (int(center_x + x), int(center_y + y)), radius)

            # Special details for specific planets
            if self.current_planet.name == "Jupiter":
                # Draw Jupiter's bands with smoother gradients
                for i in range(-planet_radius, planet_radius, 8):
                    base_color = self.current_planet.color
                    stripe_color = tuple(min(255, c + 20 + int(10 * math.sin(i * 0.1))) 
                                               for c in base_color)
                    y = center_y + i
                    x_offset = math.sqrt(max(0, planet_radius**2 - i**2))
                    pygame.draw.line(screen, stripe_color,
                                   (center_x - x_offset, y),
                                   (center_x + x_offset, y), 3)

        # Draw interactive options
        self.draw_option_button(screen, self.options['facts']['rect'], "FACTS", self.options['facts']['color'])
        self.draw_option_button(screen, self.options['quiz']['rect'], "QUIZ", self.options['quiz']['color'])
        self.draw_option_button(screen, self.options['back']['rect'], "BACK", self.options['back']['color'])

    def draw_sun(self):
        if self.use_sun_image:
            # Update rotation
            self.sun_rotation = (self.sun_rotation + self.sun_rotation_speed) % 360
            
            # Create pulsing effect for the image
            pulse = abs(math.sin(time.time())) * 10
            pulse_size = int(100 + pulse)  # Base size 100px + pulse
            
            # Draw sun glow/corona
            corona_surfaces = []
            for i in range(5):
                corona_surf = pygame.Surface((200, 200), pygame.SRCALPHA)
                radius = 80 + i * 10
                alpha = int(100 * (1 - i/5))
                pygame.draw.circle(corona_surf, (255, 200, 50, alpha), (100, 100), radius)
                corona_surfaces.append(corona_surf)
            
            # Draw corona layers
            for surf in corona_surfaces:
                screen.blit(surf, (WIDTH//2 - 100, HEIGHT//2 - 100))
            
            # Scale and rotate the sun image
            scaled_sun = pygame.transform.scale(
                self.sun_image, 
                (pulse_size, pulse_size)
            )
            rotated_sun = pygame.transform.rotate(scaled_sun, self.sun_rotation)
            
            # Center the sun image
            sun_rect = rotated_sun.get_rect(
                center=(WIDTH // 2, HEIGHT // 2)
            )
            
            # Draw the sun image
            screen.blit(rotated_sun, sun_rect)
            
        else:
            # Fallback to original sun drawing code
            corona_surfaces = []
            for i in range(5):
                corona_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
                radius = 60 + i * 10
                alpha = int(100 * (1 - i/5))
                pygame.draw.circle(corona_surf, (255, 200, 50, alpha), (50, 50), radius)
                corona_surfaces.append(corona_surf)
            
            pulse = abs(math.sin(time.time())) * 10
            
            for surf in corona_surfaces:
                screen.blit(surf, (WIDTH//2 - 50, HEIGHT//2 - 50))
            
            pygame.draw.circle(screen, YELLOW, (WIDTH//2, HEIGHT//2), 50 + pulse)
            
            for i in range(8):
                angle = time.time() + i * math.pi/4
                x = WIDTH//2 + math.cos(angle) * 45
                y = HEIGHT//2 + math.sin(angle) * 45
                pygame.draw.circle(screen, (255, 200, 50), (int(x), int(y)), 10)

    def draw_menu(self, screen):
        # Draw background
        screen.fill(BLACK)
        
        # Draw animated stars
        for star in self.stars:
            star.update()
            star.draw(screen)
        
        # Draw title text with glow effect
        title_text = self.menu_font.render("SPACE EXPLORER", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        
        # Draw title glow
        glow_surf = pygame.Surface((title_text.get_width() + 20, title_text.get_height() + 20), pygame.SRCALPHA)
        glow_color = (255, 255, 255, self.menu_alpha)
        glow_text = self.menu_font.render("SPACE EXPLORER", True, glow_color)
        glow_rect = glow_text.get_rect(center=(glow_surf.get_width() // 2, glow_surf.get_height() // 2))
        glow_surf.blit(glow_text, glow_rect)
        screen.blit(glow_surf, (title_rect.x - 10, title_rect.y - 10))
        screen.blit(title_text, title_rect)
        
        # Update button hover state
        mouse_pos = pygame.mouse.get_pos()
        self.launch_button['hover'] = self.launch_button['rect'].collidepoint(mouse_pos)
        self.dev_button['hover'] = self.dev_button['rect'].collidepoint(mouse_pos)
        
        # Draw launch button with glow effect
        button_color = (150, 150, 255) if self.launch_button['hover'] else self.launch_button['color']
        
        # Draw button glow
        glow_rect = self.launch_button['rect'].inflate(16, 16)
        for i in range(3):
            glow_alpha = 100 - i * 30
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*button_color, glow_alpha), 
                           glow_surface.get_rect(), border_radius=10)
            screen.blit(glow_surface, glow_rect.topleft)
        
        # Draw main button
        button_surface = pygame.Surface((self.launch_button['rect'].width, self.launch_button['rect'].height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*button_color, 200), 
                        button_surface.get_rect(), border_radius=8)
        screen.blit(button_surface, self.launch_button['rect'].topleft)
        
        # Draw button text
        launch_text = self.menu_font.render("LAUNCH", True, WHITE)
        text_rect = launch_text.get_rect(center=self.launch_button['rect'].center)
        screen.blit(launch_text, text_rect)
        
        # Draw development button
        dev_color = (150, 255, 150) if self.dev_button['hover'] else self.dev_button['color']
        
        # Draw button glow
        glow_rect = self.dev_button['rect'].inflate(16, 16)
        for i in range(3):
            glow_alpha = 100 - i * 30
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (*dev_color, glow_alpha), 
                           glow_surface.get_rect(), border_radius=10)
            screen.blit(glow_surface, glow_rect.topleft)
        
        # Draw main button
        button_surface = pygame.Surface((self.dev_button['rect'].width, self.dev_button['rect'].height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*dev_color, 200), 
                        button_surface.get_rect(), border_radius=8)
        screen.blit(button_surface, self.dev_button['rect'].topleft)
        
        # Draw button text
        dev_text = self.menu_font.render("DEVELOPMENT", True, WHITE)
        text_rect = dev_text.get_rect(center=self.dev_button['rect'].center)
        screen.blit(dev_text, text_rect)

    def draw_dev_mode(self, screen):
        if not self.history_images:
            screen.fill(BLACK)
            text = self.large_font.render("No history images found", True, WHITE)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
            return

        # Draw current image
        current_img = self.history_images[self.current_image_index]
        # Center the image
        x = (WIDTH - current_img.get_width()) // 2
        y = (HEIGHT - current_img.get_height()) // 2
        screen.blit(current_img, (x, y))

        # Update and draw space objects
        self.update_space_objects()  # Update asteroids and comets
        
        # Draw comets and asteroids
        for comet in self.comets:
            comet.draw(screen)
        for asteroid in self.asteroids:
            asteroid.draw(screen)

        # Draw rocket
        self.rocket.draw(screen)

        # Draw escape text in corner with glow effect
        escape_text = "press escape to go back to menu"
        text_surface = self.font.render(escape_text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (WIDTH - 20, HEIGHT - 20)  # Position in bottom-right corner

        # Add glow effect
        glow_surface = pygame.Surface((text_rect.width + 4, text_rect.height + 4), pygame.SRCALPHA)
        for offset in range(3):
            glow_alpha = 100 - offset * 30
            glow_text = self.font.render(escape_text, True, (255, 255, 255, glow_alpha))
            glow_rect = glow_text.get_rect(center=(glow_surface.get_width()//2, glow_surface.get_height()//2))
            glow_surface.blit(glow_text, glow_rect)
        
        screen.blit(glow_surface, (text_rect.x - 2, text_rect.y - 2))
        screen.blit(text_surface, text_rect)

        # Check if rocket moves to next/previous image
        if self.rocket.x > WIDTH - 50:  # Move to next image
            self.current_image_index = (self.current_image_index + 1) % len(self.history_images)
            self.rocket.x = 51
        elif self.rocket.x < 50:  # Move to previous image
            self.current_image_index = (self.current_image_index - 1) % len(self.history_images)
            self.rocket.x = WIDTH - 51

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        if self.in_menu:
                            mouse_pos = pygame.mouse.get_pos()
                            if self.launch_button['rect'].collidepoint(mouse_pos):
                                self.in_menu = False
                            elif self.dev_button['rect'].collidepoint(mouse_pos):
                                self.in_menu = False
                                self.in_dev_mode = True
                                self.rocket.x = WIDTH // 2
                                self.rocket.y = HEIGHT // 2
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.in_dev_mode:
                            self.in_dev_mode = False
                            self.in_menu = True
                        elif self.current_info_screen:
                            self.current_info_screen = None
                        elif self.planet_view:
                            self.exit_planet_view()
                        elif not self.in_menu:  # If in solar system view
                            self.in_menu = True
                            self.reset_rocket_position()

            # Update space objects for all game states except menu
            if not self.in_menu:
                self.update_space_objects()

            # Update button hover states in menu
            if self.in_menu:
                mouse_pos = pygame.mouse.get_pos()
                self.launch_button['hover'] = self.launch_button['rect'].collidepoint(mouse_pos)
                self.dev_button['hover'] = self.dev_button['rect'].collidepoint(mouse_pos)
                self.draw_menu(screen)
            elif self.in_dev_mode:
                keys = pygame.key.get_pressed()
                self.rocket.update(keys)
                self.draw_dev_mode(screen)
            elif self.current_info_screen:
                self.current_info_screen.draw(screen)
                # Draw space objects in info screen
                for comet in self.comets:
                    comet.draw(screen)
                for asteroid in self.asteroids:
                    asteroid.draw(screen)
            elif self.current_quiz_screen:
                self.current_quiz_screen.draw(screen, self.rocket)
                
                if self.current_quiz_screen.rocket_reset_position:
                    self.current_quiz_screen.reset_rocket(self.rocket)
                
                keys = pygame.key.get_pressed()
                self.rocket.update(keys)
                
                # Draw space objects
                for comet in self.comets:
                    comet.draw(screen)
                for asteroid in self.asteroids:
                    asteroid.draw(screen)
                
                rocket_rect = pygame.Rect(self.rocket.x - self.rocket.size, 
                                        self.rocket.y - self.rocket.size,
                                        self.rocket.size * 2, 
                                        self.rocket.size * 2)
                result = self.current_quiz_screen.check_answer(rocket_rect)
                if result == 'back':
                    self.current_quiz_screen = None
                    self.reset_rocket_position()
                
                self.rocket.draw(screen)
            else:
                keys = pygame.key.get_pressed()
                self.rocket.update(keys)

                if self.cooldown > 0:
                    self.cooldown -= 1
                else:
                    if not self.planet_view:
                        collided_planet = self.check_collisions()
                        if collided_planet:
                            self.enter_planet_view(collided_planet)
                    else:
                        option_hit = self.check_option_collisions()
                        if option_hit == 'facts':
                            self.current_info_screen = InfoScreen(
                                self.current_planet.name,
                                planets[self.current_planet.name]["info"]
                            )
                            self.reset_rocket_position()
                        elif option_hit == 'quiz':
                            self.current_quiz_screen = QuizScreen(self.current_planet.name)
                            self.reset_rocket_position()
                        elif option_hit == 'back':
                            self.exit_planet_view()

                screen.fill(BLACK)
                
                if not self.planet_view:
                    for star in self.stars:
                        star.update()
                        star.draw(screen)
                    self.draw_sun()
                    for planet in self.planets:
                        planet.update()
                        planet.draw(screen)
                    # Draw comets and asteroids after planets
                    for comet in self.comets:
                        comet.draw(screen)
                    for asteroid in self.asteroids:
                        asteroid.draw(screen)
                
                    # Add escape text in corner with glow effect
                    escape_text = "press escape to go back to menu"
                    text_surface = self.font.render(escape_text, True, WHITE)
                    text_rect = text_surface.get_rect()
                    text_rect.bottomright = (WIDTH - 20, HEIGHT - 20)

                    # Add glow effect
                    glow_surface = pygame.Surface((text_rect.width + 4, text_rect.height + 4), pygame.SRCALPHA)
                    for offset in range(3):
                        glow_alpha = 100 - offset * 30
                        glow_text = self.font.render(escape_text, True, (255, 255, 255, glow_alpha))
                        glow_rect = glow_text.get_rect(center=(glow_surface.get_width()//2, glow_surface.get_height()//2))
                        glow_surface.blit(glow_text, glow_rect)
                    
                    screen.blit(glow_surface, (text_rect.x - 2, text_rect.y - 2))
                    screen.blit(text_surface, text_rect)
                else:
                    self.draw_planet_screen(screen)

                self.rocket.draw(screen)

                if self.transition_alpha > 0:
                    fade_surface = pygame.Surface((WIDTH, HEIGHT))
                    fade_surface.fill(BLACK)
                    fade_surface.set_alpha(self.transition_alpha)
                    screen.blit(fade_surface, (0, 0))
                    
                    if self.planet_view:
                        self.transition_alpha = max(0, self.transition_alpha - 10)
                    else:
                        self.transition_alpha = max(0, self.transition_alpha - 10)

            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    explorer = SpaceExplorer()
    explorer.run() 