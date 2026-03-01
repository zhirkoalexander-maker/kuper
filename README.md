# 🎮 FPS TESTER v2.0

Professional GPU/CPU Performance Analysis & Stress Testing Tool

## 📊 Features

### 🎨 13 GPU Tests
- **Particle Storm** - Explosions and particle effects
- **Polygon Rush** - Rotating polygons and transforms
- **Matrix Rain** - Falling characters effect
- **Fractal Tree** - Recursive fractal generation
- **Gravity Fields** - Particles in gravity simulation
- **Bouncing Balls** - Physics simulation with collisions
- **Plasma Effect** - Procedural plasma generation
- **Mandelbrot Set** - Complex fractal calculation
- **Tunnel Effect** - 3D tunnel rendering
- **Starfield** - 3D space simulation
- **Interactive Draw** - Draw with your mouse
- **Noise Field** - Perlin noise visualization
- **Particle Attractor** - Particles follow cursor

### ⚡ 4 System Tests
- **CPU Test** - Processor stress testing
- **RAM Test** - Memory performance analysis
- **Disk I/O Test** - Storage read/write speed
- **System Monitor** - Real-time system statistics

### 📈 Key Features
- ✓ Real-time FPS display with HUD panel
- ✓ System monitoring (CPU, RAM, GPU usage)
- ✓ 5 difficulty levels (EASY to MAXIMUM)
- ✓ Game recommendations based on test results
- ✓ Silent crash protection
- ✓ Detailed performance analysis
- ✓ Cross-platform support (Windows, macOS, Linux)

### 💻 System Tests
- **CPU Test** - Processor load analysis
- **RAM Test** - Memory usage monitoring
- **Disk I/O Test** - Disk performance analysis
- **System Monitor** - Real-time system health

### Difficulty Levels
Each FPS test supports 5 difficulty levels:
- **1 - EASY**: Light load
- **2 - MEDIUM**: Balanced (default)
- **3 - HARD**: Heavy stress
- **4 - EXTREME**: Maximum load
- **5 - INSANE**: Break-it mode

## Controls

### Main Menu
- **1-E**: Select FPS test
- **C/M/D/S**: Select system test
- **ESC**: Exit

### During Test
- **ESC**: Stop test
- **S**: Settings
- **C**: Continue/Resume

## Installation

### Python
```bash
pip install pygame psutil
python fps_tester.py
```

### JavaScript (Web)
Open `index.html` in a modern browser.

## System Requirements

### Python Version
- Python 3.8+
- pygame 2.0+
- psutil (optional, for system monitoring)

### Minimum Hardware
- 2GB RAM
- 512MB VRAM (dedicated GPU recommended)
- Multi-core processor

## Architecture

The application is organized into clear layers:

1. **Configuration Layer** - Display and color settings
2. **Framework Layer** - Base classes and utilities
3. **Game Modes** - Individual stress tests
4. **UI Layer** - Menus and settings
5. **Game Engine** - Main loop and rendering
6. **Entry Point** - Application startup

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed documentation.

## Performance Metrics

The tool measures:
- **FPS (Frames Per Second)** - Real-time performance
- **Stability Score** - Consistency measurement (0-100%)
- **Peak FPS** - Maximum achieved
- **Minimum FPS** - Lowest point
- **CPU/RAM Usage** - System resource utilization
- **Bottleneck Detection** - Identify limiting component

## Recent Changes (v2.1)

- ✨ Added difficulty levels for FPS tests (EASY to INSANE)
- ✨ Implemented PerformanceMonitor class
- ✨ Added FrameRateLimiter for smooth timing
- ✨ Fixed game recommendations logic
- 🔧 Fixed keyboard shortcuts
- 🔧 Fixed menu navigation flow
- 📚 Comprehensive documentation

## Files

### Core
- `fps_tester.py` - Main Python application
- `fps_tester.js` - JavaScript version
- `index.html` - Web interface

### Documentation
- `ARCHITECTURE.md` - Code architecture
- `REFACTORING_REPORT.md` - Refactoring details
- `IMPROVEMENTS_v2.1.md` - v2.1 improvements

## Repository

[zhirkoalexander-maker/kuper](https://github.com/zhirkoalexander-maker/kuper)

---

**FPS Tester v2.1** - Professional Grade Performance Analysis