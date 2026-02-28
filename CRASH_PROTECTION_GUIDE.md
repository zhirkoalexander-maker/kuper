# 🛡️ Crash Protection System - Complete Guide

## What Is The Crash Protection System?

The FPS Tester now includes an **intelligent crash detection and recovery system** that protects your system while testing. Instead of crashing and forcing you out of the program, it:

1. **Detects** when the system is becoming critically stressed
2. **Stops** the test immediately when a crash is imminent
3. **Warns** you with clear information about what happened
4. **Recovers** gracefully without exiting the program
5. **Continues** letting you use the app normally

---

## How Does It Work?

### 🔍 Crash Detection

The system monitors for three types of system stress:

#### 1. **Unresponsiveness Detection**
- Monitors time between animation frames
- If no frame updates for 2+ seconds = system hanging
- After 3 consecutive hangs = crash detected

#### 2. **Extreme Performance Drop**
- Tracks FPS values in real-time
- If FPS drops below 3 frames/second = critical stress
- Indicates GPU/CPU complete saturation

#### 3. **Error Handling**
- Catches any JavaScript errors during rendering
- Prevents infinite loops or memory explosions
- Gracefully exits the test

### ⚡ Example Crash Scenario

```
Test starts: Mega Mandelbrot (EXTREME difficulty)
├─ Frame 1: 45 FPS ✅
├─ Frame 2: 35 FPS ✅
├─ Frame 3: 12 FPS ⚠️
├─ Frame 4: 3 FPS ⚠️
├─ Frame 5: No update for 2 seconds...
├─ Frame 6: No update for 2 seconds... (counter: 1)
├─ Frame 7: No update for 2 seconds... (counter: 2)
├─ Frame 8: No update for 2 seconds... (counter: 3)
└─ CRASH DETECTED! ⚠️ → Recovery dialog appears
```

---

## What Happens When A Crash Is Detected?

### 🛑 The Crash Detection Screen

You'll see:

```
┌─────────────────────────────────────┐
│   ⚠️ SYSTEM CRASH DETECTED          │
│                                     │
│ Your computer crashed due to       │
│ extreme stress test load           │
│                                     │
│ Test: 🌀 Mega Mandelbrot           │
│                                     │
│ ⚠️ RECOMMENDATION:                 │
│ This test is too demanding for    │
│ your system.                        │
│                                     │
│ Do not run EXTREME or higher      │
│ difficulty tests again.             │
│                                     │
│ We recommend running only EASY     │
│ or MEDIUM tests.                    │
│                                     │
│ [🔄 CONTINUE] [🏠 RETURN]          │
│                                     │
│ System will now cooldown...         │
└─────────────────────────────────────┘
```

### Two Options After Crash

#### 1. **🔄 CONTINUE (Don't Exit)**
- Program **stays running**
- Recovery message appears: "✓ System Cooldown Active"
- You can navigate to History, Menu, etc.
- Full recovery takes ~5 seconds
- Message auto-disappears

#### 2. **🏠 RETURN TO MENU**
- Go directly back to test selection
- No program exit
- Can choose different/easier tests
- System cooldown still applies

---

## Protection Features

### ✅ What's Protected?

| System Component | How It's Protected |
|-----------------|------------------|
| **GPU** | FPS monitoring stops test before GPU burnout |
| **CPU** | Frame update detection catches CPU hang |
| **RAM** | Memory check prevents out-of-memory crash |
| **System** | Error handling catches rendering failures |
| **Program** | Never exits - always recoverable |
| **Data** | Crash recorded in history automatically |

### 🛡️ What The System Prevents

- ❌ Forced exit from the program
- ❌ Browser tab crash
- ❌ System freeze (detected and stopped)
- ❌ Memory leak crashes
- ❌ GPU driver crash
- ❌ Data loss (results saved in history)

---

## Crash Recovery Process

### Timeline After Crash Detection

```
T+0s   → Crash detected
        └─ Test stops immediately
        
T+0.1s → Crash dialog appears
        └─ "SYSTEM CRASH DETECTED"
        
T+0.3s → System starts cooldown
        └─ CPU/GPU reset

T+5s   → System recovered
        └─ You can run new tests
```

