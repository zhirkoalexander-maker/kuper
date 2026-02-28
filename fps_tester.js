/**
 * FPS TESTER - JavaScript Version
 * Performance Analysis Tool for Web Browsers
 * 
 * Website Architecture:
 * - Canvas-based rendering (similar to Pygame)
 * - Dual-screen support (Test canvas + Statistics panel)
 * - WebSocket-ready for future server integration
 * 
 * Version: 2.1 - Enhanced with utility classes and monitoring
 */

// ==========================
// CONSTANTS AND CONFIGURATION
// ==========================

const WINDOW_WIDTH = 1400;
const WINDOW_HEIGHT = 900;
const FPS_CAP = 300;
const TARGET_FPS = 60;

// Colors (RGB)
const COLORS = {
  BLACK: [0, 0, 0],
  WHITE: [255, 255, 255],
  GREEN: [0, 255, 0],
  RED: [255, 0, 0],
  YELLOW: [255, 255, 0],
  BLUE: [0, 100, 255],
  CYAN: [0, 255, 255],
  MAGENTA: [255, 0, 255],
  ORANGE: [255, 165, 0],
  PURPLE: [128, 0, 128],
  DARK_GRAY: [30, 30, 30],
  LIGHT_GRAY: [200, 200, 200],
};

// Global settings with more options
const GLOBAL_SETTINGS = {
  show_fps_rounded: true,
  show_fps_real: true,
  show_hints: true,
  show_mode_stats: true,
  show_results: true,
  show_stability: true,
  show_peaks: true,
};

// ==========================
// PERFORMANCE MONITORING
// ==========================

/**
 * Real-time performance monitor with history tracking
 */
class PerformanceMonitor {
  constructor(historySize = 300) {
    this.history = [];
    this.maxHistory = historySize;
    this.peakFps = 0;
    this.lowestFps = Infinity;
    this.startTime = Date.now();
  }

  record(fps) {
    this.history.push(fps);
    if (this.history.length > this.maxHistory) {
      this.history.shift();
    }
    this.peakFps = Math.max(this.peakFps, fps);
    this.lowestFps = Math.min(this.lowestFps, fps);
  }

  getAverage() {
    if (this.history.length === 0) return 0;
    return this.history.reduce((a, b) => a + b, 0) / this.history.length;
  }

  getStability() {
    // Returns stability score 0-100 (higher = more stable)
    if (this.history.length < 2) return 100;
    
    const avg = this.getAverage();
    if (avg === 0) return 0;

    const variance = this.history.reduce((sum, fps) => {
      return sum + Math.pow(fps - avg, 2);
    }, 0) / this.history.length;

    const stability = Math.max(0, 100 - (Math.sqrt(variance) / avg * 50));
    return Math.min(100, stability);
  }

  getStatistics() {
    return {
      average: this.getAverage(),
      min: this.lowestFps === Infinity ? 0 : this.lowestFps,
      max: this.peakFps,
      stability: this.getStability(),
    };
  }

  reset() {
    this.history = [];
    this.peakFps = 0;
    this.lowestFps = Infinity;
    this.startTime = Date.now();
  }
}

/**
 * Smooth frame rate limiter with adaptive timing
 */
class FrameRateLimiter {
  constructor(targetFps) {
    this.targetFps = targetFps;
    this.frameTime = 1000 / targetFps; // in milliseconds
    this.lastTime = Date.now();
  }

  getFrameTime() {
    const now = Date.now();
    const dt = (now - this.lastTime) / 1000; // convert to seconds
    this.lastTime = now;
    
    // Clamp dt to reasonable values
    return Math.min(dt, this.frameTime * 2 / 1000);
  }

  getTargetFrameTime() {
    return this.frameTime / 1000; // return in seconds
  }
}

// ==========================
// UTILITY FUNCTIONS
// ==========================

/**
 * Convert RGB array to CSS color string
 */
function rgbToCSS(rgb) {
  return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
}

/**
 * Convert RGB array to Hex color string
 */
function rgbToHex(rgb) {
  return `#${((1 << 24) + (rgb[0] << 16) + (rgb[1] << 8) + rgb[2]).toString(16).slice(1)}`;
}

/**
 * Draw text on canvas
 */
