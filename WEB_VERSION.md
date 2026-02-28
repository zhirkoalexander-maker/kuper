# 🎮 FPS Tester - Web Version

Modern web-based FPS and performance testing tool with beautiful UI and advanced analytics.

## 🚀 Features

### ✨ Interactive Tests
- **🌪️ Particle Storm** - Intensive particle rendering
- **🔷 Polygon Rush** - Complex polygon transformations  
- **🌧️ Matrix Rain** - Text rendering performance
- **🌳 Fractal Tree** - Recursive graphics
- **🎨 Mandelbrot** - Mathematical computation
- **🌌 Tunnel Effect** - 3D graphics simulation

### 📊 Advanced Analytics
- **Real-time FPS Monitoring** - Live FPS counter during tests
- **Performance Score (1-10)** - Overall system rating
- **Bottleneck Detection** - Identifies limiting components
- **Interactive Charts** - FPS trends and performance metrics
- **Detailed Recommendations** - Actionable insights

### 💾 Smart Features
- **Test History** - Track performance over time
- **Local Storage** - Save up to 50 test results
- **Responsive Design** - Works on desktop and mobile
- **Dark Theme** - Eye-friendly modern interface
- **Real-time Graphs** - Chart.js integration

## 🎯 How to Use

### Starting Tests
1. Click "Tests" in navigation or "Start Testing" button
2. Select a test from the menu
3. Test runs automatically for 30 seconds
4. View detailed results with recommendations

### Understanding Results

**Performance Score:**
- 🟢 9-10: Excellent - All games max settings
- 🟡 7-8: Very Good - High settings 1440p
- 🟠 5-6: Good - Medium settings 1080p
- 🔴 3-4: Fair - Lower settings needed
- 🔴 1-2: Critical - System upgrade recommended

**Bottleneck Types:**
- **GPU Capacity** - Graphics card is limiting (FPS >120)
- **CPU/System Weak** - Processor needs upgrade
- **Moderate** - Balanced performance
- **CPU-GPU Balance** - Well-matched system

### Viewing History
1. Click "History" in navigation
2. See all previous tests with dates and scores
3. Delete individual tests or clear all history
4. History saved in browser localStorage

## 📁 File Structure

```
fps tester/
├── index_new.html      # Main HTML interface
├── app.js              # Test logic and rendering
├── fps_tester.py       # Original Python version
└── WEB_VERSION.md      # This file
```

## 🌐 Running the Web Version

### Option 1: Direct File
```bash
# Open in browser
open index_new.html
# or
firefox index_new.html
```

### Option 2: Local Server (Recommended)
```bash
# Python 3
python3 -m http.server 8000

# Or Node.js
npx http-server

# Then visit: http://localhost:8000
```

### Option 3: With Python Backend
```bash
# Run Flask server for API metrics
python3 backend_server.py

# Then open in browser
open http://localhost:5000
```

## 🎨 Design Features

### Modern UI
- Neon cyan/magenta color scheme
- Smooth animations and transitions
- Glassmorphism effects
- Responsive grid layouts

### Performance Optimized
- Canvas-based rendering
- RequestAnimationFrame for smooth 60 FPS
- Efficient memory management
- Lightweight JavaScript (no heavy frameworks)

### Accessibility
- High contrast text
- Clear status indicators
- Mobile-friendly layout
- Keyboard navigation support

## 📊 Test Details

### Test Duration
- Each test runs for 30 seconds
- FPS measured every second
- Can stop early with "Stop Test" button

### Performance Scoring Algorithm
```javascript
Score = 10 points base
- FPS < 30: -4 points
- FPS 30-60: -2 points
- FPS 60-120: -0.5 points
- FPS >= 120: 0 points

Final: clamp(1-10)
```

### Recommendations Logic
- FPS >= 120: "Excellent - All games max"
- FPS 90-120: "Very Good - High 1440p"
- FPS 60-90: "Good - Medium 1080p"
- FPS 45-60: "Acceptable - Lower settings"
- FPS 30-45: "Poor - Minimum settings"
- FPS < 30: "Critical - Upgrade needed"

## 🔧 Technical Stack

- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Graphics**: Canvas API + Chart.js
- **Storage**: localStorage API
- **Responsive**: CSS Grid + Flexbox
- **Animation**: RequestAnimationFrame

## 💡 Tips for Best Results

1. **Close Background Apps** - Minimize other applications
2. **Full Screen** - Use full window for accurate results
3. **Consistent Testing** - Run same test multiple times for baseline
4. **Compare Over Time** - Check history to track improvements
5. **Use Same Settings** - Run tests in similar conditions

## 🐛 Troubleshooting

### Low FPS in Tests
- Close browser tabs and background applications
- Check if system is running other heavy processes
- Try in Chrome/Firefox for better performance
- Check browser hardware acceleration settings

### Charts Not Displaying
- Refresh the page
- Check browser console for errors
- Ensure JavaScript is enabled
- Try different browser

### History Not Saving
- Check if localStorage is enabled
- Verify browser allows local storage
- Check available disk space
- Disable private/incognito mode

## 📈 Improvements Over Desktop Version

✅ **Web Advantages:**
- No installation needed
- Access from any browser
- Automatic updates
- Cross-platform
- Responsive design
- Real-time analytics

## 🔮 Future Features

- [ ] Remote backend API for real system metrics
- [ ] Comparison with other users (anonymized)
- [ ] Custom test parameters
- [ ] Export results as PDF
- [ ] Dark/Light theme toggle
- [ ] Mobile app version
- [ ] Multiplayer benchmarks

## 📝 Notes

- Web browsers cannot access real CPU/RAM metrics (security restriction)
- FPS test is simulated based on rendering performance
- For real system metrics, use Python desktop version
- Results are estimated based on frame rendering time

## 🌟 Version Information

- **Web Version**: 2.0 (Feb 2026)
- **Base on Python**: fps_tester.py (2244 lines)
- **Technologies**: HTML5, Canvas, Chart.js
- **Browser Support**: Chrome, Firefox, Safari, Edge

---

**Made with ❤️ for gamers and performance enthusiasts**
