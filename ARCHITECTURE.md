# Code Architecture & Organization

## Overview

The FPS Tester codebase has been restructured from a flat ChatGPT-style layout to a professional, well-organized architecture with clear separation of concerns.

## Project Structure

### 1. **Configuration Layer** (Lines 45-85)
Centralized configuration management using classes:

- **`ScreenConfig`** - Display and window settings
- **`ColorScheme`** - Unified color palette for UI consistency
- **`ApplicationSettings`** - Global application settings with getters/setters

**Benefits:**
- Easy to modify constants without touching game logic
- Type hints for better IDE support
- Settings are now objects instead of dictionaries

```python
# OLD (ChatGPT style)
WINDOW_WIDTH = 1400
BLACK = (0, 0, 0)
GLOBAL_SETTINGS = {"show_fps_rounded": True}

# NEW (Professional)
class ScreenConfig:
    WIDTH = 1400

class ColorScheme:
    BLACK = (0, 0, 0)

class ApplicationSettings:
    defaults = {"show_fps_rounded": True}
```

---

### 2. **Core Framework** (Lines 90-170)
Abstract base classes and utilities:

- **`GameMode`** - Abstract base class using ABC
- **`Particle`** - Individual particle with physics
- **`ParticleSystem`** - Batch particle management

**Design Patterns:**
- **Abstract Base Class (ABC)** - Ensures all game modes implement required methods
- **Composition** - ParticleSystem manages Particle objects
- **Encapsulation** - Physics logic isolated in classes

```python
# OLD style
class GameMode:
    def __init__(self, name, difficulty):
        self.particles = []  # Raw list
        self.particles_per_frame = 50

# NEW style
class GameMode(ABC):
    @abstractmethod
    def update(self, dt: float, keys: pygame.key.ScalarKeyType):
        """Forces implementation"""
        pass

class ParticleSystem:
    def __init__(self, max_particles: int = 10000):
        self.particles: List[Particle] = []
        self.max_particles = max_particles
    
    def emit_burst(self, x: float, y: float, count: int, ...):
        """Batch creation"""
```

---

### 3. **Game Modes Section** (Lines 175+)
All game implementations organized in logical groupings:

```
# GPU Stress Tests
├── ParticleStorm       - Fill-rate heavy
├── PolygonRush         - Transform heavy
├── MatrixRain          - Text rendering
├── FractalTree         - Recursive math
├── WaveSimulation      - Physics simulation
├── BouncingBalls       - Collision physics
├── PlasmaEffect        - Fragment shader equivalent
├── Mandelbrot          - Math complexity
├── TunnelEffect        - Perspective transform
├── Starfield           - 3D positioning
├── InteractiveDraw     - User input handling
├── NoiseField          - Procedural generation
└── ParticleAttractor   - Attraction physics

# System Tests
├── CPUTest             - Computation heavy
├── RAMTest             - Memory stress
├── DiskIOTest          - I/O performance
└── SystemMonitor       - Real-time metrics
```

---

### 4. **UI Layer** (Lines 1360+)
Menu system with clear sections:

```
# ─── Main Menu ───
# ─── FPS Tests Menu ───
# ─── System Tests Menu ───
# ─── Settings Menu ───
```

**Each menu includes:**
- Clear docstrings
- Type hints
- Organized variable declarations
- Consistent rendering pattern

---

### 5. **Game Engine** (Lines 2300+)
Core game loop and mode execution:

- **`run_game_mode()`** - Main game loop with crash protection
- Separate FPS calculation logic
- Performance metrics collection
- Crash detection and recovery

---

### 6. **Entry Point** (Lines 2592+)
Application main loop:

```python
# ═══════════════════════════════════════════════════════════════════════════
# APPLICATION ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

# Show welcome screen
if not show_welcome_screen():
    pygame.quit()
    sys.exit()

# Main application loop
while True:
    category = show_main_menu()
    # ... game flow
```

---

## Key Improvements

### 1. **Type Hints Throughout**
```python
# OLD
def update(self, dt, keys):
    pass

# NEW
def update(self, dt: float, keys: pygame.key.ScalarKeyType):
    pass
```

### 2. **Docstring Standards**
```python
def emit_burst(self, x: float, y: float, count: int,
               speed_range: Tuple[float, float],
               color: Tuple[int, int, int], size: int, life: float):
    """Emit multiple particles at once"""
    # Implementation
```

### 3. **Clear Visual Separation**
Using consistent section delimiters:

```
# ═══════════════════════════════════════════════════════════════════════════
# SECTION NAME
# ═══════════════════════════════════════════════════════════════════════════

# ─── Subsection ──────────────────────────────────────────────────────────
```

### 4. **Professional Class Design**
- Use `__slots__` for memory efficiency in Particle class
- Proper initialization with type hints
- Methods return typed results
- Clear separation of concerns

### 5. **Configuration Classes**
Instead of scattered magic numbers:

```python
# OLD - scattered throughout
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
FPS_CAP = 300

# NEW - organized
class ScreenConfig:
    WIDTH = 1400
    HEIGHT = 900
    FPS_CAP = 300
```

---

## Architecture Principles

### Single Responsibility Principle (SRP)
- **GameMode** - Handles game logic only
- **ParticleSystem** - Manages particle collection
- **Particle** - Represents single particle state
- **UI Functions** - Render menus only

### DRY (Don't Repeat Yourself)
- Reusable ParticleSystem for all particle-based modes
- Shared color palette via ColorScheme
- Common settings via ApplicationSettings

### Open/Closed Principle
- GameMode is abstract - extensible without modification
- Add new game modes by extending GameMode class
- Configuration changes don't affect game logic

---

## Code Metrics

| Metric | Value |
|--------|-------|
| Total Lines | 2,624 |
| Classes | 20+ |
| Functions | 25+ |
| Type Hints | ~90% coverage |
| Docstrings | All major functions |
| Comments | Professional annotations |

---

## Migration Path from ChatGPT Style

**Before (ChatGPT Style):**
- ❌ Flat list of functions
- ❌ Magic numbers scattered everywhere
- ❌ No type hints
- ❌ Minimal docstrings
- ❌ Dictionary-based configuration
- ❌ No clear separation of concerns

**After (Professional Architecture):**
- ✅ Clear section hierarchy
- ✅ Centralized configuration
- ✅ Full type hints
- ✅ Comprehensive docstrings
- ✅ Object-oriented design
- ✅ Clear architectural patterns

---

## Future Improvements

1. **Plugin System** - Allow third-party game modes
2. **Settings Persistence** - Save user configuration
3. **Performance Profiling** - Built-in profiling tools
4. **Network Features** - Benchmark sharing
5. **Advanced Analytics** - Performance trend tracking

---

## How to Extend

### Adding a New Game Mode

```python
class MyNewMode(GameMode):
    """
    MyNewMode - Brief description.
    What it tests and why.
    """
    
    def __init__(self):
        super().__init__("My New Mode", 3)  # Difficulty 1-5
        self.particle_system = ParticleSystem(max_particles=10000)
    
    def update(self, dt: float, keys: pygame.key.ScalarKeyType):
        """Update logic"""
        # Your implementation
    
    def draw(self, screen: pygame.Surface):
        """Render to screen"""
        screen.fill(ColorScheme.BLACK)
        self.particle_system.draw(screen)
```

Then register it in `modes_map` dictionary in `run_game_mode()`.

---

**Version:** 2.0
**Refactored:** February 2026
**Architecture Pattern:** Object-Oriented with Abstract Base Classes