function drawText(ctx, text, x, y, color, fontSize = 32, fontFamily = 'Arial') {
  ctx.font = `${fontSize}px ${fontFamily}`;
  ctx.fillStyle = rgbToCSS(color);
  ctx.fillText(text, x, y);
}

/**
 * Draw centered text
 */
function drawCenteredText(ctx, text, y, color, fontSize = 32, canvasWidth = WINDOW_WIDTH) {
  ctx.font = `${fontSize}px Arial`;
  ctx.fillStyle = rgbToCSS(color);
  const metrics = ctx.measureText(text);
  const x = (canvasWidth - metrics.width) / 2;
  ctx.fillText(text, x, y);
}

/**
 * Draw circle
 */
function drawCircle(ctx, x, y, radius, color) {
  ctx.fillStyle = rgbToCSS(color);
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fill();
}

/**
 * Draw rectangle
 */
function drawRect(ctx, x, y, width, height, color, filled = true) {
  ctx.fillStyle = rgbToCSS(color);
  if (filled) {
    ctx.fillRect(x, y, width, height);
  } else {
    ctx.strokeStyle = rgbToCSS(color);
    ctx.strokeRect(x, y, width, height);
  }
}

/**
 * Get random integer between min and max
 */
function randomInt(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Get random float between min and max
 */
function randomFloat(min, max) {
  return Math.random() * (max - min) + min;
}

/**
 * Choose random element from array
 */
function randomChoice(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

// ==========================
// BASE GAME MODE CLASS
// ==========================

class GameMode {
  constructor(name, difficulty = 3) {
    this.name = name;
    this.difficulty = difficulty;
    this.fps_values = [];
    this.fps_values_maxlen = 300;
    this.fps_display_timer = 0;
    this.current_fps_display = 0;
  }

  update(dt, keys, mouse) {
    // Override in subclasses
  }

  draw(ctx) {
    // Override in subclasses
  }

  getFPSDisplay(raw_fps, dt) {
    this.fps_values.push(raw_fps);
    if (this.fps_values.length > this.fps_values_maxlen) {
      this.fps_values.shift();
    }

    this.fps_display_timer += dt;
    if (this.fps_display_timer >= 0.5) {
      this.current_fps_display = Math.round(raw_fps / 10) * 10;
      this.fps_display_timer = 0;
    }

    return this.current_fps_display;
  }

  getStats() {
    if (this.fps_values.length === 0) {
      return 0, 0, 0;
    }

    const sum = this.fps_values.reduce((a, b) => a + b, 0);
    const avg = sum / this.fps_values.length;
    const min = Math.min(...this.fps_values);
    const max = Math.max(...this.fps_values);

    return avg, min, max;
  }
}

// ==========================
// GAME MODES
// ==========================

/**
 * Particle Storm - Click to create particle explosions
 */
class ParticleStorm extends GameMode {
  constructor() {
    super('Particle Storm', 4);
    this.particles = [];
    this.particles_per_frame = 50 + this.difficulty * 30;
  }

  update(dt, keys, mouse) {
    // Auto-generate particles
    for (let i = 0; i < this.particles_per_frame; i++) {
      this.particles.push({
        x: Math.random() * WINDOW_WIDTH,
        y: Math.random() * WINDOW_HEIGHT,
        vx: randomFloat(-3, 3),
        vy: randomFloat(-3, 3),
        color: randomChoice([
          COLORS.RED,
          COLORS.BLUE,
          COLORS.GREEN,
          COLORS.YELLOW,
          COLORS.CYAN,
          COLORS.MAGENTA,
        ]),
        size: randomInt(1, 4),
        life: 5.0,
      });
    }

    // Handle mouse click
    if (mouse.clicked && mouse.x && mouse.y) {
      for (let i = 0; i < 80; i++) {
        const angle = Math.random() * Math.PI * 2;
        const speed = randomFloat(2, 6);
        this.particles.push({
          x: mouse.x,
          y: mouse.y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          color: randomChoice([
            COLORS.RED,
            COLORS.BLUE,
            COLORS.GREEN,
            COLORS.YELLOW,
            COLORS.CYAN,
            COLORS.MAGENTA,
          ]),
          size: randomInt(2, 5),
          life: 2.0,
        });
      }
      mouse.clicked = false;
    }

    // Update particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.life -= dt;
      p.x += p.vx;
      p.y += p.vy;
      p.vx *= 0.98;
      p.vy *= 0.98;

      if (p.life <= 0) {
        this.particles.splice(i, 1);
      }
    }
  }

  draw(ctx) {
    // Draw particles
    for (const p of this.particles) {
      const alpha = Math.max(0, p.life / 5.0);
      ctx.globalAlpha = alpha;
      drawCircle(ctx, p.x, p.y, p.size, p.color);
      ctx.globalAlpha = 1.0;
    }

    // Draw info
    drawText(ctx, `Particles: ${this.particles.length}`, 50, 30, COLORS.WHITE, 36);
  }
}

/**
 * Polygon Rush - Rotating polygons attracted to cursor
 */
class PolygonRush extends GameMode {
  constructor() {
    super('Polygon Rush', 3);
    this.polygons = [];
    for (let i = 0; i < 15 + this.difficulty * 5; i++) {
      this.polygons.push({
        x: Math.random() * WINDOW_WIDTH,
        y: Math.random() * WINDOW_HEIGHT,
        vx: randomFloat(-2, 2),
        vy: randomFloat(-2, 2),
        rotation: Math.random() * Math.PI * 2,
        rotation_speed: randomFloat(-5, 5),
        sides: randomInt(3, 8),
        size: randomInt(20, 50),
        color: randomChoice([COLORS.RED, COLORS.BLUE, COLORS.GREEN, COLORS.CYAN, COLORS.MAGENTA]),
      });
    }
  }

  update(dt, keys, mouse) {
    const mx = mouse.x || WINDOW_WIDTH / 2;
    const my = mouse.y || WINDOW_HEIGHT / 2;

    for (const poly of this.polygons) {
      const dx = mx - poly.x;
      const dy = my - poly.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist < 500) {
        const force = (500 - dist) / 500 * 2;
        poly.vx += (dx / dist) * force * dt;
        poly.vy += (dy / dist) * force * dt;
      }

      poly.x += poly.vx;
      poly.y += poly.vy;
      poly.vx *= 0.95;
      poly.vy *= 0.95;
      poly.rotation += poly.rotation_speed * dt;

      // Boundaries
      if (poly.x < -50) poly.x = WINDOW_WIDTH + 50;
      if (poly.x > WINDOW_WIDTH + 50) poly.x = -50;
      if (poly.y < -50) poly.y = WINDOW_HEIGHT + 50;
      if (poly.y > WINDOW_HEIGHT + 50) poly.y = -50;
    }
  }

  draw(ctx) {
    for (const poly of this.polygons) {
      ctx.save();
      ctx.translate(poly.x, poly.y);
      ctx.rotate(poly.rotation);

      ctx.fillStyle = rgbToCSS(poly.color);
      ctx.beginPath();

      for (let i = 0; i < poly.sides; i++) {
        const angle = (i / poly.sides) * Math.PI * 2;
        const x = Math.cos(angle) * poly.size;
        const y = Math.sin(angle) * poly.size;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.closePath();
      ctx.fill();
      ctx.restore();
    }

    drawText(ctx, `Polygons: ${this.polygons.length}`, 50, 30, COLORS.WHITE, 36);
  }
}

/**
 * Matrix Rain - Falling characters, speed controlled by cursor Y
 */
class MatrixRain extends GameMode {
  constructor() {
    super('Matrix Rain', 3);
    this.columns = [];
    const chars = '01アイウエオカキクケコサシスセソタチツテト';

    for (let i = 0; i < Math.floor(WINDOW_WIDTH / 20); i++) {
      this.columns.push({
        x: i * 20,
        y: Math.random() * WINDOW_HEIGHT,
        speed: randomFloat(1, 3),
        chars: Array.from({ length: 10 }, () => randomChoice(chars.split(''))),
      });
    }
  }

  update(dt, keys, mouse) {
    const my = mouse.y || WINDOW_HEIGHT / 2;
    const speed_multiplier = 1.0 + (my / WINDOW_HEIGHT) * 2;

    for (const col of this.columns) {
      col.y += col.speed * speed_multiplier;
      if (col.y > WINDOW_HEIGHT) {
        col.y = -100;
      }
    }
  }

  draw(ctx) {
    ctx.font = '20px monospace';

    for (const col of this.columns) {
      for (let i = 0; i < col.chars.length; i++) {
        const char_y = col.y + i * 20;

        if (char_y >= 0 && char_y < WINDOW_HEIGHT) {
          const color_val = Math.max(0, 255 - (char_y / WINDOW_HEIGHT) * 255);
          const r = 0;
          const g = Math.min(255, color_val + 100);
          const b = 0;

          ctx.fillStyle = `rgb(${r}, ${g}, ${b})`;
          ctx.fillText(col.chars[i], col.x, char_y);
        }
      }
    }
  }
}

/**
 * Interactive Draw - Paint and create effects with mouse
 */
class InteractiveDraw extends GameMode {
  constructor() {
    super('Interactive Draw', 2);
    this.draw_points = [];
    this.particles = [];
  }

  update(dt, keys, mouse) {
    // Update particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.life -= dt;
      p.x += p.vx;
      p.y += p.vy;
      p.vx *= 0.98;
      p.vy *= 0.98;

      if (p.life <= 0) {
        this.particles.splice(i, 1);
      }
    }

    // Handle mouse drawing
    if (mouse.pressed && mouse.x && mouse.y) {
      this.draw_points.push({
        x: mouse.x,
        y: mouse.y,
        color: randomChoice([
          COLORS.RED,
          COLORS.BLUE,
          COLORS.GREEN,
          COLORS.YELLOW,
          COLORS.CYAN,
          COLORS.MAGENTA,
          COLORS.ORANGE,
        ]),
        size: randomInt(3, 8),
      });

      // Create particles around cursor
      for (let i = 0; i < 5; i++) {
        this.particles.push({
          x: mouse.x + randomInt(-20, 20),
          y: mouse.y + randomInt(-20, 20),
          vx: randomFloat(-2, 2),
          vy: randomFloat(-2, 2),
          life: 1.0,
          color: randomChoice([COLORS.RED, COLORS.CYAN, COLORS.MAGENTA]),
        });
      }

      if (this.draw_points.length > 2000) {
        this.draw_points.shift();
      }
    }
  }

  draw(ctx) {
    // Draw points
    for (const p of this.draw_points) {
      ctx.fillStyle = rgbToCSS(p.color);
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    }

    // Draw particles
    for (const p of this.particles) {
      const alpha = Math.max(0, p.life);
      ctx.globalAlpha = alpha;
      drawCircle(ctx, p.x, p.y, 3, p.color);
      ctx.globalAlpha = 1.0;
    }

    drawText(ctx, `Points: ${this.draw_points.length}`, 50, 30, COLORS.WHITE, 36);
  }
}