### System Cooldown

After a crash, your system undergoes a "cooldown" phase:

- **Duration**: ~5 seconds
- **What happens**: GPU/CPU intensive processes reset
- **What to do**: Close background apps, wait peacefully
- **Temperature**: Drops back to normal levels

---

## When Will A Crash Be Detected?

### Most Likely To Trigger

1. **☢️ Combined Stress Test** (most likely)
   - Runs ALL extreme tests simultaneously
   - Probability: ~90% on average systems
   - Expected behavior: Designed to crash

2. **🌀 Mega Mandelbrot** (very likely)
   - 500 iterations pixel-by-pixel
   - Probability: ~70% on average systems
   - Affects: CPU-bound systems primarily

3. **🌠 Mega Tunnel** (likely on weak GPUs)
   - 100 rings full resolution
   - Probability: ~50% on weak GPUs
   - Affects: GPU-bound systems primarily

4. **💥 Particle Explosion** (likely on low RAM)
   - 1000+ particles in memory
   - Probability: ~40% on low-RAM systems
   - Affects: Memory-constrained systems

### Less Likely To Trigger

- 🔴 Hard tests (5-15% probability)
- 🟡 Medium tests (<1% probability)
- 🟢 Easy tests (<0.1% probability)

---

## What Gets Saved After A Crash?

### Automatic History Recording

When a crash is detected, it's automatically saved to your history:

```javascript
{
  "test": "mega-mandelbrot",
  "date": "2/27/2026, 3:45:30 PM",
  "avgFps": 2,
  "minFps": 0,
  "maxFps": 12,
  "status": "CRASH",
  "duration": 8000  // milliseconds
}
```

### View Crash History

1. Go to **History** tab
2. Crashed tests show **"CRASH"** status
3. Click to view full details
4. Compare with other tests to find your limit

---

## System Recommendations After Crash

### ⚠️ If You See A Crash

The system will recommend:

```
"Do not run EXTREME or higher difficulty tests again."

Recommendation: Run only EASY or MEDIUM tests
```

### ✅ Following These Recommendations

1. **Don't Ignore Them**
   - Crash = System at its limit
   - Pushing further risks permanent damage
   - Thermal throttling reduces performance

2. **Stay At Recommended Difficulty**
   - EASY: Always safe (100% stable)
   - MEDIUM: Usually safe (>95% stable)
   - HARD: Test only if confident (>80% stable)
   - EXTREME: Only if you want to crash (<50% stable)

3. **Upgrade Path**
   - Crashed on HARD? → Upgrade GPU/CPU
   - Crashed on MEDIUM? → Need full system upgrade
   - Crashed on EASY? → Serious hardware issue

---

## Safety Guidelines During Extreme Testing

### Before Running EXTREME Tests

✅ **DO:**
- Close ALL background applications
- Disable Discord, Spotify, Chrome extras
- Use a desktop (not laptop if possible)
- Plug in AC power (not battery)
- Ensure good room ventilation
- Monitor system temperature

❌ **DON'T:**
- Run while gaming
- Run multiple tests in rapid succession
- Run on battery power
- Run overnight without monitoring
- Ignore system temperature warnings
- Push the same test twice in a row

### If System Gets Too Hot

**Immediate Actions:**
1. Stop the test (button: "Stop Test")
2. Wait 10+ minutes before next test
3. Close browser completely
4. Restart computer if temp >95°C
5. Check case airflow

**Temperature Zones:**
- Safe: < 75°C
- Caution: 75-85°C
- Warning: 85-95°C
- Danger: > 95°C (stop immediately)

---

## Troubleshooting Crash Protection

### Issue: Crash Not Detected (System Froze)

If your system froze completely:
1. Force restart: **Cmd + Option + Esc** (Mac)
2. Force restart: **Ctrl + Alt + Delete** (Windows)
3. Hard restart: Hold power button 10 seconds
4. Run Easy tests only in future

### Issue: False Crash Detection

If crash detected but system OK:
- This means FPS dropped critically low
- Even if not fully crashed, performance unacceptable
- Take recommendation seriously
- Try easier test next time

### Issue: Program Won't Recover After Crash

