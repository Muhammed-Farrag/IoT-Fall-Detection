/**
 * Caregiver Dashboard - API Layer
 * Single Responsibility: Handle all API communication
 */

const CaregiverAPI = {
    baseURL: '/caregiver/api',
    patientId: 'patient_001', // Would come from session/auth in real implementation
    
    /**
     * Generic fetch wrapper
     */
    async _fetch(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    /**
     * Get patient status
     */
    async getPatientStatus() {
        return await this._fetch(`${this.baseURL}/patient/status/${this.patientId}`);
    },
    
    /**
     * Get patient location
     */
    async getLocation() {
        return await this._fetch(`${this.baseURL}/patient/location/${this.patientId}`);
    },
    
    /**
     * Get alerts
     * @param {number} limit - Number of alerts to retrieve
     * @param {string} severity - Filter by severity (optional)
     */
    async getAlerts(limit = 50, severity = null) {
        let url = `${this.baseURL}/alerts/${this.patientId}?limit=${limit}`;
        if (severity) {
            url += `&severity=${severity}`;
        }
        return await this._fetch(url);
    },
    
    /**
     * Mark alert as read
     * @param {string} alertId - Alert identifier
     */
    async markAlertRead(alertId) {
        return await this._fetch(`${this.baseURL}/alerts/${alertId}/read`, {
            method: 'POST'
        });
    },
    
    /**
     * Get device battery status
     */
    async getBattery() {
        return await this._fetch(`${this.baseURL}/device/battery/${this.patientId}`);
    },
    
    /**
     * Get video stream URL
     */
    async getVideoStream() {
        return await this._fetch(`${this.baseURL}/video/stream/${this.patientId}`);
    }
};

// Make available globally
window.CaregiverAPI = CaregiverAPI;