// ==========================
// SYSTEM TEST MODES
// ==========================

/**
 * CPU Test - Processor load visualization
 */
class CPUTest extends GameMode {
  constructor() {
    super('CPU Test', 4);
    this.load_values = [];
    this.computation_count = 0;
  }

  update(dt, keys, mouse) {
    // Simulate CPU load with computations
    let load = 0;
    const iterations = 100000 * this.difficulty;

    for (let i = 0; i < iterations; i++) {
      load += Math.sqrt(i) * Math.sin(i) * Math.cos(i);
    }

    // Generate load value (0-100)
    const random_load = 40 + Math.random() * 50;
    this.load_values.push(random_load);

    if (this.load_values.length > 100) {
      this.load_values.shift();
    }
  }

  draw(ctx) {
    // Draw CPU load bars
    const bar_width = WINDOW_WIDTH / this.load_values.length;

    for (let i = 0; i < this.load_values.length; i++) {
      const load = this.load_values[i];
      const bar_height = (load / 100) * (WINDOW_HEIGHT - 100);
      const color = load > 80 ? COLORS.RED : load > 50 ? COLORS.YELLOW : COLORS.GREEN;

      drawRect(ctx, i * bar_width, WINDOW_HEIGHT - bar_height, bar_width, bar_height, color);
    }

    const current_load = this.load_values[this.load_values.length - 1] || 0;
    drawText(ctx, `CPU Load: ${Math.round(current_load)}%`, 50, 30, COLORS.WHITE, 48);
  }
}

