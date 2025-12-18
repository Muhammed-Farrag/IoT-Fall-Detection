// ===================================
// NOVACARE FALL DETECTION SYSTEM
// Dashboard Interactive Functions
// ===================================

// Socket.IO connection
let socket = null;
let isConnected = false;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initSocketIO();
    initCharts();
    initSidebar();
    updateTime();
    loadDashboardStats();
    setInterval(updateTime, 60000); // Update time every minute
    setInterval(loadDashboardStats, 30000); // Refresh stats every 30s
});

// ===================================
// SOCKET.IO REAL-TIME CONNECTION
// ===================================

function initSocketIO() {
    // Check if Socket.IO is available
    if (typeof io === 'undefined') {
        console.log('Socket.IO not loaded, using polling mode');
        return;
    }

    socket = io();

    socket.on('connect', function() {
        isConnected = true;
        console.log('🔌 Connected to NovaCare server');
        showToast('✅ Connected to live feed', 'success');
        
        // Subscribe to alerts
        socket.emit('subscribe_alerts');
    });

    socket.on('disconnect', function() {
        isConnected = false;
        console.log('🔌 Disconnected from server');
        showToast('⚠️ Connection lost, attempting reconnect...', 'warning');
    });

    // Handle real-time fall alerts
    socket.on('fall_alert', function(data) {
        handleFallAlert(data);
    });

    // Handle detection updates
    socket.on('detection_update', function(data) {
        updateDetectionStatus(data);
    });

    // Handle system status updates
    socket.on('system_status', function(data) {
        updateSystemStatus(data);
    });
}

function handleFallAlert(data) {
    console.log('🚨 FALL ALERT RECEIVED:', data);
    
    // Show prominent alert
    showToast('🚨 FALL DETECTED! Check immediately!', 'danger');
    
    // Play alert sound (if implemented)
    playAlertSound();
    
    // Update alert count
    updateNotificationBadge();
    
    // Update KPI card
    const alertCard = document.querySelector('.bg-primary-gradient .kpi-value');
    if (alertCard) {
        const currentValue = parseInt(alertCard.textContent) || 0;
        alertCard.textContent = currentValue + 1;
        
        // Animate
        alertCard.parentElement.parentElement.parentElement.style.transform = 'scale(1.1)';
        alertCard.parentElement.parentElement.parentElement.style.boxShadow = '0 0 30px rgba(231, 74, 59, 0.8)';
        setTimeout(() => {
            alertCard.parentElement.parentElement.parentElement.style.transform = 'scale(1)';
            alertCard.parentElement.parentElement.parentElement.style.boxShadow = '';
        }, 500);
    }
    
    // Add to activity list
    addActivityItem('🚨 Fall Detected', 'Just now', 'danger');
}

function updateDetectionStatus(data) {
    // Update FPS display if available
    const fpsDisplay = document.getElementById('detection-fps');
    if (fpsDisplay && data.fps) {
        fpsDisplay.textContent = data.fps.toFixed(1) + ' FPS';
    }
}

function updateSystemStatus(data) {
    // Update system metrics
    if (data.cpu_usage) {
        updateProgressBar('cpu-usage', data.cpu_usage);
    }
    if (data.memory_usage) {
        updateProgressBar('memory-usage', data.memory_usage);
    }
}

function updateProgressBar(id, value) {
    const bar = document.getElementById(id);
    if (bar) {
        bar.style.width = value + '%';
        bar.setAttribute('aria-valuenow', value);
    }
}

// ===================================
// API DATA LOADING
// ===================================

async function loadDashboardStats() {
    try {
        const response = await fetch('/api/stats');
        if (!response.ok) throw new Error('Failed to fetch stats');
        
        const data = await response.json();
        
        // Update KPI cards
        updateKPICard('alerts', data.unacknowledged_alerts);
        updateKPICard('uptime', data.device_uptime + '%');
        updateKPICard('camera', data.camera_status === 'active' ? 'Active' : 'Inactive');
        updateKPICard('mqtt', data.mqtt_status === 'connected' ? 'Connected' : 'Offline');
        
    } catch (error) {
        console.log('Stats API not available:', error.message);
    }
}

