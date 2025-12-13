/**
 * Primary User Dashboard - UI Layer
 * Single Responsibility: Handle all UI interactions and updates
 * Depends on: api.js for data fetching
 */

class PrimaryUserUI {
    constructor() {
        this.currentInputMode = 'touch';
        this.followModeActive = false;
        this.init();
    }
    
    /**
     * Initialize all UI components and event listeners
     */
    init() {
        this.initInputModeButtons();
        this.initMedicationCard();
        this.initMedicalQuery();
        this.initFollowMode();
        this.initVisionButtons();
        this.startPolling();
    }
    
    // ==================== Communication Hub ====================
    
    /**
     * Initialize input mode button handlers
     */
    initInputModeButtons() {
        const buttons = document.querySelectorAll('.input-mode-btn');
        
        buttons.forEach(btn => {
            btn.addEventListener('click', async () => {
                const mode = btn.dataset.mode;
                await this.setInputMode(mode);
            });
        });
        
        // Load current mode
        this.loadInputMode();
    }
    
    /**
     * Load and display current input mode
     */
    async loadInputMode() {
        try {
            const result = await PrimaryUserAPI.getInputMode();
            if (result.success) {
                this.currentInputMode = result.active_mode;
                this.updateInputModeUI(result.active_mode);
            }
        } catch (error) {
            console.error('Failed to load input mode:', error);
        }
    }
    
    /**
     * Set input mode
     */
    async setInputMode(mode) {
        try {
            NovaBot.showLoading(true);
            const result = await PrimaryUserAPI.setInputMode(mode);
            
            if (result.success) {
                this.currentInputMode = mode;
                this.updateInputModeUI(mode);
                NovaBot.showToast(result.message, 'success');
                
                // Add visual feedback
                await PrimaryUserAPI.sendVisualFeedback(`Input mode changed to ${mode.replace('_', ' ')}`);
                this.loadVisualFeedback();
            } else {
                NovaBot.showToast(result.message, 'error');
            }
        } catch (error) {
            NovaBot.showToast('Failed to change input mode', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
    
    /**
     * Update input mode UI
     */
    updateInputModeUI(activeMode) {
        const buttons = document.querySelectorAll('.input-mode-btn');
        
        buttons.forEach(btn => {
            const mode = btn.dataset.mode;
            const statusBadge = btn.querySelector('.status-badge');
            
            if (mode === activeMode) {
                btn.classList.add('border-primary-500', 'bg-primary-50');
                btn.classList.remove('bg-gray-100');
                statusBadge.classList.remove('hidden');
            } else {
                btn.classList.remove('border-primary-500', 'bg-primary-50');
                btn.classList.add('bg-gray-100');
                statusBadge.classList.add('hidden');
            }
        });
    }
    
    /**
     * Load and display visual feedback
     */
    async loadVisualFeedback() {
        try {
            const result = await PrimaryUserAPI.getVisualFeedback();
            if (result.success && result.feedback.length > 0) {
                const feedbackDiv = document.getElementById('visualFeedback');
                const latestFeedback = result.feedback[result.feedback.length - 1];
                
                feedbackDiv.innerHTML = `
                    <p class="text-2xl font-semibold">${latestFeedback.text}</p>
                    <p class="text-sm text-gray-500 mt-2">${NovaBot.formatRelativeTime(latestFeedback.timestamp)}</p>
                `;
            }
        } catch (error) {
            console.error('Failed to load visual feedback:', error);
        }
    }
    
    // ==================== Health & Wellness ====================
    
    /**
     * Initialize medication card
     */
    initMedicationCard() {
        this.loadNextMedication();
    }
    
    /**
     * Load next medication
     */
    async loadNextMedication() {
        try {
            const result = await PrimaryUserAPI.getNextMedication();
            
            if (result.success && result.next_medication) {
                const med = result.next_medication;
                document.getElementById('medName').textContent = med.name;
                document.getElementById('medDosage').textContent = `Dosage: ${med.dosage}`;
                document.getElementById('medTime').textContent = `Scheduled: ${med.scheduled_time} (${med.time_until})`;
            } else {
                document.getElementById('medName').textContent = 'No medications scheduled';
                document.getElementById('medDosage').textContent = '';
                document.getElementById('medTime').textContent = '';
            }
        } catch (error) {
            console.error('Failed to load medication:', error);
            document.getElementById('medName').textContent = 'Error loading medication';
        }
    }
    
    /**
     * Initialize medical query chat
     */
    initMedicalQuery() {
        const input = document.getElementById('medicalQueryInput');
        const sendBtn = document.getElementById('sendQueryBtn');
        
        sendBtn.addEventListener('click', () => this.sendMedicalQuery());
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMedicalQuery();
            }
        });
    }
    
