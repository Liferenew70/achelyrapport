# RAPPORT D'ADAPTATION TECHNIQUE : PROJET DIGITAL AGENCY WIKY (WIKY HOLDING)
**Diplôme :** Brevet de Technicien Supérieur (BTS)  
**Option :** Informatique Développeur d’Application (IDA)  
**Étudiant(e) :** KOUAME AFFOUE CYNTICHE ACHLEY DELMAS  
**Thème :** Réalisation d'un site web d'entreprise : Cas de Wiky Holding / Digital Agency Wiky  

---

## 1. Contexte de l'Adaptation Technologique

Dans le rapport initial de stage, la **Deuxième Partie : Conception du site web** décrivait l'usage du CMS WordPress et du constructeur Elementor. Cependant, le site d'origine n'étant plus disponible et afin de répondre aux exigences de compétences d'un **Développeur d'Application (IDA)**, le projet a été intégralement reconçu en **PHP Moderne sous architecture MVP / MVC (Model-View-Controller / Model-View-Presenter)** avec couche d'accès aux données par **PDO**.

Cette adaptation apporte plusieurs avantages majeurs pour la soutenance du BTS :
1. **Démonstration de compétences en programmation pure :** L'étudiant démontre sa maîtrise de la syntaxe PHP native, de l'orienté objet, du routage frontal, de la séparation des responsabilités et de la manipulation des bases de données relationnelles via PDO.
2. **Sécurité et performance accrue :** Utilisation de requêtes préparées (protection contre les injections SQL), protection CSRF sur les formulaires, échappement XSS systématique et code allégé sans surcharge de plugins tiers.
3. **Compatibilité totale avec l'hébergeur gratuit InfinityFree :** Le projet s'exécute parfaitement sur un serveur Apache/PHP/MySQL standard sans dépendances lourdes (Node/Composer au runtime non requis).

---

## 2. Refonte de la Deuxième Partie : Nouveau Chapitrage

### CHAPITRE I : ANALYSE ET CONCEPTION

#### 1.1 Analyse des besoins de l'entreprise
Digital Agency Wiky (Wiky Holding) intervient sur 4 métiers stratégiques :
- **Community Management & Modération :** Animation quotidienne, stratégie de contenu, réponse bienveillante et rapide aux commentaires et messages privés 7j/7, gestion des campagnes publicitaires (Meta Ads & Google Ads).
- **Identité Visuelle & Branding :** Conception de logos vectoriels, chartes graphiques complètes, kits papeterie et bannières pour réseaux sociaux.
- **Studio Podcast & Audiovisuel :** Studio insonorisé et équipé à Abidjan (micros broadcast, captation 4K multi-angles), montage de formats longs et capsules dynamiques (TikTok/Reels), accompagnement éditorial sur les sujets d’émissions d’entreprise.
- **Création d’Entreprise & Conseil :** Positionnement stratégique, naming, kits de lancement pour entrepreneurs et PME.

#### 1.2 Arborescence du site internet
L'arborescence a été enrichie et optimisée pour une expérience utilisateur moderne :
- **Accueil (`index.php?page=home`) :** Hero section à fort impact, chiffres clés (KPIs), aperçu des 4 pôles, sélection de réalisations, processus en 4 étapes, avis clients et CTA de conversion.
- **À Propos (`index.php?page=about`) :** Histoire de Wiky Holding, mission & vision, présentation détaillée des 4 pôles internes (issus de l'organigramme de l'agence), et valeurs fondamentales.
- **Services (`index.php?page=services`) :** Détail approfondi de chaque métier, listes des livrables inclus, tarifs indicatifs et 3 formules packs recommandées (Pack Starter, Pack Identité de Marque, Pack Studio Podcast).
- **Réalisations / Portfolio (`index.php?page=portfolio`) :** Galerie filtrable dynamiquement par catégorie (Logos/Branding, Community Management, Podcast, Startup) avec métriques d'impact mesurées.
- **Studio Podcast (`index.php?page=podcast`) :** Page dédiée mettant en lumière le studio insonorisé, les équipements broadcast (Shure SM7B, caméras 4K Sony), et un catalogue de formats/sujets d'émissions suggérés pour les entreprises.
- **Contact & Localisation (`index.php?page=contact`) :** Coordonnées à Abidjan (Cocody/Plateau), bouton de contact WhatsApp direct, formulaire sécurisé avec validation et message flash, et FAQ interactive.
- **Simulateur de Devis (`index.php?page=devis`) :** Calculateur dynamique en temps réel calculant le tarif indicatif en FCFA et enregistrant la demande détaillée en base de données.

---

### CHAPITRE II : ENVIRONNEMENT TECHNIQUE & ARCHITECTURE MVP

