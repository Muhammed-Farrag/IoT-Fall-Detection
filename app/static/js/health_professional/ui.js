/**
 * Health Professional Dashboard - UI Layer
 * Single Responsibility: Handle all UI interactions and updates
 */

class HealthProfessionalUI {
    constructor() {
        this.init();
    }
    
    init() {
        this.loadCurrentVitals();
        this.loadHealthTrends();
        this.loadMedicationAdherence();
        this.loadFallIncidents();
        this.initGenerateReport();
        this.initClinicalNotes();
        this.startPolling();
    }
    
    // ==================== Current Vitals ====================
    
    async loadCurrentVitals() {
        try {
            const result = await HealthProfessionalAPI.getCurrentVitals();
            
            if (result.success) {
                const vitals = result.vitals;
                
                // Heart Rate
                document.getElementById('heartRate').textContent = vitals.heart_rate.value;
                document.getElementById('hrStatus').textContent = vitals.heart_rate.status;
                this.updateStatusBadge('hrStatus', vitals.heart_rate.status);
                
                // Blood Pressure
                document.getElementById('bloodPressure').textContent = 
                    `${vitals.blood_pressure.systolic}/${vitals.blood_pressure.diastolic}`;
                document.getElementById('bpStatus').textContent = vitals.blood_pressure.status;
                this.updateStatusBadge('bpStatus', vitals.blood_pressure.status);
                
                // Oxygen Saturation
                document.getElementById('oxygenSat').textContent = vitals.oxygen_saturation.value;
                document.getElementById('spo2Status').textContent = vitals.oxygen_saturation.status;
                this.updateStatusBadge('spo2Status', vitals.oxygen_saturation.status);
                
                // Temperature
                document.getElementById('temperature').textContent = vitals.temperature.value;
                document.getElementById('tempStatus').textContent = vitals.temperature.status;
                this.updateStatusBadge('tempStatus', vitals.temperature.status);
                
                // Respiratory Rate
                document.getElementById('respRate').textContent = vitals.respiratory_rate.value;
                document.getElementById('rrStatus').textContent = vitals.respiratory_rate.status;
                this.updateStatusBadge('rrStatus', vitals.respiratory_rate.status);
            }
        } catch (error) {
            console.error('Failed to load vitals:', error);
            NovaBot.showToast('Failed to load vital signs', 'error');
        }
    }
    
    updateStatusBadge(elementId, status) {
        const element = document.getElementById(elementId);
        element.classList.remove('bg-accent-green/20', 'text-accent-green', 'bg-accent-orange/20', 'text-accent-orange', 'bg-accent-red/20', 'text-accent-red');
        
        if (status.toLowerCase() === 'normal') {
            element.classList.add('bg-accent-green/20', 'text-accent-green');
        } else if (status.toLowerCase() === 'warning') {
            element.classList.add('bg-accent-orange/20', 'text-accent-orange');
        } else {
            element.classList.add('bg-accent-red/20', 'text-accent-red');
        }
    }
    
    // ==================== Health Trends ====================
    
    async loadHealthTrends() {
        try {
            const result = await HealthProfessionalAPI.getHealthTrends();
            
            if (result.success) {
                const trends = result.trends;
                const container = document.getElementById('trendsData');
                
                container.innerHTML = Object.entries(trends).map(([key, data]) => {
                    const trendIcon = data.trend === 'improving' ? '📈' : data.trend === 'stable' ? '➡️' : '📉';
                    const trendColor = data.trend === 'improving' ? 'text-accent-green' : data.trend === 'stable' ? 'text-accent-blue' : 'text-accent-red';
                    
                    return `
                        <div class="glass border-2 border-dark-600 rounded-lg p-4">
                            <div class="flex items-center justify-between mb-2">
                                <span class="font-semibold text-white capitalize">${key.replace(/_/g, ' ')}</span>
                                <span class="${trendColor} font-bold">${trendIcon} ${data.trend}</span>
                            </div>
                            <div class="flex items-baseline space-x-2">
                                <span class="text-2xl font-bold text-white">
                                    ${typeof data.average === 'number' ? data.average.toFixed(1) : data.average}
                                </span>
                                <span class="text-sm text-gray-400">avg (${result.period})</span>
                            </div>
                            <div class="mt-2 text-sm ${data.change_percent >= 0 ? 'text-accent-green' : 'text-accent-red'}">
                                ${data.change_percent >= 0 ? '+' : ''}${data.change_percent}% change
                            </div>
                        </div>
                    `;
                }).join('');
            }
        } catch (error) {
            console.error('Failed to load trends:', error);
        }
    }
    
    // ==================== Medication Adherence ====================
    
