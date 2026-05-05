/**
 * EDU-PREDICT - Main JavaScript File
 * JUPEB Academic Performance Prediction System
 */

// ============================================
// THEME MANAGEMENT (DARK/LIGHT MODE)
// ============================================

const ThemeManager = {
    init() {
        this.themeToggle = document.getElementById('themeToggle');
        this.themeIcon = document.getElementById('themeIcon');
        this.htmlElement = document.documentElement;
        
        // Load saved theme or default to light
        const savedTheme = localStorage.getItem('edu-predict-theme') || 'light';
        this.setTheme(savedTheme);
        
        // Add event listener
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    },
    
    setTheme(theme) {
        this.htmlElement.setAttribute('data-bs-theme', theme);
        this.updateIcon(theme);
        localStorage.setItem('edu-predict-theme', theme);
    },
    
    toggleTheme() {
        const currentTheme = this.htmlElement.getAttribute('data-bs-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    },
    
    updateIcon(theme) {
        if (this.themeIcon) {
            if (theme === 'dark') {
                this.themeIcon.classList.remove('bi-sun-fill');
                this.themeIcon.classList.add('bi-moon-fill');
            } else {
                this.themeIcon.classList.remove('bi-moon-fill');
                this.themeIcon.classList.add('bi-sun-fill');
            }
        }
    }
};

// ============================================
// NAVBAR SCROLL EFFECT
// ============================================

const NavbarManager = {
    init() {
        this.navbar = document.querySelector('.navbar-custom');
        if (this.navbar) {
            window.addEventListener('scroll', () => this.handleScroll());
        }
    },
    
    handleScroll() {
        if (window.scrollY > 50) {
            this.navbar.classList.add('navbar-scrolled');
        } else {
            this.navbar.classList.remove('navbar-scrolled');
        }
    }
};

// ============================================
// FORM VALIDATION
// ============================================

const FormValidator = {
    init() {
        // Add validation to all forms with class 'needs-validation'
        const forms = document.querySelectorAll('.needs-validation');
        
        forms.forEach(form => {
            form.addEventListener('submit', (event) => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            });
        });
        
        // Initialize range input validation
        this.initRangeValidation();
    },
    
    initRangeValidation() {
        // CA Score validation (0-40)
        const caScore = document.getElementById('ca_score_40');
        if (caScore) {
            caScore.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                if (value < 0) e.target.value = 0;
                if (value > 40) e.target.value = 40;
            });
        }
        
        // Attendance validation (0-100)
        const attendance = document.getElementById('attendance_rate_percent');
        if (attendance) {
            attendance.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                if (value < 0) e.target.value = 0;
                if (value > 100) e.target.value = 100;
            });
        }
        
        // Mock Exam validation (0-100)
        const mockExam = document.getElementById('mock_exam_score_100');
        if (mockExam) {
            mockExam.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                if (value < 0) e.target.value = 0;
                if (value > 100) e.target.value = 100;
            });
        }
        
        // Study Hours validation (0-168)
        const studyHours = document.getElementById('study_hours_per_week');
        if (studyHours) {
            studyHours.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                if (value < 0) e.target.value = 0;
                if (value > 168) e.target.value = 168;
            });
        }
        
        // Stress Level validation (1-10)
        const stressLevel = document.getElementById('stress_level_1_10');
        if (stressLevel) {
            stressLevel.addEventListener('input', (e) => {
                const value = parseInt(e.target.value);
                if (value < 1) e.target.value = 1;
                if (value > 10) e.target.value = 10;
            });
        }
    }
};

// ============================================
// SMOOTH SCROLL
// ============================================

const SmoothScroll = {
    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const targetId = anchor.getAttribute('href');
                if (targetId !== '#') {
                    const targetElement = document.querySelector(targetId);
                    if (targetElement) {
                        e.preventDefault();
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }
};

// ============================================
// LOADING SPINNER
// ============================================

const LoadingManager = {
    show(button) {
        const spinner = button.querySelector('.spinner-border');
        if (spinner) {
            spinner.classList.remove('d-none');
        }
        button.disabled = true;
    },
    
    hide(button) {
        const spinner = button.querySelector('.spinner-border');
        if (spinner) {
            spinner.classList.add('d-none');
        }
        button.disabled = false;
    }
};

// ============================================
// TOOLTIP INITIALIZATION
// ============================================

const TooltipManager = {
    init() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        if (tooltipTriggerList.length > 0) {
            [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
        }
    }
};

// ============================================
// ANIMATION ON SCROLL
// ============================================

const ScrollAnimation = {
    init() {
        this.animatedElements = document.querySelectorAll('.animate-on-scroll');
        
        if (this.animatedElements.length > 0) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('animated');
                        this.observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1
            });
            
            this.animatedElements.forEach(el => {
                this.observer.observe(el);
            });
        }
    }
};

// ============================================
// CONFIRMATION DIALOGS
// ============================================

const ConfirmationDialog = {
    confirm(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },
    
    confirmDelete(callback) {
        this.confirm('Are you sure you want to delete this item? This action cannot be undone.', callback);
    }
};

// ============================================
// UTILITY FUNCTIONS
// ============================================

const Utils = {
    // Format date
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },
    
    // Format time
    formatTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // Debounce function
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function
    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// ============================================
// NOTIFICATION SYSTEM
// ============================================

const NotificationManager = {
    show(message, type = 'info', duration = 5000) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
        notification.innerHTML = `
            <i class="bi bi-${this.getIcon(type)}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Add styles
        notification.style.cssText = `
            position: fixed;
            top: 80px;
            right: 20px;
            z-index: 1050;
            min-width: 300px;
            max-width: 400px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            animation: slideIn 0.3s ease-out;
        `;
        
        // Add to document
        document.body.appendChild(notification);
        
        // Auto remove after duration
        setTimeout(() => {
            notification.remove();
        }, duration);
    },
    
    getIcon(type) {
        const icons = {
            success: 'check-circle',
            info: 'info-circle',
            warning: 'exclamation-triangle',
            danger: 'x-circle'
        };
        return icons[type] || 'info-circle';
    },
    
    success(message) {
        this.show(message, 'success');
    },
    
    info(message) {
        this.show(message, 'info');
    },
    
    warning(message) {
        this.show(message, 'warning');
    },
    
    error(message) {
        this.show(message, 'danger');
    }
};

// ============================================
// AJAX HELPERS
// ============================================

const AjaxHelper = {
    async get(url, options = {}) {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        return response.json();
    },
    
    async post(url, data, options = {}) {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            body: JSON.stringify(data),
            ...options
        });
        return response.json();
    },
    
    async delete(url, options = {}) {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        return response.json();
    }
};

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize all managers
    ThemeManager.init();
    NavbarManager.init();
    FormValidator.init();
    SmoothScroll.init();
    TooltipManager.init();
    ScrollAnimation.init();
    
    console.log('🎓 EDU-PREDICT System Initialized');
    console.log('📚 JUPEB Academic Performance Prediction System');
    console.log('🤖 Powered by Machine Learning (Random Forest)');
});

// ============================================
// EXPORT FOR EXTERNAL USE
// ============================================

window.EDUPredict = {
    ThemeManager,
    FormValidator,
    LoadingManager,
    NotificationManager,
    AjaxHelper,
    Utils,
    ConfirmationDialog
};