    /**
     * Send medical query
     */
    async sendMedicalQuery() {
        const input = document.getElementById('medicalQueryInput');
        const question = input.value.trim();
        
        if (!question) {
            NovaBot.showToast('Please enter a question', 'warning');
            return;
        }
        
        // Add user message to chat
        this.addChatMessage(question, 'user');
        input.value = '';
        
        try {
            NovaBot.showLoading(true);
            const result = await PrimaryUserAPI.queryMedical(question);
            
            if (result.success) {
                const response = result.response;
                this.addChatMessage(response.answer, 'bot');
                
                // Add disclaimer
                if (response.disclaimer) {
                    this.addChatMessage(response.disclaimer, 'disclaimer');
                }
            } else {
                this.addChatMessage('Sorry, I could not process your question.', 'error');
            }
        } catch (error) {
            this.addChatMessage('Error: Unable to get response', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
    
    /**
     * Add message to chat history
     */
    addChatMessage(message, type) {
        const chatHistory = document.getElementById('chatHistory');
        
        // Remove placeholder if it exists
        const placeholder = chatHistory.querySelector('.italic.text-gray-400');
        if (placeholder) {
            placeholder.remove();
        }
        
        const messageDiv = document.createElement('div');
        
        if (type === 'user') {
            messageDiv.className = 'bg-primary-500 text-white p-4 rounded-lg ml-auto max-w-[80%]';
        } else if (type === 'bot') {
            messageDiv.className = 'bg-gray-200 text-gray-800 p-4 rounded-lg mr-auto max-w-[80%]';
        } else if (type === 'disclaimer') {
            messageDiv.className = 'bg-yellow-50 border-2 border-yellow-300 text-yellow-800 p-3 rounded-lg text-sm';
        } else if (type === 'error') {
            messageDiv.className = 'bg-red-50 border-2 border-red-300 text-red-800 p-3 rounded-lg';
        }
        
        messageDiv.textContent = message;
        chatHistory.appendChild(messageDiv);
        
        // Scroll to bottom
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    // ==================== Navigation & Vision ====================
    
    /**
     * Initialize follow mode toggle
     */
    initFollowMode() {
        const toggle = document.getElementById('followModeToggle');
        
        toggle.addEventListener('click', async () => {
            await this.toggleFollowMode();
        });
        
        this.loadFollowMode();
    }
    
    /**
     * Load follow mode status
     */
    async loadFollowMode() {
        try {
            const result = await PrimaryUserAPI.getFollowModeStatus();
            if (result.success) {
                this.followModeActive = result.status.is_active;
                this.updateFollowModeUI(result.status.is_active);
            }
        } catch (error) {
            console.error('Failed to load follow mode:', error);
        }
    }
    
    /**
     * Toggle follow mode
     */
    async toggleFollowMode() {
        try {
            NovaBot.showLoading(true);
            const activate = !this.followModeActive;
            const personId = activate ? 'primary_caregiver' : null;
            
            const result = await PrimaryUserAPI.toggleFollowMode(activate, personId);
            
            if (result.success) {
                this.followModeActive = activate;
                this.updateFollowModeUI(activate);
                NovaBot.showToast(result.message, 'success');
            } else {
                NovaBot.showToast(result.message, 'error');
            }
        } catch (error) {
            NovaBot.showToast('Failed to toggle follow mode', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
    
    /**
     * Update follow mode UI
     */
    updateFollowModeUI(active) {
        const toggle = document.getElementById('followModeToggle');
        const slider = document.getElementById('followModeSlider');
        const status = document.getElementById('followModeStatus');
        
        if (active) {
            toggle.classList.remove('bg-gray-300');
            toggle.classList.add('bg-green-500');
            slider.classList.remove('translate-x-2');
            slider.classList.add('translate-x-18');
            status.textContent = '✓ Following active';
            status.classList.remove('text-gray-600');
            status.classList.add('text-green-600');
        } else {
            toggle.classList.remove('bg-green-500');
            toggle.classList.add('bg-gray-300');
            slider.classList.remove('translate-x-18');
            slider.classList.add('translate-x-2');
            status.textContent = 'Following inactive';
            status.classList.remove('text-green-600');
            status.classList.add('text-gray-600');
        }
    }
    
    /**
     * Initialize vision assistance buttons
     */
    initVisionButtons() {
        document.getElementById('identifyObjectBtn').addEventListener('click', () => {
            this.identifyObject();
        });
        
        document.getElementById('readTextBtn').addEventListener('click', () => {
            this.readText();
        });
        
        document.getElementById('describeSceneBtn').addEventListener('click', () => {
            this.describeScene();
        });
    }
    
    /**
     * Identify object
     */
    async identifyObject() {
        try {
            NovaBot.showLoading(true);
            // In real implementation, would capture image from camera
            const result = await PrimaryUserAPI.identifyObject(new Blob());
            
            if (result.success) {
                const objects = result.objects.map(obj => `${obj.name} (${Math.round(obj.confidence * 100)}%)`).join(', ');
                NovaBot.showToast(`Detected: ${objects}`, 'success');
                await PrimaryUserAPI.sendVisualFeedback(`Objects detected: ${objects}`);
                this.loadVisualFeedback();
            }
        } catch (error) {
            NovaBot.showToast('Failed to identify objects', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
    
    /**
     * Read text
     */
    async readText() {
        try {
            NovaBot.showLoading(true);
            const result = await PrimaryUserAPI.readText(new Blob());
            
            if (result.success) {
                NovaBot.showToast('Text extracted successfully', 'success');
                await PrimaryUserAPI.sendVisualFeedback(`Text: ${result.text}`);
                this.loadVisualFeedback();
            }
        } catch (error) {
            NovaBot.showToast('Failed to read text', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
    
    /**
     * Describe scene
     */
    async describeScene() {
        try {
            NovaBot.showLoading(true);
            const result = await PrimaryUserAPI.describeScene(new Blob());
            
            if (result.success) {
                NovaBot.showToast('Scene described', 'success');
                await PrimaryUserAPI.sendVisualFeedback(result.description);
                this.loadVisualFeedback();
            }
        } catch (error) {
            NovaBot.showToast('Failed to describe scene', 'error');
        } finally {
            NovaBot.showLoading(false);
        }
    }
    
    // ==================== Polling ====================
    
    /**
     * Start polling for updates
     */
    startPolling() {
        // Poll for visual feedback every 5 seconds
        setInterval(() => {
            this.loadVisualFeedback();
        }, 5000);
        
        // Poll for medication updates every 30 seconds
        setInterval(() => {
            this.loadNextMedication();
        }, 30000);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.primaryUserUI = new PrimaryUserUI();
});

