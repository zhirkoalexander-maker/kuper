"""
╔════════════════════════════════════════════════════════════════════════════╗
║                         FPS TESTER v2.0                                   ║
║                 Performance Analysis & Stress Testing Tool                 ║
║                                                                            ║
║  A professional desktop application for testing GPU/CPU performance       ║
║  with real-time metrics, system monitoring, and crash protection.         ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

import pygame
import sys
import time
import random
import math
import os
from collections import deque
from abc import ABC, abstractmethod
from enum import Enum
from typing import Tuple, List, Dict, Optional

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

pygame.init()


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════

class ScreenConfig:
    """Display and window configuration"""
    WIDTH = 1400
    HEIGHT = 900
    FPS_CAP = 300
    TARGET_FPS = 60


class ColorScheme:
    """Color palette for the application"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLUE = (0, 100, 255)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    DARK_GRAY = (30, 30, 30)
    LIGHT_GRAY = (200, 200, 200)


class ApplicationSettings:
    """Global application settings"""
    defaults = {
        "show_fps_rounded": True,
        "show_fps_real": True,
        "show_hints": True,
        "show_mode_stats": True,
        "show_results": True,
        "crash_protection": True,
    }
    
    def __init__(self):
        self.settings = self.defaults.copy()
    
    def get(self, key: str, default=None):
        return self.settings.get(key, default)
    
    def set(self, key: str, value):
        self.settings[key] = value
    
    def toggle(self, key: str):
        self.settings[key] = not self.settings.get(key, False)


WINDOW_WIDTH = ScreenConfig.WIDTH
WINDOW_HEIGHT = ScreenConfig.HEIGHT
GLOBAL_SETTINGS = ApplicationSettings()

# Quick color references for convenience
BLACK = ColorScheme.BLACK
WHITE = ColorScheme.WHITE
GREEN = ColorScheme.GREEN
RED = ColorScheme.RED
YELLOW = ColorScheme.YELLOW
BLUE = ColorScheme.BLUE
CYAN = ColorScheme.CYAN
MAGENTA = ColorScheme.MAGENTA
ORANGE = ColorScheme.ORANGE
PURPLE = ColorScheme.PURPLE
DARK_GRAY = ColorScheme.DARK_GRAY
LIGHT_GRAY = ColorScheme.LIGHT_GRAY


# ═══════════════════════════════════════════════════════════════════════════
# UTILITY CLASSES & HELPERS
# ═══════════════════════════════════════════════════════════════════════════

class PerformanceMonitor:
    """Real-time performance monitoring with history tracking"""
    
    def __init__(self, history_size: int = 300):
        self.history = deque(maxlen=history_size)
        self.peak_fps = 0.0
        self.lowest_fps = float('inf')
    
    def record(self, fps: float):
        """Record an FPS measurement"""
        self.history.append(fps)
        self.peak_fps = max(self.peak_fps, fps)
        self.lowest_fps = min(self.lowest_fps, fps)
    
    def get_average(self) -> float:
        """Get average FPS"""
        return sum(self.history) / len(self.history) if self.history else 0.0
    
    def get_stability(self) -> float:
        """Get stability score (0-100), higher = more stable"""
        if len(self.history) < 2:
            return 100.0
        
        avg = self.get_average()
        if avg == 0:
            return 0.0
        
        # Calculate variance
        variance = sum((x - avg) ** 2 for x in self.history) / len(self.history)
        # Convert to stability (0-100)
        stability = max(0, 100 - (math.sqrt(variance) / avg * 50))
        return min(100.0, stability)
    
    def reset(self):
        """Reset monitoring data"""
        self.history.clear()
        self.peak_fps = 0.0
        self.lowest_fps = float('inf')


class FrameRateLimiter:
    """Smooth frame rate limiting with adaptive timing"""
    
    def __init__(self, target_fps: int):
        self.target_fps = target_fps
        self.frame_time = 1.0 / target_fps
        self.last_time = time.time()
        self.accumulated_time = 0.0
    
    def wait(self) -> float:
        """Wait for next frame and return delta time"""
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Clamp dt to reasonable values
        dt = min(dt, self.frame_time * 2)
        
        self.accumulated_time += dt
        
        if self.accumulated_time < self.frame_time:
            sleep_time = self.frame_time - self.accumulated_time
            time.sleep(sleep_time * 0.95)  # Sleep slightly less to be safe
            self.accumulated_time = 0.0
        
        return dt


# ═══════════════════════════════════════════════════════════════════════════
# BASE GAME MODE FRAMEWORK
# ═══════════════════════════════════════════════════════════════════════════

class GameMode(ABC):
    """
    Abstract base class for all game modes.
    Defines the interface for stress testing applications.
    """
    
    def __init__(self, name: str, difficulty: int):
        self.name = name
        self.difficulty = min(5, max(1, difficulty))  # Clamp 1-5
        self.fps_values: deque = deque(maxlen=300)
        self.fps_display_timer = 0.0
        self.current_fps_display = 0
        self.start_time = time.time()
        self.frame_count = 0
    
    @abstractmethod
    def update(self, dt: float, keys: Optional[tuple]):
        """Update game state"""
        pass
    
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        """Render to screen"""
        pass
    
    def on_start(self):
        """Called when mode starts"""
        self.start_time = time.time()
        self.frame_count = 0
    
    def on_exit(self):
        """Called when mode exits"""
        pass
    
    def get_fps_display(self, raw_fps: float, dt: float) -> int:
        """Get rounded FPS for display"""
        self.fps_values.append(raw_fps)
        self.fps_display_timer += dt
        
        if self.fps_display_timer >= 0.5:
            self.current_fps_display = round(raw_fps / 10) * 10
            self.fps_display_timer = 0
        
        self.frame_count += 1
        return self.current_fps_display
    
    def get_statistics(self) -> Tuple[float, float, float]:
        """Returns (average_fps, min_fps, max_fps)"""
        if not self.fps_values:
            return 0.0, 0.0, 0.0
        
        avg = sum(self.fps_values) / len(self.fps_values)
        return avg, min(self.fps_values), max(self.fps_values)
    
    def get_elapsed_time(self) -> float:
        """Get elapsed time since mode start"""
        return time.time() - self.start_time
    
    def get_difficulty_label(self) -> str:
        """Get human-readable difficulty label"""
        labels = {1: "EASY", 2: "MEDIUM", 3: "HARD", 4: "EXTREME", 5: "MAXIMUM"}
        return labels.get(self.difficulty, "UNKNOWN")


# ═══════════════════════════════════════════════════════════════════════════
# GAME MODES - GPU STRESS TESTS
# ═══════════════════════════════════════════════════════════════════════════


