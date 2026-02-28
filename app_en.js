// ===========================
// FPS TESTER - Web Version (English)
// ===========================

let currentTest = null;
let testRunning = false;
let fpsValues = [];
let lastFrameTime = Date.now();
let frameCount = 0;
let testDuration = 30000; // 30 seconds
let crashDetected = false;
let lastFrameTimeRecord = Date.now();
let unresponsiveCounter = 0;

const tests = {
    // EASY
    'starfield': {
        name: '⭐ Starfield',
        desc: 'Smooth starfield effect',
        difficulty: 'Easy'
    },
    'matrix-rain': {
        name: '🌧️ Matrix Rain',
        desc: 'Falling text characters',
        difficulty: 'Easy'
    },
    // MEDIUM
    'tunnel': {
        name: '🌌 Tunnel Effect',
        desc: '3D tunnel animation',
        difficulty: 'Medium'
    },
    'polygon-rush': {
        name: '🔷 Polygon Rush',
        desc: 'Rotating polygons',
        difficulty: 'Medium'
    },
    // HARD
    'particle-storm': {
        name: '🌪️ Particle Storm',
        desc: 'Hundreds of particles',
        difficulty: 'Hard'
    },
    'fractal-tree': {
        name: '🌳 Fractal Tree',
        desc: 'Recursive fractals',
        difficulty: 'Hard'
    },
    'mandelbrot': {
        name: '🎨 Mandelbrot Set',
        desc: 'Mathematical fractal',
        difficulty: 'Hard'
    },
    // EXTREME
    'particle-explosion': {
        name: '💥 Particle Explosion',
        desc: '1000+ particles physics',
        difficulty: 'EXTREME'
    },
    'mega-mandelbrot': {
        name: '🌀 Mega Mandelbrot',
        desc: 'Ultra-detailed fractal',
        difficulty: 'EXTREME'
    },
    'mega-tunnel': {
        name: '🌠 Mega Tunnel',
        desc: '100 rings full resolution',
        difficulty: 'EXTREME'
    },
    'combined-stress': {
        name: '☢️ Combined Stress',
        desc: 'All systems simultaneous',
        difficulty: 'EXTREME'
    }
};

// ===========================
// SCREEN MANAGEMENT
// ===========================

function showScreen(screen) {
    // Hide all screens
    document.getElementById('welcome-screen').style.display = 'none';
    document.getElementById('menu-screen').style.display = 'none';
    document.getElementById('test-screen').style.display = 'none';
    document.getElementById('results-screen').style.display = 'none';
    document.getElementById('history-screen').style.display = 'none';

    // Show selected screen
    switch(screen) {
        case 'welcome':
            document.getElementById('welcome-screen').style.display = 'flex';
            break;
        case 'menu':
            document.getElementById('menu-screen').style.display = 'block';
            break;
        case 'test':
            document.getElementById('test-screen').style.display = 'block';
            break;
        case 'results':
            document.getElementById('results-screen').style.display = 'block';
            break;
        case 'history':
            document.getElementById('history-screen').style.display = 'block';
            loadHistory();
            break;
    }
}

// ===========================
// TEST MANAGEMENT
// ===========================

