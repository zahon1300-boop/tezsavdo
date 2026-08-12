(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initCartCount();
        initDarkModeToggle();
        initScrollAnimations();
    });

    function initCartCount() {
        fetch('/api/savatcha/soni/')
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    document.querySelectorAll('.cart-count').forEach(el => {
                        el.textContent = data.soni;
                    });
                }
            })
            .catch(() => {});
    }

    function initDarkModeToggle() {
        const toggle = document.getElementById('darkModeToggle');
        const mobileToggle = document.getElementById('mobileDarkModeToggle');
        
        const saved = localStorage.getItem('theme');
        if (saved === 'light') {
            document.body.classList.remove('dark-mode');
        }

        function toggleTheme() {
            document.body.classList.toggle('dark-mode');
            const isDark = document.body.classList.contains('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        }

        if (toggle) {
            toggle.addEventListener('click', toggleTheme);
        }
        if (mobileToggle) {
            mobileToggle.addEventListener('click', toggleTheme);
        }
    }

    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-fadeInUp');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.product-card, .category-card').forEach(function(el) {
            observer.observe(el);
        });
    }

    window.getCookie = function(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
})();
