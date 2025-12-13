/**
 * Caregiver Dashboard - UI Layer
 * Single Responsibility: Handle all UI interactions and updates
 */

class CaregiverUI {
    constructor() {
        this.currentFilter = 'all';
        this.init();
    }
    
    init() {
        this.loadPatientStatus();
        this.loadLocation();
        this.loadBattery();
        this.loadAlerts();
        this.initAlertFilters();
        this.startPolling();
    }
    
    // ==================== Patient Status ====================
    
    async loadPatientStatus() {
        try {
            const result = await CaregiverAPI.getPatientStatus();
            
            if (result.success) {
                const status = result.status;
                document.getElementById('currentActivity').textContent = status.current_activity;
                document.getElementById('currentLocation').textContent = status.location;
                document.getElementById('lastMovement').textContent = status.last_movement;
                document.getElementById('wellbeingScore').textContent = `${status.wellbeing_score}/10`;
            }
        } catch (error) {
            console.error('Failed to load patient status:', error);
            NovaBot.showToast('Failed to load patient status', 'error');
        }
    }
    
    // ==================== Location ====================
    
    async loadLocation() {
        try {
            const result = await CaregiverAPI.getLocation();
            
            if (result.success) {
                const location = result.location;
                const coords = `${location.latitude.toFixed(4)}, ${location.longitude.toFixed(4)}`;
                
                document.getElementById('locationText').textContent = location.address;
                document.getElementById('coordinates').textContent = coords;
                document.getElementById('locationAccuracy').textContent = `±${location.accuracy}m`;
                
                // In real implementation, would render map here
                // Example: initMap(location.latitude, location.longitude);
            }
        } catch (error) {
            console.error('Failed to load location:', error);
        }
    }
    
    // ==================== Battery ====================
    
    async loadBattery() {
        try {
            const result = await CaregiverAPI.getBattery();
            
            if (result.success) {
                const battery = result.battery;
                const level = battery.level;
                
                document.getElementById('batteryLevel').textContent = `${level}%`;
                document.getElementById('batteryBar').style.width = `${level}%`;
                
                // Update color based on level
                const bar = document.getElementById('batteryBar');
                bar.classList.remove('bg-green-500', 'bg-yellow-500', 'bg-red-500');
                
                if (level > 50) {
                    bar.classList.add('bg-green-500');
                } else if (level > 20) {
                    bar.classList.add('bg-yellow-500');
                } else {
                    bar.classList.add('bg-red-500');
                }
                
                // Show warning if low
                if (level < 20) {
                    NovaBot.showToast(`Warning: Battery low (${level}%)`, 'warning');
                }
            }
        } catch (error) {
            console.error('Failed to load battery:', error);
        }
    }
    
    // ==================== Alerts ====================
    
    initAlertFilters() {
        const filters = document.querySelectorAll('.alert-filter');
        
        filters.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active state
                filters.forEach(f => {
                    f.classList.remove('active', 'bg-blue-500', 'text-white');
                    f.classList.add('bg-gray-200', 'text-gray-700');
                });
                
                btn.classList.add('active', 'bg-blue-500', 'text-white');
                btn.classList.remove('bg-gray-200', 'text-gray-700');
                
                // Load filtered alerts
                this.currentFilter = btn.dataset.filter;
                this.loadAlerts();
            });
        });
    }
    
    async loadAlerts() {
        try {
            const severity = this.currentFilter === 'all' ? null : this.currentFilter;
            const result = await CaregiverAPI.getAlerts(50, severity);
            
            if (result.success) {
                this.renderAlerts(result.alerts);
                document.getElementById('unreadCount').textContent = result.unread;
                
                // Hide badge if no unread
                const badge = document.getElementById('unreadCount');
                if (result.unread === 0) {
                    badge.classList.add('hidden');
                } else {
                    badge.classList.remove('hidden');
                }
            }
        } catch (error) {
            console.error('Failed to load alerts:', error);
        }
    }
    
    renderAlerts(alerts) {
        const container = document.getElementById('alertsList');
        
        if (alerts.length === 0) {
            container.innerHTML = '<p class="text-gray-400 italic text-sm">No alerts to display</p>';
            return;
        }
        
        container.innerHTML = alerts.map(alert => {
            const severityColors = {
                'critical': 'bg-red-50 border-red-300',
                'high': 'bg-orange-50 border-orange-300',
                'medium': 'bg-yellow-50 border-yellow-300',
                'low': 'bg-blue-50 border-blue-300'
            };
            
            const severityBadges = {
                'critical': 'bg-red-500',
                'high': 'bg-orange-500',
                'medium': 'bg-yellow-500',
                'low': 'bg-blue-500'
            };
            
            const colorClass = severityColors[alert.severity] || 'bg-gray-50 border-gray-300';
            const badgeClass = severityBadges[alert.severity] || 'bg-gray-500';
            const opacity = alert.read ? 'opacity-50' : '';
            
            return `
                <div class="alert-item ${colorClass} ${opacity} border-2 rounded-lg p-4 cursor-pointer hover:shadow-md transition-all"
                     data-alert-id="${alert.id}" 
                     ${!alert.read ? 'data-unread="true"' : ''}>
                    <div class="flex items-start justify-between mb-2">
                        <div class="flex-1">
                            <div class="flex items-center space-x-2 mb-1">
                                <span class="${badgeClass} text-white px-2 py-1 rounded text-xs font-bold uppercase">
                                    ${alert.severity}
                                </span>
                                <span class="text-sm font-semibold text-gray-700">${alert.type}</span>
                            </div>
                            <p class="text-sm text-gray-600">${alert.message}</p>
                        </div>
                        ${!alert.read ? '<div class="w-2 h-2 bg-red-500 rounded-full ml-2"></div>' : ''}
                    </div>
                    <div class="flex items-center justify-between text-xs text-gray-500">
                        <span>📍 ${alert.location}</span>
                        <span>${NovaBot.formatRelativeTime(alert.timestamp)}</span>
                    </div>
                </div>
            `;
        }).join('');
        
        // Add click handlers
        container.querySelectorAll('.alert-item[data-unread="true"]').forEach(item => {
            item.addEventListener('click', async () => {
                const alertId = item.dataset.alertId;
                await this.markAlertRead(alertId);
            });
        });
    }
    
    async markAlertRead(alertId) {
        try {
            const result = await CaregiverAPI.markAlertRead(alertId);
            
            if (result.success) {
                // Reload alerts
                this.loadAlerts();
            }
        } catch (error) {
            console.error('Failed to mark alert as read:', error);
        }
    }
    
    // ==================== Polling ====================
    
    startPolling() {
        // Poll patient status every 10 seconds
        setInterval(() => {
            this.loadPatientStatus();
        }, 10000);
        
        // Poll location every 30 seconds
        setInterval(() => {
            this.loadLocation();
        }, 30000);
        
        // Poll battery every 60 seconds
        setInterval(() => {
            this.loadBattery();
        }, 60000);
        
        // Poll alerts every 15 seconds
        setInterval(() => {
            this.loadAlerts();
        }, 15000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.caregiverUI = new CaregiverUI();
});