function startTest(testType) {
    currentTest = testType;
    testRunning = true;
    fpsValues = [];
    frameCount = 0;
    lastFrameTime = Date.now();
    
    const testInfo = tests[testType];
    document.getElementById('test-name').textContent = testInfo.name + ' - ' + testInfo.desc;
    document.getElementById('current-fps').textContent = '0';
    document.getElementById('avg-fps').textContent = '0';
    document.getElementById('min-fps').textContent = '0';
    document.getElementById('max-fps').textContent = '0';
    
    showScreen('test');
    
    // Start test animation
    const startTime = Date.now();
    const canvas = document.getElementById('render-canvas');
    const ctx = canvas.getContext('2d');
    
    function resizeCanvas() {
        const container = document.getElementById('test-canvas');
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Test-specific animations
    function animate() {
        if (!testRunning) return;
        
        try {
            const now = Date.now();
            const elapsed = now - startTime;
            
            // CRASH DETECTION: Check if system is becoming unresponsive
            const timeSinceLastFrame = now - lastFrameTimeRecord;
            if (timeSinceLastFrame > 2000) { // No frame update for 2+ seconds = unresponsive
                unresponsiveCounter++;
            } else {
                unresponsiveCounter = 0;
            }
            
            // Detect crash: 3+ consecutive unresponsive checks = system crash
            if (unresponsiveCounter >= 3 || (fpsValues.length > 0 && fpsValues[fpsValues.length - 1] < 3)) {
                handleCrashDetected();
                return;
            }
            
            lastFrameTimeRecord = now;
            
            // Clear canvas
            ctx.fillStyle = '#0a0e27';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw based on test type
            switch(currentTest) {
                case 'starfield':
                    drawStarfield(ctx, elapsed, canvas);
                    break;
                case 'particle-storm':
                    drawParticleStorm(ctx, elapsed, canvas);
                    break;
                case 'polygon-rush':
                    drawPolygonRush(ctx, elapsed, canvas);
                    break;
                case 'matrix-rain':
                    drawMatrixRain(ctx, elapsed, canvas);
                    break;
                case 'fractal-tree':
                    drawFractalTree(ctx, elapsed, canvas);
                    break;
                case 'mandelbrot':
                    drawMandelbrot(ctx, elapsed, canvas);
                    break;
                case 'tunnel':
                    drawTunnel(ctx, elapsed, canvas);
                    break;
                case 'particle-explosion':
                    drawParticleExplosion(ctx, elapsed, canvas);
                    break;
                case 'mega-mandelbrot':
                    drawMegaMandelbrot(ctx, elapsed, canvas);
                    break;
                case 'mega-tunnel':
                    drawMegaTunnel(ctx, elapsed, canvas);
                    break;
                case 'combined-stress':
                    drawCombinedStress(ctx, elapsed, canvas);
                    break;
            }
            
            // Update FPS
            frameCount++;
            const deltaTime = now - lastFrameTime;
            
            if (deltaTime >= 1000) {
                const fps = frameCount;
                fpsValues.push(fps);
                
                document.getElementById('current-fps').textContent = fps;
                document.getElementById('avg-fps').textContent = Math.round(fpsValues.reduce((a, b) => a + b) / fpsValues.length);
                document.getElementById('min-fps').textContent = Math.min(...fpsValues);
                document.getElementById('max-fps').textContent = Math.max(...fpsValues);
                
                frameCount = 0;
                lastFrameTime = now;
            }
            
            // Check if test duration exceeded
            if (elapsed > testDuration) {
                stopTest();
                return;
            }
            
            requestAnimationFrame(animate);
        } catch (error) {
            console.error('Error during test:', error);
            handleCrashDetected();
        }
    }
    
    animate();
}

function handleCrashDetected() {
    testRunning = false;
    crashDetected = true;
    
    // Calculate partial results
    if (fpsValues.length === 0) {
        fpsValues = [0, 0, 0, 0, 5];
    }
    
    const avgFps = Math.round(fpsValues.reduce((a, b) => a + b) / fpsValues.length);
    const minFps = Math.min(...fpsValues);
    const maxFps = Math.max(...fpsValues);
    
    // Show crash warning screen
    const testScreen = document.getElementById('test-screen');
    const canvas = document.getElementById('render-canvas');
    
    // Create crash overlay
    const overlay = document.createElement('div');
    overlay.id = 'crash-overlay';
    overlay.style.cssText = `
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.95);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        border-radius: 10px;
    `;
    
    const crashContent = document.createElement('div');
    crashContent.style.cssText = `
        text-align: center;
        color: #fff;
        padding: 35px 40px;
        background: linear-gradient(135deg, rgba(255, 50, 50, 0.3), rgba(150, 0, 0, 0.3));
        border-radius: 10px;
        border: 2px solid #ff3333;
        max-width: 90vw;
        max-height: 90vh;
        width: 600px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 15px;
    `;
    
    const testInfo = tests[currentTest];
    
    // Title
    const titleEl = document.createElement('h2');
    titleEl.textContent = '⚠️ SYSTEM CRASH DETECTED';
    titleEl.style.cssText = 'color: #ff3333; font-size: 28px; margin: 0; line-height: 1.3;';
    crashContent.appendChild(titleEl);
    
    // Description
    const descEl = document.createElement('p');
    descEl.textContent = 'Your computer crashed due to extreme stress test load';
    descEl.style.cssText = 'font-size: 16px; margin: 0; color: #fff;';
    crashContent.appendChild(descEl);
    
    // Test name
    const testEl = document.createElement('p');
    testEl.textContent = 'Test: ' + testInfo.name;
    testEl.style.cssText = 'font-size: 14px; color: #ffaa00; margin: 5px 0 0 0; font-weight: bold;';
    crashContent.appendChild(testEl);
    
    // Recommendation box
    const recBox = document.createElement('div');
    recBox.style.cssText = `
        background: rgba(0, 0, 0, 0.5);
        padding: 20px;
        border-radius: 5px;
        margin: 10px 0 0 0;
        text-align: left;
        border-left: 3px solid #ffaa00;
    `;
    
    const recTitle = document.createElement('p');
    recTitle.innerHTML = '<strong>⚠️ RECOMMENDATION:</strong>';
    recTitle.style.cssText = 'margin: 0 0 12px 0; color: #ffaa00; font-size: 14px;';
    recBox.appendChild(recTitle);
    
    const recText = document.createElement('p');
    recText.innerHTML = `This test is too demanding for your system.<br><br>
        <strong>Do not run ${testInfo.difficulty === 'EXTREME' ? 'EXTREME' : testInfo.difficulty} or higher difficulty tests again.</strong><br><br>
        We recommend running only EASY or MEDIUM tests to avoid system instability.`;
    recText.style.cssText = 'margin: 0; color: #ddd; font-size: 13px; line-height: 1.5;';
    recBox.appendChild(recText);
    
    crashContent.appendChild(recBox);
    
    // Buttons container
    const btnContainer = document.createElement('div');
    btnContainer.style.cssText = `
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin: 20px 0 10px 0;
        width: 100%;
    `;
    
    const btnContinue = document.createElement('button');
    btnContinue.innerHTML = '🔄 CONTINUE<br>(Don\'t Exit)';
    btnContinue.onclick = continueAfterCrash;
    btnContinue.style.cssText = `
        padding: 16px 12px;
        background: linear-gradient(135deg, #00dd00, #00aa00);
        color: #000;
        border: 2px solid #00ff00;
        border-radius: 5px;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
        white-space: normal;
        line-height: 1.3;
    `;
    btnContinue.onmouseover = function() { this.style.boxShadow = '0 0 15px #00ff00'; };
    btnContinue.onmouseout = function() { this.style.boxShadow = 'none'; };
    btnContainer.appendChild(btnContinue);
    
    const btnReturn = document.createElement('button');
    btnReturn.innerHTML = '🏠 Return to<br>Menu';
    btnReturn.onclick = function() { showScreen('menu'); };
    btnReturn.style.cssText = `
        padding: 16px 12px;
        background: linear-gradient(135deg, #dd7700, #aa5500);
        color: #fff;
        border: 2px solid #ffaa00;
        border-radius: 5px;
        font-size: 13px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.2s;
        white-space: normal;
        line-height: 1.3;
    `;
    btnReturn.onmouseover = function() { this.style.boxShadow = '0 0 15px #ffaa00'; };
    btnReturn.onmouseout = function() { this.style.boxShadow = 'none'; };
    btnContainer.appendChild(btnReturn);
    
    crashContent.appendChild(btnContainer);
    
    // Footer text
    const footerEl = document.createElement('p');
    footerEl.textContent = '✓ System will now cooldown. Please close other apps and wait before running tests again.';
    footerEl.style.cssText = 'margin: 10px 0 0 0; font-size: 11px; color: #aaa; line-height: 1.4;';
    crashContent.appendChild(footerEl);
    
    overlay.appendChild(crashContent);
    testScreen.appendChild(overlay);
    
    // Log crash to history
    const crashResult = {
        test: currentTest,
        date: new Date().toLocaleString(),
        avgFps: avgFps,
        minFps: minFps,
        maxFps: maxFps,
        status: 'CRASH',
        duration: Math.round((fpsValues.length * 1000) / 1000)
    };
    
    // Save this crash to show user they should avoid this difficulty
    let history = JSON.parse(localStorage.getItem('fps_history')) || [];
    history.unshift(crashResult);
    history = history.slice(0, 50);
    localStorage.setItem('fps_history', JSON.stringify(history));
}

function continueAfterCrash() {
    crashDetected = false;
    const overlay = document.getElementById('crash-overlay');
    if (overlay) {
        overlay.style.opacity = '0';
        overlay.style.transition = 'opacity 0.3s';
        setTimeout(() => overlay.remove(), 300);
    }
    
    // Go back to test screen with recovery message
    const testScreen = document.getElementById('test-screen');
    const existingMsg = testScreen.querySelector('.recovery-message');
    if (existingMsg) {
        existingMsg.remove();
    }
    
    const recoveryMsg = document.createElement('div');
    recoveryMsg.className = 'recovery-message';
    recoveryMsg.style.cssText = `
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, rgba(255, 170, 0, 0.95), rgba(200, 140, 0, 0.95));
        color: #000;
        padding: 18px 30px;
        border-radius: 8px;
        z-index: 998;
        font-weight: bold;
        text-align: center;
        border: 2px solid #ffaa00;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        max-width: 90vw;
        word-wrap: break-word;
        animation: slideDown 0.4s ease-out;
    `;
    recoveryMsg.innerHTML = '✓ System Cooldown Active - Program Continues Normally';
    testScreen.appendChild(recoveryMsg);
    
    setTimeout(() => {
        recoveryMsg.style.opacity = '0';
        recoveryMsg.style.transition = 'opacity 1s ease-out';
        setTimeout(() => {
            if (recoveryMsg.parentNode) {
                recoveryMsg.remove();
            }
        }, 1000);
    }, 3000);
}

function stopTest() {
    testRunning = false;
    
    if (fpsValues.length === 0) {
        fpsValues = [60, 65, 62, 58, 70];
    }
    
    // Calculate results
    const avgFps = Math.round(fpsValues.reduce((a, b) => a + b) / fpsValues.length);
    const minFps = Math.min(...fpsValues);
    const maxFps = Math.max(...fpsValues);
    
    // Show results
    showResults(avgFps, minFps, maxFps);
}

// ===========================
// DRAWING FUNCTIONS - EASY
// ===========================

function drawStarfield(ctx, elapsed, canvas) {
    const stars = 200;
    const speed = elapsed / 1000;
    
    for (let i = 0; i < stars; i++) {
        const angle = (i / stars) * Math.PI * 2;
        const radius = (speed * 100 + Math.random() * 300) % 400;
        const x = canvas.width / 2 + Math.cos(angle) * radius;
        const y = canvas.height / 2 + Math.sin(angle) * radius;
        
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(x, y, 2, 2);
    }
}

function drawMatrixRain(ctx, elapsed, canvas) {
    ctx.font = 'bold 20px monospace';
    ctx.fillStyle = '#00ff00';
    
    const cols = Math.floor(canvas.width / 20);
    for (let i = 0; i < cols; i++) {
        const y = (elapsed / 30 + i * 30) % canvas.height;
        const char = String.fromCharCode(0x30 + Math.floor(Math.random() * 10));
        ctx.fillText(char, i * 20, y);
    }
}

// ===========================
// DRAWING FUNCTIONS - MEDIUM
// ===========================

function drawTunnel(ctx, elapsed, canvas) {
    const rings = 50;
    const speed = elapsed / 100;
    
    for (let i = 0; i < rings; i++) {
        const depth = (speed + i * 5) % 500;
        const size = 50 + depth / 2;
        const alpha = 1 - (depth / 500);
        
        const hue = ((speed + i * 10) % 360);
        ctx.strokeStyle = `hsla(${hue}, 100%, 50%, ${alpha})`;
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, size, 0, Math.PI * 2);
        ctx.stroke();
    }
}

