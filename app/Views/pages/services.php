<?php
require dirname(__DIR__) . '/layout/header.php';
?>

<!-- ============================================================== -->
<!-- SERVICES HERO                                                  -->
<!-- ============================================================== -->
<section class="page-hero">
    <div class="container text-center">
        <div class="badge">Solutions Stratégiques & Créatives</div>
        <h1 class="page-title">Nos Prestations & Formules d’Accompagnement</h1>
        <p class="page-lead max-w-reading">
            Des services calibrés pour bâtir une notoriété durable, générer des prospects qualifiés et transformer vos réseaux sociaux en véritables canaux de vente.
        </p>
    </div>
</section>

<!-- ============================================================== -->
<!-- DÉTAIL DES SERVICES                                            -->
<!-- ============================================================== -->
<section class="section">
    <div class="container">
        <div class="services-detailed-list">
            <?php foreach ($services as $index => $srv): ?>
                <div class="card service-detail-item <?= $index % 2 === 1 ? 'service-detail-item--reverse' : '' ?>" id="<?= e($srv['id']) ?>">
                    <div class="service-detail-content">
                        <div class="service-detail-meta">
                            <span class="badge"><?= e($srv['category']) ?></span>
                            <?php if (!empty($srv['badge'])): ?>
                                <span class="service-pill"><?= e($srv['badge']) ?></span>
                            <?php endif; ?>
                        </div>
                        <h2 class="service-detail-title"><?= e($srv['title']) ?></h2>
                        <p class="service-detail-desc"><?= e($srv['short_desc']) ?></p>

                        <div class="service-features-list">
                            <h4 class="features-heading">Ce qui est inclus dans cette prestation :</h4>
                            <ul>
                                <?php foreach ($srv['features'] as $feat): ?>
                                    <li>
                                        <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" class="check-icon"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                        <span><?= e($feat) ?></span>
                                    </li>
                                <?php endforeach; ?>
                            </ul>
                        </div>

                        <div class="service-detail-action">
                            <div class="service-price-block">
                                <span class="price-label">Tarif indicatif :</span>
                                <span class="price-value"><?= e($srv['pricing']) ?></span>
                            </div>
                            <a href="<?= e(url('devis')) ?>?service=<?= e($srv['id']) ?>" class="btn btn--primary">
                                <span>Demander ce service</span>
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg>
                            </a>
                        </div>
                    </div>

                    <div class="service-detail-media">
                        <div class="service-media-card bg-grad-<?= e($srv['id']) ?>">
                            <div class="media-icon-large">
                                <?php if ($srv['icon'] === 'message-circle'): ?>
                                    <svg width="64" height="64" fill="none" stroke="white" stroke-width="1.8"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                                <?php elseif ($srv['icon'] === 'feather'): ?>
                                    <svg width="64" height="64" fill="none" stroke="white" stroke-width="1.8"><path d="M20.24 12.24a6 6 0 0 0-8.49-8.49L5 10.5V19h8.5z"></path><line x1="16" y1="8" x2="2" y2="22"></line><line x1="17.5" y1="15" x2="9" y2="15"></line></svg>
                                <?php elseif ($srv['icon'] === 'mic'): ?>
                                    <svg width="64" height="64" fill="none" stroke="white" stroke-width="1.8"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path><path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line></svg>
                                <?php else: ?>
                                    <svg width="64" height="64" fill="none" stroke="white" stroke-width="1.8"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>
                                <?php endif; ?>
                            </div>
                            <span class="media-title"><?= e($srv['title']) ?></span>
                            <span class="media-badge">Expertise Wiky Holding 360°</span>
                        </div>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- ============================================================== -->
<!-- PACKS TARIFAIRES                                               -->
<!-- ============================================================== -->
<section class="section bg-alt">
    <div class="container">
        <div class="section-header">
            <div class="badge">Formules Clés en Main</div>
            <h2 class="section-title">Nos Packs d’Accompagnement Recommandés</h2>
            <p class="section-lead">Des forfaits transparents pensés pour accélérer votre développement sans frais cachés.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3">
            <?php foreach ($packs as $pack): ?>
                <div class="card pricing-card <?= $pack['popular'] ? 'pricing-card--popular' : '' ?>">
                    <?php if ($pack['popular']): ?>
                        <div class="popular-ribbon">Recommandé</div>
                    <?php endif; ?>
                    <h3 class="pack-name"><?= e($pack['name']) ?></h3>
                    <p class="pack-target"><?= e($pack['target']) ?></p>
                    <div class="pack-price"><?= e($pack['price']) ?></div>

                    <ul class="pack-features">
                        <?php foreach ($pack['features'] as $f): ?>
                            <li>
                                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                <span><?= e($f) ?></span>
                            </li>
                        <?php endforeach; ?>
                    </ul>

                    <div class="pack-action">
                        <a href="<?= e(url('devis')) ?>" class="btn <?= $pack['popular'] ? 'btn--primary' : 'btn--outline' ?> btn--full">
                            <span>Choisir cette formule</span>
                        </a>
                    </div>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<?php require dirname(__DIR__) . '/layout/footer.php'; ?>