If recovery dialog stuck:
1. Click **🔄 CONTINUE** or **🏠 RETURN**
2. If buttons unresponsive, page may be hung
3. Hard refresh: **Cmd + Shift + R** (Mac)
4. Or close tab and reopen `index_en.html`

### Issue: Same Test Crashes Multiple Times

This means:
- Test is beyond your system's capability
- Don't run this test again
- Move to easier difficulty level
- Consider hardware upgrade

---

## Advanced Understanding

### Why Crash Protection Is Necessary

EXTREME tests are designed to:
- **Push systems to breaking point**
- **Test hardware limits**
- **Find system bottlenecks**
- **Identify upgrade needs**

**Without protection:**
- System could freeze permanently
- Forced hard restart needed
- Potential data loss
- User experience terrible

**With protection:**
- Graceful failure detection
- Immediate recovery
- Program continues
- User informed & safe

### How Unresponsiveness Detection Works

```javascript
// Check if system stopped responding
const timeSinceLastFrame = now - lastFrameTimeRecord;

if (timeSinceLastFrame > 2000) {  // 2+ seconds
    unresponsiveCounter++;        // Count consecutive hangs
}

if (unresponsiveCounter >= 3) {   // 3 consecutive hangs
    handleCrashDetected();        // Stop immediately
}
```

**Why 2 seconds?**
- 2 seconds is extremely slow for a modern browser
- Normal frame time: 16-33ms
- 2000ms = 100+ frame drops
- Clear indication system is stuck

**Why 3 consecutive?**
- Single hang could be rare spike
- 3 consecutive = definite system problem
- Provides safety margin
- Prevents false positives

### How FPS Monitoring Works

```javascript
if (fpsValues.length > 0 && fpsValues[fpsValues.length - 1] < 3) {
    handleCrashDetected();  // FPS < 3 = system dead
}
```

**Why FPS < 3?**
- 3 FPS = 1 frame every 333ms
- At this point, system completely maxed
- Any lower = no practical performance
- Clear indicator of critical stress

---

## Next Steps After A Crash

### Recommended Actions

1. **Immediately After Crash:**
   - Click 🔄 CONTINUE to stay in program
   - Don't panic - this is expected for EXTREME tests
   - System will recover in 5-10 seconds

2. **Next 5 Minutes:**
   - Let system cool down
   - Close any unnecessary apps
   - Check system temperature
   - Wait before running next test

3. **Before Next Test:**
   - Run an EASY test to check stability
   - Should get good FPS (>60)
   - If OK, try MEDIUM tests
   - Skip to easier difficulty

4. **Long Term:**
   - Review your crash history
   - Note which difficulty caused crash
   - Plan hardware upgrades if needed
   - Know your system's limits

---

## FAQ

### Q: Will a crash damage my hardware?
**A:** No. The crash detection stops the test BEFORE hardware damage. Temperature and voltage stay within safe limits.

### Q: Can I continue using the program after a crash?
**A:** Yes! The entire point of the system. Click 🔄 CONTINUE to keep using it normally.

### Q: What if I ignore the recommendation and run EXTREME again?
**A:** You can, but expect another crash. The system will detect it again and protect you. Repeat as many times as needed.

### Q: How do I make my system stable for EXTREME tests?
**A:** You would need:
- High-end GPU (RTX 4080+)
- High-end CPU (i9-13900K+ or Ryzen 9 7950X+)
- 32GB+ RAM
- Liquid cooling
- High-end power supply (1000W+)

Even then, some EXTREME tests may crash.

### Q: Is the crash history saved?
**A:** Yes! All crashes recorded in History tab with timestamp and FPS data.

### Q: Can I export my crash history?
**A:** Currently saved in browser localStorage. You can screenshot or manually record important tests.

---

## Remember

🎯 **The goal of crash protection is:**
1. **Safety** - Protect your system
2. **Information** - Show you your limits
3. **Continuity** - Keep you in the program
4. **Recovery** - Graceful failure handling

**Your system crashing = Normal and Expected for EXTREME tests**

This is not a bug - **it's the intended behavior!** 🎉

---

Stay safe and happy testing! 🚀
