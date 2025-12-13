/**
 * Emergency Service Dashboard - UI Layer
 * Single Responsibility: Handle all UI interactions and updates
 */

class EmergencyUI {
    constructor() {
        this.startTime = new Date();
        this.emergencyId = document.getElementById('emergencyId')?.textContent || 'emg_001';
        EmergencyAPI.init(this.emergencyId);
        this.init();
    }
    
    init() {
        this.loadEmergencyData();
        this.loadCriticalData();
        this.loadEnvironmentalData();
        this.initStatusUpdate();
        this.initReassurance();
        this.startTimer();
    }
    
    // ==================== Timer ====================
    
    startTimer() {
        setInterval(() => {
            const now = new Date();
            const elapsed = Math.floor((now - this.startTime) / 1000);
            
            const hours = Math.floor(elapsed / 3600).toString().padStart(2, '0');
            const minutes = Math.floor((elapsed % 3600) / 60).toString().padStart(2, '0');
            const seconds = (elapsed % 60).toString().padStart(2, '0');
            
            document.getElementById('timeElapsed').textContent = `${hours}:${minutes}:${seconds}`;
        }, 1000);
    }
    
    // ==================== Emergency Data ====================
    
    async loadEmergencyData() {
        try {
            const result = await EmergencyAPI.getEmergencyDetails();
            
            if (result.success) {
                const emergency = result.emergency;
                
                // Event nature
                document.getElementById('eventNature').textContent = emergency.type.replace(/_/g, ' ');
                
                // Location
                const loc = emergency.location;
                document.getElementById('coordinates').textContent = 
                    `${loc.latitude.toFixed(4)}, ${loc.longitude.toFixed(4)}`;
                document.getElementById('address').textContent = loc.address;
                document.getElementById('unitFloor').textContent = loc.unit || 'N/A';
                
                // Patient data
                const patient = emergency.patient;
                document.getElementById('patientAge').textContent = patient.age;
                document.getElementById('patientGender').textContent = patient.name.split(' ')[0];
                
                // Allergies
                document.getElementById('allergies').textContent = 
                    patient.allergies.join(', ') || 'None reported';
                
                // Nearest responders
                this.renderNearestResponders(emergency.nearest_responders);
                
                // Load nearby facilities
                this.loadNearbyFacilities(loc.latitude, loc.longitude);
            }
        } catch (error) {
            console.error('Failed to load emergency data:', error);
            NovaBot.showToast('Failed to load emergency data', 'error');
        }
    }
    
    async loadCriticalData() {
        try {
            const result = await EmergencyAPI.getCriticalData();
            
            if (result.success) {
                const critical = result.critical_data;
                
                // Location access notes
                document.getElementById('accessNotes').textContent = 
                    critical.location.access_notes;
                
                // Patient summary
                const summary = critical.patient_summary;
                document.getElementById('livingStatus').textContent = 
                    summary.living_situation.split(' ').slice(0, 2).join(' ');
                
                // Medications
                const medsList = document.getElementById('medications');
                medsList.innerHTML = critical.medications.map(med => 
                    `<li class="flex items-center text-gray-300"><span class="w-2 h-2 bg-accent-blue rounded-full mr-2"></span>${med}</li>`
                ).join('');
                
                // Immediate concerns
                const concernsList = document.getElementById('immediateConcerns');
                concernsList.innerHTML = critical.immediate_concerns.map(concern => `
                    <li class="glass rounded-lg p-4 border-l-4 border-accent-red flex items-center">
                        <span class="text-accent-red mr-3 text-xl">●</span>
                        <span class="font-semibold text-white">${concern}</span>
                    </li>
                `).join('');
                
                // Healthcare proxy
                const proxy = critical.healthcare_proxy;
                document.getElementById('healthcareProxy').innerHTML = `
                    <p class="font-semibold text-white">${proxy.name}</p>
                    <p class="text-sm text-gray-400">${proxy.phone}</p>
                    <div class="mt-2 flex items-center space-x-2">
                        <span class="text-sm ${proxy.contacted ? 'text-accent-green' : 'text-gray-400'}">
                            ${proxy.contacted ? '✓ Contacted' : '○ Not yet contacted'}
                        </span>
                    </div>
                    ${proxy.contacted ? `<p class="text-sm text-gray-400 mt-1">ETA: ${proxy.eta}</p>` : ''}
                `;
            }
        } catch (error) {
            console.error('Failed to load critical data:', error);
        }
    }
    
