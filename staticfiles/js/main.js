(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        initCartFunctions();
        initScrollAnimations();
        initThemeToggle();
    });

    function initCartFunctions() {
        window.miqdorYangilash = function(itemId, miqdor) {
            fetch('/savatcha/' + itemId + '/miqdor/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ miqdor: miqdor }),
            }).then(response => response.json())
              .then(data => {
                  if (data.success) {
                      location.reload();
                  } else {
                      alert('Xatolik: ' + data.error);
                  }
              });
        };

        window.savatchadanOlibTashlash = function(itemId) {
            fetch('/savatcha/' + itemId + '/olib-tashlash/', {
                method: 'POST',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
            }).then(() => location.reload());
        };

        window.savatchaniTozalash = function() {
            if (confirm('Savatchani tozalashni xohlaysizmi?')) {
                fetch('/savatcha/tozalash/', {
                    method: 'POST',
                    headers: { 'X-CSRFToken': getCookie('csrftoken') },
                }).then(() => location.reload());
            }
        };
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

    function initThemeToggle() {
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const body = document.body;

        if (!themeToggle || !themeIcon) return;

        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') {
            body.classList.add('dark-mode');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
        }

        themeToggle.addEventListener('click', function() {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            themeIcon.classList.toggle('fa-moon', !isDark);
            themeIcon.classList.toggle('fa-sun', isDark);
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
