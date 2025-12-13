/**
 * Health Professional Dashboard - API Layer
 * Single Responsibility: Handle all API communication
 */

const HealthProfessionalAPI = {
    baseURL: '/health-professional/api',
    patientId: 'patient_001',
    
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
     * Get current vitals
     */
    async getCurrentVitals() {
        return await this._fetch(`${this.baseURL}/patient/vitals/${this.patientId}`);
    },
    
    /**
     * Get vitals history
     * @param {string} type - Vital type (optional)
     * @param {number} hours - Hours of history
     */
    async getVitalsHistory(type = null, hours = 24) {
        let url = `${this.baseURL}/patient/vitals/${this.patientId}/history?hours=${hours}`;
        if (type) {
            url += `&type=${type}`;
        }
        return await this._fetch(url);
    },
    
    /**
     * Get health trends
     */
    async getHealthTrends() {
        return await this._fetch(`${this.baseURL}/patient/trends/${this.patientId}`);
    },
    
    /**
     * Generate health report
     * @param {string} reportType - Type of report
     */
    async generateReport(reportType = 'comprehensive') {
        return await this._fetch(`${this.baseURL}/patient/report/${this.patientId}`, {
            method: 'POST',
            body: JSON.stringify({ type: reportType })
        });
    },
    
    /**
     * Get medication adherence
     */
    async getMedicationAdherence() {
        return await this._fetch(`${this.baseURL}/patient/medication-adherence/${this.patientId}`);
    },
    
    /**
     * Get fall incidents
     * @param {number} days - Number of days of history
     */
    async getFallIncidents(days = 30) {
        return await this._fetch(`${this.baseURL}/patient/falls/${this.patientId}?days=${days}`);
    }
};

window.HealthProfessionalAPI = HealthProfessionalAPI;

