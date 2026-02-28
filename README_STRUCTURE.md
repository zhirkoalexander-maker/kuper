# FPS Tester - Multi-Platform Implementation

## Overview

This is a comprehensive FPS testing and performance analysis tool with implementations in both **Python** and **JavaScript**.

### Files:
- `fps_tester.py` - Desktop version (Python 3 with Pygame)
- `fps_tester.js` - Web version (JavaScript for browsers)

---

## Architecture

### Python Version (`fps_tester.py`)
**Language:** Python 3.9+  
**Framework:** Pygame  
**Resolution:** 1400x900  
**Dependencies:** pygame, psutil (optional)

#### Key Components:
1. **GameMode Base Class** - Template for all test modes
2. **13 FPS Test Modes:**
   - Particle Storm (click-triggered explosions)
   - Polygon Rush (cursor-attracted polygons)
   - Matrix Rain (cursor Y controls speed)
   - Fractal Tree (rotating recursive trees)
   - Wave Simulation (water physics)
   - Bouncing Balls (physics with cursor interaction)
   - Plasma Effect (sine/cosine distortion field)
   - Mandelbrot (fractal zoom)
   - Tunnel Effect (3D visual)
   - Starfield (3D perspective)
   - Interactive Draw (free-form painting)
   - Noise Field (ripple generation)
   - Particle Attractor (particles follow cursor)

3. **4 System Test Modes:**
   - CPU Test (computational load visualization)
   - RAM Test (memory allocation visualization)
   - Disk I/O Test (file operations)
   - System Monitor (real-time CPU/RAM graphs with psutil)

4. **UI Screens:**
   - Welcome Screen (animated intro)
   - Main Menu (3 options with particle animation background)
   - FPS Menu (13 game modes, 2-column layout)
   - System Menu (4 tests)
   - Settings Menu (5 toggle options)
   - Results Screen (stats + AI-generated recommendations)

5. **Features:**
   - Real-time FPS display (rounded + precise 0.1)
   - Performance recommendations based on FPS
   - FPS stability analysis
   - Scrollable recommendations
   - Configurable HUD display

---

### JavaScript Version (`fps_tester.js`)
**Language:** JavaScript (ES6+)  
**Target:** Modern web browsers  
**Canvas API:** Native HTML5 Canvas  
**Resolution:** 1400x900

#### Mirrors Python Structure:
```
JavaScript Class                ↔ Python Class
====================================================
GameMode                        ↔ GameMode (base)
ParticleStorm                   ↔ ParticleStorm
PolygonRush                     ↔ PolygonRush
MatrixRain                      ↔ MatrixRain
InteractiveDraw                 ↔ InteractiveDraw
CPUTest                         ↔ CPUTest
RAMTest                         ↔ RAMTest
```

#### Utility Functions (Python→JavaScript):
- `rgbToCSS()` - Convert RGB array to CSS color
- `drawText()` - Text rendering on canvas
- `drawCenteredText()` - Centered text
- `drawCircle()` - Circle drawing
- `drawRect()` - Rectangle drawing
- `randomInt()` / `randomFloat()` - Random generators
- `randomChoice()` - Array element selection

#### Screen Functions:
- `showWelcomeScreen()` - Async welcome with animations
- `showMainMenu()` - Async main menu with particle background
- `showResults()` - Async results with recommendations

---

## Game Modes Details

### FPS Tests (All Interactive)

**Particle Storm**
- Left-click anywhere to create 80-particle explosion
- Auto-spawning particles fill the screen
- Different colors for visual distinction

**Polygon Rush**
- Rotating polygons (3-8 sides randomly)
- Attracted to cursor position
- Physics-based movement

**Matrix Rain**
- Falling characters and symbols
- Cursor Y position controls falling speed
- Green neon color scheme

**Fractal Tree**
- Recursive binary tree structure
- Rotates toward cursor with smooth interpolation
- Doubles in complexity with difficulty

**Wave Simulation**
- Grid-based water physics
- Waves propagate from center
- Physics calculations drive FPS

**Bouncing Balls**
- Balls bounce with velocity
- Left-click attracts, right-click repels
- Gravity simulation

**Plasma Effect**
- Sine/cosine mathematical formula visualization
- Cursor distortion field
- Color gradient mapping

**Mandelbrot**
- Fractal zoom toward cursor position
- Iteration-based coloring
- Math-intensive computation

**Tunnel Effect**
- 3D tunnel with rainbow gradient
- Rotation based on cursor X position
- Perspective projection

**Starfield**
- 3D star field with depth
- Moves in direction of cursor velocity
- Simulates speed sensation

**Interactive Draw**
- Paint/draw with mouse (up to 2000 points)
- Trailing particles follow cursor
- Multiple colors

**Noise Field**
- Click to create ripple disturbances
- Perlin noise-like field
- Physics-based propagation

**Particle Attractor**
- 300+ particles
- Magnetically follow cursor
- Gravity and air resistance

