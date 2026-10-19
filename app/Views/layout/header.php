<?php
/**
 * Layout Header - Digital Agency Wiky / Wiky Holding
 */
if (!defined('APP_NAME')) {
    require_once dirname(__DIR__, 2) . '/Config/App.php';
}
?>
<!DOCTYPE html>
<html lang="fr" class="no-js">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    
    <title><?= e($pageTitle ?? APP_NAME . ' • Agence de Communication Digitale & Branding') ?></title>
    <meta name="description" content="Digital Agency Wiky (Wiky Holding) : Spécialiste à Abidjan en Community Management, modération de commentaires, création de logos, identité visuelle, studio podcast et accompagnement création d’entreprise.">
    <meta name="author" content="Digital Agency Wiky">
    <meta name="robots" content="index, follow">

    <!-- Open Graph / Réseaux Sociaux -->
    <meta property="og:title" content="<?= e($pageTitle ?? APP_NAME) ?>">
    <meta property="og:description" content="Sublimez votre marque et dominez vos réseaux avec Digital Agency Wiky.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="<?= e(BASE_URL) ?>">

    <!-- Préconnexion aux polices pour optimisation de chargement (Discipline 1 du design system) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap" rel="stylesheet">

    <!-- Feuille de styles principale (Design Tokens & Styles d'Élite) -->
    <link rel="stylesheet" href="<?= e(ASSETS_URL) ?>/css/style.css">

    <!-- Favicon SVG élégant -->
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect width='100' height='100' rx='24' fill='%234F46E5'/><path d='M25 35L42 70L50 54L58 70L75 35H63L50 60L37 35Z' fill='%23FFFFFF'/><circle cx='76' cy='35' r='5' fill='%23F97316'/></svg>">
</head>
<body class="page-<?= e($currentPage ?? 'default') ?>">
    <div class="site-wrapper">
        <?php require __DIR__ . '/navbar.php'; ?>
        <main id="main-content" class="main-content">