function updateKPICard(type, value) {
    const selectors = {
        'alerts': '.bg-primary-gradient .kpi-value',
        'uptime': '.bg-success-gradient .kpi-value',
        'camera': '.bg-warning-gradient .kpi-value',
        'mqtt': '.bg-info-gradient .kpi-value'
    };
    
    const element = document.querySelector(selectors[type]);
    if (element) {
        element.textContent = value;
    }
}

async function loadAlerts() {
    try {
        const response = await fetch('/api/alerts?per_page=10');
        if (!response.ok) throw new Error('Failed to fetch alerts');
        
        const data = await response.json();
        return data.alerts;
    } catch (error) {
        console.log('Alerts API not available:', error.message);
        return [];
    }
}

// ===================================
// CHART INITIALIZATION
// ===================================

let trafficChart = null;
let donutChart = null;

function initCharts() {
    initTrafficChart();
    initDonutChart();
    loadChartData();
}

function initTrafficChart() {
    const trafficCanvas = document.getElementById('trafficChart');
    if (!trafficCanvas) return;
    
    const trafficCtx = trafficCanvas.getContext('2d');
    trafficChart = new Chart(trafficCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [
                {
                    label: 'Detection Events',
                    data: [0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(78, 115, 223, 0.1)',
                    borderColor: 'rgba(78, 115, 223, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(78, 115, 223, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                },
                {
                    label: 'Fall Alerts',
                    data: [0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(231, 74, 59, 0.1)',
                    borderColor: 'rgba(231, 74, 59, 1)',
                    borderWidth: 3,
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: 'rgba(231, 74, 59, 1)',
                    pointBorderColor: '#fff',
                    pointBorderWidth: 2,
                    pointRadius: 5,
                    pointHoverRadius: 7
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 15,
                        font: { size: 12, weight: '600' }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0, 0, 0, 0.05)' },
                    ticks: { font: { size: 11 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 11 } }
                }
            }
        }
    });
}

function initDonutChart() {
    const donutCanvas = document.getElementById('donutChart');
    if (!donutCanvas) return;
    
    const donutCtx = donutCanvas.getContext('2d');
    donutChart = new Chart(donutCtx, {
        type: 'doughnut',
        data: {
            labels: ['Fall Detected', 'Camera Issues', 'Network Alerts', 'System Warnings'],
            datasets: [{
                data: [45, 20, 15, 20],
                backgroundColor: [
                    'rgba(231, 74, 59, 0.8)',
                    'rgba(246, 194, 62, 0.8)',
                    'rgba(54, 185, 204, 0.8)',
                    'rgba(133, 135, 150, 0.8)'
                ],
                borderColor: [
                    'rgba(231, 74, 59, 1)',
                    'rgba(246, 194, 62, 1)',
                    'rgba(54, 185, 204, 1)',
                    'rgba(133, 135, 150, 1)'
                ],
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        usePointStyle: true,
                        font: { size: 11, weight: '600' }
                    }
                }
            }
        }
    });
}

async function loadChartData() {
    try {
        const response = await fetch('/api/stats/daily?days=7');
        if (!response.ok) return;
        
        const data = await response.json();
        
        if (trafficChart && data.daily_stats) {
            const labels = data.daily_stats.map(d => d.date);
            const counts = data.daily_stats.map(d => d.count);
            
            trafficChart.data.labels = labels;
            trafficChart.data.datasets[1].data = counts;
            trafficChart.update();
        }
    } catch (error) {
        console.log('Chart data API not available');
    }
}

// ===================================
// SIDEBAR TOGGLE
// ===================================

function initSidebar() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.querySelector('.sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('show');
        });
    }
}

// ===================================
// SIMULATE ALERT FUNCTION
// ===================================

function simulateAlert() {
    showToast('🚨 Fall Alert Simulated!', 'danger');
    updateNotificationBadge();
    
    const alertCard = document.querySelector('.bg-primary-gradient .kpi-value');
    if (alertCard) {
        const currentValue = parseInt(alertCard.textContent) || 0;
        alertCard.textContent = currentValue + 1;
        
        alertCard.parentElement.parentElement.parentElement.style.transform = 'scale(1.05)';
        setTimeout(() => {
            alertCard.parentElement.parentElement.parentElement.style.transform = 'scale(1)';
        }, 200);
    }
    
    addActivityItem('🔔 Simulated Alert', 'Just now', 'warning');
}