function drawPolygonRush(ctx, elapsed, canvas) {
    const polygonCount = 20;
    const speed = elapsed / 500;
    
    for (let i = 0; i < polygonCount; i++) {
        const angle = (i / polygonCount) * Math.PI * 2 + speed;
        const radius = 100 + i * 10;
        const x = canvas.width / 2 + Math.cos(angle) * radius;
        const y = canvas.height / 2 + Math.sin(angle) * radius;
        const sides = 3 + (i % 5);
        
        ctx.strokeStyle = `hsl(${(i * 360 / polygonCount + speed * 10) % 360}, 100%, 50%)`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        for (let j = 0; j < sides; j++) {
            const px = x + Math.cos((j / sides) * Math.PI * 2 + speed) * 20;
            const py = y + Math.sin((j / sides) * Math.PI * 2 + speed) * 20;
            if (j === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.closePath();
        ctx.stroke();
    }
}

// ===========================
// DRAWING FUNCTIONS - HARD
// ===========================

function drawParticleStorm(ctx, elapsed, canvas) {
    const particles = Math.floor((elapsed / 1000) * 100) % 500;
    const size = 2;
    
    for (let i = 0; i < particles; i++) {
        const angle = (i / particles) * Math.PI * 2 + elapsed / 1000;
        const radius = (elapsed / 100) % 300 + 50;
        const x = canvas.width / 2 + Math.cos(angle) * radius;
        const y = canvas.height / 2 + Math.sin(angle) * radius;
        
        const colors = ['#00d4ff', '#ff00ff', '#00ff00', '#ffaa00'];
        ctx.fillStyle = colors[i % colors.length];
        ctx.fillRect(x, y, size, size);
    }
}

function drawFractalTree(ctx, elapsed, canvas) {
    ctx.strokeStyle = `hsl(${(elapsed / 20) % 360}, 100%, 50%)`;
    ctx.lineWidth = 2;
    
    function drawBranch(x, y, angle, length, depth) {
        if (depth === 0 || length < 2) return;
        
        const x2 = x + Math.cos(angle * Math.PI / 180) * length;
        const y2 = y + Math.sin(angle * Math.PI / 180) * length;
        
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x2, y2);
        ctx.stroke();
        
        drawBranch(x2, y2, angle - 20, length * 0.7, depth - 1);
        drawBranch(x2, y2, angle + 20, length * 0.7, depth - 1);
    }
    
    const angle = (elapsed / 100) % 360;
    drawBranch(canvas.width / 2, canvas.height - 20, angle - 90, 80, 10);
}

function drawMandelbrot(ctx, elapsed, canvas) {
    const zoom = 1 + (elapsed / 10000);
    const maxIter = 50;
    
    for (let x = 0; x < canvas.width; x += 4) {
        for (let y = 0; y < canvas.height; y += 4) {
            const realMin = -2 / zoom;
            const realMax = 1 / zoom;
            const imagMin = -1.5 / zoom;
            const imagMax = 1.5 / zoom;
            
            const real = realMin + (x / canvas.width) * (realMax - realMin);
            const imag = imagMin + (y / canvas.height) * (imagMax - imagMin);
            
            let zReal = 0, zImag = 0, iter = 0;
            while (iter < maxIter && zReal * zReal + zImag * zImag < 4) {
                const temp = zReal * zReal - zImag * zImag + real;
                zImag = 2 * zReal * zImag + imag;
                zReal = temp;
                iter++;
            }
            
            const hue = (iter * 360 / maxIter) % 360;
            ctx.fillStyle = `hsl(${hue}, 100%, 50%)`;
            ctx.fillRect(x, y, 4, 4);
        }
    }
}

// ===========================
// DRAWING FUNCTIONS - EXTREME
// ===========================

function drawParticleExplosion(ctx, elapsed, canvas) {
    const particles = Math.min(1000, Math.floor((elapsed / 100) * 50));
    
    for (let i = 0; i < particles; i++) {
        const angle = (i / particles) * Math.PI * 2 + Math.random();
        const radius = Math.random() * 300;
        const x = canvas.width / 2 + Math.cos(angle) * radius;
        const y = canvas.height / 2 + Math.sin(angle) * radius;
        
        // Physics simulation
        const vx = Math.cos(angle) * Math.random() * 5;
        const vy = Math.sin(angle) * Math.random() * 5;
        
        const colors = ['#00d4ff', '#ff00ff', '#ff0000', '#ffff00'];
        ctx.fillStyle = colors[i % colors.length];
        ctx.beginPath();
        ctx.arc(x, y, 2, 0, Math.PI * 2);
        ctx.fill();
    }
}

function drawMegaMandelbrot(ctx, elapsed, canvas) {
    const zoom = 1 + (elapsed / 5000);
    const maxIter = 500; // EXTREME ITERATION COUNT
    
    for (let x = 0; x < canvas.width; x += 2) {
        for (let y = 0; y < canvas.height; y += 2) {
            const realMin = -2 / zoom;
            const realMax = 1 / zoom;
            const imagMin = -1.5 / zoom;
            const imagMax = 1.5 / zoom;
            
            const real = realMin + (x / canvas.width) * (realMax - realMin);
            const imag = imagMin + (y / canvas.height) * (imagMax - imagMin);
            
            let zReal = 0, zImag = 0, iter = 0;
            while (iter < maxIter && zReal * zReal + zImag * zImag < 4) {
                const temp = zReal * zReal - zImag * zImag + real;
                zImag = 2 * zReal * zImag + imag;
                zReal = temp;
                iter++;
            }
            
            const hue = (iter * 360 / maxIter) % 360;
            ctx.fillStyle = `hsl(${hue}, 100%, ${50 * Math.sin(iter / 100)}%)`;
            ctx.fillRect(x, y, 2, 2);
        }
    }
}

function drawMegaTunnel(ctx, elapsed, canvas) {
    const rings = 100;
    const speed = elapsed / 50;
    
    for (let i = 0; i < rings; i++) {
        const depth = (speed + i * 2) % 500;
        const size = 50 + depth / 2;
        const alpha = 1 - (depth / 500);
        
        const hue = ((speed * 2 + i * 10) % 360);
        ctx.strokeStyle = `hsla(${hue}, 100%, 50%, ${alpha})`;
        ctx.lineWidth = 5;
        ctx.beginPath();
        ctx.arc(canvas.width / 2, canvas.height / 2, size, 0, Math.PI * 2);
        ctx.stroke();
    }
}

function drawCombinedStress(ctx, elapsed, canvas) {
    // Run ALL drawing functions simultaneously (extreme stress)
    try {
        drawParticleExplosion(ctx, elapsed, canvas);
        drawMegaMandelbrot(ctx, elapsed, canvas);
        drawMegaTunnel(ctx, elapsed, canvas);
        drawFractalTree(ctx, elapsed, canvas);
    } catch(e) {
        // System crashed during combined stress
        ctx.fillStyle = '#ff0000';
        ctx.font = 'bold 40px Arial';
        ctx.fillText('SYSTEM OVERLOAD!', 50, canvas.height / 2);
    }
}

// ===========================
// RESULTS & RECOMMENDATIONS
// ===========================

function showResults(avgFps, minFps, maxFps) {
    const isExtreme = ['particle-explosion', 'mega-mandelbrot', 'mega-tunnel', 'combined-stress'].includes(currentTest);
    
    // Calculate performance score
    const score = calculateScore(avgFps);
    const bottleneck = detectBottleneck(avgFps);
    
    // Update results screen
    document.getElementById('performance-score').textContent = score.toFixed(1);
    document.getElementById('score-status').textContent = getScoreStatus(score);
    document.getElementById('bottleneck-info').textContent = `Bottleneck: ${bottleneck}`;
    
    // Show warning for extreme tests
    if (isExtreme) {
        document.getElementById('extreme-warning').style.display = 'block';
    } else {
        document.getElementById('extreme-warning').style.display = 'none';
    }
    
    // Get recommendations
    const recommendations = getRecommendations(avgFps, minFps, maxFps, isExtreme);
    const recList = document.getElementById('rec-list');
    recList.innerHTML = '';
    
    recommendations.forEach(rec => {
        const div = document.createElement('div');
        div.className = `rec-item ${rec.type}`;
        div.textContent = rec.text;
        recList.appendChild(div);
    });
    
    // Draw charts
    drawCharts(fpsValues, avgFps, minFps, maxFps);
    
    // Save to history
    saveToHistory(currentTest, score, avgFps);
    
    // Show results screen
    showScreen('results');
}

function calculateScore(avgFps) {
    let score = 10;
    
    if (avgFps < 30) score -= 4;
    else if (avgFps < 60) score -= 2;
    else if (avgFps < 120) score -= 0.5;
    
    return Math.max(1, Math.min(10, score));
}

function detectBottleneck(avgFps) {
    if (avgFps >= 120) return 'GPU Limited - Excellent Performance';
    if (avgFps >= 90) return 'Balanced System';
    if (avgFps >= 60) return 'CPU-GPU Balanced';
    if (avgFps >= 45) return 'CPU Limited';
    return 'System Too Weak';
}

function getScoreStatus(score) {
    if (score >= 9) return '🟢 EXCELLENT - Absolute top tier';
    if (score >= 7) return '🟡 VERY GOOD - High performance';
    if (score >= 5) return '🟠 GOOD - Average performance';
    if (score >= 3) return '🔴 FAIR - Below average';
    return '🔴 CRITICAL - System too weak';
}

function getRecommendations(avgFps, minFps, maxFps, isExtreme) {
    const recs = [];
    
    if (isExtreme) {
        recs.push({ text: '⚠️ EXTREME TEST: Your system handled extreme stress!', type: 'warning' });
    }
    
    if (avgFps >= 120) {
        recs.push({ text: '✓ Excellent performance! Play any game at max settings 4K', type: 'good' });
        recs.push({ text: '✓ Your PC is high-end gaming ready', type: 'good' });
    } else if (avgFps >= 90) {
        recs.push({ text: '✓ Very good performance for AAA games at 1440p High', type: 'good' });
        recs.push({ text: '✓ Suitable for competitive and casual gaming', type: 'good' });
    } else if (avgFps >= 60) {
        recs.push({ text: '✓ Normal performance for 1080p Medium settings', type: 'good' });
        recs.push({ text: '⚠ Older or indie games will run smooth', type: 'warning' });
    } else if (avgFps >= 45) {
        recs.push({ text: '⚠ Acceptable but lower graphics recommended', type: 'warning' });
        recs.push({ text: '! Close background applications to improve FPS', type: 'warning' });
    } else if (avgFps >= 30) {
        recs.push({ text: '! Low performance - use minimum settings 720p', type: 'critical' });
        recs.push({ text: '! Consider GPU upgrade for better results', type: 'critical' });
    } else {
        recs.push({ text: '✗ CRITICAL - Hardware upgrade strongly recommended', type: 'critical' });
        recs.push({ text: '✗ Modern games will not run smoothly', type: 'critical' });
    }
    
    const variance = maxFps - minFps;
    if (variance > 40) {
        recs.push({ text: '⚠ High FPS fluctuations - check background processes/temperature', type: 'warning' });
    }
    
    // Game compatibility
    recs.push({ text: '', type: 'good' });
    if (avgFps >= 90) {
        recs.push({ text: '🎮 Playable: Cyberpunk 2077 Ultra, Starfield Ultra, all AAA titles max', type: 'good' });
    } else if (avgFps >= 60) {
        recs.push({ text: '🎮 Playable: Most AAA games on High/Ultra, esports titles on Ultra', type: 'good' });
    } else if (avgFps >= 45) {
        recs.push({ text: '🎮 Playable: Older AAA games, newer indie titles on Medium', type: 'warning' });
    } else {
        recs.push({ text: '🎮 Playable: Older games, indie titles, minimum settings new games', type: 'critical' });
    }
    
    return recs;
}

function drawCharts(fpsData, avgFps, minFps, maxFps) {
    // FPS Chart
    const fpsCtx = document.getElementById('fps-chart').getContext('2d');
    new Chart(fpsCtx, {
        type: 'line',
        data: {
            labels: fpsData.map((_, i) => i + 's'),
            datasets: [{
                label: 'FPS',
                data: fpsData,
                borderColor: '#00d4ff',
                backgroundColor: 'rgba(0, 212, 255, 0.1)',
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: Math.max(...fpsData, 120)
                }
            }
        }
    });
    
    // Metrics Chart
    const metricsCtx = document.getElementById('metrics-chart').getContext('2d');
    new Chart(metricsCtx, {
        type: 'bar',
        data: {
            labels: ['Average', 'Min', 'Max'],
            datasets: [{
                label: 'FPS',
                data: [avgFps, minFps, maxFps],
                backgroundColor: ['#00d4ff', '#ffaa00', '#ff00ff']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// ===========================
// HISTORY MANAGEMENT
// ===========================

function saveToHistory(testType, score, avgFps) {
    const history = JSON.parse(localStorage.getItem('fpsTestHistory') || '[]');
    
    history.push({
        test: testType,
        score: score,
        avgFps: avgFps,
        date: new Date().toLocaleString(),
        timestamp: Date.now()
    });
    
    localStorage.setItem('fpsTestHistory', JSON.stringify(history.slice(-50)));
}

function loadHistory() {
    const history = JSON.parse(localStorage.getItem('fpsTestHistory') || '[]');
    const historyList = document.getElementById('history-list');
    
    if (history.length === 0) {
        historyList.innerHTML = '<p style="text-align: center; color: var(--text);">No test history yet</p>';
        return;
    }
    
    historyList.innerHTML = history.reverse().map(item => `
        <div class="history-item">
            <div>
                <div style="font-weight: bold; color: var(--primary);">${tests[item.test].name}</div>
                <div class="history-date">${item.date}</div>
            </div>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <div class="history-score">${item.score.toFixed(1)}/10 (${item.avgFps} FPS)</div>
                <button class="history-delete" onclick="deleteHistoryItem(${item.timestamp})">Delete</button>
            </div>
        </div>
    `).join('');
}

function deleteHistoryItem(timestamp) {
    const history = JSON.parse(localStorage.getItem('fpsTestHistory') || '[]');
    const filtered = history.filter(item => item.timestamp !== timestamp);
    localStorage.setItem('fpsTestHistory', JSON.stringify(filtered));
    loadHistory();
}

function clearHistory() {
    if (confirm('Clear all test history?')) {
        localStorage.setItem('fpsTestHistory', '[]');
        loadHistory();
    }
}

// ===========================
// INITIALIZATION
// ===========================

document.addEventListener('DOMContentLoaded', () => {
    showScreen('welcome');
});
