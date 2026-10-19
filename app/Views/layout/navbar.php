<?php
/**
 * Layout Navbar - Navigation Principale
 */
$currentPage = $currentPage ?? 'home';
?>
<header class="site-header" id="site-header">
    <div class="container header-container">
        <!-- Logo de l'Agence -->
        <a href="<?= e(url()) ?>" class="brand-logo" aria-label="Digital Agency Wiky - Accueil">
            <span class="logo-mark" aria-hidden="true">
                <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
                    <rect width="32" height="32" rx="8" fill="url(#logo-gradient)"/>
                    <path d="M7 10L13 22L16 16L19 22L25 10H21L16 19.5L11 10H7Z" fill="white"/>
                    <circle cx="25" cy="9" r="2.5" fill="#F97316"/>
                    <defs>
                        <linearGradient id="logo-gradient" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
                            <stop stop-color="#4F46E5"/>
                            <stop offset="1" stop-color="#7C3AED"/>
                        </linearGradient>
                    </defs>
                </svg>
            </span>
            <div class="logo-text">
                <span class="brand-name">WIKY<span class="brand-dot">.</span>AGENCY</span>
                <span class="brand-sub">Wiky Holding • Abidjan</span>
            </div>
        </a>

        <!-- Menu de Navigation Desktop -->
        <nav class="main-nav" id="main-nav" aria-label="Navigation principale">
            <ul class="nav-list">
                <li class="nav-item">
                    <a href="<?= e(url()) ?>" class="nav-link <?= $currentPage === 'home' ? 'is-active' : '' ?>">Accueil</a>
                </li>
                <li class="nav-item">
                    <a href="<?= e(url('about')) ?>" class="nav-link <?= $currentPage === 'about' ? 'is-active' : '' ?>">À Propos</a>
                </li>
                <li class="nav-item">
                    <a href="<?= e(url('services')) ?>" class="nav-link <?= $currentPage === 'services' ? 'is-active' : '' ?>">Services</a>
                </li>
                <li class="nav-item">
                    <a href="<?= e(url('portfolio')) ?>" class="nav-link <?= $currentPage === 'portfolio' ? 'is-active' : '' ?>">Réalisations</a>
                </li>
                <li class="nav-item">
                    <a href="<?= e(url('podcast')) ?>" class="nav-link <?= $currentPage === 'podcast' ? 'is-active' : '' ?>">Studio Podcast</a>
                </li>
                <li class="nav-item">
                    <a href="<?= e(url('contact')) ?>" class="nav-link <?= $currentPage === 'contact' ? 'is-active' : '' ?>">Contact</a>
                </li>
            </ul>
        </nav>

        <!-- CTA & Actions -->
        <div class="header-actions">
            <a href="<?= e(url('devis')) ?>" class="btn btn--primary btn--header">
                <span>Devis Gratuit</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </a>

            <!-- Bouton Hamburger Mobile -->
            <button class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="Ouvrir le menu">
                <span class="hamburger-bar"></span>
                <span class="hamburger-bar"></span>
                <span class="hamburger-bar"></span>
            </button>
        </div>
    </div>
</header>