/**
 * RAM Test - Memory usage visualization
 */
class RAMTest extends GameMode {
  constructor() {
    super('RAM Test', 3);
    this.memory_blocks = [];
    this.ram_history = [];
    this.update_timer = 0;
  }

  update(dt, keys, mouse) {
    this.update_timer += dt;

    if (this.update_timer > 0.1) {
      // Simulate memory allocation
      const block_size = randomInt(1, 10);
      if (Math.random() > 0.3) {
        this.memory_blocks.push({
          size: block_size,
          age: 0,
          color: randomChoice([COLORS.BLUE, COLORS.CYAN, COLORS.MAGENTA]),
        });
      }

      // Calculate RAM usage
      let total_ram = this.memory_blocks.reduce((sum, block) => sum + block.size, 0);
      total_ram = Math.min(100, total_ram);
      this.ram_history.push(total_ram);

      if (this.ram_history.length > 100) {
        this.ram_history.shift();
      }

      // Remove old blocks
      this.memory_blocks = this.memory_blocks.filter(
        (block) => {
          block.age += dt;
          return block.age < 2.0;
        }
      );

      this.update_timer = 0;
    }
  }

  draw(ctx) {
    // Draw RAM graph
    const graph_x = 150;
    const graph_y = 200;
    const graph_width = WINDOW_WIDTH - 300;
    const graph_height = 200;

    if (this.ram_history.length > 1) {
      ctx.strokeStyle = rgbToCSS(COLORS.BLUE);
      ctx.lineWidth = 2;
      ctx.beginPath();

      for (let i = 0; i < this.ram_history.length; i++) {
        const x = graph_x + (i / this.ram_history.length) * graph_width;
        const y = graph_y + graph_height - (this.ram_history[i] / 100) * graph_height;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      }

      ctx.stroke();
    }

    // Draw current RAM usage
    const current_ram = this.ram_history[this.ram_history.length - 1] || 0;
    drawText(ctx, `RAM Usage: ${Math.round(current_ram)}%`, 50, 30, COLORS.WHITE, 48);
  }
}

