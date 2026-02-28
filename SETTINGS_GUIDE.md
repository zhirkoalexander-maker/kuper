# FPS Tester - Settings Guide

## Overview
The application now has a **Settings system** that lets you customize what information is displayed during tests and in results.

## How to Access Settings

### Method 1: From Main Menu
1. Start the application
2. Navigate to **"3. Settings"** (use arrow keys or A/D)
3. Press ENTER to open the settings menu

### Method 2: During a Test
1. While running any test, press **S** to open settings
2. The test will pause while you configure
3. Changes apply immediately when you return

## Available Settings

| Setting | Description |
|---------|-------------|
| **Show FPS Rounded** | Toggle the large rounded FPS display (0, 10, 20, 30...) |
| **Show FPS Real** | Toggle the precise real FPS display (e.g., "Real: 47.3 FPS") |
| **Show Hints** | Toggle the ESC/Settings hint at bottom of screen |
| **Show Mode Stats** | Toggle mode-specific statistics (particles, score, etc.) |
| **Show Results** | Toggle the results summary screen after each test |

## How to Configure

In the Settings menu:
- **Navigation**: Use ↑/↓ arrow keys or W/S to select settings
- **Toggle**: Press SPACE or ENTER to toggle ON/OFF
- **Quick Set**: 
  - Press LEFT or A to turn OFF
  - Press RIGHT or D to turn ON
- **Exit**: Press ESC to return to main menu

### Visual Indicators
- **Green "ON"** = Setting is enabled
- **Red "OFF"** = Setting is disabled
- **Magenta highlight** = Currently selected setting

## Default Configuration

All settings are **ON** by default:
```
Show FPS Rounded: ON
Show FPS Real: ON
Show Hints: ON
Show Mode Stats: ON
Show Results: ON
```

## Examples

### Minimal Display Mode
- Disable: Show Hints, Show Mode Stats
- This shows only FPS data during tests

### Performance Focus Mode
- Enable only: Show FPS Real
- This shows precise FPS numbers only

### Statistics Mode
- Enable only: Show Mode Stats, Show Results
- This focuses on detailed statistics

## Tips
- Settings are **saved in memory** during your session
- They reset when you restart the application
- Different test modes may display different stats (e.g., particles for Particle Storm)
- You can change settings at any time without restarting tests

## Keyboard Reference

| Key | Action |
|-----|--------|
| ↑/↓ | Navigate settings |
| W/S | Navigate settings (alternate) |
| SPACE | Toggle selected setting |
| ENTER | Toggle selected setting |
| LEFT / A | Turn setting OFF |
| RIGHT / D | Turn setting ON |
| ESC | Exit settings (back to menu) |
| S | Open settings from during a test |