    async loadEnvironmentalData() {
        try {
            const result = await EmergencyAPI.getEnvironmentalData();
            
            if (result.success) {
                const env = result.environmental_data;
                const container = document.getElementById('environmentalData');
                
                const items = [
                    { label: 'Smoke', value: env.smoke_detected ? '⚠️ YES' : '✓ No', alert: env.smoke_detected },
                    { label: 'Temperature', value: `${env.temperature}°C`, alert: false },
                    { label: 'CO Level', value: `${env.carbon_monoxide} ppm`, alert: env.carbon_monoxide > 0 },
                    { label: 'Air Quality', value: env.air_quality, alert: false },
                    { label: 'Lighting', value: env.lighting, alert: false },
                    { label: 'Audio', value: env.audio_detected, alert: true },
                    { label: 'Movement', value: env.movement_detected, alert: false },
                    { label: 'Doors', value: env.doors_locked ? '🔒 Locked' : '🔓 Unlocked', alert: env.doors_locked }
                ];
                
                container.innerHTML = items.map(item => {
                    const bgClass = item.alert ? 'glass border-accent-orange' : 'glass border-dark-600';
                    const textClass = item.alert ? 'text-accent-orange' : 'text-white';
                    
                    return `
                        <div class="${bgClass} rounded-lg p-4 border">
                            <p class="text-xs text-gray-400 mb-1">${item.label}</p>
                            <p class="font-semibold ${textClass}">${item.value}</p>
                        </div>
                    `;
                }).join('');
            }
        } catch (error) {
            console.error('Failed to load environmental data:', error);
        }
    }
    
    renderNearestResponders(responders) {
        const container = document.getElementById('nearestResponders');
        
        if (!responders || responders.length === 0) {
            container.innerHTML = '<p class="text-gray-400 italic">No units available</p>';
            return;
        }
        
        container.innerHTML = responders.map((unit, index) => {
            if (index === 0) {
                return `
                    <div class="bg-accent-blue/20 border-2 border-accent-blue rounded-lg p-4">
                        <div class="flex items-center justify-between mb-2">
                            <span class="font-bold text-white">${unit.unit}</span>
                            <span class="text-xs bg-accent-blue text-white px-3 py-1 rounded-full font-bold">NEAREST</span>
                        </div>
                        <p class="text-sm text-gray-300 mb-1">📍 ${unit.distance} away</p>
                        <p class="text-sm font-semibold text-accent-blue">⏱️ ETA: ${unit.eta}</p>
                    </div>
                `;
            } else {
                return `
                    <div class="glass rounded-lg p-4 border border-dark-600">
                        <div class="flex items-center justify-between mb-2">
                            <span class="font-bold text-white">${unit.unit}</span>
                        </div>
                        <p class="text-sm text-gray-400 mb-1">📍 ${unit.distance} away</p>
                        <p class="text-sm font-semibold text-gray-300">⏱️ ETA: ${unit.eta}</p>
                    </div>
                `;
            }
        }).join('');
    }
    
