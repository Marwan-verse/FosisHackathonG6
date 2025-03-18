import pygame
import math
import sys
from random import randint, choice, random, shuffle  # Add shuffle to the imports
import time
import os
from earth_platformer import EarthPlatformer
from planet_platformer import PlanetPlatformer, Player

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
        "image": "Sun.png",
        "stage2_image": "SunStage2.png",
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
        "color": (169, 169, 169),  # Gray
        "radius": 10,
        "orbit": 100,
        "speed": 0.02,
        "image": "Murcury.png",  # Small image for solar system view
        "stage2_image": "MercuryStage2.png",  # Large image for planet screen
        "info": [
            "Mercury is the smallest and innermost planet in our Solar System. Its surface is heavily cratered, resembling Earth's Moon. The planet experiences extreme temperature variations, from scorching 430°C during the day to -180°C at night.",
            
            "Mercury has no atmosphere to speak of, just a thin exosphere made mostly of oxygen, sodium, hydrogen, helium, and potassium. This lack of atmosphere means there's no weather and no protection from meteoroid impacts.",
            
            "Despite being the closest planet to the Sun, Mercury is not the hottest planet - that's Venus. Mercury's orbit is highly elliptical, and it completes three rotations for every two orbits around the Sun.",
            
            "Mercury's core makes up about 55% of its volume, the largest core-to-planet ratio in the Solar System. This large iron core generates a magnetic field about 1% as strong as Earth's.",
            
            "The planet's surface is covered in wrinkles called scarps, formed as Mercury's core cooled and shrank. These scarps can be up to a mile high and hundreds of miles long."
        ]
    },
    "Venus": {
        "color": (218, 165, 32),  # Golden
        "radius": 15,
        "orbit": 150,
        "speed": 0.015,
        "image": "Venus.png",
        "stage2_image": "VenusStage2.png",
        "info": [
            "Venus is often called Earth's twin due to their similar size and mass, but it's a hostile world with surface temperatures hot enough to melt lead - around 462°C. This extreme heat is caused by a runaway greenhouse effect.",
            
            "The planet's thick atmosphere is primarily carbon dioxide, with clouds of sulfuric acid. The atmospheric pressure at the surface is 90 times greater than Earth's, equivalent to the pressure at 900 meters under Earth's oceans.",
            
            "Venus rotates backwards compared to most other planets, and its day is longer than its year. One Venusian day takes 243 Earth days, while it orbits the Sun in 225 Earth days.",
            
            "The surface of Venus is relatively young, reshaped by volcanic activity about 300-500 million years ago. The planet has more volcanoes than any other planet in the Solar System.",
            
            "Venus has no moons and no magnetic field. The lack of a magnetic field means the solar wind interacts directly with the atmosphere, causing some of it to escape into space."
        ]
    },
    "Earth": {
        "color": (34, 139, 34),  # Green
        "radius": 18,
        "orbit": 200,
        "speed": 0.01,
        "image": "Earth.png",
        "stage2_image": "EarthStage2.png",
        "info": [
            "Earth's atmosphere is a complex system that protects all life. The atmosphere is 78% nitrogen and 21% oxygen, with small amounts of other gases. The ozone layer, a special part of the atmosphere, blocks harmful UV radiation from reaching the surface.",
            
            "Earth's surface is a dynamic landscape shaped by powerful forces. 70% is covered by oceans containing liquid water, a unique feature in our solar system. The remaining 30% consists of continents with mountains, forests, and deserts.",
            
            "Earth's core is an incredible powerhouse. Its temperature matches the Sun's surface at about 5,400°C. This molten core generates a magnetic field that protects us from harmful solar radiation and helps some animals navigate.",
            
            "Earth's daily and yearly cycles create our familiar patterns of life. It completes one rotation every 24 hours, giving us day and night. The planet's 23.5-degree tilt causes our seasons as we orbit the Sun.",
            
            "Earth's gravity, averaging 9.8 m/s², keeps everything grounded. This force holds our atmosphere in place, keeps the oceans in their basins, and helps maintain the Moon's orbit."
        ]
    },
    "Mars": {
        "color": (205, 92, 92),  # Indian red
        "radius": 14,
        "orbit": 250,
        "speed": 0.008,
        "image": "Mars.png",
        "stage2_image": "MarsStage2.png",
        "info": [
            "Mars is known as the Red Planet due to iron oxide (rust) on its surface. It has a thin atmosphere made mostly of carbon dioxide, and atmospheric pressure less than 1% of Earth's. The low pressure means liquid water can't exist on the surface for long.",
            
            "Mars has the largest volcano in the Solar System, Olympus Mons, and the longest canyon, Valles Marineris. These features formed when Mars was geologically active, billions of years ago.",
            
            "Evidence suggests Mars once had liquid water on its surface. Ancient river valleys, lake beds, and minerals that only form in water's presence indicate Mars might have been habitable in the past.",
            
            "Mars has two small, irregularly shaped moons: Phobos and Deimos. They're likely captured asteroids and orbit very close to the planet. Phobos is gradually moving closer to Mars and will eventually break apart or crash into the planet.",
            
            "The planet experiences dramatic dust storms that can cover the entire planet and last for weeks or months. These storms, combined with the planet's red color, make Mars appear even more reddish during these events."
        ]
    },
    "Jupiter": {
        "color": (244, 164, 96),  # Sandy brown
        "radius": 40,
        "orbit": 320,
        "speed": 0.005,
        "image": "Jupiter.png",
        "stage2_image": "JupiterStage2.png",
        "info": [
            "Jupiter is the largest planet in our Solar System, with a mass more than twice that of all other planets combined. It's a gas giant, primarily composed of hydrogen and helium, similar to the composition of the Sun.",
            
            "The Great Red Spot is Jupiter's most famous feature - a giant storm that has been raging for at least 400 years. This storm is so large that three Earths could fit inside it. The spot's color comes from unknown compounds that turn red when exposed to sunlight.",
            
            "Jupiter has the strongest magnetic field of any planet, about 14 times stronger than Earth's. This powerful field creates intense radiation belts around the planet and produces spectacular auroras at its poles.",
            
            "The planet has at least 79 known moons, including the four large Galilean moons: Io, Europa, Ganymede, and Callisto. Ganymede is the largest moon in the Solar System, bigger than the planet Mercury.",
            
            "Jupiter's atmosphere features multiple bands of clouds moving in alternating directions, creating zones and belts. These bands are driven by powerful winds that can reach speeds of up to 650 kilometers per hour."
        ]
    },
    "Saturn": {
        "color": (238, 232, 205),  # Pale goldenrod
        "radius": 35,
        "orbit": 400,
        "speed": 0.003,
        "image": "Saturn.png",
        "stage2_image": "SaturnStage2.png",
        "info": [
            "Saturn is famous for its spectacular ring system, the most extensive in the Solar System. The rings are made mostly of water ice, with some rocky debris and dust. Despite being up to 280,000 km wide, the rings are only about 10 meters thick.",
            
            "Like Jupiter, Saturn is a gas giant composed mainly of hydrogen and helium. It's the only planet less dense than water - if there were a bathtub big enough, Saturn would float! This low density is due to its gaseous composition.",
            
            "Saturn has at least 82 moons, including Titan, the only moon in the Solar System with a substantial atmosphere. Titan is larger than Mercury and has lakes and seas of liquid methane on its surface.",
            
            "The planet's hexagonal storm at its north pole is a unique feature in the Solar System. This six-sided jet stream has been observed since the Voyager missions in the 1980s and is about 25,000 km across.",
            
            "Saturn's magnetic field is weaker than Jupiter's but still 578 times stronger than Earth's. The field creates auroras at both poles and interacts with the planet's rings and moons in complex ways."
        ]
    },
    "Uranus": {
        "color": (173, 216, 230),  # Light blue
        "radius": 25,
        "orbit": 470,
        "speed": 0.002,
        "image": "Uranus.png",
        "stage2_image": "UranusStage2.png",
        "info": [
            "Uranus is unique among planets because it rotates on its side, with its axis tilted at 98 degrees. This unusual tilt means that its poles experience 42 years of continuous sunlight followed by 42 years of darkness.",
            
            "The planet is an ice giant, composed mainly of water, methane, and ammonia ices beneath its hydrogen-helium atmosphere. The methane in its atmosphere gives Uranus its blue-green color by absorbing red light.",
            
            "Uranus has 27 known moons, all named after characters from the works of William Shakespeare and Alexander Pope. The five largest are Miranda, Ariel, Umbriel, Titania, and Oberon.",
            
            "The planet's atmosphere contains layers of clouds at different heights. The innermost clouds are made of water, while the outer layers contain methane ice. Wind speeds can reach up to 900 kilometers per hour.",
            
            "Uranus has a complex ring system, though much fainter than Saturn's. These rings were the first to be discovered after Saturn's, found in 1977 when the planet passed in front of a star and briefly blocked its light."
        ]
    },
    "Neptune": {
        "color": (0, 0, 139),  # Dark blue
        "radius": 24,
        "orbit": 520,
        "speed": 0.001,
        "image": "Neptune.png",
        "stage2_image": "NeptuneStage2.png",
        "info": [
            "Neptune is the windiest planet in the Solar System, with speeds reaching up to 2,100 kilometers per hour. These winds drive huge storms, including the Great Dark Spot, similar to Jupiter's Great Red Spot but more transient.",
            
            "Like Uranus, Neptune is an ice giant composed primarily of water, ammonia, and methane ices. Its blue color comes from methane in its atmosphere absorbing red light, but Neptune's blue is notably deeper than Uranus's blue-green.",
            
            "The planet has 14 known moons, with Triton being the largest. Triton orbits Neptune backwards (retrograde orbit), suggesting it's a captured Kuiper Belt object. It has active geysers that spew nitrogen ice and dust into space.",
            
            "Neptune's magnetic field is tilted 47 degrees from its rotational axis and offset from the planet's center. This unusual configuration creates complex magnetic interactions with the solar wind.",
            
            "The planet has a system of rings, though they're dark and difficult to see. These rings contain unusually high percentages of dust compared to ice, making them quite different from Saturn's bright, icy rings."
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
            self.y = 0 if random() < 0.1 else HEIGHT
        
        # Increased speed range (was 1-3, now 3-6)
        self.speed = random() * 3 + 2  # Speed between 3 and 6
        
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
        self.x = 100  # Changed from WIDTH // 2
        self.y = 100  # Changed from HEIGHT // 4
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
        self.shoot_delay = 15  # Frames between shots

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
        try:
            font_path = os.path.join("fonts", "PressStart2P-Regular.ttf")
            self.font_title = pygame.font.Font(font_path, 32)
            self.font_info = pygame.font.Font(font_path, 16)
        except:
            print("Could not load custom font for InfoScreen, falling back to system font")
            self.font_title = pygame.font.SysFont('courier', 48)
            self.font_info = pygame.font.SysFont('courier', 36)

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
    def __init__(self, planet_name, parent):
        self.parent = parent
        try:
            font_path = os.path.join("fonts", "PressStart2P-Regular.ttf")
            self.font = pygame.font.Font(font_path, 16)
        except:
            print("Could not load custom font for QuizScreen, falling back to system font")
            self.font = pygame.font.SysFont('courier', 36)
        self.planet_name = planet_name
        self.show_correct_answer = False
        
        # Adjust option boxes to be wider
        self.options = {
            'answer1': {'rect': pygame.Rect(WIDTH//4 - 200, HEIGHT//2 - 100, 400, 50), 'color': (100, 100, 200)},
            'answer2': {'rect': pygame.Rect(WIDTH*3//4 - 200, HEIGHT//2 - 100, 400, 50), 'color': (100, 100, 200)},
            'answer3': {'rect': pygame.Rect(WIDTH//4 - 200, HEIGHT//2 + 50, 400, 50), 'color': (100, 100, 200)},
            'answer4': {'rect': pygame.Rect(WIDTH*3//4 - 200, HEIGHT//2 + 50, 400, 50), 'color': (100, 100, 200)},
            'back': {'rect': pygame.Rect(WIDTH//2 - 120, HEIGHT - 60, 240, 40), 'color': (100, 100, 200)}
        }
        
        self.used_questions = []
        self.result = None
        self.result_timer = 0
        self.rocket_reset_position = False
        self.stars = [(randint(0, WIDTH), randint(0, HEIGHT), random() * 2, choice(STAR_COLORS)) 
                     for _ in range(100)]

        # Get planet-specific questions
        self.questions = self.get_questions_for_planet(planet_name)
        try:
            self.get_new_question()
        except Exception as e:
            print(f"Error in initialization: {e}")
            self.current_question = {
                "question": "Loading Error",
                "answers": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "correct": 0
            }

        # Add particle system for correct answer effect
        self.particles = []
        self.particle_colors = [
            (100, 255, 100),  # Light green
            (50, 200, 50),    # Medium green
            (0, 255, 0),      # Bright green
            (150, 255, 150)   # Pale green
        ]

    def get_questions_for_planet(self, planet_name):
        if planet_name == "Sun":
            return [
                {
                    "question": "What type of star is the Sun?",
                    "answers": ["Yellow Dwarf", "Red Giant", "White Dwarf", "Blue Giant"],
                    "correct": 0
                },
                {
                    "question": "What is the Sun's surface temperature?",
                    "answers": ["5,500°C", "1,000°C", "10,000°C", "3,000°C"],
                    "correct": 0
                },
                {
                    "question": "What powers the Sun?",
                    "answers": ["Nuclear fusion", "Nuclear fission", "Chemical reactions", "Electrical energy"],
                    "correct": 0
                },
                {
                    "question": "How much of the solar system's mass is in the Sun?",
                    "answers": ["99.86%", "75%", "50%", "85%"],
                    "correct": 0
                },
                {
                    "question": "How long does light from the Sun take to reach Earth?",
                    "answers": ["8 minutes", "1 hour", "1 second", "30 minutes"],
                    "correct": 0
                },
                {
                    "question": "What is the Sun's core temperature?",
                    "answers": ["15 million °C", "5,500°C", "1 million °C", "10,000°C"],
                    "correct": 0
                },
                {
                    "question": "What causes sunspots?",
                    "answers": ["Magnetic activity", "Solar flares", "Asteroid impacts", "Gas explosions"],
                    "correct": 0
                },
                {
                    "question": "How many Earths could fit inside the Sun?",
                    "answers": ["1.3 million", "100,000", "500,000", "2 million"],
                    "correct": 0
                },
                {
                    "question": "What will happen to the Sun in its final stage?",
                    "answers": ["Become a White Dwarf", "Explode as Supernova", "Become a Black Hole", "Fade Away"],
                    "correct": 0
                },
                {
                    "question": "What is the Sun's rotation period at its equator?",
                    "answers": ["27 Earth days", "365 Earth days", "7 Earth days", "100 Earth days"],
                    "correct": 0
                },
                {
                    "question": "What is the Sun's atmosphere called?",
                    "answers": ["Corona", "Photosphere", "Chromosphere", "Magnetosphere"],
                    "correct": 0
                },
                {
                    "question": "What percentage of the Sun's energy reaches Earth?",
                    "answers": ["0.0000001%", "1%", "10%", "0.1%"],
                    "correct": 0
                },
                {
                    "question": "What causes solar wind?",
                    "answers": ["Escaping plasma", "Nuclear fusion", "Surface explosions", "Magnetic fields"],
                    "correct": 0
                },
                {
                    "question": "How long will the Sun continue to shine?",
                    "answers": ["5 billion years", "1 billion years", "10 billion years", "500 million years"],
                    "correct": 0
                },
                {
                    "question": "What element is most abundant in the Sun?",
                    "answers": ["Hydrogen", "Helium", "Oxygen", "Carbon"],
                    "correct": 0
                }
            ]
        elif planet_name == "Mercury":
            return [
                {
                    "question": "What is Mercury's average distance from the Sun?",
                    "answers": ["57.9 million km", "149.6 million km", "227.9 million km", "778.5 million km"],
                    "correct": 0
                },
                {
                    "question": "What is the surface temperature range on Mercury?",
                    "answers": ["-180°C to 430°C", "-140°C to 320°C", "-90°C to 200°C", "0°C to 100°C"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Mercury have?",
                    "answers": ["None", "One", "Two", "Three"],
                    "correct": 0
                },
                {
                    "question": "What is Mercury's core made of?",
                    "answers": ["Iron", "Rock", "Ice", "Gas"],
                    "correct": 0
                },
                {
                    "question": "How long is a Mercury day?",
                    "answers": ["176 Earth days", "24 Earth hours", "50 Earth days", "365 Earth days"],
                    "correct": 0
                },
                {
                    "question": "Why is Mercury heavily cratered?",
                    "answers": ["No atmosphere", "Low gravity", "High temperature", "Solar winds"],
                    "correct": 0
                },
                {
                    "question": "What spacecraft first visited Mercury?",
                    "answers": ["Mariner 10", "Voyager 1", "Pioneer", "New Horizons"],
                    "correct": 0
                },
                {
                    "question": "What percentage of Mercury's volume is its core?",
                    "answers": ["55%", "25%", "35%", "45%"],
                    "correct": 0
                },
                {
                    "question": "What causes Mercury's surface scarps?",
                    "answers": ["Core cooling", "Solar heat", "Meteor impacts", "Volcanic activity"],
                    "correct": 0
                },
                {
                    "question": "What is Mercury's orbital period?",
                    "answers": ["88 Earth days", "225 Earth days", "365 Earth days", "687 Earth days"],
                    "correct": 0
                },
                {
                    "question": "What is Mercury's atmosphere called?",
                    "answers": ["Exosphere", "Troposphere", "Stratosphere", "None"],
                    "correct": 0
                },
                {
                    "question": "What causes Mercury's tail?",
                    "answers": ["Solar wind", "Volcanic gas", "Asteroid debris", "Cosmic rays"],
                    "correct": 0
                },
                {
                    "question": "What is Mercury's magnetic field strength compared to Earth's?",
                    "answers": ["1%", "10%", "50%", "100%"],
                    "correct": 0
                },
                {
                    "question": "What is Mercury's nickname?",
                    "answers": ["Swift Planet", "Morning Star", "Red Planet", "Gas Giant"],
                    "correct": 0
                },
                {
                    "question": "What is unique about Mercury's orbit?",
                    "answers": ["Most elliptical", "Most circular", "Fastest", "Slowest"],
                    "correct": 0
                }
            ]
        elif planet_name == "Venus":
            return [
                {
                    "question": "What is Venus's atmospheric composition mainly?",
                    "answers": ["Carbon Dioxide", "Nitrogen", "Oxygen", "Hydrogen"],
                    "correct": 0
                },
                {
                    "question": "What is Venus's surface temperature?",
                    "answers": ["462°C", "15°C", "120°C", "-63°C"],
                    "correct": 0
                },
                {
                    "question": "Venus rotates in which direction?",
                    "answers": ["Clockwise", "Counter-clockwise", "It doesn't rotate", "Changes direction"],
                    "correct": 0
                },
                {
                    "question": "What creates Venus's greenhouse effect?",
                    "answers": ["CO2 atmosphere", "Water vapor", "Methane", "Oxygen"],
                    "correct": 0
                },
                {
                    "question": "How many Earth days is a Venusian day?",
                    "answers": ["243", "100", "365", "500"],
                    "correct": 0
                },
                {
                    "question": "What causes Venus's lightning?",
                    "answers": ["Volcanic activity", "Solar radiation", "Atmospheric pressure", "Surface heat"],
                    "correct": 0
                },
                {
                    "question": "What color is Venus's surface?",
                    "answers": ["Orange-red", "Blue", "Green", "White"],
                    "correct": 0
                },
                {
                    "question": "What percentage of Earth's gravity is Venus's?",
                    "answers": ["90%", "50%", "75%", "110%"],
                    "correct": 0
                },
                {
                    "question": "What causes Venus's super-rotation?",
                    "answers": ["Atmospheric dynamics", "Solar radiation", "Core rotation", "Surface heat"],
                    "correct": 0
                },
                {
                    "question": "What is Venus's atmospheric pressure compared to Earth's?",
                    "answers": ["90 times greater", "50 times greater", "20 times greater", "10 times greater"],
                    "correct": 0
                },
                {
                    "question": "What are Venus's clouds made of?",
                    "answers": ["Sulfuric acid", "Water vapor", "Methane", "Nitrogen"],
                    "correct": 0
                },
                {
                    "question": "How many volcanoes are on Venus?",
                    "answers": ["1,600+", "500", "100", "50"],
                    "correct": 0
                },
                {
                    "question": "What is Venus's nickname?",
                    "answers": ["Morning Star", "Red Planet", "Gas Giant", "Ice Giant"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Venus have?",
                    "answers": ["0", "1", "2", "3"],
                    "correct": 0
                },
                {
                    "question": "What spacecraft first mapped Venus's surface?",
                    "answers": ["Magellan", "Voyager", "Pioneer", "Cassini"],
                    "correct": 0
                }
            ]
        elif planet_name == "Earth":
            return [
                {
                    "question": "What percentage of Earth's atmosphere is nitrogen?",
                    "answers": ["78%", "21%", "1%", "50%"],
                    "correct": 0
                },
                {
                    "question": "How long does it take Earth to orbit the Sun?",
                    "answers": ["365.25 days", "300 days", "400 days", "500 days"],
                    "correct": 0
                },
                {
                    "question": "What is Earth's core mainly made of?",
                    "answers": ["Iron and Nickel", "Gold and Silver", "Rock and Stone", "Ice and Water"],
                    "correct": 0
                },
                {
                    "question": "What percentage of Earth is covered by water?",
                    "answers": ["71%", "50%", "85%", "60%"],
                    "correct": 0
                },
                {
                    "question": "What causes Earth's seasons?",
                    "answers": ["Axial tilt", "Distance from Sun", "Rotation speed", "Ocean currents"],
                    "correct": 0
                },
                {
                    "question": "How old is Earth?",
                    "answers": ["4.54 billion years", "2 billion years", "6 billion years", "3 billion years"],
                    "correct": 0
                },
                {
                    "question": "What is Earth's average surface temperature?",
                    "answers": ["15°C", "25°C", "0°C", "30°C"],
                    "correct": 0
                },
                {
                    "question": "How thick is Earth's crust on average?",
                    "answers": ["30 kilometers", "100 kilometers", "10 kilometers", "500 kilometers"],
                    "correct": 0
                },
                {
                    "question": "What causes Earth's magnetic field?",
                    "answers": ["Liquid outer core", "Solar radiation", "Moon's gravity", "Atmosphere"],
                    "correct": 0
                },
                {
                    "question": "How fast does Earth rotate at the equator?",
                    "answers": ["1,037 mph", "500 mph", "2,000 mph", "100 mph"],
                    "correct": 0
                },
                {
                    "question": "What is Earth's atmosphere mostly made of?",
                    "answers": ["Nitrogen", "Oxygen", "Carbon dioxide", "Argon"],
                    "correct": 0
                },
                {
                    "question": "How many layers does Earth's atmosphere have?",
                    "answers": ["5", "3", "7", "4"],
                    "correct": 0
                },
                {
                    "question": "What is Earth's average distance from the Sun?",
                    "answers": ["93 million miles", "50 million miles", "150 million miles", "200 million miles"],
                    "correct": 0
                },
                {
                    "question": "How many tectonic plates does Earth have?",
                    "answers": ["7 major plates", "4 major plates", "10 major plates", "15 major plates"],
                    "correct": 0
                },
                {
                    "question": "What is unique about Earth in our solar system?",
                    "answers": ["Only planet with liquid water", "Largest planet", "Hottest planet", "Fastest rotating"],
                    "correct": 0
                }
            ]
        elif planet_name == "Mars":
            return [
                {
                    "question": "What gives Mars its red color?",
                    "answers": ["Iron Oxide (Rust)", "Red Rocks", "Red Vegetation", "Red Gases"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Mars have?",
                    "answers": ["2", "1", "3", "0"],
                    "correct": 0
                },
                {
                    "question": "What is the name of Mars' largest volcano?",
                    "answers": ["Olympus Mons", "Mount Everest", "Mauna Kea", "Mount Vesuvius"],
                    "correct": 0
                },
                {
                    "question": "What is Mars' atmosphere mostly made of?",
                    "answers": ["Carbon Dioxide", "Nitrogen", "Oxygen", "Hydrogen"],
                    "correct": 0
                },
                {
                    "question": "How long is a Martian day?",
                    "answers": ["24 hours 37 minutes", "24 hours", "30 hours", "20 hours"],
                    "correct": 0
                },
                {
                    "question": "What is the average temperature on Mars?",
                    "answers": ["-63°C", "15°C", "-10°C", "-100°C"],
                    "correct": 0
                },
                {
                    "question": "What is the name of Mars' largest canyon?",
                    "answers": ["Valles Marineris", "Grand Canyon", "Olympus Valley", "Hellas Basin"],
                    "correct": 0
                },
                {
                    "question": "What are Mars' moons called?",
                    "answers": ["Phobos and Deimos", "Titan and Europa", "Io and Ganymede", "Luna and Charon"],
                    "correct": 0
                },
                {
                    "question": "What causes Mars' dust storms?",
                    "answers": ["Solar heating", "Volcanic activity", "Meteor impacts", "Underground explosions"],
                    "correct": 0
                },
                {
                    "question": "How strong is Mars' gravity compared to Earth's?",
                    "answers": ["38%", "50%", "75%", "25%"],
                    "correct": 0
                },
                {
                    "question": "What evidence suggests Mars once had water?",
                    "answers": ["River valleys", "Blue rocks", "Green patches", "Steam vents"],
                    "correct": 0
                },
                {
                    "question": "How thick is Mars' atmosphere compared to Earth's?",
                    "answers": ["1%", "10%", "25%", "50%"],
                    "correct": 0
                },
                {
                    "question": "What is Mars' nickname?",
                    "answers": ["The Red Planet", "The Blue Planet", "The Ringed Planet", "The Ice Planet"],
                    "correct": 0
                },
                {
                    "question": "How long is Mars' year?",
                    "answers": ["687 Earth days", "365 Earth days", "500 Earth days", "800 Earth days"],
                    "correct": 0
                },
                {
                    "question": "What type of ice is found at Mars' poles?",
                    "answers": ["Water and CO2", "Nitrogen", "Methane", "Ammonia"],
                    "correct": 0
                }
            ]
        elif planet_name == "Jupiter":
            return [
                {
                    "question": "What is Jupiter's Great Red Spot?",
                    "answers": ["A giant storm", "A volcano", "A crater", "A desert"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Jupiter have?",
                    "answers": ["79+", "50", "25", "10"],
                    "correct": 0
                },
                {
                    "question": "What is Jupiter mainly made of?",
                    "answers": ["Hydrogen and Helium", "Rock and Metal", "Ice and Water", "Carbon Dioxide"],
                    "correct": 0
                },
                {
                    "question": "How long is a day on Jupiter?",
                    "answers": ["10 Earth hours", "24 Earth hours", "5 Earth hours", "48 Earth hours"],
                    "correct": 0
                },
                {
                    "question": "What causes Jupiter's colorful bands?",
                    "answers": ["Atmospheric flows", "Surface painting", "Magnetic fields", "Solar radiation"],
                    "correct": 0
                },
                {
                    "question": "How strong is Jupiter's magnetic field compared to Earth's?",
                    "answers": ["14 times stronger", "5 times stronger", "2 times stronger", "Same strength"],
                    "correct": 0
                },
                {
                    "question": "What is Jupiter's largest moon?",
                    "answers": ["Ganymede", "Io", "Europa", "Callisto"],
                    "correct": 0
                },
                {
                    "question": "How many Earth's could fit inside Jupiter?",
                    "answers": ["1,321", "500", "2,000", "100"],
                    "correct": 0
                },
                {
                    "question": "What is the Great Red Spot's size compared to Earth?",
                    "answers": ["2-3 Earths wide", "Same size", "Half Earth's size", "10 Earths wide"],
                    "correct": 0
                },
                {
                    "question": "How long has the Great Red Spot existed?",
                    "answers": ["At least 400 years", "50 years", "1000 years", "100 years"],
                    "correct": 0
                },
                {
                    "question": "What are Jupiter's rings made of?",
                    "answers": ["Dust", "Ice", "Rock", "Gas"],
                    "correct": 0
                },
                {
                    "question": "What spacecraft first visited Jupiter?",
                    "answers": ["Pioneer 10", "Voyager 1", "Galileo", "Cassini"],
                    "correct": 0
                },
                {
                    "question": "What is Jupiter's core temperature?",
                    "answers": ["24,000°C", "5,000°C", "50,000°C", "10,000°C"],
                    "correct": 0
                },
                {
                    "question": "How long is Jupiter's year?",
                    "answers": ["12 Earth years", "5 Earth years", "20 Earth years", "8 Earth years"],
                    "correct": 0
                },
                {
                    "question": "What causes Jupiter's auroras?",
                    "answers": ["Magnetic field", "Solar wind", "Moon interactions", "Surface radiation"],
                    "correct": 0
                }
            ]
        elif planet_name == "Saturn":
            return [
                {
                    "question": "What are Saturn's rings made of?",
                    "answers": ["Ice and Rock", "Gas", "Metal", "Dust"],
                    "correct": 0
                },
                {
                    "question": "Which is Saturn's largest moon?",
                    "answers": ["Titan", "Enceladus", "Mimas", "Rhea"],
                    "correct": 0
                },
                {
                    "question": "Would Saturn float in water?",
                    "answers": ["Yes", "No", "Sometimes", "Only in salt water"],
                    "correct": 0
                },
                {
                    "question": "How many major rings does Saturn have?",
                    "answers": ["7", "5", "10", "3"],
                    "correct": 0
                },
                {
                    "question": "What is Saturn mainly made of?",
                    "answers": ["Hydrogen and Helium", "Rock and Metal", "Ice and Water", "Carbon Dioxide"],
                    "correct": 0
                },
                {
                    "question": "How long is a day on Saturn?",
                    "answers": ["10.7 Earth hours", "24 Earth hours", "5 Earth hours", "48 Earth hours"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Saturn have?",
                    "answers": ["82", "50", "25", "100"],
                    "correct": 0
                },
                {
                    "question": "What is unique about Titan?",
                    "answers": ["Has thick atmosphere", "Is perfectly round", "Has water oceans", "Is very hot"],
                    "correct": 0
                },
                {
                    "question": "How thick are Saturn's rings?",
                    "answers": ["10 meters", "10 kilometers", "100 kilometers", "1 kilometer"],
                    "correct": 0
                },
                {
                    "question": "What causes Saturn's hexagonal storm?",
                    "answers": ["Jet stream pattern", "Magnetic field", "Moon gravity", "Ring shadows"],
                    "correct": 0
                },
                {
                    "question": "How long is Saturn's year?",
                    "answers": ["29.5 Earth years", "10 Earth years", "50 Earth years", "15 Earth years"],
                    "correct": 0
                },
                {
                    "question": "What spacecraft studied Saturn extensively?",
                    "answers": ["Cassini", "Voyager", "Pioneer", "Galileo"],
                    "correct": 0
                },
                {
                    "question": "What is Saturn's average temperature?",
                    "answers": ["-178°C", "-50°C", "-100°C", "-300°C"],
                    "correct": 0
                },
                {
                    "question": "How strong is Saturn's magnetic field?",
                    "answers": ["578 times Earth's", "100 times Earth's", "1000 times Earth's", "50 times Earth's"],
                    "correct": 0
                },
                {
                    "question": "What causes Saturn's yellowish color?",
                    "answers": ["Atmospheric chemicals", "Ring reflection", "Surface rocks", "Solar radiation"],
                    "correct": 0
                }
            ]
        elif planet_name == "Neptune":
            return [
                {
                    "question": "What is Neptune's largest moon?",
                    "answers": ["Triton", "Nereid", "Naiad", "Thalassa"],
                    "correct": 0
                },
                {
                    "question": "What are Neptune's wind speeds?",
                    "answers": ["2,100 km/h", "1,000 km/h", "500 km/h", "100 km/h"],
                    "correct": 0
                },
                {
                    "question": "What gives Neptune its blue color?",
                    "answers": ["Methane", "Water", "Nitrogen", "Oxygen"],
                    "correct": 0
                },
                {
                    "question": "How many Earth masses is Neptune?",
                    "answers": ["17", "10", "5", "25"],
                    "correct": 0
                },
                {
                    "question": "How many rings does Neptune have?",
                    "answers": ["5", "3", "7", "10"],
                    "correct": 0
                },
                {
                    "question": "What is Neptune's Great Dark Spot?",
                    "answers": ["A storm system", "A crater", "A sea", "A mountain"],
                    "correct": 0
                },
                {
                    "question": "How long is Neptune's year?",
                    "answers": ["165 Earth years", "100 Earth years", "200 Earth years", "50 Earth years"],
                    "correct": 0
                },
                {
                    "question": "What is Neptune's average temperature?",
                    "answers": ["-214°C", "-100°C", "-150°C", "-300°C"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Neptune have?",
                    "answers": ["14", "8", "20", "5"],
                    "correct": 0
                },
                {
                    "question": "What spacecraft has visited Neptune?",
                    "answers": ["Voyager 2", "Pioneer", "Cassini", "New Horizons"],
                    "correct": 0
                },
                {
                    "question": "What is unique about Triton's orbit?",
                    "answers": ["Backwards orbit", "Perfect circle", "Very fast", "Very slow"],
                    "correct": 0
                },
                {
                    "question": "How was Neptune discovered?",
                    "answers": ["Mathematical prediction", "Telescope observation", "Space probe", "Accident"],
                    "correct": 0
                },
                {
                    "question": "What is Neptune mainly made of?",
                    "answers": ["Ice and rock", "Hydrogen and helium", "Pure ice", "Pure rock"],
                    "correct": 0
                },
                {
                    "question": "How long is a day on Neptune?",
                    "answers": ["16 Earth hours", "24 Earth hours", "10 Earth hours", "48 Earth hours"],
                    "correct": 0
                },
                {
                    "question": "What causes Neptune's magnetic field?",
                    "answers": ["Liquid metallic core", "Solar radiation", "Moon interaction", "Ring system"],
                    "correct": 0
                }
            ]
        elif planet_name == "Uranus":
            return [
                {
                    "question": "What gives Uranus its blue-green color?",
                    "answers": ["Methane gas", "Water", "Nitrogen", "Oxygen"],
                    "correct": 0
                },
                {
                    "question": "How many rings does Uranus have?",
                    "answers": ["13", "7", "20", "None"],
                    "correct": 0
                },
                {
                    "question": "What is unique about Uranus's rotation?",
                    "answers": ["It rotates on its side", "It doesn't rotate", "It rotates backwards", "It rotates very fast"],
                    "correct": 0
                },
                {
                    "question": "How many moons does Uranus have?",
                    "answers": ["27", "15", "32", "8"],
                    "correct": 0
                },
                {
                    "question": "What are Uranus's moons named after?",
                    "answers": ["Shakespeare characters", "Greek gods", "Roman gods", "Scientists"],
                    "correct": 0
                },
                {
                    "question": "How long is a year on Uranus?",
                    "answers": ["84 Earth years", "50 Earth years", "100 Earth years", "30 Earth years"],
                    "correct": 0
                },
                {
                    "question": "What is Uranus mainly made of?",
                    "answers": ["Ice and rock", "Hydrogen and helium", "Pure ice", "Pure rock"],
                    "correct": 0
                },
                {
                    "question": "What spacecraft has visited Uranus?",
                    "answers": ["Voyager 2", "Pioneer", "Cassini", "None"],
                    "correct": 0
                },
                {
                    "question": "What is Uranus's average temperature?",
                    "answers": ["-224°C", "-100°C", "-150°C", "-300°C"],
                    "correct": 0
                },
                {
                    "question": "Who discovered Uranus?",
                    "answers": ["William Herschel", "Galileo Galilei", "Johannes Kepler", "Isaac Newton"],
                    "correct": 0
                },
                {
                    "question": "What type of planet is Uranus?",
                    "answers": ["Ice Giant", "Gas Giant", "Rocky Planet", "Dwarf Planet"],
                    "correct": 0
                },
                {
                    "question": "What causes Uranus's extreme seasons?",
                    "answers": ["Its tilted axis", "Its distance from Sun", "Its moons", "Its atmosphere"],
                    "correct": 0
                },
                {
                    "question": "How long is a day on Uranus?",
                    "answers": ["17 Earth hours", "24 Earth hours", "10 Earth hours", "48 Earth hours"],
                    "correct": 0
                },
                {
                    "question": "What is Uranus's largest moon?",
                    "answers": ["Titania", "Miranda", "Oberon", "Ariel"],
                    "correct": 0
                },
                {
                    "question": "What color are Uranus's rings?",
                    "answers": ["Dark grey", "Blue", "White", "Red"],
                    "correct": 0
                }
            ]
        # Add default questions if planet not found
        return [
            {
                "question": f"What is {planet_name}?",
                "answers": ["A Planet", "A Star", "A Moon", "An Asteroid"],
                "correct": 0
            }
        ]

    def get_new_question(self):
        try:
            available_questions = [q for q in self.questions if q not in self.used_questions]
            if not available_questions:
                self.used_questions = []
                available_questions = self.questions
            
            self.current_question = choice(available_questions)
            self.used_questions.append(self.current_question)
            
            # Randomize answers
            answers = self.current_question['answers'].copy()
            correct_answer = answers[self.current_question['correct']]
            shuffle(answers)
            self.current_question['correct'] = answers.index(correct_answer)
            self.current_question['answers'] = answers
        except Exception as e:
            print(f"Error getting new question: {e}")
            self.current_question = {
                "question": "Error loading question",
                "answers": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "correct": 0
            }

    def create_success_particles(self, x, y):
        # Create 30 particles at the rocket's position
        for _ in range(30):
            angle = random() * 2 * math.pi
            speed = random() * 5 + 2
            self.particles.append({
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': 60,  # Particle lifetime in frames
                'color': choice(self.particle_colors),
                'size': random() * 3 + 1
            })

    def update_particles(self):
        # Update particle positions and lifetimes
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self, screen):
        # Draw all active particles
        for particle in self.particles:
            alpha = int((particle['life'] / 60) * 255)
            color = (*particle['color'], alpha)
            
            # Create particle surface with glow effect
            size = int(particle['size'] * 4)
            particle_surf = pygame.Surface((size, size), pygame.SRCALPHA)
            
            # Draw glowing circle
            for radius in range(int(size//2), 0, -1):
                glow_alpha = int(alpha * (radius / (size//2)))
                pygame.draw.circle(
                    particle_surf,
                    (*particle['color'], glow_alpha),
                    (size//2, size//2),
                    radius
                )
            
            screen.blit(
                particle_surf,
                (int(particle['x'] - size//2), int(particle['y'] - size//2))
            )

    def check_answer(self, rocket_rect):
        if self.result is not None:
            if self.result_timer <= 0:
                if self.show_correct_answer:
                    self.get_new_question()
                    self.show_correct_answer = False
                else:
                    self.show_correct_answer = True
                    self.result_timer = 180
                self.result = None
            return None

        for i, (key, data) in enumerate(self.options.items()):
            if key != 'back' and rocket_rect.colliderect(data['rect']):
                if i == self.current_question['correct']:
                    self.result = True
                    self.result_timer = 60
                    # Create particle effect at rocket position
                    self.create_success_particles(rocket_rect.centerx, rocket_rect.centery)
                    # Add score for correct answer
                    try:
                        self.parent.add_score(10, WIDTH//2, HEIGHT//2)
                    except:
                        print("Could not add score")
                else:
                    self.result = False
                    self.result_timer = 120
                    # Subtract score for wrong answer
                    try:
                        self.parent.add_score(-5, WIDTH//2, HEIGHT//2)
                    except:
                        print("Could not subtract score")
                self.rocket_reset_position = True
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
        # Add fullscreen tracking
        self.fullscreen = False
        self.window_size = (WIDTH, HEIGHT)
        
        # Initialize display
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Space Explorer")
        
        # Load custom pixel font
        try:
            font_path = os.path.join("fonts", "PressStart2P-Regular.ttf")
            self.font = pygame.font.Font(font_path, 16)  # Smaller size for regular text
            self.large_font = pygame.font.Font(font_path, 24)  # Medium size
            self.menu_font = pygame.font.Font(font_path, 48)  # Large size for menu
            self.score_font = pygame.font.Font(font_path, 32)  # Size for score
            self.popup_font = pygame.font.Font(font_path, 24)  # Size for popups
        except:
            print("Could not load custom font, falling back to system font")
            self.font = pygame.font.SysFont('courier', 24)
            self.large_font = pygame.font.SysFont('courier', 36)
            self.menu_font = pygame.font.SysFont('courier', 74)
            self.score_font = pygame.font.SysFont('courier', 48)
            self.popup_font = pygame.font.SysFont('courier', 36)
        
        # Rest of your initialization code...
        self.planets = [Planet(name, data) for name, data in planets.items() if name != "Sun"]
        self.stars = [Star() for _ in range(200)]
        self.rocket = Rocket()
        self.asteroids = []
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
        self.earth_platformer = None
        self.planet_platformer = None
        self.score = 0
        self.score_popups = []  # List of dictionaries containing score popup info
        
    def add_score(self, points, x, y):
        try:
            # Calculate new score but don't let it go below 0
            new_score = max(0, self.score + points)
            
            # Only show popup if score actually changed
            if new_score != self.score:
                # Add a score popup (red for negative, white for positive)
                color = (255, 100, 100) if points < 0 else (255, 255, 255)
                self.score_popups.append({
                    'text': f'{points:+d}',  # Shows + or - sign
                    'x': x,
                    'y': y,
                    'alpha': 255,
                    'lifetime': 60,
                    'color': color
                })
            
            self.score = new_score
        except Exception as e:
            print(f"Error adding score: {e}")

    def update_score_popups(self):
        # Update existing popups
        for popup in self.score_popups[:]:
            popup['y'] -= 1  # Move up
            popup['alpha'] = max(0, popup['alpha'] - (255 / popup['lifetime']))  # Prevent negative alpha
            popup['lifetime'] -= 1
            if popup['lifetime'] <= 0:
                self.score_popups.remove(popup)

    def draw_score(self, screen):
        # Draw main score counter
        score_text = f"Score: {self.score}"
        score_surface = self.score_font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(midtop=(WIDTH // 2, 10))
        
        # Add glow effect to score
        glow_surface = pygame.Surface((score_rect.width + 4, score_rect.height + 4), pygame.SRCALPHA)
        for offset in range(3):
            glow_alpha = max(0, 100 - offset * 30)  # Prevent negative alpha
            glow_text = self.score_font.render(score_text, True, (255, 255, 255, glow_alpha))
            glow_rect = glow_text.get_rect(center=(glow_surface.get_width()//2, glow_surface.get_height()//2))
            glow_surface.blit(glow_text, glow_rect)
        
        screen.blit(glow_surface, (score_rect.x - 2, score_rect.y - 2))
        screen.blit(score_surface, score_rect)
        
        # Draw score popups with colors
        for popup in self.score_popups:
            alpha = max(0, min(255, int(popup['alpha'])))  # Clamp alpha between 0 and 255
            color = (*popup['color'][:3], alpha)  # Use stored color with calculated alpha
            popup_surface = self.popup_font.render(popup['text'], True, color)
            popup_rect = popup_surface.get_rect(center=(popup['x'], popup['y']))
            screen.blit(popup_surface, popup_rect)

    def reset_rocket_position(self):
        if not self.planet_view:
            # Position rocket in the top left of the solar system screen
            self.rocket.x = 100
            self.rocket.y = 100
        else:
            if self.current_quiz_screen:
                # Position rocket in the middle for quiz
                self.rocket.x = WIDTH // 2
                self.rocket.y = HEIGHT * 3 // 4  # Changed from HEIGHT // 4 to HEIGHT * 3 // 4
            else:
                # Position rocket on the planet screen
                self.rocket.x = WIDTH // 2
                self.rocket.y = HEIGHT // 4
        self.rocket.speed = 0
        self.cooldown = 30

    def check_collisions(self):
        if not self.planet_view:
            # Check collision with comets
            for comet in self.comets[:]:
                try:
                    distance = math.sqrt(
                        (self.rocket.x - comet.x)**2 + 
                        (self.rocket.y - comet.y)**2
                    )
                    if distance < self.rocket.size + comet.size:
                        self.comets.remove(comet)
                        self.add_score(1, comet.x, comet.y)
                        return None
                except Exception as e:
                    print(f"Error in comet collision: {e}")
                    continue

            # Existing planet collision checks
            distance_to_sun = math.sqrt(
                (self.rocket.x - WIDTH//2)**2 + 
                (self.rocket.y - HEIGHT//2)**2
            )
            if distance_to_sun < 40 + self.rocket.size:
                return Planet("Sun", planets["Sun"])
            
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

        # Load and draw the Stage 2 planet image
        try:
            image_path = os.path.join(ASSETS_DIR, "stage2", planets[self.current_planet.name]["stage2_image"])
            planet_image = pygame.image.load(image_path).convert_alpha()
            
            # Scale image to fit screen while maintaining aspect ratio
            scale = min(WIDTH * 0.8 / planet_image.get_width(), 
                       HEIGHT * 0.8 / planet_image.get_height())
            new_width = int(planet_image.get_width() * scale)
            new_height = int(planet_image.get_height() * scale)
            planet_image = pygame.transform.scale(planet_image, (new_width, new_height))
            
            # Center the image on screen
            x = WIDTH // 2 - new_width // 2
            y = HEIGHT // 2 - new_height // 2
            screen.blit(planet_image, (x, y))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load Stage 2 image for {self.current_planet.name}: {e}")
            # Fallback to original drawing method if image loading fails
            # ... existing planet drawing code ...

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

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # Store the window size before going fullscreen
            self.window_size = self.screen.get_size()
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            # Return to windowed mode with previous size
            self.screen = pygame.display.set_mode(self.window_size)

    def run(self):
        pygame.init()
        
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # Add fullscreen toggle controls
                    if event.key == pygame.K_F11 or (event.key == pygame.K_RETURN and event.mod & pygame.KMOD_ALT):
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_ESCAPE:
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

            # Update space objects for all game states except menu
            if not self.in_menu:
                self.update_space_objects()

            # Update button hover states in menu
            if self.in_menu:
                mouse_pos = pygame.mouse.get_pos()
                self.launch_button['hover'] = self.launch_button['rect'].collidepoint(mouse_pos)
                self.dev_button['hover'] = self.dev_button['rect'].collidepoint(mouse_pos)
                self.draw_menu(self.screen)
            elif self.in_dev_mode:
                keys = pygame.key.get_pressed()
                self.rocket.update(keys)
                self.draw_dev_mode(self.screen)
            elif self.current_info_screen:
                self.current_info_screen.draw(self.screen)
                # Draw space objects in info screen
                for comet in self.comets:
                    comet.draw(self.screen)
                for asteroid in self.asteroids:
                    asteroid.draw(self.screen)
            elif self.current_quiz_screen:
                self.current_quiz_screen.draw(self.screen, self.rocket)
                
                if self.current_quiz_screen.rocket_reset_position:
                    self.current_quiz_screen.reset_rocket(self.rocket)
                
                keys = pygame.key.get_pressed()
                self.rocket.update(keys)
                
                # Draw space objects
                for comet in self.comets:
                    comet.draw(self.screen)
                for asteroid in self.asteroids:
                    asteroid.draw(self.screen)
                
                rocket_rect = pygame.Rect(self.rocket.x - self.rocket.size, 
                                        self.rocket.y - self.rocket.size,
                                        self.rocket.size * 2, 
                                        self.rocket.size * 2)
                result = self.current_quiz_screen.check_answer(rocket_rect)
                if result == 'back':
                    self.current_quiz_screen = None
                    self.reset_rocket_position()
                
                self.rocket.draw(self.screen)
            elif self.earth_platformer:
                # Run the Earth platformer game
                continue_space = self.earth_platformer.run()
                if continue_space:
                    self.earth_platformer = None
                    self.exit_planet_view()
            elif self.planet_platformer:
                # Run the planet platformer game
                continue_space = self.planet_platformer.run()
                if continue_space:
                    self.planet_platformer = None
                    self.exit_planet_view()
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
                            if self.current_planet.name == "Earth":
                                self.earth_platformer = EarthPlatformer()
                            else:
                                # Create planet-specific platformer
                                self.planet_platformer = PlanetPlatformer(
                                    self.current_planet.name,
                                    self.current_planet.color,
                                    planets[self.current_planet.name]["info"],
                                    (0, 0, 0)  # Black background
                                )
                            self.reset_rocket_position()
                        elif option_hit == 'quiz':
                            try:
                                self.current_quiz_screen = QuizScreen(self.current_planet.name, self)
                                self.reset_rocket_position()
                            except Exception as e:
                                print(f"Error creating quiz screen: {e}")
                                self.current_quiz_screen = None
                        elif option_hit == 'back':
                            self.exit_planet_view()

                self.screen.fill(BLACK)
                
                if not self.planet_view:
                    for star in self.stars:
                        star.update()
                        star.draw(self.screen)
                    self.draw_sun()
                    for planet in self.planets:
                        planet.update()
                        planet.draw(self.screen)
                    # Draw comets and asteroids after planets
                    for comet in self.comets:
                        comet.draw(self.screen)
                    for asteroid in self.asteroids:
                        asteroid.draw(self.screen)
                
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
                    
                    self.screen.blit(glow_surface, (text_rect.x - 2, text_rect.y - 2))
                    self.screen.blit(text_surface, text_rect)
                else:
                    self.draw_planet_screen(self.screen)

                self.rocket.draw(self.screen)

                if self.transition_alpha > 0:
                    fade_surface = pygame.Surface((WIDTH, HEIGHT))
                    fade_surface.fill(BLACK)
                    fade_surface.set_alpha(self.transition_alpha)
                    self.screen.blit(fade_surface, (0, 0))
                    
                    if self.planet_view:
                        self.transition_alpha = max(0, self.transition_alpha - 10)
                    else:
                        self.transition_alpha = max(0, self.transition_alpha - 10)

            # Update score popups
            self.update_score_popups()
            
            # Draw score (add this before pygame.display.flip())
            self.draw_score(self.screen)
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == "__main__":
    explorer = SpaceExplorer()
    explorer.run() 