class Particle:
    """Represents a single particle in the simulation"""
    
    __slots__ = ['x', 'y', 'vx', 'vy', 'color', 'size', 'life', 'max_life']
    
    def __init__(self, x: float, y: float, vx: float, vy: float,
                 color: Tuple[int, int, int], size: int, life: float):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
    
    def update(self, dt: float, gravity: float = 0.0, friction: float = 1.0):
        """Update particle physics"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += gravity * dt
        self.vx *= friction
        self.vy *= friction
        self.life -= dt
    
    def is_alive(self) -> bool:
        """Check if particle is still alive"""
        return self.life > 0
    
    def get_alpha(self) -> float:
        """Get fade-out alpha (0.0 to 1.0)"""
        return max(0.0, self.life / self.max_life)


class ParticleSystem:
    """Manages a collection of particles with efficient batch operations"""
    
    def __init__(self, max_particles: int = 10000):
        self.particles: List[Particle] = []
        self.max_particles = max_particles
    
    def emit(self, particle: Particle):
        """Add a new particle"""
        if len(self.particles) < self.max_particles:
            self.particles.append(particle)
    
    def emit_burst(self, x: float, y: float, count: int,
                   speed_range: Tuple[float, float],
                   color: Tuple[int, int, int], size: int, life: float):
        """Emit multiple particles at once"""
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*speed_range)
            
            particle = Particle(
                x, y,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                color, size, life
            )
            self.particles.append(particle)
    
    def update(self, dt: float, bounds: Optional[Tuple[int, int, int, int]] = None,
               gravity: float = 0.0):
        """Update all particles"""
        alive_particles = []
        
        for particle in self.particles:
            particle.update(dt, gravity)
            
            if particle.is_alive():
                # Boundary checking
                if bounds:
                    x_min, y_min, x_max, y_max = bounds
                    if particle.x < x_min or particle.x > x_max:
                        particle.vx *= -0.9
                        particle.x = max(x_min, min(x_max, particle.x))
                    if particle.y < y_min or particle.y > y_max:
                        particle.vy *= -0.9
                        particle.y = max(y_min, min(y_max, particle.y))
                
                alive_particles.append(particle)
        
        self.particles = alive_particles
    
    def draw(self, screen: pygame.Surface):
        """Draw all particles"""
        for particle in self.particles:
            if particle.size > 0:
                pygame.draw.circle(screen, particle.color,
                                   (int(particle.x), int(particle.y)),
                                   particle.size)
    
    def clear(self):
        """Remove all particles"""
        self.particles.clear()
    
    def get_count(self) -> int:
        """Get current particle count"""
        return len(self.particles)


# ═══════════════════════════════════════════════════════════════════════════

class ParticleStorm(GameMode):
    """
    Particle Storm - Screen fills with thousands of particles.
    Tests GPU fill rate and particle rendering performance.
    Click to trigger particle explosions.
    """
    
    def __init__(self):
        super().__init__("Particle Storm", 4)
        self.particle_system = ParticleSystem(max_particles=50000)
        self.emission_rate = 50 + self.difficulty * 30
        self.color_palette = [
            ColorScheme.RED, ColorScheme.BLUE, ColorScheme.GREEN,
            ColorScheme.YELLOW, ColorScheme.CYAN, ColorScheme.MAGENTA
        ]
    
    def update(self, dt: float, keys: Optional[tuple]):
        """Handle particle updates and user input"""
        # Handle explosion on mouse click
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            self.particle_system.emit_burst(
                x=mx, y=my, count=80,
                speed_range=(2.0, 6.0),
                color=random.choice(self.color_palette),
                size=random.randint(2, 5),
                life=2.0
            )
        
        # Continuous particle emission
        for _ in range(self.emission_rate):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            
            particle = Particle(
                x, y,
                random.uniform(-3, 3),
                random.uniform(-3, 3),
                random.choice(self.color_palette),
                random.randint(1, 4),
                5.0
            )
            self.particle_system.emit(particle)
        
        # Update all particles with boundary wrapping
        bounds = (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.particle_system.update(dt, bounds=bounds)
    
    def draw(self, screen: pygame.Surface):
        """Render all particles"""
        screen.fill(ColorScheme.BLACK)
        self.particle_system.draw(screen)
        
        # Debug info
        font = pygame.font.Font(None, 36)
        info = font.render(
            f"Particles: {self.particle_system.get_count()} | Click for explosion",
            True, ColorScheme.WHITE
        )
        screen.blit(info, (50, 30))

class PolygonRush(GameMode):
    """Polygon Rush - rotating polygons, move towards cursor"""
    def __init__(self):
        super().__init__("Polygon Rush", 4)
        self.polygons = []
        self.time = 0
        self.polygon_count = 30 + self.difficulty * 10
        
        for _ in range(self.polygon_count):
            self.polygons.append({
                'x': random.randint(100, WINDOW_WIDTH - 100),
                'y': random.randint(100, WINDOW_HEIGHT - 100),
                'size': random.randint(20, 60),
                'angle': random.uniform(0, 360),
                'angular_velocity': random.uniform(-5, 5),
                'sides': random.randint(3, 8),
                'color': random.choice([RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, ORANGE])
            })
    
    def update(self, dt, keys):
        self.time += dt
        mx, my = pygame.mouse.get_pos()
        
        for poly in self.polygons:
            poly['angle'] += poly['angular_velocity']
            
            # Move towards cursor
            dx = mx - poly['x']
            dy = my - poly['y']
            dist = math.sqrt(dx*dx + dy*dy) + 1
            
            speed = 50
            poly['x'] += (dx / dist) * speed * dt
            poly['y'] += (dy / dist) * speed * dt
    
    def draw(self, screen):
        for poly in self.polygons:
            points = []
            for i in range(poly['sides']):
                angle = (360 / poly['sides'] * i + poly['angle']) * math.pi / 180
                x = poly['x'] + poly['size'] * math.cos(angle)
                y = poly['y'] + poly['size'] * math.sin(angle)
                points.append((x, y))
            
            if len(points) > 2:
                pygame.draw.polygon(screen, poly['color'], points, 2)
        
        font = pygame.font.Font(None, 36)
        count = font.render(f"Polygons: {len(self.polygons)} | Move cursor", True, WHITE)
        screen.blit(count, (50, 30))

class MatrixRain(GameMode):
    """Matrix Rain - falling characters, speed depends on mouse"""
    def __init__(self):
        super().__init__("Matrix Rain", 3)
        self.columns = WINDOW_WIDTH // 20
        self.columns_data = []
        for _ in range(self.columns):
            self.columns_data.append({
                'y': random.randint(-500, 0),
                'speed': random.uniform(2, 5) + self.difficulty * 0.5,
                'chars': [chr(random.randint(33, 126)) for _ in range(50)]
            })
    
    def update(self, dt, keys):
        mx, my = pygame.mouse.get_pos()
        speed_multiplier = 1.0 + (my / WINDOW_HEIGHT) * 2  # Speed depends on mouse height
        
        for col in self.columns_data:
            col['y'] += col['speed'] * speed_multiplier
            if col['y'] > WINDOW_HEIGHT:
                col['y'] = -100
    
    def draw(self, screen):
        font = pygame.font.Font(None, 20)
        for i, col in enumerate(self.columns_data):
            x = i * 20
            y = col['y']
            for j, char in enumerate(col['chars']):
                char_y = y + j * 20
                if 0 <= char_y < WINDOW_HEIGHT:
                    color_val = int(255 * (1 - (char_y / WINDOW_HEIGHT)))
                    color = (0, min(255, color_val + 100), 0)
                    text = font.render(char, True, color)
                    screen.blit(text, (x, char_y))
        
        font = pygame.font.Font(None, 36)
        text = font.render("Move cursor up/down to change speed", True, WHITE)
        screen.blit(text, (50, 30))

class FractalTree(GameMode):
    """Fractal Tree - recursive fractals, rotate towards cursor"""
    def __init__(self):
        super().__init__("Fractal Tree", 5)
        self.angle = 0
        self.depth = 10 + self.difficulty * 2
    
    def draw_tree(self, screen, x, y, angle, length, depth, color):
        if depth == 0 or length < 2:
            return
        
        # End of line
        x_end = x + length * math.cos(angle * math.pi / 180)
        y_end = y + length * math.sin(angle * math.pi / 180)
        
        pygame.draw.line(screen, color, (x, y), (x_end, y_end), max(1, depth // 2))
        
        # Recursion
        self.draw_tree(screen, x_end, y_end, angle - 25, length * 0.7, depth - 1, color)
        self.draw_tree(screen, x_end, y_end, angle + 25, length * 0.7, depth - 1, color)
    
    def update(self, dt, keys):
        mx, my = pygame.mouse.get_pos()
        # Calculate angle to cursor
        dx = mx - WINDOW_WIDTH // 2
        dy = my - WINDOW_HEIGHT // 2
        target_angle = math.atan2(dy, dx) * 180 / math.pi - 90
        
        # Smooth rotation to cursor
        diff = target_angle - self.angle
        while diff > 180:
            diff -= 360
        while diff < -180:
            diff += 360
        
        self.angle += diff * 0.1
    
    def draw(self, screen):
        color_val = int(127 + 127 * math.sin(self.angle * math.pi / 180))
        color = (color_val, 200, 100)
        self.draw_tree(screen, WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50, self.angle - 90, 80, self.depth, color)
        
        font = pygame.font.Font(None, 36)
        depth_text = font.render(f"Depth: {self.depth} | Move cursor to rotate", True, WHITE)
        screen.blit(depth_text, (50, 30))

class WaveSimulation(GameMode):
    """Wave Simulation - wave simulation"""
    def __init__(self):
        super().__init__("Wave Simulation", 4)
        self.grid_size = 40
        self.grid_x = WINDOW_WIDTH // self.grid_size
        self.grid_y = WINDOW_HEIGHT // self.grid_size
        self.height_map = [[0 for _ in range(self.grid_x)] for _ in range(self.grid_y)]
        self.velocity_map = [[0 for _ in range(self.grid_x)] for _ in range(self.grid_y)]
        self.time = 0
    
    def update(self, dt, keys):
        self.time += dt
        
        # Add disturbance to center
        cx, cy = self.grid_x // 2, self.grid_y // 2
        force = math.sin(self.time * 5) * 50
        self.height_map[cy][cx] = force
        
        # Wave simulation (very simplified)
        new_height = [[0 for _ in range(self.grid_x)] for _ in range(self.grid_y)]
        damping = 0.99
        
        for y in range(1, self.grid_y - 1):
            for x in range(1, self.grid_x - 1):
                avg = (self.height_map[y-1][x] + self.height_map[y+1][x] + 
                       self.height_map[y][x-1] + self.height_map[y][x+1]) / 4
                self.velocity_map[y][x] = (avg - self.height_map[y][x]) * 2
                new_height[y][x] = self.height_map[y][x] + self.velocity_map[y][x] * damping
        
        self.height_map = new_height
    
    def draw(self, screen):
        for y in range(self.grid_y):
            for x in range(self.grid_x):
                height = self.height_map[y][x]
                color_val = int(127 + height)
                color_val = max(0, min(255, color_val))
                color = (color_val, 100, 255 - color_val)
                
                pygame.draw.rect(screen, color, 
                                (x * self.grid_size, y * self.grid_size, 
                                 self.grid_size, self.grid_size))

class BouncingBalls(GameMode):
    """Bouncing Balls - bouncing balls, attracted to mouse"""
    def __init__(self):
        super().__init__("Bouncing Balls", 3)
        self.balls = []
        self.ball_count = 40 + self.difficulty * 20
        self.repel_mode = False
        
        for _ in range(self.ball_count):
            self.balls.append({
                'x': random.randint(20, WINDOW_WIDTH - 20),
                'y': random.randint(20, WINDOW_HEIGHT - 20),
                'vx': random.uniform(-4, 4),
                'vy': random.uniform(-4, 4),
                'radius': random.randint(5, 15),
                'color': random.choice([RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, ORANGE])
            })
    
    def update(self, dt, keys):
        mx, my = pygame.mouse.get_pos()
        # Right mouse button = repulsion
        self.repel_mode = pygame.mouse.get_pressed()[2]
        
        for ball in self.balls:
            ball['x'] += ball['vx']
            ball['y'] += ball['vy']
            
            # Attraction/repulsion to mouse
            dx = mx - ball['x']
            dy = my - ball['y']
            dist = math.sqrt(dx*dx + dy*dy) + 1
            
            force = 50 / (dist + 1)
            if self.repel_mode:
                force *= -1
            
            ball['vx'] += (dx / dist) * force * dt
            ball['vy'] += (dy / dist) * force * dt
            
            # Friction
            ball['vx'] *= 0.98
            ball['vy'] *= 0.98
            
            # Bounce off walls
            if ball['x'] - ball['radius'] < 0 or ball['x'] + ball['radius'] > WINDOW_WIDTH:
                ball['vx'] *= -1
                ball['x'] = max(ball['radius'], min(WINDOW_WIDTH - ball['radius'], ball['x']))
            
            if ball['y'] - ball['radius'] < 0 or ball['y'] + ball['radius'] > WINDOW_HEIGHT:
                ball['vy'] *= -1
                ball['y'] = max(ball['radius'], min(WINDOW_HEIGHT - ball['radius'], ball['y']))
    
    def draw(self, screen):
        for ball in self.balls:
            pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), ball['radius'])
        
        font = pygame.font.Font(None, 36)
        text = f"Balls: {len(self.balls)} | Left click: attract | Right click: repel"
        count = font.render(text, True, WHITE)
        screen.blit(count, (50, 30))

class PlasmaEffect(GameMode):
    """Plasma Effect - plasma effect, reacts to mouse"""
    def __init__(self):
        super().__init__("Plasma Effect", 4)
        self.time = 0
        self.scale = 50
        self.mouse_influence = 0
    
    def update(self, dt, keys):
        self.time += dt
        mx, my = pygame.mouse.get_pos()
        self.mouse_x = mx
        self.mouse_y = my
    
    def draw(self, screen):
        for y in range(0, WINDOW_HEIGHT, 5):
            for x in range(0, WINDOW_WIDTH, 5):
                # Distance to mouse
                dx = x - self.mouse_x
                dy = y - self.mouse_y
                dist = math.sqrt(dx*dx + dy*dy) + 1
                
                # Plasma formula with mouse influence
                value = (math.sin(x / self.scale + self.time) * 
                        math.cos(y / self.scale + self.time) * 
                        math.sin((x + y) / 50 + self.time) * 
                        (1.0 / (dist / 200 + 1)) * 255)
                
                color_val = int(127 + value)
                color_val = max(0, min(255, color_val))
                
                color = pygame.Color(color_val, 100, 255 - color_val)
                pygame.draw.rect(screen, color, (x, y, 5, 5))
        
        font = pygame.font.Font(None, 36)
        text = font.render("Move cursor to distort plasma", True, WHITE)
        screen.blit(text, (50, 30))

class Mandelbrot(GameMode):
    """Mandelbrot Set - Mandelbrot set, zoom with mouse"""
    def __init__(self):
        super().__init__("Mandelbrot", 5)
        self.zoom = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.iteration = 20 + self.difficulty * 10
        self.mouse_zoom = 1.0
    
    def mandelbrot_value(self, x, y, max_iter):
        """Calculate Mandelbrot value"""
        c = complex(x, y)
        z = 0j
        for n in range(max_iter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return max_iter
    
    def update(self, dt, keys):
        mx, my = pygame.mouse.get_pos()
        
        # Zoom to mouse position
        zoom_factor = 1.02
        self.zoom *= zoom_factor
        
        # Offset to mouse center
        xc = (mx - WINDOW_WIDTH / 2) / (WINDOW_WIDTH / 4 * self.zoom)
        yc = (my - WINDOW_HEIGHT / 2) / (WINDOW_HEIGHT / 4 * self.zoom)
        
        self.pan_x = xc * 0.1 + self.pan_x * 0.9
        self.pan_y = yc * 0.1 + self.pan_y * 0.9
    
    def draw(self, screen):
        step = 4
        for y in range(0, WINDOW_HEIGHT, step):
            for x in range(0, WINDOW_WIDTH, step):
                # Transform screen coordinates to complex
                xc = (x - WINDOW_WIDTH / 2) / (WINDOW_WIDTH / 4 * self.zoom) + self.pan_x
                yc = (y - WINDOW_HEIGHT / 2) / (WINDOW_HEIGHT / 4 * self.zoom) + self.pan_y
                
                value = self.mandelbrot_value(xc, yc, self.iteration)
                
                color_val = int(255 * (value / self.iteration))
                color = (color_val, 100, 255 - color_val)
                
                pygame.draw.rect(screen, color, (x, y, step, step))
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Zoom level: {self.zoom:.2f} | Move cursor to navigate", True, WHITE)
        screen.blit(text, (50, 30))

class TunnelEffect(GameMode):
    """Tunnel Effect - 3D tunnel, rotates towards mouse"""
    def __init__(self):
        super().__init__("Tunnel Effect", 4)
        self.time = 0
        self.rings = 50
        self.rotation = 0
    
    def update(self, dt, keys):
        self.time += dt
        mx, my = pygame.mouse.get_pos()
        
        # Rotation depends on mouse
        self.rotation = (mx / WINDOW_WIDTH) * 360
    
    def draw(self, screen):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        for i in range(self.rings):
            # Ring size depends on depth
            depth = (self.time * 100 + i * 10) % 1000
            ring_size = int(50 + depth / 2)
            
            color_val = int(255 * (1 - depth / 1000))
            
            # Color changes with rotation
            hue = (self.rotation + i * 5) % 360
            if hue < 60:
                color = (255, int(hue * 4.25), 0)
            elif hue < 120:
                color = (int(255 * (2 - hue / 60)), 255, 0)
            elif hue < 180:
                color = (0, 255, int((hue - 120) * 4.25))
            elif hue < 240:
                color = (0, int(255 * (4 - hue / 60)), 255)
            elif hue < 300:
                color = (int((hue - 240) * 4.25), 0, 255)
            else:
                color = (255, 0, int(255 * (6 - hue / 60)))
            
            pygame.draw.circle(screen, color, (center_x, center_y), ring_size, 3)
        
        font = pygame.font.Font(None, 36)
        text = font.render("Move cursor left/right to rotate tunnel", True, WHITE)
        screen.blit(text, (50, 30))

class Starfield(GameMode):
    """Starfield - starfield, follows mouse"""
    def __init__(self):
        super().__init__("Starfield", 2)
        self.stars = []
        self.star_count = 200 + self.difficulty * 50
        self.velocity_x = 0
        self.velocity_y = 0
        
        for _ in range(self.star_count):
            self.stars.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'z': random.randint(1, 100),
                'color': random.choice([WHITE, YELLOW, CYAN])
            })
    
    def update(self, dt, keys):
        mx, my = pygame.mouse.get_pos()
        
        # Smooth movement to mouse
        target_x = (mx - WINDOW_WIDTH // 2) / 100
        target_y = (my - WINDOW_HEIGHT // 2) / 100
        
        self.velocity_x += (target_x - self.velocity_x) * 0.1
        self.velocity_y += (target_y - self.velocity_y) * 0.1
        
        for star in self.stars:
            star['z'] -= self.velocity_x + 1
            if star['z'] <= 0:
                star['z'] = 100
                star['x'] = random.randint(0, WINDOW_WIDTH)
                star['y'] = random.randint(0, WINDOW_HEIGHT)
    
    def draw(self, screen):
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        for star in self.stars:
            # Perspective projection
            scale = 300 / star['z']
            x = center_x + (star['x'] - center_x) * scale
            y = center_y + (star['y'] - center_y) * scale
            
            size = max(1, int(3 * (1 - star['z'] / 100)))
            
            if 0 <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT:
                pygame.draw.circle(screen, star['color'], (int(x), int(y)), size)
        
        font = pygame.font.Font(None, 36)
        count = font.render(f"Stars: {len(self.stars)} | Move cursor to control", True, WHITE)
        screen.blit(count, (50, 30))

class CPUTest(GameMode):
    """CPU Test - processor load and recommendations"""
    def __init__(self):
        super().__init__("CPU Test", 5)
        self.time = 0
        self.cpu_history = deque(maxlen=100)
        self.computation_load = 50000 + self.difficulty * 50000
        self.status_text = ""
    
    def update(self, dt, keys):
        self.time += dt
        
        # Heavy computations to load CPU
        result = 0
        for i in range(self.computation_load):
            result += math.sqrt(i) * math.sin(i) * math.cos(i)
        
        # Get CPU usage if psutil is available
        if HAS_PSUTIL:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.01)
                self.cpu_history.append(cpu_percent)
            except:
                cpu_percent = 50 + 30 * math.sin(self.time)
                self.cpu_history.append(cpu_percent)
        else:
            cpu_percent = 50 + 30 * math.sin(self.time)
            self.cpu_history.append(cpu_percent)
        
        # Generate status based on CPU usage
        if cpu_percent > 80:
            self.status_text = "HEAVY LOAD - Consider closing background apps"
        elif cpu_percent > 60:
            self.status_text = "Moderate load - System is working"
        else:
            self.status_text = "Light load - CPU has capacity"
    
    def draw(self, screen):
        font_title = pygame.font.Font(None, 60)
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)
        
        # Title
        title = font_title.render("CPU Load Monitor", True, CYAN)
        screen.blit(title, (50, 30))
        
        # Current CPU usage
        if self.cpu_history:
            current_cpu = self.cpu_history[-1]
            cpu_text = font_large.render(f"{current_cpu:.1f}%", True, GREEN if current_cpu < 60 else YELLOW if current_cpu < 80 else RED)
            screen.blit(cpu_text, (50, 120))
            
            cpu_label = font_medium.render("Current CPU Usage", True, WHITE)
            screen.blit(cpu_label, (50, 190))
        
        # Status message
        status_color = GREEN if "Light" in self.status_text else YELLOW if "Moderate" in self.status_text else RED
        status = font_medium.render(self.status_text, True, status_color)
        screen.blit(status, (50, 260))
        
        # CPU Graph
        y_base = 450
        if len(self.cpu_history) > 1:
            for i in range(1, len(self.cpu_history)):
                x1 = 50 + (i - 1) * (WINDOW_WIDTH - 100) / len(self.cpu_history)
                x2 = 50 + i * (WINDOW_WIDTH - 100) / len(self.cpu_history)
                y1 = y_base - (self.cpu_history[i-1] / 100) * 200
                y2 = y_base - (self.cpu_history[i] / 100) * 200
                pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 3)
        
        # Grid and labels
        pygame.draw.line(screen, (50, 50, 50), (50, y_base), (WINDOW_WIDTH - 50, y_base), 1)
        
        for level in [25, 50, 75, 100]:
            y = y_base - (level / 100) * 200
            pygame.draw.line(screen, (40, 40, 40), (50, y), (WINDOW_WIDTH - 50, y), 1)
            label = font_small.render(f"{level}%", True, (100, 100, 100))
            screen.blit(label, (10, y - 15))
        
        # Recommendations
        rec_y = WINDOW_HEIGHT - 120
        recs = [
            "💡 Tips to reduce CPU load:",
            "• Close unnecessary applications",
            "• Disable browser extensions",
            "• Check Task Manager for heavy processes"
        ]
        
        for i, rec in enumerate(recs):
            rec_text = font_small.render(rec, True, YELLOW if "Tips" in rec else WHITE)
            screen.blit(rec_text, (50, rec_y + i * 30))


class RAMTest(GameMode):
    """RAM Test - memory usage and analysis"""
    def __init__(self):
        super().__init__("RAM Test", 4)
        self.time = 0
        self.memory_usage = 0
        self.memory_history = deque(maxlen=100)
        self.total_memory = 0
        self.status_text = ""
    
    def update(self, dt, keys):
        self.time += dt
        
        # Get memory information
        if HAS_PSUTIL:
            try:
                process = psutil.Process(os.getpid())
                self.memory_usage = process.memory_info().rss / 1024 / 1024  # MB
                
                vm = psutil.virtual_memory()
                total_mem = vm.total / 1024 / 1024  # MB
                available = vm.available / 1024 / 1024
                used_percent = vm.percent
                
                self.memory_history.append(used_percent)
                self.total_memory = total_mem
                
                if used_percent > 85:
                    self.status_text = "⚠ CRITICAL - Memory almost full!"
                elif used_percent > 70:
                    self.status_text = "⚠ HIGH - Consider closing some applications"
                elif used_percent > 50:
                    self.status_text = "✓ Normal - System has enough memory"
                else:
                    self.status_text = "✓ Good - Plenty of available memory"
            except:
                self.memory_usage = 100 + 50 * math.sin(self.time)
                self.memory_history.append(50 + 20 * math.sin(self.time))
        else:
            self.memory_usage = 100 + 50 * math.sin(self.time)
            self.memory_history.append(50 + 20 * math.sin(self.time))
    
    def draw(self, screen):
        font_title = pygame.font.Font(None, 60)
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)
        
        # Title
        title = font_title.render("Memory Monitor", True, CYAN)
        screen.blit(title, (50, 30))
        
        # Process memory
        mem_text = font_large.render(f"{self.memory_usage:.1f} MB", True, BLUE)
        screen.blit(mem_text, (50, 120))
        
        mem_label = font_medium.render("Process Memory Usage", True, WHITE)
        screen.blit(mem_label, (50, 190))
        
        # Status
        if self.memory_history:
            status_color = GREEN if self.memory_history[-1] < 50 else YELLOW if self.memory_history[-1] < 70 else RED
            status = font_medium.render(self.status_text, True, status_color)
            screen.blit(status, (50, 260))
        
        # Memory graph
        y_base = 450
        if len(self.memory_history) > 1:
            for i in range(1, len(self.memory_history)):
                x1 = 50 + (i - 1) * (WINDOW_WIDTH - 100) / len(self.memory_history)
                x2 = 50 + i * (WINDOW_WIDTH - 100) / len(self.memory_history)
                y1 = y_base - (self.memory_history[i-1] / 100) * 200
                y2 = y_base - (self.memory_history[i] / 100) * 200
                pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2), 3)
        
        # Grid and labels
        pygame.draw.line(screen, (50, 50, 50), (50, y_base), (WINDOW_WIDTH - 50, y_base), 1)
        
        for level in [25, 50, 75, 100]:
            y = y_base - (level / 100) * 200
            pygame.draw.line(screen, (40, 40, 40), (50, y), (WINDOW_WIDTH - 50, y), 1)
            label = font_small.render(f"{level}%", True, (100, 100, 100))
            screen.blit(label, (10, y - 15))
        
        # Recommendations
        rec_y = WINDOW_HEIGHT - 120
        recs = [
            "💡 How to free up memory:",
            "• Close unused browser tabs",
            "• Restart memory-heavy applications",
            "• Check for memory leaks in Task Manager"
        ]
        
        for i, rec in enumerate(recs):
            rec_text = font_small.render(rec, True, YELLOW if "How" in rec else WHITE)
            screen.blit(rec_text, (50, rec_y + i * 30))


class DiskIOTest(GameMode):
    """Disk I/O Test - read/write performance"""
    def __init__(self):
        super().__init__("Disk I/O Test", 3)
        self.time = 0
        self.write_count = 0
        self.read_count = 0
        self.test_file = "/tmp/fps_test_file.bin"
        self.io_history = deque(maxlen=100)
        self.speed_history = deque(maxlen=100)
        self.last_io_count = 0
    
    def update(self, dt, keys):
        self.time += dt
        
        # Perform write operations
        if int(self.time * 5) % 2 == 0 and int(self.time * 5) != self.write_count:
            self.write_count = int(self.time * 5)
            try:
                with open(self.test_file, 'wb') as f:
                    f.write(bytes([random.randint(0, 255) for _ in range(1000000)]))
            except:
                pass
        
        # Perform read operations
        if int(self.time * 3) % 2 == 1:
            try:
                with open(self.test_file, 'rb') as f:
                    data = f.read()
                    self.read_count = len(data) // 1000000
            except:
                pass
        
        # Track I/O speed
        current_io = self.write_count + self.read_count
        speed = (current_io - self.last_io_count) * 10  # Operations per second
        self.speed_history.append(speed)
        self.last_io_count = current_io
    
    def draw(self, screen):
        font_title = pygame.font.Font(None, 60)
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)
        
        # Title
        title = font_title.render("Disk I/O Monitor", True, CYAN)
        screen.blit(title, (50, 30))
        
        # Write operations
        write_text = font_large.render(f"Writes: {self.write_count}", True, GREEN)
        screen.blit(write_text, (50, 120))
        
        # Read operations
        read_text = font_large.render(f"Reads: {self.read_count} MB", True, BLUE)
        screen.blit(read_text, (50, 190))
        
        # I/O Speed
        if self.speed_history:
            avg_speed = sum(self.speed_history) / len(self.speed_history)
            speed_color = GREEN if avg_speed < 5 else YELLOW if avg_speed < 10 else RED
            speed_text = font_medium.render(f"Speed: {avg_speed:.1f} ops/sec", True, speed_color)
            screen.blit(speed_text, (50, 260))
        
        # Status
        status = "✓ Disk I/O normal" if self.speed_history and sum(self.speed_history) / len(self.speed_history) < 10 else "⚠ High disk usage"
        status_text = font_medium.render(status, True, YELLOW if "High" in status else GREEN)
        screen.blit(status_text, (50, 330))
        
        # Recommendations
        rec_y = WINDOW_HEIGHT - 150
        recs = [
            "💡 Tips for better disk performance:",
            "• Disable unnecessary background processes",
            "• Run disk cleanup regularly",
            "• Consider upgrading to SSD if using HDD",
            "• Check for malware with antivirus"
        ]
        
        for i, rec in enumerate(recs):
            rec_text = font_small.render(rec, True, YELLOW if "Tips" in rec else WHITE)
            screen.blit(rec_text, (50, rec_y + i * 30))


class SystemMonitor(GameMode):
    """System Monitor - comprehensive system overview"""
    def __init__(self):
        super().__init__("System Monitor", 2)
        self.time = 0
        self.cpu_history = deque(maxlen=100)
        self.ram_history = deque(maxlen=100)
        self.cpu_usage = 0
        self.ram_usage = 0
        self.overall_status = "Good"
    
    def update(self, dt, keys):
        self.time += dt
        
        # Get system information
        if HAS_PSUTIL:
            try:
                self.cpu_usage = psutil.cpu_percent(interval=0.01)
                vm = psutil.virtual_memory()
                self.ram_usage = vm.percent
            except:
                self.cpu_usage = 50 + 30 * math.sin(self.time)
                self.ram_usage = 40 + 20 * math.cos(self.time * 0.5)
        else:
            self.cpu_usage = 50 + 30 * math.sin(self.time)
            self.ram_usage = 40 + 20 * math.cos(self.time * 0.5)
        
        self.cpu_history.append(self.cpu_usage)
        self.ram_history.append(self.ram_usage)
        
        # Determine overall system status
        avg_cpu = sum(self.cpu_history) / len(self.cpu_history)
        avg_ram = sum(self.ram_history) / len(self.ram_history)
        
        if avg_cpu > 80 or avg_ram > 85:
            self.overall_status = "⚠ Poor - System stressed"
        elif avg_cpu > 60 or avg_ram > 70:
            self.overall_status = "✓ Fair - Some stress"
        else:
            self.overall_status = "✓ Good - Running smoothly"
    
    def draw(self, screen):
        font_title = pygame.font.Font(None, 60)
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)
        
        # Title
        title = font_title.render("System Health Monitor", True, CYAN)
        screen.blit(title, (50, 30))
        
        # CPU info
        cpu_color = GREEN if self.cpu_usage < 60 else YELLOW if self.cpu_usage < 80 else RED
        cpu_text = font_large.render(f"CPU: {self.cpu_usage:.1f}%", True, cpu_color)
        screen.blit(cpu_text, (50, 120))
        
        # RAM info
        ram_color = GREEN if self.ram_usage < 60 else YELLOW if self.ram_usage < 80 else RED
        ram_text = font_large.render(f"RAM: {self.ram_usage:.1f}%", True, ram_color)
        screen.blit(ram_text, (50, 190))
        
        # Overall status
        status_color = GREEN if "Good" in self.overall_status else YELLOW if "Fair" in self.overall_status else RED
        status_text = font_medium.render(self.overall_status, True, status_color)
        screen.blit(status_text, (50, 260))
        
        # CPU Graph
        y_base = 450
        if len(self.cpu_history) > 1:
            for i in range(1, len(self.cpu_history)):
                x1 = 50 + (i - 1) * (WINDOW_WIDTH - 100) / 2 / len(self.cpu_history)
                x2 = 50 + i * (WINDOW_WIDTH - 100) / 2 / len(self.cpu_history)
                y1 = y_base - (self.cpu_history[i-1] / 100) * 150
                y2 = y_base - (self.cpu_history[i] / 100) * 150
                pygame.draw.line(screen, GREEN, (x1, y1), (x2, y2), 2)
        
        # RAM Graph
        if len(self.ram_history) > 1:
            for i in range(1, len(self.ram_history)):
                x1 = WINDOW_WIDTH // 2 + 50 + (i - 1) * (WINDOW_WIDTH - 100) / 2 / len(self.ram_history)
                x2 = WINDOW_WIDTH // 2 + 50 + i * (WINDOW_WIDTH - 100) / 2 / len(self.ram_history)
                y1 = y_base - (self.ram_history[i-1] / 100) * 150
                y2 = y_base - (self.ram_history[i] / 100) * 150
                pygame.draw.line(screen, BLUE, (x1, y1), (x2, y2), 2)
        
        # Grid
        pygame.draw.line(screen, (50, 50, 50), (50, y_base), (WINDOW_WIDTH - 50, y_base), 1)
        pygame.draw.line(screen, (50, 50, 50), (WINDOW_WIDTH // 2, 320), (WINDOW_WIDTH // 2, y_base), 1)
        
        # Labels
        cpu_label = font_small.render("CPU Usage", True, GREEN)
        screen.blit(cpu_label, (50, y_base + 20))
        
        ram_label = font_small.render("RAM Usage", True, BLUE)
        screen.blit(ram_label, (WINDOW_WIDTH // 2 + 50, y_base + 20))
        
        # Recommendations
        rec_y = WINDOW_HEIGHT - 80
        recs = [
            "💡 System optimization: Balance workload, close unnecessary apps, keep drivers updated"
        ]
        
        for i, rec in enumerate(recs):
            rec_text = font_small.render(rec, True, YELLOW)
            screen.blit(rec_text, (50, rec_y + i * 30))
        
        # CPU
        cpu_text = font_large.render(f"{self.cpu_history[-1]:.1f}%", True, GREEN)
        screen.blit(cpu_text, (100, 100))
        
        cpu_label = font_medium.render("CPU Usage", True, WHITE)
        screen.blit(cpu_label, (100, 190))
        
        # RAM
        ram_text = font_large.render(f"{self.ram_history[-1]:.1f}%", True, BLUE)
        screen.blit(ram_text, (100, 350))
        
        ram_label = font_medium.render("RAM Usage", True, WHITE)
        screen.blit(ram_label, (100, 440))
        
        # CPU graph
        if len(self.cpu_history) > 1:
            for i in range(1, len(self.cpu_history)):
                y1 = WINDOW_HEIGHT - 200 - (self.cpu_history[i-1] / 100) * 100
                y2 = WINDOW_HEIGHT - 200 - (self.cpu_history[i] / 100) * 100
                pygame.draw.line(screen, GREEN, 
                               (WINDOW_WIDTH // 2 + i * 3, y1),
                               (WINDOW_WIDTH // 2 + (i+1) * 3, y2), 2)
        
        # RAM graph
        if len(self.ram_history) > 1:
            for i in range(1, len(self.ram_history)):
                y1 = WINDOW_HEIGHT - 200 - (self.ram_history[i-1] / 100) * 100
                y2 = WINDOW_HEIGHT - 200 - (self.ram_history[i] / 100) * 100
                pygame.draw.line(screen, BLUE,
                               (WINDOW_WIDTH // 2 + i * 3, y1),
                               (WINDOW_WIDTH // 2 + (i+1) * 3, y2), 2)
        
        # Information
        status = "✓ psutil installed" if HAS_PSUTIL else "⚠ psutil not installed (showing simulation)"
        info = font_small.render(f"CPU Usage (green) | RAM Usage (blue) | {status}", True, WHITE)
        screen.blit(info, (50, 30))

class InteractiveDraw(GameMode):
    """Interactive Draw - draw and create effects with mouse"""
    def __init__(self):
        super().__init__("Interactive Draw", 3)
        self.draw_points = []
        self.particles = []
    
    def update(self, dt, keys):
        # Update particles
        for p in self.particles[:]:
            p['life'] -= dt
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vx'] *= 0.98
            p['vy'] *= 0.98
            if p['life'] <= 0:
                self.particles.remove(p)
        
        # Update drawing points
        if pygame.mouse.get_pressed()[0]:  # Left button
            mx, my = pygame.mouse.get_pos()
            self.draw_points.append({
                'x': mx,
                'y': my,
                'color': random.choice([RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, ORANGE]),
                'size': random.randint(3, 8)
            })
            
            # Create particles around cursor
            for _ in range(5):
                self.particles.append({
                    'x': mx + random.randint(-20, 20),
                    'y': my + random.randint(-20, 20),
                    'vx': random.uniform(-2, 2),
                    'vy': random.uniform(-2, 2),
                    'life': 1.0,
                    'color': random.choice([RED, CYAN, MAGENTA])
                })
            
            # Limit size
            if len(self.draw_points) > 2000:
                self.draw_points.pop(0)
    
    def draw(self, screen):
        # Draw line from points
        for p in self.draw_points:
            pygame.draw.circle(screen, p['color'], (p['x'], p['y']), p['size'])
        
        # Draw particles
        for p in self.particles:
            alpha = int(255 * p['life'])
            size = max(1, int(3 * p['life']))
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), size)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Points: {len(self.draw_points)} | Click to draw", True, WHITE)
        screen.blit(text, (50, 30))

class NoiseField(GameMode):
    """Noise Field - noise field with interactivity"""
    def __init__(self):
        super().__init__("Noise Field", 4)
        self.time = 0
        self.disturbances = []
    
    def update(self, dt, keys):
        self.time += dt
        
        # Mouse click creates disturbance
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            self.disturbances.append({
                'x': mx,
                'y': my,
                'radius': 0,
                'max_radius': 200,
                'strength': 1.0
            })
        
        # Update disturbances
        for d in self.disturbances[:]:
            d['radius'] += 5
            if d['radius'] > d['max_radius']:
                self.disturbances.remove(d)
    
    def draw(self, screen):
        # Background noise
        for y in range(0, WINDOW_HEIGHT, 20):
            for x in range(0, WINDOW_WIDTH, 20):
                # Perlin-like noise (simplified)
                noise = math.sin(x / 50 + self.time) * math.cos(y / 50 + self.time)
                
                # Check disturbances
                for d in self.disturbances:
                    dist = math.sqrt((x - d['x'])**2 + (y - d['y'])**2)
                    if dist < d['radius']:
                        influence = (1 - dist / d['radius']) * d['strength']
                        noise += influence * math.sin(self.time)
                
                color_val = int(127 + noise * 127)
                color_val = max(0, min(255, color_val))
                color = (color_val, 100, 255 - color_val)
                
                pygame.draw.rect(screen, color, (x, y, 20, 20))
        
        # Draw disturbance waves
        for d in self.disturbances:
            color = (255, int(255 * (1 - d['radius'] / d['max_radius'])), 0)
            pygame.draw.circle(screen, color, (d['x'], d['y']), int(d['radius']), 2)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Click to disturb | Disturbances: {len(self.disturbances)}", True, WHITE)
        screen.blit(text, (50, 30))

class ParticleAttractor(GameMode):
    """Particle Attractor - particles attracted to cursor"""
    def __init__(self):
        super().__init__("Particle Attractor", 4)
        self.particles = []
        self.particle_count = 300 + self.difficulty * 100
        
        for _ in range(self.particle_count):
            self.particles.append({
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(0, WINDOW_HEIGHT),
                'vx': 0,
                'vy': 0,
                'color': random.choice([RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA])
            })
    
    def update(self, dt, keys):
        mx, my = pygame.mouse.get_pos()
        
        for p in self.particles:
            # Vector to cursor
            dx = mx - p['x']
            dy = my - p['y']
            dist = math.sqrt(dx*dx + dy*dy) + 1
            
            # Attraction force
            force = 200 / (dist + 1)
            
            p['vx'] += (dx / dist) * force * dt
            p['vy'] += (dy / dist) * force * dt
            
            # Friction
            p['vx'] *= 0.95
            p['vy'] *= 0.95
            
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Boundaries
            if p['x'] < 0 or p['x'] > WINDOW_WIDTH:
                p['vx'] *= -1
                p['x'] = max(0, min(WINDOW_WIDTH, p['x']))
            if p['y'] < 0 or p['y'] > WINDOW_HEIGHT:
                p['vy'] *= -1
                p['y'] = max(0, min(WINDOW_HEIGHT, p['y']))
    
    def draw(self, screen):
        for p in self.particles:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), 2)
        
        # Cursor as big point
        mx, my = pygame.mouse.get_pos()
        pygame.draw.circle(screen, YELLOW, (mx, my), 20, 2)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Move cursor to attract particles | Count: {len(self.particles)}", True, WHITE)
        screen.blit(text, (50, 30))

# ═══════════════════════════════════════════════════════════════════════════
# UI LAYER - MENUS AND INTERFACES
# ═══════════════════════════════════════════════════════════════════════════


# ─── Main Menu ───────────────────────────────────────────────────────────

def show_main_menu():
    """
    Main menu - choose between FPS, System tests and Settings.
    Provides visual category selection with animated background.
    """
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("FPS Tester - Main Menu")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 100)
    font_mode = pygame.font.Font(None, 50)
    font_desc = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 28)
    
    selecting = True
    highlight = 0  # 0 = FPS Tests, 1 = System Tests, 2 = Settings
    
    # Background animation
    particles = []
    for _ in range(20):
        particles.append({
            'x': random.randint(0, WINDOW_WIDTH),
            'y': random.randint(0, WINDOW_HEIGHT),
            'vx': random.uniform(-0.5, 0.5),
            'vy': random.uniform(-1, 0),
            'size': random.randint(1, 3),
            'color': random.choice([CYAN, MAGENTA, GREEN])
        })
    
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    highlight = (highlight - 1) % 3
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    highlight = (highlight + 1) % 3
                if event.key == pygame.K_UP:
                    highlight = (highlight - 1) % 3
                if event.key == pygame.K_DOWN:
                    highlight = (highlight + 1) % 3
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if highlight == 0:
                        return "fps"
                    elif highlight == 1:
                        return "system"
                    else:
                        show_settings_menu()
                if event.key == pygame.K_ESCAPE:
                    return None
                if event.unicode == "1":
                    return "fps"
                if event.unicode == "2":
                    return "system"
                if event.unicode == "3":
                    show_settings_menu()
        
        # Update background particles
        for p in particles:
            p['y'] += p['vy']
            p['x'] += p['vx']
            if p['y'] < -10:
                p['y'] = WINDOW_HEIGHT + 10
                p['x'] = random.randint(0, WINDOW_WIDTH)
        
        screen.fill(BLACK)
        
        # Draw background with particles
        for p in particles:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), p['size'])
        
        # Title with effect
        title = font_title.render("FPS TESTER", True, YELLOW)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 40))
        # Add glow
        for offset in [4, 2]:
            shadow = font_title.render("FPS TESTER", True, (50, 50, 0))
            shadow_rect = shadow.get_rect(center=(WINDOW_WIDTH // 2 + offset, 40 + offset))
            screen.blit(shadow, shadow_rect)
        screen.blit(title, title_rect)
        
        subtitle = font_small.render("Select test category or settings", True, WHITE)
        screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 160))
        
        # FPS Tests
        fps_color = CYAN if highlight == 0 else WHITE
        fps_text = font_mode.render("1. FPS Tests", True, fps_color)
        fps_box_color = CYAN if highlight == 0 else (100, 100, 100)
        fps_box_width = 5 if highlight == 0 else 1
        pygame.draw.rect(screen, fps_box_color, (50, 250, 400, 180), fps_box_width)
        if highlight == 0:
            pygame.draw.rect(screen, CYAN, (50, 250, 400, 180), 5)
        screen.blit(fps_text, (80, 270))
        
        fps_desc = font_desc.render("Interactive game modes", True, WHITE)
        screen.blit(fps_desc, (80, 330))
        
        # System Tests
        sys_color = MAGENTA if highlight == 1 else WHITE
        sys_text = font_mode.render("2. System Tests", True, sys_color)
        sys_box_color = MAGENTA if highlight == 1 else (100, 100, 100)
        sys_box_width = 5 if highlight == 1 else 1
        pygame.draw.rect(screen, sys_box_color, (500, 250, 400, 180), sys_box_width)
        if highlight == 1:
            pygame.draw.rect(screen, MAGENTA, (500, 250, 400, 180), 5)
        screen.blit(sys_text, (530, 270))
        
        sys_desc = font_desc.render("Monitor CPU/RAM/Disk", True, WHITE)
        screen.blit(sys_desc, (530, 330))
        
        # Settings
        set_color = GREEN if highlight == 2 else WHITE
        set_text = font_mode.render("3. Settings", True, set_color)
        set_box_color = GREEN if highlight == 2 else (100, 100, 100)
        set_box_width = 5 if highlight == 2 else 1
        pygame.draw.rect(screen, set_box_color, (950, 250, 400, 180), set_box_width)
        if highlight == 2:
            pygame.draw.rect(screen, GREEN, (950, 250, 400, 180), 5)
        screen.blit(set_text, (980, 270))
        
        set_desc = font_desc.render("Configure display", True, WHITE)
        screen.blit(set_desc, (980, 330))
        
        # Information
        info1 = font_small.render("Use ← → or A D or ↑ ↓ to navigate | ENTER to select", True, WHITE)
        info2 = font_small.render("Or press 1/2/3 | ESC to exit", True, WHITE)
        screen.blit(info1, (WINDOW_WIDTH // 2 - info1.get_width() // 2, WINDOW_HEIGHT - 100))
        screen.blit(info2, (WINDOW_WIDTH // 2 - info2.get_width() // 2, WINDOW_HEIGHT - 60))
        
        pygame.display.flip()
        clock.tick(60)


# ─── FPS Tests Menu ──────────────────────────────────────────────────────

def show_fps_menu():
    """
    Menu to select FPS mode.
    Displays all available GPU/CPU stress tests with descriptions.
    """
    modes = [
        ("1", "Particle Storm", "Particles and explosions"),
        ("2", "Polygon Rush", "Rotating polygons"),
        ("3", "Matrix Rain", "Falling characters"),
        ("4", "Fractal Tree", "Recursive trees"),
        ("5", "Wave Simulation", "Wave simulation"),
        ("6", "Bouncing Balls", "Bouncing balls"),
        ("7", "Plasma Effect", "Plasma effect"),
        ("8", "Mandelbrot", "Mandelbrot set"),
        ("9", "Tunnel Effect", "3D tunnel"),
        ("0", "Starfield", "Starfield"),
        ("Q", "Interactive Draw", "Draw with mouse"),
        ("W", "Noise Field", "Noise field"),
        ("E", "Particle Attractor", "Particles to cursor"),
    ]
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("FPS Tester - Select FPS Test")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 80)
    font_mode = pygame.font.Font(None, 40)
    font_desc = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 24)
    
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                for key, _, _ in modes:
                    if event.unicode.upper() == key:
                        # Show difficulty selection for FPS tests
                        difficulty = show_difficulty_menu()
                        return (key, difficulty)
                if event.key == pygame.K_ESCAPE:
                    return None
        
        screen.fill(BLACK)
        
        title = font_title.render("FPS TESTS", True, CYAN)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))
        
        y_pos = 100
        modes_per_column = 7
        x_offset = 50
        
        for idx, (key, name, desc) in enumerate(modes):
            if idx == modes_per_column:
                y_pos = 100
                x_offset = 700
            
            key_text = font_mode.render(f"{key}", True, GREEN)
            name_text = font_mode.render(f"{name}", True, CYAN)
            desc_text = font_desc.render(desc, True, WHITE)
            
            screen.blit(key_text, (x_offset, y_pos))
            screen.blit(name_text, (x_offset + 40, y_pos))
            screen.blit(desc_text, (x_offset + 50, y_pos + 40))
            y_pos += 75
        
        hint = font_small.render("Press ESC to go back", True, WHITE)
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)


# ─── Difficulty Selection Menu ───────────────────────────────────────────

def show_difficulty_menu():
    """
    Menu to select difficulty level for FPS tests.
    Different difficulties stress the hardware differently.
    """
    difficulties = [
        ("1", "EASY", "Light load - basic particles/shapes"),
        ("2", "MEDIUM", "Moderate load - balanced challenge"),
        ("3", "HARD", "Heavy load - serious stress test"),
        ("4", "EXTREME", "Maximum load - push to limits"),
        ("5", "INSANE", "Ultra extreme - break it mode"),
    ]
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("FPS Tester - Select Difficulty")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 80)
    font_mode = pygame.font.Font(None, 50)
    font_desc = pygame.font.Font(None, 32)
    font_small = pygame.font.Font(None, 28)
    
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 2  # Default to MEDIUM
            if event.type == pygame.KEYDOWN:
                for key, _, _ in difficulties:
                    if event.unicode.upper() == key:
                        return int(key)
                if event.key == pygame.K_ESCAPE:
                    return 2  # Default to MEDIUM
        
        screen.fill(BLACK)
        
        title = font_title.render("SELECT DIFFICULTY", True, YELLOW)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
        
        y_pos = 180
        for key, name, desc in difficulties:
            key_text = font_mode.render(f"{key}", True, GREEN)
            name_text = font_mode.render(f"{name}", True, YELLOW if key == "2" else CYAN)
            desc_text = font_desc.render(desc, True, WHITE)
            
            screen.blit(key_text, (150, y_pos))
            screen.blit(name_text, (220, y_pos))
            screen.blit(desc_text, (220, y_pos + 50))
            y_pos += 110
        
        hint = font_small.render("Default: MEDIUM (2) | ESC to go back", True, WHITE)
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)


# ─── System Tests Menu ───────────────────────────────────────────────────

def show_system_menu():
    """
    Menu to select System tests.
    CPU, RAM, and Disk benchmarking options.
    """
    modes = [
        ("C", "CPU Test", "Processor test"),
        ("M", "RAM Test", "Memory test"),
        ("D", "Disk I/O Test", "Disk test"),
        ("S", "System Monitor", "System monitor"),
    ]
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("FPS Tester - Select System Test")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 80)
    font_mode = pygame.font.Font(None, 60)
    font_desc = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 32)
    
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                for key, _, _ in modes:
                    if event.unicode.upper() == key:
                        return key
                if event.key == pygame.K_ESCAPE:
                    return None
        
        screen.fill(BLACK)
        
        title = font_title.render("SYSTEM TESTS", True, MAGENTA)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 50))
        
        y_pos = 200
        for key, name, desc in modes:
            key_text = font_mode.render(f"{key}", True, GREEN)
            name_text = font_mode.render(f"{name}", True, MAGENTA)
            desc_text = font_desc.render(desc, True, WHITE)
            
            screen.blit(key_text, (150, y_pos))
            screen.blit(name_text, (220, y_pos))
            screen.blit(desc_text, (250, y_pos + 45))
            y_pos += 150
        
        hint = font_small.render("Press ESC to go back", True, WHITE)
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)

# ==========================
# SETTINGS MENU
# ==========================

def show_welcome_screen():
    """Welcome screen with information"""
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("FPS Tester - Welcome")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 100)
    font_large = pygame.font.Font(None, 60)
    font_medium = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 28)
    
    welcome = True
    alpha_timer = 0
    
    while welcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
                    return True
        
        # Text appearing animation
        alpha_timer += 1
        
        screen.fill(BLACK)
        
        # Draw stars in background
        for i in range(30):
            x = (i * 47 + alpha_timer * 2) % WINDOW_WIDTH
            y = (i * 31) % WINDOW_HEIGHT
            pygame.draw.circle(screen, (100, 100, 100), (x, y), 1)
        
        # Title
        title = font_title.render("FPS TESTER", True, CYAN)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 80))
        
        subtitle = font_large.render("Performance Analysis Tool", True, YELLOW)
        screen.blit(subtitle, (WINDOW_WIDTH // 2 - subtitle.get_width() // 2, 200))
        
        # Information
        y_pos = 320
        
        info_lines = [
            "✓ Analyze your computer's gaming performance",
            "✓ Test with interactive game modes",
            "✓ Monitor CPU, RAM, and Disk I/O",
            "✓ Get personalized recommendations",
            "",
            "🌐 Web version coming soon!",
            "   Dual-screen architecture for weak PCs:",
            "   - Test screen + Statistics screen",
            "   - Automatic restart on crash",
        ]
        
        for line in info_lines:
            if line.startswith("🌐") or line.startswith("   "):
                color = MAGENTA
                font = font_small
            elif line == "":
                continue
            else:
                color = GREEN
                font = font_medium
            
            text = font.render(line, True, color)
            screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, y_pos))
            y_pos += 45
        
        # Pulsing invitation
        pulse = abs(math.sin(alpha_timer * 0.05))
        brightness = int(255 * (0.5 + pulse * 0.5))
        
        hint = font_medium.render("Press SPACE to continue", True, (brightness, brightness, brightness))
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT - 100))
        
        pygame.display.flip()
        clock.tick(60)

def show_settings_menu():
    """Menu for configuring display settings"""
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("FPS Tester - Settings")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 60)
    font_menu = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 28)
    
    settings_list = [
        ("Show FPS Rounded", "show_fps_rounded"),
        ("Show FPS Real", "show_fps_real"),
        ("Show Hints", "show_hints"),
        ("Show Mode Stats", "show_mode_stats"),
        ("Show Results", "show_results")
    ]
    
    highlight = 0
    
    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_UP:
                    highlight = (highlight - 1) % len(settings_list)
                if event.key == pygame.K_DOWN:
                    highlight = (highlight + 1) % len(settings_list)
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    _, key = settings_list[highlight]
                    GLOBAL_SETTINGS[key] = not GLOBAL_SETTINGS[key]
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    _, key = settings_list[highlight]
                    GLOBAL_SETTINGS[key] = False
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    _, key = settings_list[highlight]
                    GLOBAL_SETTINGS[key] = True
        
        screen.fill(BLACK)
        
        title = font_title.render("Settings", True, CYAN)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 40))
        
        y_pos = 150
        for idx, (label, key) in enumerate(settings_list):
            status = "ON" if GLOBAL_SETTINGS[key] else "OFF"
            status_color = GREEN if GLOBAL_SETTINGS[key] else RED
            
            if idx == highlight:
                bg_rect = pygame.Rect(100, y_pos - 5, WINDOW_WIDTH - 200, 50)
                pygame.draw.rect(screen, MAGENTA, bg_rect)
                text_color = WHITE
            else:
                text_color = WHITE
            
            text = font_menu.render(f"{label}: ", True, text_color)
            status_text = font_menu.render(status, True, status_color)
            
            screen.blit(text, (150, y_pos))
            screen.blit(status_text, (WINDOW_WIDTH // 2 + 100, y_pos))
            
            y_pos += 80
        
        hint1 = font_small.render("SPACE/ENTER - Toggle | LEFT/RIGHT - Off/On", True, YELLOW)
        screen.blit(hint1, (WINDOW_WIDTH // 2 - hint1.get_width() // 2, WINDOW_HEIGHT - 80))
        
        hint2 = font_small.render("ESC - Back", True, WHITE)
        screen.blit(hint2, (WINDOW_WIDTH // 2 - hint2.get_width() // 2, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)

# ==========================

def show_menu():
    """Menu to select mode"""
    modes = [
        ("1", "Geometry Dash", "Jump over obstacles"),
        ("2", "Particle Storm", "Particles fill screen"),
        ("3", "Polygon Rush", "Rotating polygons"),
        ("4", "Matrix Rain", "Falling characters"),
        ("5", "Fractal Tree", "Recursive trees"),
        ("6", "Wave Simulation", "Wave simulation"),
        ("7", "Bouncing Balls", "Bouncing balls"),
        ("8", "Plasma Effect", "Plasma effect"),
        ("9", "Mandelbrot", "Mandelbrot set"),
        ("0", "Tunnel Effect", "3D tunnel"),
        ("Q", "Starfield", "Starfield"),
        ("W", "Interactive Draw", "Draw with mouse"),
        ("E", "Noise Field", "Noise field"),
        ("R", "Particle Attractor", "Particles to cursor"),
        ("A", "CPU Test", "Processor test"),
        ("S", "RAM Test", "Memory test"),
        ("D", "Disk I/O Test", "Disk test"),
        ("F", "System Monitor", "System monitor"),
    ]
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("FPS Tester - Select Mode")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 80)
    font_mode = pygame.font.Font(None, 40)
    font_desc = pygame.font.Font(None, 28)
    font_small = pygame.font.Font(None, 24)
    
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                for key, _, _ in modes:
                    if event.unicode.upper() == key:
                        return key
                if event.key == pygame.K_ESCAPE:
                    return None
        
        screen.fill(BLACK)
        
        title = font_title.render("FPS TESTER", True, YELLOW)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))
        
        y_pos = 100
        modes_per_column = 9
        x_offset = 50
        
        for idx, (key, name, desc) in enumerate(modes):
            if idx == modes_per_column:
                y_pos = 100
                x_offset = 700
            
            key_text = font_mode.render(f"{key}", True, GREEN)
            name_text = font_mode.render(f"{name}", True, CYAN)
            desc_text = font_desc.render(desc, True, WHITE)
            
            screen.blit(key_text, (x_offset, y_pos))
            screen.blit(name_text, (x_offset + 40, y_pos))
            screen.blit(desc_text, (x_offset + 50, y_pos + 40))
            y_pos += 75
        
        hint = font_small.render("Press ESC to exit", True, WHITE)
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT - 40))
        
        pygame.display.flip()
        clock.tick(60)

# ==========================
# RECOMMENDATION SYSTEM
# ==========================

def get_performance_recommendations(avg_fps, min_fps, max_fps):
    """Generates recommendations based on FPS"""
    recommendations = []
    
    # Check performance level
    if avg_fps >= 120:
        status = "EXCELLENT"
        status_color = (0, 255, 0)  # GREEN
        recommendations.append("✓ Excellent performance! Your computer can handle maximum settings")
        recommendations.append("✓ Graphics on maximum, 4K resolution, all effects enabled")
    elif avg_fps >= 90:
        status = "VERY GOOD"
        status_color = (100, 255, 100)  # Light Green
        recommendations.append("✓ Very good performance")
        recommendations.append("✓ High graphics settings, 1440p resolution")
        recommendations.append("• Try enabling maximum effects")
    elif avg_fps >= 60:
        status = "GOOD"
        status_color = (255, 255, 0)  # YELLOW
        recommendations.append("✓ Normal performance (60+ FPS)")
        recommendations.append("✓ Medium-High settings, 1080p resolution")
        recommendations.append("• Some heavy effects might need to be disabled")
    elif avg_fps >= 45:
        status = "ACCEPTABLE"
        status_color = (255, 165, 0)  # ORANGE
        recommendations.append("⚠ Acceptable performance for casual gaming")
        recommendations.append("⚠ Medium graphics settings, 1080p")
        recommendations.append("! Lower resolution or disable some effects")
        recommendations.append("! Close background applications")
    elif avg_fps >= 30:
        status = "POOR"
        status_color = (255, 100, 0)  # Dark Orange
        recommendations.append("✗ Low performance")
        recommendations.append("! Lower resolution to 720p or below")
        recommendations.append("! Disable graphics effects")
        recommendations.append("! Close all background applications")
    else:
        status = "CRITICAL"
        status_color = (255, 0, 0)  # RED
        recommendations.append("✗ CRITICAL LOW PERFORMANCE")
        recommendations.append("! Upgrade your graphics card or processor")
        recommendations.append("! Use minimum settings (720p, no effects)")
    
    # Check stability (difference between min and max)
    fps_variance = max_fps - min_fps
    if fps_variance > 40:
        recommendations.append("")
        recommendations.append("⚠ INSTABILITY: Large FPS fluctuations")
        recommendations.append("  May be caused by: overheating, background processes, weak power supply")
    
    return status, status_color, recommendations


def get_system_recommendations(game_mode):
    """Generate recommendations based on system test data"""
    recommendations = []
    
    # Analyze based on test type
    if game_mode.name == "CPU Test":
        if hasattr(game_mode, 'cpu_history') and game_mode.cpu_history:
            avg_cpu = sum(game_mode.cpu_history) / len(game_mode.cpu_history)
            max_cpu = max(game_mode.cpu_history)
            
            recommendations.append(f"📊 Average CPU usage: {avg_cpu:.1f}%")
            recommendations.append(f"📊 Peak CPU usage: {max_cpu:.1f}%")
            recommendations.append("")
            
            if max_cpu > 95:
                recommendations.append("⚠ CPU is running at maximum capacity")
                recommendations.append("✓ Action: Close unnecessary background applications")
                recommendations.append("✓ Action: Disable browser extensions")
                recommendations.append("✓ Action: Check for malware or resource-heavy processes")
                recommendations.append("✓ Action: Update drivers and BIOS")
            elif max_cpu > 80:
                recommendations.append("⚠ CPU is under heavy load")
                recommendations.append("✓ Action: Monitor temperature to avoid throttling")
                recommendations.append("✓ Action: Close some background programs")
                recommendations.append("✓ Action: Consider upgrading if frequently at 80%+")
            elif max_cpu > 60:
                recommendations.append("✓ CPU usage is normal")
                recommendations.append("✓ Your processor is handling tasks well")
                recommendations.append("• Could upgrade for more headroom if needed")
            else:
                recommendations.append("✓ CPU is underutilized - plenty of capacity")
                recommendations.append("✓ You can run demanding applications easily")
    
    elif game_mode.name == "RAM Test":
        if hasattr(game_mode, 'memory_history') and game_mode.memory_history:
            avg_ram = sum(game_mode.memory_history) / len(game_mode.memory_history)
            max_ram = max(game_mode.memory_history)
            
            recommendations.append(f"📊 Average RAM usage: {avg_ram:.1f}%")
            recommendations.append(f"📊 Peak RAM usage: {max_ram:.1f}%")
            recommendations.append("")
            
            if max_ram > 90:
                recommendations.append("✗ CRITICAL: RAM almost full!")
                recommendations.append("✓ Action: Close applications immediately")
                recommendations.append("✓ Action: Restart your computer to free memory")
                recommendations.append("✓ Recommendation: Upgrade to more RAM")
                recommendations.append("✓ Action: Use 64-bit OS to support more RAM")
            elif max_ram > 80:
                recommendations.append("⚠ RAM usage is very high")
                recommendations.append("✓ Action: Close unused browser tabs and applications")
                recommendations.append("✓ Action: Clear temporary files and cache")
                recommendations.append("! Recommendation: Consider upgrading RAM")
            elif max_ram > 70:
                recommendations.append("⚠ RAM usage is getting high")
                recommendations.append("✓ Action: Monitor for memory leaks in Task Manager")
                recommendations.append("• Close some background applications if needed")
            elif max_ram > 50:
                recommendations.append("✓ RAM usage is normal")
                recommendations.append("✓ Your system has good memory capacity")
                recommendations.append("• Plenty of room for multitasking")
            else:
                recommendations.append("✓ RAM usage is very low")
                recommendations.append("✓ Excellent memory headroom for applications")
    
    elif game_mode.name == "Disk I/O Test":
        recommendations.append("📊 Disk I/O Performance Test")
        recommendations.append("")
        recommendations.append("✓ Action: Keep your disk at least 10% free")
        recommendations.append("✓ Action: Defragment HDD regularly (not SSD)")
        recommendations.append("✓ Action: Run disk cleanup to remove temp files")
        recommendations.append("✓ Action: Check disk health with CrystalDiskInfo")
        recommendations.append("! Performance Tip: SSDs are 5-10x faster than HDDs")
        recommendations.append("! Tip: Keep OS on SSD for fastest performance")
    
    elif game_mode.name == "System Monitor":
        if hasattr(game_mode, 'cpu_history') and hasattr(game_mode, 'ram_history'):
            if game_mode.cpu_history:
                avg_cpu = sum(game_mode.cpu_history) / len(game_mode.cpu_history)
            else:
                avg_cpu = 0
            
            if game_mode.ram_history:
                avg_ram = sum(game_mode.ram_history) / len(game_mode.ram_history)
            else:
                avg_ram = 0
            
            recommendations.append(f"📊 System Health Summary:")
            recommendations.append(f"   CPU Average: {avg_cpu:.1f}%")
            recommendations.append(f"   RAM Average: {avg_ram:.1f}%")
            recommendations.append("")
            
            if avg_cpu > 70 or avg_ram > 75:
                recommendations.append("⚠ System is under stress")
                recommendations.append("✓ Action: Close unnecessary applications")
                recommendations.append("✓ Action: Disable startup programs (msconfig or Task Manager)")
                recommendations.append("✓ Action: Reduce visual effects (Aero, transparency)")
                recommendations.append("✓ Action: Consider upgrading hardware")
            elif avg_cpu > 50 or avg_ram > 60:
                recommendations.append("✓ System is performing normally")
                recommendations.append("✓ Good balance between usage and capacity")
                recommendations.append("• You can handle most tasks comfortably")
            else:
                recommendations.append("✓ System is performing optimally")
                recommendations.append("✓ Very healthy resource usage")
                recommendations.append("✓ Excellent potential for gaming and multitasking")
    
    # Add general optimization tips at the end
    recommendations.append("")
    recommendations.append("💡 General Optimization Tips:")
    recommendations.append("  • Disable visual effects if performance is priority")
    recommendations.append("  • Keep Windows and drivers updated")
    recommendations.append("  • Run antivirus scans regularly")
    recommendations.append("  • Clean temporary files monthly")
    recommendations.append("  • Monitor temperatures to prevent throttling")
    
    return recommendations


def calculate_performance_score(avg_fps, cpu_usage, ram_usage):
    """Calculate overall performance score (1-10)"""
    score = 10
    
    # Deduct points based on FPS
    if avg_fps < 30:
        score -= 4
    elif avg_fps < 60:
        score -= 2
    elif avg_fps < 120:
        score -= 0.5
    
    # Deduct points based on CPU usage
    if cpu_usage > 90:
        score -= 2
    elif cpu_usage > 70:
        score -= 1
    
    # Deduct points based on RAM usage
    if ram_usage > 90:
        score -= 2
    elif ram_usage > 80:
        score -= 1
    
    return max(1, min(10, score))


def detect_bottleneck(avg_fps, cpu_usage, ram_usage):
    """Detect which component is the bottleneck"""
    bottleneck = None
    severity = "None"
    
    # High CPU usage with low FPS = CPU bottleneck
    if cpu_usage > 85:
        bottleneck = "CPU-Bound"
        severity = "Critical" if cpu_usage > 95 else "High" if cpu_usage > 90 else "Medium"
    # High RAM usage = RAM bottleneck
    elif ram_usage > 85:
        bottleneck = "RAM-Bound"
        severity = "Critical" if ram_usage > 95 else "High" if ram_usage > 90 else "Medium"
    # Low FPS despite low CPU/RAM = GPU bottleneck (expected in graphics tests)
    elif avg_fps < 60 and cpu_usage < 75 and ram_usage < 80:
        bottleneck = "GPU-Bound"
        severity = "High" if avg_fps < 30 else "Medium"
    # Very low FPS overall = Overall system weak
    elif avg_fps < 30:
        bottleneck = "Overall-Weak"
        severity = "Critical"
    # Good balance = well-balanced system
    else:
        bottleneck = "Balanced"
        severity = "Good"
    
    return bottleneck, severity


def get_game_recommendations(avg_fps, cpu_usage, ram_usage):
    """Recommend what games can be played based on stress test results"""
    recommendations = []
    
    recommendations.append("🎮 Game Recommendations Based on Test Results:")
    recommendations.append("")
    recommendations.append("Note: These are estimated based on stress test performance")
    recommendations.append("")
    
    # Higher FPS in stress tests = better hardware = can handle harder games
    if avg_fps >= 180:
        recommendations.append("✓ EXTREME PERFORMANCE: Top-tier gaming machine")
        recommendations.append("✓ Can handle: 4K Ultra AAA games at 60+ FPS")
        recommendations.append("✓ Can handle: 1440p Ultra with raytracing")
        recommendations.append("✓ Can handle: Competitive gaming at 144+ FPS")
        recommendations.append("✓ VR: All VR titles at maximum settings")
    elif avg_fps >= 140:
        recommendations.append("✓ EXCELLENT: High-end gaming system")
        recommendations.append("✓ Can handle: 1440p Ultra AAA games at 60+ FPS")
        recommendations.append("✓ Can handle: 1080p Ultra with raytracing at 100+ FPS")
        recommendations.append("✓ Can handle: Competitive gaming smoothly")
        recommendations.append("✓ VR: All VR games at high settings")
    elif avg_fps >= 100:
        recommendations.append("✓ VERY GOOD: Strong gaming PC")
        recommendations.append("✓ Can handle: 1080p High/Ultra AAA games at 60+ FPS")
        recommendations.append("✓ Can handle: Most modern games at good settings")
        recommendations.append("✓ Can handle: Competitive games at 90+ FPS")
        recommendations.append("✓ VR: Most VR titles playable")
    elif avg_fps >= 70:
        recommendations.append("✓ GOOD: Solid mid-range gaming PC")
        recommendations.append("✓ Can handle: 1080p Medium/High AAA games")
        recommendations.append("✓ Can handle: Popular games at comfortable FPS")
        recommendations.append("• Some AAA ultra/4K may need settings reduction")
        recommendations.append("• VR: Most titles playable on medium settings")
    elif avg_fps >= 45:
        recommendations.append("⚠ ACCEPTABLE: Entry-level gaming")
        recommendations.append("⚠ Can handle: 1080p Low/Medium settings AAA")
        recommendations.append("⚠ Can handle: Older/lighter games on high settings")
        recommendations.append("! Demanding AAA games need lower settings")
        recommendations.append("! VR: Limited support, lower quality games only")
    elif avg_fps >= 30:
        recommendations.append("⚠ MINIMAL: Weak gaming performance")
        recommendations.append("⚠ Can handle: Indie games, older AAA titles")
        recommendations.append("⚠ Can handle: Web games, 2D games smoothly")
        recommendations.append("! Modern AAA games not recommended")
        recommendations.append("! VR: Not suitable")
    else:
        recommendations.append("✗ NOT GAMING-READY: Hardware too weak")
        recommendations.append("✗ Can only run: Older games, casual/web games")
        recommendations.append("✗ Not recommended for: Gaming at all")
        recommendations.append("! Hardware upgrade strongly needed for gaming")
    
    return recommendations


def get_upgrade_recommendations(avg_fps, cpu_usage, ram_usage, bottleneck):
    """Suggest specific hardware upgrades based on bottleneck analysis"""
    recommendations = []
    
    recommendations.append("")
    recommendations.append("⚡ Upgrade Recommendations:")
    
    if bottleneck == "CPU-Bound":
        recommendations.append("🔴 PRIMARY BOTTLENECK: CPU is limiting performance")
        recommendations.append("   Action: Upgrade to newer/faster CPU")
        recommendations.append("   Expected gain: +30-50% FPS improvement")
        recommendations.append("   Cost priority: HIGH")
    elif bottleneck == "RAM-Bound":
        recommendations.append("🔴 PRIMARY BOTTLENECK: RAM insufficient or too slow")
        if ram_usage > 95:
            recommendations.append("   Action: Increase RAM to 32GB+ or upgrade speed")
            recommendations.append("   Current: System at critical memory limit")
        else:
            recommendations.append("   Action: Increase RAM to 24GB+ or upgrade speed")
            recommendations.append("   Current: Memory bandwidth insufficient")
        recommendations.append("   Expected gain: +20-40% FPS improvement")
        recommendations.append("   Cost priority: MEDIUM")
    elif bottleneck == "GPU-Bound":
        recommendations.append("🔴 PRIMARY BOTTLENECK: GPU is the limiting factor")
        recommendations.append("   Action: Upgrade to newer/stronger GPU")
        recommendations.append("   Expected gain: +40-100% FPS improvement")
        recommendations.append("   Cost priority: HIGH (most expensive)")
    elif bottleneck == "Overall-Weak":
        recommendations.append("🔴 CRITICAL: Entire system is underpowered")
        recommendations.append("   Action: Major upgrade or full system replacement")
        recommendations.append("   Priority: CPU + GPU upgrade combo")
        recommendations.append("   Or: Replace entire system")
    else:
        recommendations.append("✅ NO UPGRADES NEEDED")
        recommendations.append("   Your system is well-balanced!")
        recommendations.append("   Optional improvements:")
        recommendations.append("   • SSD upgrade for faster loading")
        recommendations.append("   • Additional storage (if needed)")
    
    return recommendations


def show_results(game_mode):
    """Results screen with recommendations - handles both FPS and system tests"""
    # Determine if this is a system test
    system_tests = {"CPU Test", "RAM Test", "Disk I/O Test", "System Monitor"}
    is_system_test = game_mode.name in system_tests
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("FPS Tester - Results")
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 80)
    font_large = pygame.font.Font(None, 70)
    font_medium = pygame.font.Font(None, 50)
    font_stats = pygame.font.Font(None, 40)
    font_small = pygame.font.Font(None, 28)
    font_tiny = pygame.font.Font(None, 22)
    font_score = pygame.font.Font(None, 140)  # For big performance score
    
    showing = True
    scroll_offset = 0
    
    # Get recommendations based on test type
    if is_system_test:
        recommendations = get_system_recommendations(game_mode)
        status = "System Analysis Complete"
        status_color = CYAN
        all_recommendations = recommendations
    else:
        avg_fps, min_fps, max_fps = game_mode.get_stats()
        status, status_color, fps_recommendations = get_performance_recommendations(avg_fps, min_fps, max_fps)
        
        # Get system metrics for analysis (default values if not available)
        cpu_usage = 50
        ram_usage = 60
        
        # Try to get real system metrics if available
        if HAS_PSUTIL:
            try:
                cpu_usage = psutil.cpu_percent(interval=0.1)
                ram_usage = psutil.virtual_memory().percent
            except:
                pass
        
        # Calculate performance score
        perf_score = calculate_performance_score(avg_fps, cpu_usage, ram_usage)
        
        # Detect bottleneck
        bottleneck, bottleneck_severity = detect_bottleneck(avg_fps, cpu_usage, ram_usage)
        
        # Get game playability recommendations
        game_recs = get_game_recommendations(avg_fps, cpu_usage, ram_usage)
        
        # Get upgrade recommendations
        upgrade_recs = get_upgrade_recommendations(avg_fps, cpu_usage, ram_usage, bottleneck)
        
        # Combine all recommendations
        all_recommendations = fps_recommendations + game_recs + upgrade_recs
    
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE]:
                    return
                if event.key == pygame.K_UP:
                    scroll_offset = min(0, scroll_offset + 30)
                if event.key == pygame.K_DOWN:
                    scroll_offset = max(-(len(all_recommendations) * 25), scroll_offset - 30)
        
        screen.fill(BLACK)
        
        # Title
        title = font_title.render("Test Complete!", True, YELLOW)
        screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))
        
        game_text = font_medium.render(game_mode.name, True, CYAN)
        screen.blit(game_text, (WINDOW_WIDTH // 2 - game_text.get_width() // 2, 110))
        
        # Status
        status_text = font_large.render(status, True, status_color)
        screen.blit(status_text, (WINDOW_WIDTH // 2 - status_text.get_width() // 2, 180))
        
        # FPS Statistics (only for FPS tests)
        if not is_system_test:
            y_pos = 260
            
            avg_fps, min_fps, max_fps = game_mode.get_stats()
            
            # Performance Score (big visual indicator)
            score_color = GREEN if perf_score >= 7 else YELLOW if perf_score >= 5 else RED
            score_text = font_score.render(f"{perf_score:.1f}/10", True, score_color)
            screen.blit(score_text, (50, y_pos - 20))
            
            score_label = font_small.render("Performance Score", True, WHITE)
            screen.blit(score_label, (50, y_pos + 100))
            
            # Bottleneck indicator
            bottleneck_color = GREEN if bottleneck_severity == "Good" else YELLOW if bottleneck_severity == "Medium" else RED
            bottleneck_text = font_stats.render(f"Bottleneck: {bottleneck} ({bottleneck_severity})", True, bottleneck_color)
            screen.blit(bottleneck_text, (600, y_pos + 30))
            
            # FPS Stats
            avg_label = font_stats.render(f"Avg: {int(avg_fps)} FPS", True, GREEN)
            screen.blit(avg_label, (600, y_pos + 90))
            
            min_color = RED if min_fps < 60 else YELLOW
            min_label = font_stats.render(f"Min: {int(min_fps)} FPS", True, min_color)
            screen.blit(min_label, (600, y_pos + 150))
            
            rec_start_y = 450
        else:
            rec_start_y = 280
        
        # Recommendations
        y_pos = rec_start_y
        
        rec_title = font_stats.render("Analysis & Recommendations:", True, CYAN)
        screen.blit(rec_title, (50, y_pos))
        
        y_pos += 60
        
        # Display recommendations with scrolling
        for idx, rec in enumerate(all_recommendations):
            screen_y = y_pos + (idx * 28) + scroll_offset
            
            if y_pos + 250 > screen_y > y_pos - 30:  # Visible on screen
                if rec.startswith("✓"):
                    color = GREEN
                elif rec.startswith("✗"):
                    color = RED
                elif rec.startswith("!"):
                    color = ORANGE
                elif rec.startswith("⚠"):
                    color = (255, 165, 0)
                elif rec.startswith("🎮"):
                    color = CYAN
                elif rec.startswith("⚡"):
                    color = YELLOW
                else:
                    color = WHITE
                
                rec_text = font_tiny.render(rec, True, color)
                screen.blit(rec_text, (70, screen_y))
        
        # Hint
        hint = font_small.render("Press SPACE to return | ↑ ↓ to scroll", True, WHITE)
        screen.blit(hint, (WINDOW_WIDTH // 2 - hint.get_width() // 2, WINDOW_HEIGHT - 50))
        
        pygame.display.flip()
        clock.tick(60)


# ═══════════════════════════════════════════════════════════════════════════
# GAME ENGINE & MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════

def run_game_mode(mode_key):
    """
    Run selected game mode.
    Handles game loop, FPS counting, and crash protection.
    
    Args:
        mode_key: Either a string (system tests) or tuple (key, difficulty) for FPS tests
    """
    # Handle both formats: string for system tests, tuple for FPS tests with difficulty
    difficulty = 2  # Default to MEDIUM
    if isinstance(mode_key, tuple):
        mode_key, difficulty = mode_key
    
    # Create mode
    modes_map = {
        "1": ParticleStorm,
        "2": PolygonRush,
        "3": MatrixRain,
        "4": FractalTree,
        "5": WaveSimulation,
        "6": BouncingBalls,
        "7": PlasmaEffect,
        "8": Mandelbrot,
        "9": TunnelEffect,
        "0": Starfield,
        "Q": InteractiveDraw,
        "W": NoiseField,
        "E": ParticleAttractor,
        "C": CPUTest,
        "M": RAMTest,
        "D": DiskIOTest,
        "S": SystemMonitor,
    }
    
    # Create game mode with difficulty level
    game_mode = modes_map[mode_key](difficulty)
    
    # ===== CRASH PROTECTION VARIABLES =====
    crash_detected = False
    fps_history = deque(maxlen=10)
    frozen_frame_count = 0
    last_frame_time = time.time()
    
    try:
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(f"FPS Tester - {game_mode.name}")
        clock = pygame.time.Clock()
        
        font_fps = pygame.font.Font(None, 100)
        font_small = pygame.font.Font(None, 32)
        font_warning = pygame.font.Font(None, 48)
        
        running = True
        last_time = time.time()
        
        while running:
            try:
                current_time = time.time()
                dt = min(current_time - last_time, 0.016)
                last_time = current_time
                
                # ===== CRASH DETECTION =====
                time_since_last_frame = current_time - last_frame_time
                
                # Detect if system is frozen (no frame updates for 2+ seconds)
                if time_since_last_frame > 2.0:
                    frozen_frame_count += 1
                else:
                    frozen_frame_count = 0
                
                last_frame_time = current_time
                
                # Check FPS for critical stress
                raw_fps = clock.get_fps()
                fps_history.append(raw_fps)
                
                # If FPS < 3 or frozen for 3+ frames = CRASH
                if raw_fps < 3 or frozen_frame_count >= 3:
                    crash_detected = True
                
                # ===== EVENT HANDLING =====
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return None
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        if event.key == pygame.K_s and not crash_detected:
                            show_settings_menu()
                        # Allow continuing after crash with 'C' key
                        if event.key == pygame.K_c:
                            if crash_detected:
                                crash_detected = False
                                frozen_frame_count = 0
                
                if not running:
                    break
                
                # ===== SKIP DRAWING IF CRASH DETECTED =====
                if crash_detected:
                    # Show crash warning instead of game
                    screen.fill(BLACK)
                    
                    # Red warning border
                    pygame.draw.rect(screen, RED, (10, 10, WINDOW_WIDTH-20, WINDOW_HEIGHT-20), 5)
                    
                    # Warning title
                    warning_title = font_warning.render("⚠️  SYSTEM CRASH DETECTED", True, RED)
                    screen.blit(warning_title, (WINDOW_WIDTH//2 - warning_title.get_width()//2, 100))
                    
                    # Warning message
                    msg1 = font_small.render("Your system has crashed or become unresponsive", True, YELLOW)
                    msg2 = font_small.render(f"Test: {game_mode.name}", True, YELLOW)
                    msg3 = font_small.render("The program is still running and protected!", True, GREEN)
                    msg4 = font_small.render("Press C to CONTINUE or ESC to RETURN to menu", True, CYAN)
                    
                    screen.blit(msg1, (WINDOW_WIDTH//2 - msg1.get_width()//2, 250))
                    screen.blit(msg2, (WINDOW_WIDTH//2 - msg2.get_width()//2, 320))
                    screen.blit(msg3, (WINDOW_WIDTH//2 - msg3.get_width()//2, 420))
                    screen.blit(msg4, (WINDOW_WIDTH//2 - msg4.get_width()//2, 550))
                    
                    # Recommendation
                    rec_text = font_small.render("RECOMMENDATION: Do not run this test again", True, RED)
                    screen.blit(rec_text, (WINDOW_WIDTH//2 - rec_text.get_width()//2, 700))
                    
                    pygame.display.flip()
                    clock.tick(30)  # Slow down to prevent further stress
                    continue
                
                # ===== NORMAL GAME RENDERING =====
                # Controls
                keys = pygame.key.get_pressed()
                
                # Update mode
                game_mode.update(dt, keys)
                
                # Get FPS
                raw_fps = clock.get_fps()
                current_fps_display = game_mode.get_fps_display(raw_fps, dt)
                
                # Render/Draw
                screen.fill(BLACK)
                game_mode.draw(screen)
                
                # ===== HUD PANEL (RIGHT BOTTOM CORNER) =====
                # Create semi-transparent HUD panel with better styling
                hud_width = 340
                hud_height = 240
                hud_x = WINDOW_WIDTH - hud_width - 15
                hud_y = WINDOW_HEIGHT - hud_height - 15
                
                # Create HUD surface with transparency
                hud_surface = pygame.Surface((hud_width, hud_height), pygame.SRCALPHA)
                # Dark background with gradient effect
                pygame.draw.rect(hud_surface, (15, 15, 35, 200), (0, 0, hud_width, hud_height))
                # Bright border
                pygame.draw.rect(hud_surface, (0, 255, 255, 255), (0, 0, hud_width, hud_height), 3)
                # Top accent line
                pygame.draw.line(hud_surface, (0, 200, 255, 255), (5, 5), (hud_width-5, 5), 2)
                
                # Draw HUD content - create fonts here
                font_hud_title = pygame.font.Font(None, 20)
                font_hud_value = pygame.font.Font(None, 42)
                font_hud_label = pygame.font.Font(None, 16)
                
                # Title bar
                title_text = font_hud_title.render("═════ PERFORMANCE ═════", True, (0, 200, 255))
                hud_surface.blit(title_text, (int(hud_width//2 - title_text.get_width()//2), 12))
                
                hud_content_y = 50
                
                # FPS Display (Large)
                if GLOBAL_SETTINGS["show_fps_rounded"]:
                    fps_label = font_hud_title.render("FPS (Rounded):", True, (200, 200, 200))
                    fps_value = font_hud_value.render(str(current_fps_display), True, (0, 255, 255))
                    
                    hud_surface.blit(fps_label, (20, hud_content_y))
                    hud_surface.blit(fps_value, (20, hud_content_y + 22))
                    
                    # Color code the FPS value
                    if current_fps_display >= 120:
                        fps_status = "EXCELLENT"
                        color = (0, 255, 0)
                    elif current_fps_display >= 60:
                        fps_status = "GOOD"
                        color = (100, 255, 100)
                    else:
                        fps_status = "LOW"
                        color = (255, 100, 0)
                    
                    status_text = font_hud_label.render(fps_status, True, color)
                    hud_surface.blit(status_text, (20 + fps_value.get_width() + 15, hud_content_y + 35))
                    
                    hud_content_y += 85
                    # Separator line
                    pygame.draw.line(hud_surface, (100, 150, 200, 150), (15, hud_content_y - 5), (hud_width - 15, hud_content_y - 5), 1)
                
                # Real FPS (smaller)
                if GLOBAL_SETTINGS["show_fps_real"]:
                    real_label = font_hud_label.render("Real FPS:", True, (200, 200, 200))
                    real_value = font_hud_label.render(f"{raw_fps:.1f}", True, (255, 255, 100))
                    
                    hud_surface.blit(real_label, (20, hud_content_y))
                    hud_surface.blit(real_value, (140, hud_content_y))
                    hud_content_y += 30
                
                # Test Name
                test_label = font_hud_label.render("Test:", True, (200, 200, 200))
                test_name = font_hud_label.render(f"{game_mode.name[:28]}", True, (100, 255, 100))
                
                hud_surface.blit(test_label, (20, hud_content_y))
                hud_surface.blit(test_name, (20, hud_content_y + 18))
                hud_content_y += 48
                
                # Difficulty indicator
                diff_text = f"Level: {game_mode.difficulty}/5"
                diff_label = font_hud_label.render(diff_text, True, (255, 150, 100))
                hud_surface.blit(diff_label, (20, hud_content_y))
                
                # Blit HUD to main screen
                screen.blit(hud_surface, (hud_x, hud_y))
                
                # ===== BOTTOM LEFT HINTS PANEL =====
                if GLOBAL_SETTINGS["show_hints"]:
                    hints_width = 360
                    hints_height = 60
                    hints_x = 15
                    hints_y = WINDOW_HEIGHT - hints_height - 15
                    
                    hints_surface = pygame.Surface((hints_width, hints_height), pygame.SRCALPHA)
                    pygame.draw.rect(hints_surface, (15, 15, 35, 200), (0, 0, hints_width, hints_height))
                    pygame.draw.rect(hints_surface, (255, 100, 255, 255), (0, 0, hints_width, hints_height), 3)
                    pygame.draw.line(hints_surface, (200, 100, 255, 255), (5, 5), (hints_width-5, 5), 2)
                    
                    hint_title = font_hud_title.render("─── CONTROLS ───", True, (200, 150, 255))
                    hints_surface.blit(hint_title, (int(hints_width//2 - hint_title.get_width()//2), 8))
                    
                    hint = font_hud_label.render("ESC - Finish Test  |  S - Settings", True, (200, 200, 200))
                    hints_surface.blit(hint, (15, 30))
                    
                    screen.blit(hints_surface, (hints_x, hints_y))
                
                pygame.display.flip()
                clock.tick()  # Unlimited FPS
                
            except Exception as frame_error:
                # Catch rendering errors
                crash_detected = True
                continue
        
        # Show results (even if crash occurred)
        if GLOBAL_SETTINGS["show_results"] and not crash_detected:
            show_results(game_mode)
        
        return True
    
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"CRASH PROTECTION ACTIVATED")
        print(f"{'='*60}")
        print(f"Test: {game_mode.name}")
        print(f"Error: {e}")
        print(f"{'='*60}")
        print(f"The program has recovered and will return to main menu.")
        print(f"Do NOT run this test again - it exceeds your system's limits.")
        print(f"{'='*60}\n")
        
        import traceback
        traceback.print_exc()
        
        # Show crash warning on screen for 3 seconds
        try:
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption("FPS Tester - CRASH RECOVERY")
            font_title = pygame.font.Font(None, 64)
            font_text = pygame.font.Font(None, 32)
            
            for i in range(3):
                screen.fill(BLACK)
                pygame.draw.rect(screen, RED, (20, 20, WINDOW_WIDTH-40, WINDOW_HEIGHT-40), 8)
                
                title = font_title.render("SYSTEM CRASHED", True, RED)
                msg1 = font_text.render(f"Test: {game_mode.name}", True, YELLOW)
                msg2 = font_text.render("The program has safely recovered!", True, GREEN)
                msg3 = font_text.render("Returning to main menu in 3 seconds...", True, CYAN)
                
                screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 150))
                screen.blit(msg1, (WINDOW_WIDTH//2 - msg1.get_width()//2, 300))
                screen.blit(msg2, (WINDOW_WIDTH//2 - msg2.get_width()//2, 400))
                screen.blit(msg3, (WINDOW_WIDTH//2 - msg3.get_width()//2, 550))
                
                pygame.display.flip()
                pygame.time.wait(1000)
        except:
            pass
        
        return False


# ═══════════════════════════════════════════════════════════════════════════
# APPLICATION ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

# Show welcome screen
if not show_welcome_screen():
    pygame.quit()
    sys.exit()

# Main application loop
while True:
    # Show main menu
    category = show_main_menu()
    
    if category is None:
        # Exit requested from main menu
        break
    
    # Select test category
    if category == "fps":
        selected = show_fps_menu()
    else:  # system
        selected = show_system_menu()
    
    if selected is None:
        # Back to main menu if no test selected
        continue
    
    # Run the selected game mode
    run_game_mode(selected)
    # Return to main menu after test completes (whether exited or finished)

pygame.quit()
sys.exit()
