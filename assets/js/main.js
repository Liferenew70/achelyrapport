/**
 * Digital Agency Wiky - Script Principal Frontend
 * Micro-interactions, Filtrage fluide, Simulateur en direct & Navigation Mobile
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------
    // 1. Sticky Header & Scroll Elevation
    // -------------------------------------------------------------
    const header = document.getElementById('site-header');
    const backToTop = document.getElementById('back-to-top');

    const handleScroll = () => {
        const scrollY = window.scrollY;
        if (header) {
            if (scrollY > 30) {
                header.classList.add('is-scrolled');
            } else {
                header.classList.remove('is-scrolled');
            }
        }
        if (backToTop) {
            if (scrollY > 400) {
                backToTop.classList.add('is-visible');
            } else {
                backToTop.classList.remove('is-visible');
            }
        }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    // -------------------------------------------------------------
    // 2. Menu Mobile & Hamburger Toggle
    // -------------------------------------------------------------
    const navToggle = document.getElementById('nav-toggle');
    const mainNav = document.getElementById('main-nav');

    if (navToggle && mainNav) {
        navToggle.addEventListener('click', () => {
            const isOpen = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', String(!isOpen));
            header.classList.toggle('is-nav-open');
            document.body.classList.toggle('no-scroll', !isOpen);
        });

        // Fermer au clic sur un lien de navigation
        mainNav.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                navToggle.setAttribute('aria-expanded', 'false');
                header.classList.remove('is-nav-open');
                document.body.classList.remove('no-scroll');
            });
        });
    }

    // -------------------------------------------------------------
    // 3. Filtrage Dynamique du Portfolio (Sans rechargement si JS actif)
    // -------------------------------------------------------------
    const filterPills = document.querySelectorAll('.portfolio-filter-bar .filter-pill');
    const portfolioCards = document.querySelectorAll('.portfolio-grid .portfolio-card');

    if (filterPills.length > 0 && portfolioCards.length > 0) {
        filterPills.forEach(pill => {
            pill.addEventListener('click', (e) => {
                e.preventDefault();
                const filter = pill.getAttribute('data-filter') || 'all';

                filterPills.forEach(p => p.classList.remove('is-active'));
                pill.classList.add('is-active');

                portfolioCards.forEach(card => {
                    const cardCat = card.getAttribute('data-category');
                    if (filter === 'all' || cardCat === filter) {
                        card.style.display = 'flex';
                        card.style.opacity = '0';
                        setTimeout(() => {
                            card.style.transition = 'opacity 250ms ease-out';
                            card.style.opacity = '1';
                        }, 20);
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }

    // -------------------------------------------------------------
    // 4. Simulateur de Devis en Temps Réel
    // -------------------------------------------------------------
    const calcService = document.getElementById('calc-service');
    const calcScope = document.getElementById('calc-scope');
    const calcSpeed = document.getElementById('calc-speed');
    const calcResult = document.getElementById('calc-result');

    if (calcService && calcScope && calcSpeed && calcResult) {
        const basePrices = {
            'community-management': 150000,
            'branding-logos': 250000,
            'studio-podcast': 80000,
            'creation-entreprise': 450000
        };

        const scopeMultipliers = {
            'starter': 1.0,
            'standard': 1.6,
            'premium': 2.4
        };

        const speedMultipliers = {
            'normal': 1.0,
            'urgent': 1.3
        };

        const updateLiveEstimate = () => {
            const srv = calcService.value;
            const scope = calcScope.value;
            const speed = calcSpeed.value;

            const base = basePrices[srv] || 150000;
            const mScope = scopeMultipliers[scope] || 1.0;
            const mSpeed = speedMultipliers[speed] || 1.0;

            const total = Math.round(base * mScope * mSpeed);
            calcResult.textContent = new Intl.NumberFormat('fr-FR').format(total) + ' FCFA';
            
            // Animation subtile du chiffre
            calcResult.classList.add('price-updated');
            setTimeout(() => calcResult.classList.remove('price-updated'), 300);
        };

        calcService.addEventListener('change', updateLiveEstimate);
        calcScope.addEventListener('change', updateLiveEstimate);
        calcSpeed.addEventListener('change', updateLiveEstimate);
        updateLiveEstimate();
    }
});
