# FPS Tester

Test your computer's gaming performance. See what games you can run.

## What it is

Quick tool to check if your GPU/CPU is fast enough for games. Run tests, get your FPS, see recommendations.

## How to use

### On desktop (Python)

```bash
python fps_tester.py
```

Needs pygame and psutil:
```bash
pip install pygame psutil
```

### In browser

Open `browser-tester.html` in any browser. Everything runs locally, no internet needed.

## Tests

**Graphics tests (13):**
- Particles
- Polygons  
- Matrix rain
- Fractals
- Gravity
- Bouncing balls
- Plasma
- Mandelbrot
- Tunnel
- Starfield
- Draw
- Noise
- Attractor

**System tests (4):**
- CPU
- RAM
- Disk
- Monitor

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