// ==========================
// PERFORMANCE RECOMMENDATIONS
// ==========================

function getPerformanceRecommendations(avg_fps, min_fps, max_fps) {
  const recommendations = [];
  let status, status_color;

  if (avg_fps >= 120) {
    status = 'EXCELLENT';
    status_color = COLORS.GREEN;
    recommendations.push('✓ Excellent performance! Your computer can handle maximum settings');
    recommendations.push('✓ Graphics on maximum, 4K resolution, all effects enabled');
  } else if (avg_fps >= 90) {
    status = 'VERY GOOD';
    status_color = [100, 255, 100];
    recommendations.push('✓ Very good performance');
    recommendations.push('✓ High graphics settings, 1440p resolution');
    recommendations.push('• Try enabling maximum effects');
  } else if (avg_fps >= 60) {
    status = 'GOOD';
    status_color = COLORS.YELLOW;
    recommendations.push('✓ Normal performance (60+ FPS)');
    recommendations.push('✓ Medium-High settings, 1080p resolution');
    recommendations.push('• Some heavy effects might need to be disabled');
  } else if (avg_fps >= 45) {
    status = 'ACCEPTABLE';
    status_color = COLORS.ORANGE;
    recommendations.push('⚠ Acceptable performance for casual gaming');
    recommendations.push('⚠ Medium graphics settings, 1080p');
    recommendations.push('! Lower resolution or disable some effects');
    recommendations.push('! Close background applications');
  } else if (avg_fps >= 30) {
    status = 'POOR';
    status_color = [255, 100, 0];
    recommendations.push('✗ Low performance');
    recommendations.push('! Lower resolution to 720p or below');
    recommendations.push('! Disable graphics effects');
    recommendations.push('! Close all background applications');
  } else {
    status = 'CRITICAL';
    status_color = COLORS.RED;
    recommendations.push('✗ CRITICAL LOW PERFORMANCE');
    recommendations.push('! Upgrade your graphics card or processor');
    recommendations.push('! Use minimum settings (720p, no effects)');
  }

  // Check stability
  const fps_variance = max_fps - min_fps;
  if (fps_variance > 40) {
    recommendations.push('');
    recommendations.push('⚠ INSTABILITY: Large FPS fluctuations');
    recommendations.push('  May be caused by: overheating, background processes, weak power supply');
  }

  return { status, status_color, recommendations };
}

// ==========================
// SCREEN RENDERING FUNCTIONS
// ==========================

/**
 * Welcome screen with animation
 */