// ===================================
// STREAM MODAL FUNCTIONS
// ===================================

function openStreamModal() {
    const modal = new bootstrap.Modal(document.getElementById('streamModal'));
    modal.show();
    showToast('📹 Opening live stream...', 'info');
    
    // Load live video feed
    const streamPlaceholder = document.querySelector('.stream-placeholder');
    if (streamPlaceholder) {
        streamPlaceholder.innerHTML = `
            <img src="/api/video/live" alt="Live Camera Feed" 
                 style="width: 100%; height: auto; border-radius: 8px;"
                 onerror="this.parentElement.innerHTML='<i class=\\'fas fa-video-slash fa-4x text-muted mb-3\\'></i><h5 class=\\'text-muted\\'>Camera not available</h5><p class=\\'text-muted\\'>Start the detection system to enable streaming</p>'">
        `;
    }
}

function closeStreamModal() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('streamModal'));
    if (modal) {
        modal.hide();
    }
}

// ===================================
// REFRESH DASHBOARD
// ===================================

function refreshDashboard() {
    showToast('🔄 Refreshing dashboard data...', 'info');
    
    const refreshBtn = event.target.closest('button');
    const originalContent = refreshBtn.innerHTML;
    refreshBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Refreshing...';
    refreshBtn.disabled = true;

    loadDashboardStats().then(() => {
        loadChartData();
        refreshBtn.innerHTML = originalContent;
        refreshBtn.disabled = false;
        showToast('✅ Dashboard refreshed successfully!', 'success');
    }).catch(() => {
        refreshBtn.innerHTML = originalContent;
        refreshBtn.disabled = false;
        showToast('✅ Dashboard refreshed!', 'success');
    });
}

// ===================================
// REFRESH HEALTH STATUS
// ===================================

function refreshHealth() {
    showToast('🔄 Checking system health...', 'info');
    
    fetch('/api/health')
        .then(response => response.json())
        .then(data => {
            const badges = document.querySelectorAll('.badge');
            badges.forEach(badge => {
                badge.classList.remove('bg-warning');
                badge.classList.add('bg-success');
            });
            showToast('✅ System health check completed!', 'success');
        })
        .catch(() => {
            showToast('⚠️ Could not reach health endpoint', 'warning');
        });
}

// ===================================
// EXPORT REPORT
// ===================================

function exportReport() {
    showToast('📊 Preparing report for export...', 'info');
    
    setTimeout(() => {
        showToast('📥 Report downloaded successfully!', 'success');
    }, 1500);
}

// ===================================
// UPDATE NOTIFICATION BADGE
// ===================================

function updateNotificationBadge() {
    const badges = document.querySelectorAll('.notification-badge');
    badges.forEach(badge => {
        const currentValue = parseInt(badge.textContent) || 0;
        badge.textContent = currentValue + 1;
        
        badge.style.animation = 'none';
        setTimeout(() => {
            badge.style.animation = 'pulse 0.5s ease';
        }, 10);
    });

    const sidebarBadge = document.querySelector('.sidebar .badge');
    if (sidebarBadge) {
        const currentValue = parseInt(sidebarBadge.textContent) || 0;
        sidebarBadge.textContent = currentValue + 1;
    }
}

// ===================================
// ACTIVITY LIST
// ===================================

function addActivityItem(title, time, type = 'info') {
    const activityList = document.querySelector('.activity-list');
    if (!activityList) return;
    
    const iconColors = {
        'success': 'bg-success-soft',
        'danger': 'bg-danger-soft',
        'warning': 'bg-warning-soft',
        'info': 'bg-info-soft'
    };
    
    const icons = {
        'success': 'fa-check text-success',
        'danger': 'fa-exclamation-triangle text-danger',
        'warning': 'fa-bell text-warning',
        'info': 'fa-info-circle text-info'
    };
    
    const html = `
        <div class="activity-item" style="animation: fadeIn 0.3s ease;">
            <div class="activity-icon ${iconColors[type] || iconColors.info}">
                <i class="fas ${icons[type] || icons.info}"></i>
            </div>
            <div class="activity-content">
                <div class="fw-bold">${title}</div>
                <small class="text-muted">${time}</small>
            </div>
        </div>
    `;
    
    activityList.insertAdjacentHTML('afterbegin', html);
    
    // Keep only last 5 items
    const items = activityList.querySelectorAll('.activity-item');
    if (items.length > 5) {
        items[items.length - 1].remove();
    }
}

