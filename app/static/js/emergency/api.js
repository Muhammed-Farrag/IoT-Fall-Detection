/**
 * Emergency Service Dashboard - API Layer
 * Single Responsibility: Handle all API communication
 */

const EmergencyAPI = {
    baseURL: '/emergency/api',
    emergencyId: null,
    
    init(emergencyId) {
        this.emergencyId = emergencyId || 'emg_001';
    },
    
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
     * Get emergency details
     */
    async getEmergencyDetails() {
        return await this._fetch(`${this.baseURL}/emergency/${this.emergencyId}`);
    },
    
    /**
     * Get critical data
     */
    async getCriticalData() {
        return await this._fetch(`${this.baseURL}/emergency/${this.emergencyId}/critical`);
    },
    
    /**
     * Update response status
     * @param {string} status - New status
     * @param {string} responderId - Responder ID
     * @param {string} notes - Optional notes
     */
    async updateStatus(status, responderId, notes = '') {
        return await this._fetch(`${this.baseURL}/emergency/${this.emergencyId}/status`, {
            method: 'POST',
            body: JSON.stringify({
                status,
                responder_id: responderId,
                notes
            })
        });
    },
    
    /**
     * Get environmental data
     */
    async getEnvironmentalData() {
        return await this._fetch(`${this.baseURL}/emergency/${this.emergencyId}/environmental`);
    },
    
    /**
     * Send reassurance message
     * @param {string} message - Message to send
     */
    async sendReassurance(message) {
        return await this._fetch(`${this.baseURL}/emergency/${this.emergencyId}/reassure`, {
            method: 'POST',
            body: JSON.stringify({ message })
        });
    },
    
    /**
     * Get nearby facilities
     * @param {number} lat - Latitude
     * @param {number} lng - Longitude
     */
    async getNearbyFacilities(lat, lng) {
        return await this._fetch(`${this.baseURL}/facilities?lat=${lat}&lng=${lng}`);
    }
};

window.EmergencyAPI = EmergencyAPI;

