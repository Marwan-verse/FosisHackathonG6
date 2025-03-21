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
STAR_COLORS = [(255, 255, 255), (255, 255, 200), (200, 200, 255), (255, 200, 200)]

# Add after other constants
ASSETS_DIR = "assets"  # Create this directory to store your pixel art images

# Planet data with extended information
planets = {
    "Mercury": {
        "color": (169, 169, 169),  # Grey
        "radius": 10,
        "orbit": 100,
        "speed": 0.02,
        "image": "mercury.png",  # Add your pixel art filenames here
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

        # Draw Saturn's rings if applicable
        if self.name == "Saturn":
            ring_surface = pygame.Surface((self.radius * 4, self.radius * 2), pygame.SRCALPHA)
            for r in range(self.radius + 15, self.radius + 25):
                alpha = int(150 * (1 - (r - self.radius - 15) / 10))
                pygame.draw.ellipse(ring_surface, (*self.color, alpha),
                                  (0, self.radius - r//4, self.radius * 4, r//2), 1)
            screen.blit(ring_surface,
                       (self.x - self.radius * 2, self.y - self.radius))

class Rocket:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
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

    def update(self, keys):
        # Rotation with both arrow keys and A/D
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle -= 5
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle += 5

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

        # Update existing particles
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= particle['fade_rate']
            particle['size'] = max(0.1, particle['size'] - 0.1)
            
            # Remove dead particles
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw(self, screen):
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

class SpaceExplorer:
    def __init__(self):
        self.planets = [Planet(name, data) for name, data in planets.items()]
        self.stars = [Star() for _ in range(200)]
        self.rocket = Rocket()
        self.font = pygame.font.Font(None, 24)
        self.current_info_screen = None
        self.cooldown = 0  # Add cooldown timer

    def reset_rocket_position(self):
        # Move rocket to center of screen, away from planets
        self.rocket.x = WIDTH // 2
        self.rocket.y = HEIGHT // 2
        self.rocket.speed = 0  # Stop rocket movement
        self.cooldown = 30  # Set cooldown timer (30 frames)

    def check_collisions(self):
        for planet in self.planets:
            distance = math.sqrt((self.rocket.x - planet.x)**2 + 
                               (self.rocket.y - planet.y)**2)
            if distance < planet.radius + self.rocket.size:
                return planet
        return None

    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and self.current_info_screen:
                        self.current_info_screen = None
                        self.reset_rocket_position()  # Reset position when exiting info screen

            if self.current_info_screen:
                self.current_info_screen.draw(screen)
            else:
                keys = pygame.key.get_pressed()
                self.rocket.update(keys)

                # Only check for collisions if cooldown is over
                if self.cooldown > 0:
                    self.cooldown -= 1
                else:
                    # Check for planet collisions
                    collided_planet = self.check_collisions()
                    if collided_planet:
                        self.current_info_screen = InfoScreen(
                            collided_planet.name,
                            planets[collided_planet.name]["info"]
                        )

                screen.fill(BLACK)
                
                # Draw stars
                for star in self.stars:
                    star.update()
                    star.draw(screen)
                
                # Draw sun
                self.draw_sun()
                
                # Draw planets
                for planet in self.planets:
                    planet.update()
                    planet.draw(screen)
                
                # Draw rocket
                self.rocket.draw(screen)

            pygame.display.flip()
            clock.tick(60)

    def draw_sun(self):
        # Draw sun corona
        corona_surfaces = []
        for i in range(5):
            corona_surf = pygame.Surface((150, 150), pygame.SRCALPHA)
            radius = 60 + i * 10
            alpha = int(100 * (1 - i/5))
            pygame.draw.circle(corona_surf, (255, 200, 50, alpha), (75, 75), radius)
            corona_surfaces.append(corona_surf)
        
        # Create pulsing effect
        pulse = abs(math.sin(time.time())) * 10
        
        # Draw corona layers
        for surf in corona_surfaces:
            screen.blit(surf, (WIDTH//2 - 75, HEIGHT//2 - 75))
        
        # Draw sun core
        pygame.draw.circle(screen, YELLOW, (WIDTH//2, HEIGHT//2), 50 + pulse)
        
        # Draw sun surface details
        for i in range(8):
            angle = time.time() + i * math.pi/4
            x = WIDTH//2 + math.cos(angle) * 45
            y = HEIGHT//2 + math.sin(angle) * 45
            pygame.draw.circle(screen, (255, 200, 50), (int(x), int(y)), 10)

if __name__ == "__main__":
    explorer = SpaceExplorer()
    explorer.run() 