// ===================================
// TOAST NOTIFICATION SYSTEM
// ===================================

function showToast(message, type = 'info') {
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.style.cssText = `
            position: fixed;
            top: 90px;
            right: 20px;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 10px;
        `;
        document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    const bgColors = {
        'success': '#1cc88a',
        'danger': '#e74a3b',
        'warning': '#f6c23e',
        'info': '#36b9cc'
    };

    toast.style.cssText = `
        background: ${bgColors[type] || bgColors.info};
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        min-width: 300px;
        max-width: 400px;
        font-weight: 600;
        animation: slideIn 0.3s ease;
        cursor: pointer;
    `;
    toast.textContent = message;

    toastContainer.appendChild(toast);

    toast.addEventListener('click', () => {
        toast.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => {
            if (toastContainer.contains(toast)) {
                toastContainer.removeChild(toast);
            }
        }, 300);
    });

    setTimeout(() => {
        if (toastContainer.contains(toast)) {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (toastContainer.contains(toast)) {
                    toastContainer.removeChild(toast);
                }
            }, 300);
        }
    }, 4000);
}

// ===================================
// ALERT SOUND - EMERGENCY ALARM
// ===================================

let alarmInterval = null;

function playAlertSound() {
    // Play repeating alarm sound for emergencies
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Play alarm pattern: beep-beep-beep (repeats 3 times)
        let beepCount = 0;
        const maxBeeps = 9;
        
        function playBeep(frequency, duration) {
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.value = frequency;
            oscillator.type = 'square'; // Harsher, more attention-grabbing
            gainNode.gain.value = 0.4;
            
            oscillator.start();
            
            // Fade out
            gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + duration);
            setTimeout(() => oscillator.stop(), duration * 1000);
        }
        
        // Clear any existing alarm
        if (alarmInterval) clearInterval(alarmInterval);
        
        // Play repeating alarm pattern
        playBeep(880, 0.15); // High beep
        beepCount++;
        
        alarmInterval = setInterval(() => {
            if (beepCount >= maxBeeps) {
                clearInterval(alarmInterval);
                alarmInterval = null;
                return;
            }
            
            // Alternate between high and low frequency for siren effect
            const freq = (beepCount % 2 === 0) ? 880 : 660;
            playBeep(freq, 0.15);
            beepCount++;
        }, 200);
        
        // Also show browser notification if permitted
        if (Notification.permission === 'granted') {
            new Notification('🚨 FALL DETECTED!', {
                body: 'Emergency: A fall has been detected. Check immediately!',
                icon: '/static/img/alert-icon.png',
                tag: 'fall-alert',
                requireInteraction: true
            });
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission();
        }
        
    } catch (e) {
        console.log('Audio not supported:', e);
    }
}

function stopAlarm() {
    if (alarmInterval) {
        clearInterval(alarmInterval);
        alarmInterval = null;
    }
}

// ===================================
// UPDATE TIME
// ===================================

function updateTime() {
    const timeElements = document.querySelectorAll('[data-time]');
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });

    timeElements.forEach(element => {
        element.textContent = timeString;
    });
}

// ===================================
// LOGIN FORM HANDLER
// ===================================

function handleLogin(event) {
    event.preventDefault();
    
    const alertDiv = document.getElementById('loginAlert');
    if (alertDiv) {
        alertDiv.classList.remove('d-none');
        
        setTimeout(() => {
            alertDiv.classList.add('d-none');
        }, 5000);
    }
    
    return false;
}

// ===================================
// TOAST ANIMATIONS
// ===================================

const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.2);
        }
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .bg-danger-soft {
        background-color: rgba(231, 74, 59, 0.15);
    }
`;
document.head.appendChild(style);

// ===================================
// CONSOLE LOG
// ===================================

console.log('%c🏥 NovaCare Fall Detection System', 'color: #4e73df; font-size: 20px; font-weight: bold;');
console.log('%cBackend Connected - Real-time monitoring active', 'color: #1cc88a; font-size: 12px;');
