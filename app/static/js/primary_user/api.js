/**
 * Primary User Dashboard - API Layer
 * Single Responsibility: Handle all API communication
 * Separation of Concerns: UI logic is in ui.js
 */

const PrimaryUserAPI = {
    baseURL: '/primary/api',
    
    /**
     * Generic fetch wrapper with error handling
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
    
    // ==================== Communication API ====================
    
    /**
     * Get current active input mode
     */
    async getInputMode() {
        return await this._fetch(`${this.baseURL}/input-mode`);
    },
    
    /**
     * Set active input mode
     * @param {string} mode - 'spoken', 'sign_language', or 'touch'
     */
    async setInputMode(mode) {
        return await this._fetch(`${this.baseURL}/input-mode`, {
            method: 'POST',
            body: JSON.stringify({ mode })
        });
    },
    
    /**
     * Get visual feedback queue
     */
    async getVisualFeedback() {
        return await this._fetch(`${this.baseURL}/visual-feedback`);
    },
    
    /**
     * Send visual feedback
     * @param {string} text - Text to display
     * @param {number} duration - Duration in seconds
     */
    async sendVisualFeedback(text, duration = 5) {
        return await this._fetch(`${this.baseURL}/visual-feedback`, {
            method: 'POST',
            body: JSON.stringify({ text, duration })
        });
    },
    
    // ==================== Health API ====================
    
    /**
     * Get next scheduled medication
     * @param {string} userId - User identifier
     */
    async getNextMedication(userId = 'default_user') {
        return await this._fetch(`${this.baseURL}/medication/next?user_id=${userId}`);
    },
    
    /**
     * Get all medication schedules
     * @param {string} userId - User identifier
     */
    async getMedicationSchedules(userId = 'default_user') {
        return await this._fetch(`${this.baseURL}/medication/schedules?user_id=${userId}`);
    },
    
    /**
     * Query medical knowledge base (RAG)
     * @param {string} question - Medical question
     * @param {object} context - Optional context
     */
    async queryMedical(question, context = {}) {
        return await this._fetch(`${this.baseURL}/medical-query`, {
            method: 'POST',
            body: JSON.stringify({ question, context })
        });
    },
    
    // ==================== Navigation API ====================
    
    /**
     * Get follow mode status
     */
    async getFollowModeStatus() {
        return await this._fetch(`${this.baseURL}/navigation/follow-mode`);
    },
    
    /**
     * Toggle follow mode
     * @param {boolean} activate - Whether to activate or deactivate
     * @param {string} personId - Person to follow (required when activating)
     */
    async toggleFollowMode(activate, personId = null) {
        return await this._fetch(`${this.baseURL}/navigation/follow-mode`, {
            method: 'POST',
            body: JSON.stringify({ activate, person_id: personId })
        });
    },
    
    /**
     * Identify objects in image
     * @param {Blob} imageData - Image data
     */
    async identifyObject(imageData) {
        return await this._fetch(`${this.baseURL}/vision/identify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/octet-stream'
            },
            body: imageData
        });
    },
    
    /**
     * Read text from image (OCR)
     * @param {Blob} imageData - Image data
     */
    async readText(imageData) {
        return await this._fetch(`${this.baseURL}/vision/read-text`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/octet-stream'
            },
            body: imageData
        });
    },
    
    /**
     * Get scene description
     * @param {Blob} imageData - Image data
     */
    async describeScene(imageData) {
        return await this._fetch(`${this.baseURL}/vision/describe-scene`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/octet-stream'
            },
            body: imageData
        });
    },
    
    // ==================== Settings API ====================
    
    /**
     * Get all user settings
     * @param {string} userId - User identifier
     */
    async getSettings(userId = 'default_user') {
        return await this._fetch(`${this.baseURL}/settings?user_id=${userId}`);
    },
    
    /**
     * Update accessibility settings
     * @param {string} mode - Accessibility mode
     * @param {string} userId - User identifier
     */
    async updateAccessibility(mode, userId = 'default_user') {
        return await this._fetch(`${this.baseURL}/settings/accessibility`, {
            method: 'POST',
            body: JSON.stringify({ user_id: userId, mode })
        });
    },
    
    /**
     * Update privacy settings
     * @param {string} sharingLevel - Data sharing level
     * @param {string} userId - User identifier
     */
    async updatePrivacy(sharingLevel, userId = 'default_user') {
        return await this._fetch(`${this.baseURL}/settings/privacy`, {
            method: 'POST',
            body: JSON.stringify({ user_id: userId, sharing_level: sharingLevel })
        });
    }
};

// Make available globally
window.PrimaryUserAPI = PrimaryUserAPI;