#### 2.1 Langages et Outils retenus
- **Langage Backend :** PHP 7.4+ / 8.x natif (Programmation Orientée Objet, Typage strict, Namespaces).
- **Accès aux Données :** PHP Data Objects (PDO) avec requêtes préparées pour une sécurité optimale.
- **Système de Gestion de Base de Données (SGBD) :** MySQL / MariaDB (production sur InfinityFree) avec adaptateur SQLite autonome pour le développement local.
- **Frontend :** HTML5 sémantique, CSS3 moderne sans framework externe (Design tokens, Clamp typographique, flexbox/grid, animations GPU non bloquantes, respect de `prefers-reduced-motion`) et JavaScript ES6 vanilla sans jQuery.
- **Serveur Web & Hébergement :** Apache HTTP Server avec fichier `.htaccess` (sécurité et réécriture d'URL) hébergé sur la plateforme **InfinityFree**.

#### 2.2 Structure du Projet (Patron d'Architecture MVC / MVP)
```
BTS Achley/
├── app/
│   ├── Config/
│   │   ├── App.php             # Constantes, métadonnées et helpers globaux
│   │   └── Database.php        # Singleton PDO, connexion MySQL / fallback SQLite
│   ├── Controllers/
│   │   ├── HomeController.php      # Gestion de la page d'accueil
│   │   ├── AboutController.php     # Présentation de l'agence et des pôles
│   │   ├── ServiceController.php   # Prestations et packs tarifaires
│   │   ├── PortfolioController.php # Galerie filtrable des réalisations
│   │   ├── PodcastController.php   # Studio podcast & équipements
│   │   ├── ContactController.php   # Formulaire de contact & traitement POST
│   │   └── DevisController.php     # Simulateur et demandes de devis
│   ├── Models/
│   │   ├── ContactModel.php        # Persistance des messages (PDO)
│   │   ├── DevisModel.php          # Persistance des devis et calculs
│   │   ├── PortfolioModel.php      # Modèle de données des réalisations
│   │   └── ServiceModel.php        # Modèle de données des offres
│   └── Views/
│       ├── layout/
│       │   ├── header.php          # En-tête HTML, polices Google Fonts, métas SEO
│       │   ├── navbar.php          # Barre de navigation sticky et tiroir mobile
│       │   └── footer.php          # Pied de page institutionnel et scripts
│       └── pages/
│           ├── home.php
│           ├── about.php
│           ├── services.php
│           ├── portfolio.php
│           ├── podcast.php
│           ├── contact.php
│           └── devis.php
├── assets/
│   ├── css/style.css           # Système de design d'élite (7 disciplines front-end)
│   └── js/main.js              # Micro-interactions, filtrage & simulateur temps réel
├── database.sql                # Script d'installation MySQL (phpMyAdmin)
├── .htaccess                   # Règles Apache, sécurité et rewriting
└── index.php                   # Contrôleur frontal (Front Controller)
```

#### 2.3 Modèle Relationnel de Données
Le schéma comprend deux tables dynamiques principales créées dans la base :
1. **`messages` :**
   - `id` (INT, Clé primaire, Auto-incrément)
   - `name` (VARCHAR 120, Nom complet)
   - `email` (VARCHAR 150, Adresse email)
   - `phone` (VARCHAR 50, Téléphone)
   - `service` (VARCHAR 100, Prestation souhaitée)
   - `subject` (VARCHAR 200, Objet)
   - `message` (TEXT, Contenu de la demande)
   - `created_at` (DATETIME, Horodatage de réception)

2. **`devis_requests` :**
   - `id` (INT, Clé primaire, Auto-incrément)
   - `company_name` (VARCHAR 150, Entreprise ou projet)
   - `contact_name` (VARCHAR 120, Nom du responsable)
   - `email` (VARCHAR 150, Email professionnel)
   - `phone` (VARCHAR 50, Téléphone)
   - `service_type` (VARCHAR 100, Service choisi)
   - `budget_range` (VARCHAR 50, Échelle budgétaire)
   - `urgency` (VARCHAR 50, Délai exigé)
   - `project_details` (TEXT, Cahier des charges abrégé)
   - `created_at` (DATETIME, Date de la simulation)

---

### CHAPITRE III : DÉPLOIEMENT SUR INFINITYFREE & VALIDATION

#### 3.1 Guide de Déploiement étape par étape sur InfinityFree
1. **Création du compte et du nom de domaine :**
   - Se connecter sur [app.infinityfree.com](https://app.infinityfree.com).
   - Créer un compte d'hébergement gratuit et choisir un sous-domaine (ex: `wikyholding.infinityfreeapp.com`).
2. **Création de la base de données MySQL :**
   - Accéder au cPanel InfinityFree -> rubrique **MySQL Databases**.
   - Créer une nouvelle base (ex: `if0_37000000_wikydb`).
   - Noter les 4 identifiants : Hôte MySQL (`sqlXXX.infinityfree.com`), Nom de la base, Utilisateur (`if0_37000000`) et Mot de passe de compte.
3. **Importation du schéma SQL :**
   - Ouvrir **phpMyAdmin** depuis le cPanel.
   - Sélectionner la base de données créée.
   - Cliquer sur **Importer**, sélectionner le fichier `database.sql` du projet et exécuter.
4. **Configuration du fichier `app/Config/Database.php` :**
   - Modifier les constantes `DB_HOST`, `DB_NAME`, `DB_USER`, et `DB_PASS` avec les identifiants réels notés à l'étape 2.
5. **Transfert FTP vers le répertoire `htdocs/` :**
   - Ouvrir FileZilla (ou le Web File Manager d'InfinityFree).
   - Copier l'intégralité du contenu du dossier dans le répertoire `htdocs/`.
   - Le site est immédiatement accessible en ligne avec HTTPS automatique.

---

## 3. Synthèse des Bénéfices pour la Soutenance du BTS

| Critère | Ancienne Approche (WordPress) | Nouvelle Approche (PHP MVP + PDO) |
| :--- | :--- | :--- |
| **Profil Métier** | Intégrateur CMS / No-Code | **Développeur d'Application (IDA)** |
| **Maîtrise du Code** | Dépendance aux thèmes et plugins | **100% de code propriétaire et structuré** |
| **Vitesse d'affichage** | Lourd (>3s, requêtes multiples) | **Ultra-rapide (<500ms, CSS et JS purs)** |
| **Accès Base de Données** | Abstrait par WordPress | **Requêtes préparées PDO explicites** |
| **Sécurité** | Failles récurrentes de plugins | **Sanitisation, CSRF tokens, XSS escapers** |
| **Indépendance** | Maintenance complexe des versions | **Pérennité totale sur n'importe quel hébergeur** |