### System Tests (Educational)

**CPU Test**
- Performs heavy calculations (sqrt, sin, cos)
- Shows load percentage as bar chart
- Color-coded: Green <50%, Yellow 50-80%, Red >80%

**RAM Test**
- Allocates memory blocks progressively
- Shows usage as percentage
- Graphs memory history over time

**Disk I/O Test**
- Performs file read/write operations
- Shows operation count
- Measures I/O performance

**System Monitor**
- Real-time CPU % graph
- Real-time RAM % graph
- Uses psutil if available, otherwise simulates

---

## Performance Recommendations System

### FPS Thresholds:
- **120+ FPS** → EXCELLENT (Green)
  - Can handle 4K, maximum effects
  
- **90-120 FPS** → VERY GOOD (Light Green)
  - 1440p high settings
  
- **60-90 FPS** → GOOD (Yellow)
  - 1080p, medium-high settings
  
- **45-60 FPS** → ACCEPTABLE (Orange)
  - 1080p medium, some effects disabled
  
- **30-45 FPS** → POOR (Dark Orange)
  - 720p low settings
  
- **<30 FPS** → CRITICAL (Red)
  - Minimal settings or hardware upgrade needed

### Stability Analysis:
- Calculates FPS variance (max - min)
- Detects instability patterns
- Suggests causes: overheating, background processes, weak PSU

---

## Architecture for Website (Planned)

### Dual-Screen System:
```
┌─────────────────────────────────────────┐
│           BROWSER TAB                   │
├──────────────────┬──────────────────────┤
│                  │                      │
│   SCREEN 1       │    SCREEN 2          │
│  (Testing Canvas)│ (Statistics Panel)   │
│                  │                      │
│   Game Modes     │  Real-time FPS       │
│   Rendering      │  Recommendations     │
│                  │  CPU/RAM Graphs      │
│                  │  [Restart] Button    │
│                  │                      │
│                  │  ← Always Stable     │
│  ← Can Crash     │                      │
│                  │                      │
└──────────────────┴──────────────────────┘
```

### Communication:
- WebSocket for real-time data sync
- Screen 2 persists if Screen 1 crashes
- Independent restart capability
- Statistics preserved during reload

---

## Current Status

✅ **Complete:**
- 13 interactive FPS test modes
- 4 system monitoring modes
- Full UI with animations
- Recommendations system
- Settings panel
- Results screen with scrollable recommendations

🔄 **In Progress:**
- JavaScript port (structures complete, ready for integration)

📋 **TODO for Website:**
- HTML5 canvas setup
- WebSocket server for dual-screen architecture
- Performance persistence (IndexedDB/localStorage)
- Responsive design for different screen sizes
- Deploy to web server

---

## Usage

### Python Desktop Version:
```bash
python3 fps_tester.py
```

1. See Welcome Screen
2. Navigate Main Menu with Arrow Keys or QWERTY (1/2/3)
3. Select category (FPS or System Tests)
4. Select specific mode
5. Interact with mode (click, move cursor)
6. Press ESC when done
7. View Results and Recommendations
8. Press SPACE to return to menu

### JavaScript Web Version:
(Coming soon - ready for HTML5 integration)

---

## File Statistics

| File | Size | Lines | Language |
|------|------|-------|----------|
| fps_tester.py | 65 KB | 1700+ | Python 3 |
| fps_tester.js | 28 KB | 1087 | JavaScript |

---

## Key Design Patterns

### Python ↔ JavaScript Similarity:
1. **Class-based architecture** - Both use classes for modes
2. **Event handling** - Similar event listener patterns
3. **Render loop** - Frame-based animation in both
4. **Color constants** - RGB arrays in both
5. **Utility functions** - Math helpers consistent across both
6. **State management** - Settings global state
7. **Async screens** - Promise-based flow (JS) mirrors while-loops (Python)

### Consistent APIs:
```python
# Python
class MyMode(GameMode):
    def __init__(self):
        super().__init__("Name", difficulty)
    
    def update(self, dt, keys):
        pass
    
    def draw(self, screen):
        pass
```

```javascript
// JavaScript
class MyMode extends GameMode {
    constructor() {
        super("Name", difficulty);
    }
    
    update(dt, keys, mouse) {
        // ...
    }
    
    draw(ctx) {
        // ...
    }
}
```

---

## Notes for Website Integration

1. **Dual-Screen Architecture Coded:** See comments in `fps_tester.py` lines 11-20
2. **JavaScript Ready:** Full class structure mirrors Python implementation
3. **Next Steps:**
   - Create HTML template with two Canvas elements
   - Integrate JavaScript via `<script>` tags
   - Setup WebSocket connection (optional for dual-screen)
   - Add CSS for responsive layout

---

## Internationalization

- **Python:** Fully translated to English
- **JavaScript:** Built with English strings

Future support for multiple languages via external translation maps.

