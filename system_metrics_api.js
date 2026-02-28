/**
 * FPS Tester - System Metrics Helper
 * Handles fetching real system metrics from backend server
 * or falls back to simulation if server unavailable
 */

const BACKEND_URL = 'http://localhost:5000';
let BACKEND_AVAILABLE = false;

/**
 * Initialize backend connection
 * Check if server is running
 */
async function initializeBackend() {
  try {
    const response = await fetch(`${BACKEND_URL}/api/health`, {
      mode: 'cors'
    });
    if (response.ok) {
      BACKEND_AVAILABLE = true;
      console.log('✓ Backend server available - Using real system metrics');
      return true;
    }
  } catch (error) {
    console.warn('⚠ Backend server not available - Using simulated metrics');
    BACKEND_AVAILABLE = false;
  }
  return false;
}

/**
 * Get current system metrics from backend or simulation
 */
async function getSystemMetrics() {
  if (BACKEND_AVAILABLE) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/system-metrics`);
      const data = await response.json();
      
      if (data.status === 'success') {
        return {
          cpu_percent: data.cpu_percent || 0,
          ram_percent: data.ram_percent || 0,
          disk_percent: data.disk_percent || 0,
          ram_usage_mb: data.ram_usage_mb || 0,
          ram_available_mb: data.ram_available_mb || 0,
          ram_total_mb: data.ram_total_mb || 0,
          disk_free_gb: data.disk_free_gb || 0,
          source: 'backend'  // Real metrics from server
        };
      }
    } catch (error) {
      console.warn('Error fetching metrics from backend:', error);
    }
  }
  
  // Fallback: simulate metrics
  return simulateSystemMetrics();
}

/**
 * Simulate system metrics (when backend unavailable)
 */
function simulateSystemMetrics() {
  const baseCPU = 40 + Math.random() * 30;
  const baseRAM = 50 + Math.random() * 25;
  
  return {
    cpu_percent: baseCPU,
    ram_percent: baseRAM,
    disk_percent: 75 + Math.random() * 15,
    ram_usage_mb: Math.round(baseRAM * 10.24),
    ram_available_mb: Math.round((100 - baseRAM) * 10.24),
    ram_total_mb: 1024,
    disk_free_gb: 200 + Math.random() * 100,
    source: 'simulation'  // Simulated metrics
  };
}

/**
 * Get system information (CPU count, RAM total, etc)
 */
async function getSystemInfo() {
  if (BACKEND_AVAILABLE) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/system-info`);
      const data = await response.json();
      
      if (data.status === 'success') {
        return {
          processor_count: data.processor_count,
          total_ram_gb: data.total_ram_gb,
          hostname: data.hostname,
          platform: data.platform,
          source: 'backend'
        };
      }
    } catch (error) {
      console.warn('Error fetching system info:', error);
    }
  }
  
  // Fallback: default values
  return {
    processor_count: 8,
    total_ram_gb: 16,
    hostname: 'Unknown',
    platform: 'Unknown',
    source: 'simulation'
  };
}

/**
 * Get metrics history for graphs
 */
async function getMetricsHistory() {
  if (BACKEND_AVAILABLE) {
    try {
      const response = await fetch(`${BACKEND_URL}/api/system-metrics-history`);
      const data = await response.json();
      
      return {
        cpu: data.cpu || [],
        ram: data.ram || [],
        disk: data.disk || [],
        timestamps: data.timestamps || [],
        source: 'backend'
      };
    } catch (error) {
      console.warn('Error fetching history:', error);
    }
  }
  
  // Empty fallback
  return {
    cpu: [],
    ram: [],
    disk: [],
    timestamps: [],
    source: 'simulation'
  };
}

/**
 * Get status message based on metric value
 */
function getStatusMessage(metric_type, value) {
  if (metric_type === 'cpu') {
    if (value > 80) return 'HEAVY LOAD - Close background apps';
    if (value > 60) return 'Moderate load - System working';
    return 'Light load - CPU has capacity';
  }
  
  if (metric_type === 'ram') {
    if (value > 85) return '⚠ CRITICAL - Memory almost full!';
    if (value > 70) return '⚠ HIGH - Consider closing apps';
    if (value > 50) return '✓ Normal - System has enough memory';
    return '✓ Good - Plenty of available memory';
  }
  
  if (metric_type === 'disk') {
    if (value > 90) return '⚠ CRITICAL - Disk almost full!';
    if (value > 80) return '⚠ HIGH - Low disk space';
    return '✓ Normal - Plenty of disk space';
  }
  
  return 'Unknown';
}

/**
 * Format metric value for display
 */
function formatMetric(value, type) {
  if (type === 'percent') {
    return value.toFixed(1) + '%';
  }
  if (type === 'mb') {
    return value.toFixed(1) + ' MB';
  }
  if (type === 'gb') {
    return value.toFixed(1) + ' GB';
  }
  return value;
}

// Export functions for use in main app
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    initializeBackend,
    getSystemMetrics,
    getSystemInfo,
    getMetricsHistory,
    getStatusMessage,
    formatMetric
  };
}
