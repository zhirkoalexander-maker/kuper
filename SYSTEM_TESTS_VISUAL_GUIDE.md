# System Tests - Visual Guide

## CPU Test Screen Layout

```
┌─────────────────────────────────────────────────────┐
│                  CPU Load Monitor                   │
│                                                     │
│  Current CPU Usage                                  │
│  45.3%                                              │
│  Moderate load - System is working                  │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ 100%                              ╱╲    ╱╲ │  │
│  │ 75%       ╱╲    ╱╲               ╱  ╲  ╱  │  │
│  │ 50%      ╱  ╲  ╱  ╲  ╱╲         ╱    ╲╱   │  │
│  │ 25%  ╱╲ ╱    ╲╱    ╲╱  ╲  ╱╲   ╱           │  │
│  │ 0%   ──────────────────────────────────────   │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  💡 Tips to reduce CPU load:                       │
│  • Close unnecessary applications                  │
│  • Disable browser extensions                      │
│  • Check Task Manager for heavy processes          │
│                                                     │
│  Press SPACE to return | ↑ ↓ to scroll            │
└─────────────────────────────────────────────────────┘
```

## RAM Test Screen Layout

```
┌─────────────────────────────────────────────────────┐
│                Memory Monitor                        │
│                                                     │
│  Process Memory Usage                               │
│  156.2 MB                                           │
│  ⚠ HIGH - Consider closing some applications        │
│                                                     │
│  ┌─────────────────────────────────────────────┐  │
│  │ 100%                                    ░░░│  │
│  │ 75%                      ░░░             ░░░│  │
│  │ 50%  ░░░  ░░░  ░░░      ░░░  ░░░  ░░░  ░░░│  │
│  │ 25%  ░░░  ░░░  ░░░  ░░░ ░░░  ░░░  ░░░  ░░░│  │
│  │ 0%   ──────────────────────────────────────   │  │
│  └─────────────────────────────────────────────┘  │
│                                                     │
│  💡 How to free up memory:                         │
│  • Close unused browser tabs                       │
│  • Restart memory-heavy applications               │
│  • Check for memory leaks in Task Manager          │
│                                                     │
│  Press SPACE to return | ↑ ↓ to scroll            │
└─────────────────────────────────────────────────────┘
```

## Disk I/O Test Screen Layout

```
┌─────────────────────────────────────────────────────┐
│                Disk I/O Monitor                      │
│                                                     │
│  Writes: 5                                          │
│  Reads: 4 MB                                        │
│  Speed: 3.2 ops/sec                                │
│  ✓ Disk I/O normal                                 │
│                                                     │
│  💡 Tips for better disk performance:              │
│  • Disable unnecessary background processes        │
│  • Run disk cleanup regularly                       │
│  • Consider upgrading to SSD if using HDD           │
│  • Check for malware with antivirus                │
│                                                     │
│                                                     │
│  Press SPACE to return | ↑ ↓ to scroll            │
└─────────────────────────────────────────────────────┘
```

## System Monitor Screen Layout

```
┌─────────────────────────────────────────────────────┐
│           System Health Monitor                      │
│                                                     │
│  CPU: 42.5%                RAM: 58.3%              │
│  ✓ Good - Running smoothly                         │
│                                                     │
│  ┌──────────────────────┬──────────────────────┐   │
│  │ CPU Usage            │ RAM Usage            │   │
│  │ 100%                 │ 100%                 │   │
│  │ 75%  ╱╲              │ 75%  ╱╲              │   │
│  │ 50% ╱  ╲ ╱╲ ╱╲     │ 50% ╱  ╲ ╱╲ ╱╲     │   │
│  │ 25%     ╱  ╲╱  ╲    │ 25%     ╱  ╲╱  ╲    │   │
│  │ 0%  ─────────────    │ 0%  ─────────────    │   │
│  │ CPU Usage            │ RAM Usage            │   │
│  └──────────────────────┴──────────────────────┘   │
│                                                     │
│  💡 System optimization: Balance workload,         │
│  close unnecessary apps, keep drivers updated      │
│                                                     │
│  Press SPACE to return | ↑ ↓ to scroll            │
└─────────────────────────────────────────────────────┘
```

## Results Screen - System Test Example

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│              Test Complete!                        │
│                  RAM Test                          │
│         System Analysis Complete                   │
│                                                     │
│  📊 Average RAM usage: 68.4%                       │
│  📊 Peak RAM usage: 82.1%                          │
│                                                     │
│  ⚠ RAM usage is getting high                       │
│  ✓ Action: Monitor for memory leaks in Task Mgr    │
│  • Close some background applications if needed    │
│                                                     │
│  Recommendations:                                   │
│  ✓ Action: Clear temporary files and cache        │
│  ! Recommendation: Consider upgrading RAM          │
│  ✓ General: Keep Windows and drivers updated       │
│  ✓ General: Run antivirus scans regularly          │
│  ✓ General: Clean temporary files monthly          │
│                                                     │
│  Press SPACE to return | ↑ ↓ to scroll            │
└─────────────────────────────────────────────────────┘
```

## Color Coding Reference

### Status Colors
- **Green (0, 255, 0)**: Excellent / Normal / Good
- **Yellow (255, 255, 0)**: Caution / Moderate
- **Orange (255, 165, 0)**: Warning / High
- **Red (255, 0, 0)**: Critical / Very High
- **Cyan (0, 255, 255)**: Information

### Recommendation Prefixes
- **✓**: Positive / Recommended action
- **✗**: Critical / Must fix
- **!**: Important / Warning
- **⚠**: Caution / Be aware
- **•**: Optional / Nice to have
- **📊**: Information / Data point
- **💡**: Tip / Suggestion

## Key Differences from FPS Tests

| Feature | FPS Tests | System Tests |
|---------|-----------|--------------|
| Displays | FPS metrics (Avg/Min/Max) | System metrics (CPU%/RAM%/Disk I/O) |
| Status | Gaming performance tier | System health status |
| Focus | Gaming capability | System optimization |
| Recommendations | Gaming settings | Hardware optimization |
| Graph Type | FPS over time | Usage percentage over time |
| Results Title | Test Complete! | System Analysis Complete |

## Interpretation Guide

### CPU Test Ranges
- **0-30%**: Idle - no heavy workload
- **30-60%**: Normal - system handling tasks well
- **60-80%**: Moderate - getting busy but still okay
- **80-95%**: High - nearly maxed out
- **95-100%**: Critical - at maximum capacity

### RAM Test Ranges
- **0-50%**: Excellent - plenty of available memory
- **50-70%**: Normal - good available capacity
- **70-85%**: High - limited capacity
- **85-90%**: Critical - almost out of memory
- **90-100%**: Dangerous - system will become very slow

### Disk I/O Ranges
- **0-2 ops/sec**: Very slow/idle
- **2-5 ops/sec**: Normal
- **5-10 ops/sec**: Busy
- **10+ ops/sec**: Very high activity
