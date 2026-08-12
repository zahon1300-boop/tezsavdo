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
        const icon = document.getElementById('themeIcon');
        const saved = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (saved === 'dark' || (!saved && prefersDark)) {
            document.body.classList.add('dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
        }

        function updateThemeIcon() {
            if (!icon) return;
            icon.classList.toggle('fa-sun', !document.body.classList.contains('dark-mode'));
            icon.classList.toggle('fa-moon', document.body.classList.contains('dark-mode'));
        }

        function toggleTheme() {
            const isDark = document.body.classList.toggle('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            updateThemeIcon();
        }

        if (toggle) {
            toggle.addEventListener('click', toggleTheme);
        }
        if (mobileToggle) {
            mobileToggle.addEventListener('click', toggleTheme);
        }

        updateThemeIcon();
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