async function showWelcomeScreen(canvas, ctx) {
  return new Promise((resolve) => {
    let alpha_timer = 0;
    let animating = true;

    function drawWelcome() {
      alpha_timer++;

      ctx.fillStyle = rgbToCSS(COLORS.BLACK);
      ctx.fillRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT);

      // Draw animated stars
      for (let i = 0; i < 30; i++) {
        const x = (i * 47 + alpha_timer * 2) % WINDOW_WIDTH;
        const y = (i * 31) % WINDOW_HEIGHT;
        ctx.fillStyle = 'rgb(100, 100, 100)';
        ctx.fillRect(x, y, 2, 2);
      }

      // Title
      drawCenteredText(ctx, 'FPS TESTER', 100, COLORS.CYAN, 100);

      // Subtitle
      drawCenteredText(ctx, 'Performance Analysis Tool', 220, COLORS.YELLOW, 60);

      // Info lines
      const lines = [
        '✓ Analyze your computer\'s gaming performance',
        '✓ Test with interactive game modes',
        '✓ Monitor CPU, RAM, and Disk I/O',
        '✓ Get personalized recommendations',
        '',
        '🌐 Web version coming soon!',
        '   Dual-screen architecture for weak PCs:',
        '   - Test screen + Statistics screen',
        '   - Automatic restart on crash',
      ];

      let y_pos = 330;
      for (const line of lines) {
        if (line === '') {
          y_pos += 30;
          continue;
        }

        const color = line.startsWith('🌐') || line.startsWith('   ')
          ? COLORS.MAGENTA
          : COLORS.GREEN;
        const fontSize = line.startsWith('   ') ? 28 : 36;

        drawCenteredText(ctx, line, y_pos, color, fontSize);
        y_pos += 45;
      }

      // Pulsing hint
      const pulse = Math.abs(Math.sin(alpha_timer * 0.05));
      const brightness = Math.round(255 * (0.5 + pulse * 0.5));

      drawCenteredText(
        ctx,
        'Press SPACE to continue',
        WINDOW_HEIGHT - 100,
        [brightness, brightness, brightness],
        48
      );

      if (animating) {
        requestAnimationFrame(drawWelcome);
      }
    }

    // Handle keyboard
    const handleKeyPress = (e) => {
      if (e.code === 'Space') {
        e.preventDefault();
        animating = false;
        document.removeEventListener('keydown', handleKeyPress);
        resolve();
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    drawWelcome();
  });
}

/**
 * Main menu with animated background
 */
async function showMainMenu(canvas, ctx) {
  return new Promise((resolve) => {
    let highlight = 0;
    let animating = true;
    let frame = 0;

    // Background particles
    const particles = [];
    for (let i = 0; i < 20; i++) {
      particles.push({
        x: Math.random() * WINDOW_WIDTH,
        y: Math.random() * WINDOW_HEIGHT,
        vx: randomFloat(-0.5, 0.5),
        vy: randomFloat(-1, 0),
        size: randomInt(1, 3),
        color: randomChoice([COLORS.CYAN, COLORS.MAGENTA, COLORS.GREEN]),
      });
    }

    function drawMenu() {
      frame++;

      // Update particles
      for (const p of particles) {
        p.y += p.vy;
        p.x += p.vx;
        if (p.y < -10) {
          p.y = WINDOW_HEIGHT + 10;
          p.x = Math.random() * WINDOW_WIDTH;
        }
      }

      ctx.fillStyle = rgbToCSS(COLORS.BLACK);
      ctx.fillRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT);

      // Draw background particles
      for (const p of particles) {
        drawCircle(ctx, p.x, p.y, p.size, p.color);
      }

      // Title with glow
      for (let offset of [4, 2]) {
        ctx.globalAlpha = 0.3;
        drawCenteredText(ctx, 'FPS TESTER', 50, [50, 50, 0], 100);
        ctx.globalAlpha = 1.0;
      }
      drawCenteredText(ctx, 'FPS TESTER', 50, COLORS.YELLOW, 100);

      // Subtitle
      drawCenteredText(ctx, 'Select test category or settings', 170, COLORS.WHITE, 28);

      // FPS Tests box
      const fps_color = highlight === 0 ? COLORS.CYAN : COLORS.WHITE;
      const fps_box_color = highlight === 0 ? COLORS.CYAN : [100, 100, 100];
      const fps_box_width = highlight === 0 ? 5 : 1;

      ctx.strokeStyle = rgbToCSS(fps_box_color);
      ctx.lineWidth = fps_box_width;
      ctx.strokeRect(50, 250, 400, 180);

      drawText(ctx, '1. FPS Tests', 80, 290, fps_color, 50);
      drawText(ctx, 'Interactive game modes', 80, 340, COLORS.WHITE, 32);

      // System Tests box
      const sys_color = highlight === 1 ? COLORS.MAGENTA : COLORS.WHITE;
      const sys_box_color = highlight === 1 ? COLORS.MAGENTA : [100, 100, 100];
      const sys_box_width = highlight === 1 ? 5 : 1;

      ctx.strokeStyle = rgbToCSS(sys_box_color);
      ctx.lineWidth = sys_box_width;
      ctx.strokeRect(500, 250, 400, 180);

      drawText(ctx, '2. System Tests', 530, 290, sys_color, 50);
      drawText(ctx, 'Monitor CPU/RAM/Disk', 530, 340, COLORS.WHITE, 32);

      // Settings box
      const set_color = highlight === 2 ? COLORS.GREEN : COLORS.WHITE;
      const set_box_color = highlight === 2 ? COLORS.GREEN : [100, 100, 100];
      const set_box_width = highlight === 2 ? 5 : 1;

      ctx.strokeStyle = rgbToCSS(set_box_color);
      ctx.lineWidth = set_box_width;
      ctx.strokeRect(950, 250, 400, 180);

      drawText(ctx, '3. Settings', 980, 290, set_color, 50);
      drawText(ctx, 'Configure display', 980, 340, COLORS.WHITE, 32);

      // Info
      drawCenteredText(
        ctx,
        'Use ← → or A/D or ↑ ↓ to navigate | ENTER to select',
        WINDOW_HEIGHT - 100,
        COLORS.WHITE,
        28
      );
      drawCenteredText(
        ctx,
        'Or press 1/2/3 | ESC to exit',
        WINDOW_HEIGHT - 60,
        COLORS.WHITE,
        28
      );

      if (animating) {
        requestAnimationFrame(drawMenu);
      }
    }

    const handleKeyPress = (e) => {
      if (e.code === 'ArrowLeft' || e.code === 'KeyA') {
        highlight = (highlight - 1 + 3) % 3;
      } else if (e.code === 'ArrowRight' || e.code === 'KeyD') {
        highlight = (highlight + 1) % 3;
      } else if (e.code === 'ArrowUp') {
        highlight = (highlight - 1 + 3) % 3;
      } else if (e.code === 'ArrowDown') {
        highlight = (highlight + 1) % 3;
      } else if (e.code === 'Enter' || e.code === 'Space') {
        e.preventDefault();
        animating = false;
        document.removeEventListener('keydown', handleKeyPress);
        if (highlight === 0) {
          resolve('fps');
        } else if (highlight === 1) {
          resolve('system');
        } else {
          resolve('settings');
        }
      } else if (e.code === 'Escape') {
        animating = false;
        document.removeEventListener('keydown', handleKeyPress);
        resolve(null);
      } else if (e.key === '1') {
        animating = false;
        document.removeEventListener('keydown', handleKeyPress);
        resolve('fps');
      } else if (e.key === '2') {
        animating = false;
        document.removeEventListener('keydown', handleKeyPress);
        resolve('system');
      } else if (e.key === '3') {
        animating = false;
        document.removeEventListener('keydown', handleKeyPress);
        resolve('settings');
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    drawMenu();
  });
}

/**
 * Results screen with recommendations
 */
async function showResults(canvas, ctx, gameMode) {
  return new Promise((resolve) => {
    const avg_fps, min_fps, max_fps = gameMode.getStats();
    const { status, status_color, recommendations } = getPerformanceRecommendations(
      avg_fps,
      min_fps,
      max_fps
    );

    let scroll_offset = 0;
    let animating = true;

    function drawResults() {
      ctx.fillStyle = rgbToCSS(COLORS.BLACK);
      ctx.fillRect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT);

      // Title
      drawCenteredText(ctx, 'Test Complete!', 50, COLORS.YELLOW, 80);

      // Game mode name
      drawCenteredText(ctx, gameMode.name, 130, COLORS.CYAN, 50);

      // Status
      drawCenteredText(ctx, status, 200, status_color, 70);

      // FPS Stats
      drawText(ctx, `Avg: ${Math.round(avg_fps)} FPS`, 100, 310, COLORS.GREEN, 40);
      drawText(
        ctx,
        `Min: ${Math.round(min_fps)} FPS`,
        600,
        310,
        min_fps < 60 ? COLORS.RED : COLORS.YELLOW,
        40
      );

      drawText(ctx, `Max: ${Math.round(max_fps)} FPS`, 100, 380, COLORS.GREEN, 40);

      const variance = max_fps - min_fps;
      const variance_color =
        variance < 30 ? COLORS.GREEN : variance < 50 ? COLORS.YELLOW : COLORS.RED;
      drawText(ctx, `Stability: ${Math.round(variance)} FPS variance`, 600, 380, variance_color, 40);

      // Recommendations
      let y_pos = 480;
      drawText(ctx, 'Recommendations:', 50, y_pos, COLORS.CYAN, 40);

      y_pos += 60;

      for (let idx = 0; idx < recommendations.length; idx++) {
        const rec = recommendations[idx];
        const screen_y = y_pos + idx * 28 + scroll_offset;

        if (screen_y > y_pos - 30 && screen_y < y_pos + 250) {
          let color = COLORS.WHITE;
          if (rec.startsWith('✓')) color = COLORS.GREEN;
          else if (rec.startsWith('✗')) color = COLORS.RED;
          else if (rec.startsWith('!')) color = COLORS.ORANGE;
          else if (rec.startsWith('⚠')) color = [255, 165, 0];

          drawText(ctx, rec, 70, screen_y, color, 22);
        }
      }

      // Hint
      drawCenteredText(
        ctx,
        'Press SPACE to return | ↑ ↓ to scroll',
        WINDOW_HEIGHT - 50,
        COLORS.WHITE,
        28
      );

      if (animating) {
        requestAnimationFrame(drawResults);
      }
    }

    const handleKeyPress = (e) => {
      if (e.code === 'Space' || e.code === 'Enter' || e.code === 'Escape') {
        e.preventDefault();
        animating = false;
        document.removeEventListener('keydown', handleKeyPress);
        resolve();
      } else if (e.code === 'ArrowUp') {
        scroll_offset = Math.min(0, scroll_offset + 30);
      } else if (e.code === 'ArrowDown') {
        scroll_offset = Math.max(-(recommendations.length * 28), scroll_offset - 30);
      }
    };

    document.addEventListener('keydown', handleKeyPress);
    drawResults();
  });
}

// ==========================
// MAIN GAME LOOP
// ==========================

class FPSTesterApp {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.mouse = {
      x: 0,
      y: 0,
      pressed: false,
      clicked: false,
    };
    this.keys = {};

    // Setup event listeners
    this.canvas.addEventListener('mousemove', (e) => this.handleMouseMove(e));
    this.canvas.addEventListener('mousedown', (e) => this.handleMouseDown(e));
    this.canvas.addEventListener('mouseup', (e) => this.handleMouseUp(e));
    document.addEventListener('keydown', (e) => this.handleKeyDown(e));
    document.addEventListener('keyup', (e) => this.handleKeyUp(e));
  }

  handleMouseMove(e) {
    const rect = this.canvas.getBoundingClientRect();
    this.mouse.x = e.clientX - rect.left;
    this.mouse.y = e.clientY - rect.top;
  }

  handleMouseDown(e) {
    this.mouse.pressed = true;
    this.mouse.clicked = true;
  }

  handleMouseUp(e) {
    this.mouse.pressed = false;
  }

  handleKeyDown(e) {
    this.keys[e.code] = true;
  }

  handleKeyUp(e) {
    this.keys[e.code] = false;
  }

  async start() {
    // Show welcome screen
    await showWelcomeScreen(this.canvas, this.ctx);

    // Main loop
    while (true) {
      const category = await showMainMenu(this.canvas, this.ctx);

      if (category === null) {
        break;
      }

      if (category === 'settings') {
        // TODO: Implement settings menu
        continue;
      }

      // TODO: Run game mode and show results
    }
  }
}

// ==========================
// EXPORT FOR HTML
// ==========================

if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    FPSTesterApp,
    GameMode,
    ParticleStorm,
    PolygonRush,
    MatrixRain,
    InteractiveDraw,
    CPUTest,
    RAMTest,
  };
}