    async loadNearbyFacilities(lat, lng) {
        try {
            const result = await EmergencyAPI.getNearbyFacilities(lat, lng);
            
            if (result.success) {
                const container = document.getElementById('nearbyFacilities');
                const facilities = result.facilities;
                
                container.innerHTML = facilities.map((facility, index) => {
                    const levelBg = facility.trauma_level === 'Level I' ? 'bg-accent-green/20 text-accent-green' : 'bg-accent-blue/20 text-accent-blue';
                    
                    return `
                        <div class="glass rounded-lg p-4 border border-dark-600">
                            <div class="flex items-center justify-between mb-2">
                                <span class="font-bold text-white text-sm">${facility.name}</span>
                                ${facility.trauma_level !== 'N/A' ? 
                                    `<span class="text-xs ${levelBg} px-2 py-1 rounded-full font-bold">${facility.trauma_level}</span>` 
                                    : ''}
                            </div>
                            <p class="text-xs text-gray-400 mb-2">${facility.type}</p>
                            <div class="flex items-center justify-between text-xs">
                                <span class="text-gray-400">📍 ${facility.distance} km</span>
                                <span class="text-gray-400">⏱️ ${facility.eta}</span>
                            </div>
                            <div class="flex items-center justify-between text-xs mt-2">
                                <span class="text-gray-400">Wait: ${facility.current_wait}</span>
                                <span class="font-semibold ${facility.beds_available > 2 ? 'text-accent-green' : 'text-accent-orange'}">
                                    🛏️ ${facility.beds_available} beds
                                </span>
                            </div>
                        </div>
                    `;
                }).join('');
            }
        } catch (error) {
            console.error('Failed to load nearby facilities:', error);
        }
    }
    
    // ==================== Status Update ====================
    
    initStatusUpdate() {
        document.getElementById('submitStatusBtn').addEventListener('click', async () => {
            await this.updateStatus();
        });
    }
    
    async updateStatus() {
        try {
            const status = document.getElementById('statusSelect').value;
            const responderId = 'responder_001'; // Would come from auth
            
            NovaBot.showLoading(true);
            const result = await EmergencyAPI.updateStatus(status, responderId);
            
            if (result.success) {
                NovaBot.showToast(`Status updated to ${status}`, 'success');
                
                // Update status display
                const statusStyles = {
                    'DISPATCHED': { bg: 'bg-accent-orange/20', border: 'border-accent-orange', text: 'text-accent-orange', icon: '⏳' },
                    'EN_ROUTE': { bg: 'bg-accent-blue/20', border: 'border-accent-blue', text: 'text-accent-blue', icon: '🚑' },
                    'ON_SCENE': { bg: 'bg-accent-purple/20', border: 'border-accent-purple', text: 'text-accent-purple', icon: '📍' },
                    'RESOLVED': { bg: 'bg-accent-green/20', border: 'border-accent-green', text: 'text-accent-green', icon: '✓' },
                    'CANCELLED': { bg: 'bg-dark-600', border: 'border-dark-500', text: 'text-gray-400', icon: '✕' }
                };
                
                const style = statusStyles[status] || statusStyles['DISPATCHED'];
                document.getElementById('responseStatus').innerHTML = `
                    <div class="${style.bg} border-2 ${style.border} rounded-lg p-4">
                        <p class="font-bold ${style.text} text-sm mb-1">${style.icon} ${status.replace(/_/g, ' ')}</p>
                        <p class="text-xs text-gray-300">${result.message}</p>
                    </div>
                `;
            }
        } catch (error) {
            NovaBot.showToast('Failed to update status', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
    
    // ==================== Reassurance ====================
    
    initReassurance() {
        document.getElementById('sendReassuranceBtn').addEventListener('click', async () => {
            await this.sendReassurance();
        });
    }
    
    async sendReassurance() {
        try {
            const message = 'Help is on the way. Please stay calm. Emergency responders will be with you shortly.';
            
            NovaBot.showLoading(true);
            const result = await EmergencyAPI.sendReassurance(message);
            
            if (result.success) {
                NovaBot.showToast('Reassurance message sent to patient', 'success');
            }
        } catch (error) {
            NovaBot.showToast('Failed to send reassurance', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.emergencyUI = new EmergencyUI();
});

