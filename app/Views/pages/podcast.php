<?php
require dirname(__DIR__) . '/layout/header.php';
?>

<!-- ============================================================== -->
<!-- PODCAST HERO                                                   -->
<!-- ============================================================== -->
<section class="page-hero">
    <div class="container text-center">
        <div class="badge">Studio Insonorisé & Équipé • Abidjan</div>
        <h1 class="page-title">Enregistrez Votre Podcast & Vos Vidéos Pro</h1>
        <p class="page-lead max-w-reading">
            Donnez de la voix à votre marque dans un environnement acoustique parfait. Régie 4K multi-caméras, micros broadcast et montage clé en main pour vos formats longs et courts.
        </p>
        <div class="hero-actions justify-center mt-6">
            <a href="<?= e(url('contact')) ?>" class="btn btn--primary btn--lg">
                <span>Réserver une session de tournage</span>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
            </a>
            <a href="<?= e(url('devis')) ?>" class="btn btn--secondary btn--lg">
                <span>Devis pour une saison</span>
            </a>
        </div>
    </div>
</section>

<!-- ============================================================== -->
<!-- PRÉSENTATION DU STUDIO                                         -->
<!-- ============================================================== -->
<section class="section">
    <div class="container">
        <div class="about-story-grid">
            <div class="story-content">
                <span class="badge">L'expérience studio</span>
                <h2 class="section-title">Un espace pensé pour les créateurs & les entreprises</h2>
                <p>
                    Le format audio et vidéo conversationnelle est aujourd’hui l’arme de communication la plus engageante. Que vous soyez chef d’entreprise, consultant, influenceur ou créateur, <strong>Digital Agency Wiky</strong> met à votre disposition son studio professionnel situé à Abidjan.
                </p>
                <p>
                    Vous n'avez qu'à venir avec votre sujet ou vos invités : notre équipe technique (ingénieur du son, cadreur et notre directrice de production) s'occupe de la mise en place, des niveaux sonores, des lumières et de l’enregistrement haute fidélité.
                </p>
                <div class="features-check-grid mt-6">
                    <div class="check-item">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <span>Jusqu’à 4 intervenants au micro</span>
                    </div>
                    <div class="check-item">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <span>Retour vidéo & prompteur sur demande</span>
                    </div>
                    <div class="check-item">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <span>Livraison des rushs bruts ou montés en 48h</span>
                    </div>
                    <div class="check-item">
                        <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                        <span>Export adapté Spotify, Apple Podcast & YouTube</span>
                    </div>
                </div>
            </div>

            <div class="story-card">
                <div class="studio-badge-card">
                    <div class="studio-status-tag">
                        <span class="live-dot"></span>
                        <span>Studio Wiky • Prêt à Enregistrer</span>
                    </div>
                    <div class="studio-visual-art">
                        <svg width="80" height="80" fill="none" stroke="currentColor" stroke-width="1.5" class="mic-art"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
                    </div>
                    <div class="studio-quick-pricing">
                        <span class="pricing-badge">Tarif Session Simple</span>
                        <div class="price-val">80.000 FCFA <span class="price-unit">/ séance</span></div>
                        <p class="price-includes">Comprend 1h30 de studio, prise de son broadcast et fichiers audio nettoyés.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ============================================================== -->
<!-- MATÉRIEL ET ÉQUIPEMENTS                                        -->
<!-- ============================================================== -->
<section class="section bg-alt">
    <div class="container">
        <div class="section-header">
            <div class="badge">Spécifications Techniques</div>
            <h2 class="section-title">Des équipements broadcast sans compromis</h2>
            <p class="section-lead">Votre voix et votre image méritent une qualité sonore et visuelle irréprochable.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
            <?php foreach ($equipment as $eq): ?>
                <div class="card equipment-card">
                    <div class="equipment-icon">
                        <svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 14 14"></polyline></svg>
                    </div>
                    <h3 class="equipment-name"><?= e($eq['name']) ?></h3>
                    <p class="equipment-desc"><?= e($eq['desc']) ?></p>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- ============================================================== -->
<!-- IDÉATION & SUJETS DE PODCASTS SUGGÉRÉS                         -->
<!-- ============================================================== -->
<section class="section">
    <div class="container">
        <div class="section-header">
            <div class="badge">Accompagnement Éditorial</div>
            <h2 class="section-title">Besoin d’idées de sujets pour votre émission ?</h2>
            <p class="section-lead">Notre équipe vous aide à structurer le ton, les questions et la dynamique de vos épisodes.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3">
            <?php foreach ($suggestedTopics as $t): ?>
                <div class="card topic-card">
                    <span class="topic-format-badge"><?= e($t['format']) ?></span>
                    <h3 class="topic-title"><?= e($t['title']) ?></h3>
                    <p class="topic-target"><?= e($t['target']) ?></p>
                    <div class="topic-capsules">
                        <span class="capsule-label">Déclinaisons réseaux :</span>
                        <span class="capsule-desc"><?= e($t['capsules']) ?></span>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- ============================================================== -->
<!-- CTA                                                            -->
<!-- ============================================================== -->
<section class="cta-banner-section">
    <div class="container">
        <div class="cta-banner">
            <div class="cta-text">
                <h2 class="cta-title">Visitez le studio ou réservez votre créneau</h2>
                <p class="cta-lead">Nos techniciens vous accueillent pour tester le matériel et caler votre calendrier d’enregistrement.</p>
            </div>
            <div class="cta-buttons">
                <a href="<?= e(url('contact')) ?>" class="btn btn--white btn--lg">
                    <span>Prendre rendez-vous au studio</span>
                </a>
            </div>
        </div>
    </div>
</section>

<?php require dirname(__DIR__) . '/layout/footer.php'; ?>