    async loadMedicationAdherence() {
        try {
            const result = await HealthProfessionalAPI.getMedicationAdherence();
            
            if (result.success) {
                const adherence = result.adherence;
                const container = document.getElementById('medicationAdherence');
                
                container.innerHTML = `
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <span class="text-lg font-semibold text-white">Overall Adherence</span>
                            <span class="text-3xl font-bold text-accent-green">${adherence.overall_rate}%</span>
                        </div>
                        <div class="w-full bg-dark-600 rounded-full h-4">
                            <div class="bg-gradient-to-r from-accent-green to-green-600 h-full rounded-full transition-all" style="width: ${adherence.overall_rate}%"></div>
                        </div>
                        <div class="grid grid-cols-2 gap-4 mt-4">
                            <div class="glass rounded-lg p-3 border border-accent-red/30">
                                <p class="text-sm text-gray-400">Missed This Week</p>
                                <p class="text-2xl font-bold text-accent-red">${adherence.missed_doses_week}</p>
                            </div>
                            <div class="glass rounded-lg p-3 border border-accent-green/30">
                                <p class="text-sm text-gray-400">On Time Rate</p>
                                <p class="text-2xl font-bold text-accent-green">${adherence.on_time_rate}%</p>
                            </div>
                        </div>
                        <div class="mt-4">
                            <h4 class="font-semibold text-white mb-2">By Medication:</h4>
                            <div class="space-y-2">
                                ${adherence.medications.map(med => `
                                    <div class="flex items-center justify-between glass rounded-lg p-3 border border-dark-600">
                                        <span class="font-medium text-white">${med.name}</span>
                                        <div class="flex items-center space-x-3">
                                            <span class="text-sm text-gray-400">${med.doses_taken}/${med.doses_scheduled}</span>
                                            <span class="font-bold ${med.adherence_rate >= 90 ? 'text-accent-green' : 'text-accent-orange'}">
                                                ${med.adherence_rate}%
                                            </span>
                                        </div>
                                    </div>
                                `).join('')}
                            </div>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Failed to load medication adherence:', error);
        }
    }
    
    // ==================== Fall Incidents ====================
    
    async loadFallIncidents() {
        try {
            const result = await HealthProfessionalAPI.getFallIncidents();
            
            if (result.success) {
                const incidents = result.incidents;
                const container = document.getElementById('fallIncidents');
                
                if (incidents.length === 0) {
                    container.innerHTML = '<p class="text-accent-green font-semibold">✓ No fall incidents recorded</p>';
                    return;
                }
                
                container.innerHTML = `
                    <div class="mb-4">
                        <span class="text-2xl font-bold text-white">${incidents.length}</span>
                        <span class="text-gray-400"> incident(s) in last ${result.period}</span>
                    </div>
                    <div class="space-y-3 max-h-64 overflow-y-auto">
                        ${incidents.map(incident => {
                            const severityColors = {
                                'minor': 'bg-accent-orange/10 border-accent-orange/30',
                                'moderate': 'bg-accent-orange/20 border-accent-orange/50',
                                'severe': 'bg-accent-red/20 border-accent-red/50'
                            };
                            const textColors = {
                                'minor': 'text-accent-orange',
                                'moderate': 'text-accent-orange',
                                'severe': 'text-accent-red'
                            };
                            const colorClass = severityColors[incident.severity] || 'bg-dark-700 border-dark-600';
                            const textColor = textColors[incident.severity] || 'text-white';
                            
                            return `
                                <div class="glass ${colorClass} border-2 rounded-lg p-3">
                                    <div class="flex items-center justify-between mb-2">
                                        <span class="font-semibold ${textColor} capitalize">${incident.severity}</span>
                                        <span class="text-sm text-gray-400">${NovaBot.formatRelativeTime(incident.timestamp)}</span>
                                    </div>
                                    <p class="text-sm text-gray-300">📍 ${incident.location}</p>
                                    <p class="text-sm text-gray-300">⏱️ Response: ${incident.response_time}</p>
                                    ${incident.injuries ? '<p class="text-sm text-accent-red font-semibold">⚠️ Injuries reported</p>' : ''}
                                </div>
                            `;
                        }).join('')}
                    </div>
                `;
            }
        } catch (error) {
            console.error('Failed to load fall incidents:', error);
        }
    }
    
    // ==================== Report Generation ====================
    
    initGenerateReport() {
        document.getElementById('generateReportBtn').addEventListener('click', async () => {
            await this.generateReport();
        });
    }
    
    async generateReport() {
        try {
            NovaBot.showLoading(true);
            const result = await HealthProfessionalAPI.generateReport('comprehensive');
            
            if (result.success) {
                NovaBot.showToast('Report generated successfully!', 'success');
                
                // Show download link
                const report = result.report;
                const message = `Report ready: ${report.type} (ID: ${report.id.substring(0, 8)}...)`;
                NovaBot.showToast(message, 'info');
                
                // In real implementation, would trigger download
                console.log('Download URL:', report.download_url);
            }
        } catch (error) {
            NovaBot.showToast('Failed to generate report', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
    
    // ==================== Clinical Notes ====================
    
    initClinicalNotes() {
        document.getElementById('saveClinicalNoteBtn').addEventListener('click', () => {
            this.saveClinicalNote();
        });
    }
    
    saveClinicalNote() {
        const note = document.getElementById('clinicalNoteInput').value.trim();
        
        if (!note) {
            NovaBot.showToast('Please enter a note', 'warning');
            return;
        }
        
        // In real implementation, would save via API
        NovaBot.showToast('Clinical note saved', 'success');
        document.getElementById('clinicalNoteInput').value = '';
    }
    
    // ==================== Polling ====================
    
    startPolling() {
        // Poll vitals every 30 seconds
        setInterval(() => {
            this.loadCurrentVitals();
        }, 30000);
        
        // Refresh trends every 5 minutes
        setInterval(() => {
            this.loadHealthTrends();
            this.loadMedicationAdherence();
        }, 300000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.healthProfessionalUI = new HealthProfessionalUI();
});

