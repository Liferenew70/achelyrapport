# 📋 Fiche de Synthèse & Documentation Globale du Projet
> **Projet :** Site Web Professionnel & Rapport de Stage — Digital Agency Wiky (Wiky Holding)  
> **Auteur / Étudiante :** KOUAME AFFOUE CYNTICHE ACHLEY DELMAS  
> **Diplôme & Filière :** Brevet de Technicien Supérieur (BTS) — Informatique Développeur d'Application (IDA)  
> **Architecture :** PHP Vanilla MVP/MVC • Couche d'accès aux données PDO (MySQL & SQLite Fallback) • Vanilla CSS3 & Vanilla JS ES6  
> **Hébergement cible :** InfinityFree (mutualisé gratuit Apache/PHP/MySQL) & Compatible WAMP/XAMPP/PHP CLI  

---

## 1. 🎯 Contexte, Origine et Objectifs du Projet

### Le Contexte Académique (Soutenance BTS IDA)
Ce projet constitue le support technique de la soutenance de fin de cycle pour l'obtention du **BTS Informatique Développeur d'Application (IDA)** en Côte d'Ivoire.

### La Problématique Initiale & L'Adaptation Technologique
- **Origine :** Dans le stage initial, le site d'origine de l'agence avait été abordé via le CMS WordPress et l'extension Elementor.
- **Problème :** Le site WordPress d'origine n'était plus disponible en ligne. De plus, pour un jury de BTS IDA (filière de **développeurs** et non de simples intégrateurs No-Code), l'utilisation d'un CMS ne permettait pas de démontrer la maîtrise effective des compétences de programmation, d'architecture logicielle et de sécurité des données.
- **Solution apportée :** Reconversion complète du projet de zéro en **code propriétaire pur** en PHP moderne selon le patron d'architecture **MVP / MVC**, sans framework lourd (ni Laravel ni Symfony) afin de garantir :
  1. Une légèreté absolue et une exécution ultra-rapide (< 500 ms).
  2. Une compatibilité sans faille avec les contraintes des hébergeurs mutualisés gratuits comme **InfinityFree** (pas d'accès terminal SSH, pas de Composer en ligne, limites mémoire strictes).
  3. Une démonstration irréfutable des acquis de développement : orienté objet, routage frontal, séparation des responsabilités, requêtes préparées anti-injections SQL via PDO, tokens de protection CSRF, et sanitisation XSS.

---

## 2. 🏢 L'Entreprise : Digital Agency Wiky (Wiky Holding)

**Wiky Holding (Digital Agency Wiky SARL)** est une agence conseil 360° en communication, branding et médias numériques située à **Abidjan (Cocody Riviera Faya, Côte d'Ivoire)**.

### Coordonnées officielles :
- **Adresse :** Abidjan, Cocody Riviera Faya, Côte d'Ivoire
- **Téléphones :** +225 07 88 83 70 24 / +225 27 24 42 42 00
- **Email :** `Wikytechnologieci@gmail.com`
- **Horaires :** Lundi - Vendredi : 08h30 - 18h30 | Samedi : 09h00 - 14h00

### Les 4 Pôles d'Expertise Métier (Organisation interne) :
1. **Pôle Direction & Gestion de Projets :** Cadrage stratégique, relation client et suivi du cahier des charges.
2. **Pôle Communication Digitale & Community Management :** Animation quotidienne des réseaux sociaux (Facebook, Instagram, LinkedIn, TikTok), modération active et bienveillante des commentaires 7j/7, rédaction publicitaire (copywriting) et campagnes sponsorisées (Meta Ads & Google Ads).
3. **Pôle Graphisme & Identité Visuelle :** Création de logos vectoriels uniques, chartes graphiques complètes, kits papeterie et bannières pour réseaux sociaux.
4. **Pôle Audiovisuel & Studio Podcast :** Studio dédié insonorisé à Abidjan avec micros broadcast Shure SM7B, régie et caméras Sony 4K cinéma, éclairage Godox, montage dynamique et déclinaison en capsules virales (TikTok, Reels, Shorts).

---

## 3. 🏗️ Architecture Logicielle & Choix Techniques

Le projet respecte rigoureusement la séparation des responsabilités à travers le modèle **MVP / MVC (Modèle - Vue - Présentateur / Contrôleur)** :

```
             ┌─────────────────────────┐
             │       Navigateur        │
             └────────────┬────────────┘
                          │ Requête HTTP (URL propre ou ?page=...)
                          ▼
             ┌─────────────────────────┐
             │   index.php (Routeur)   │
             └────────────┬────────────┘
                          │ Instancie et appelle l'action
                          ▼
             ┌─────────────────────────┐
             │      Controllers/       │
             │ (ex: ContactController) │
             └──────┬────────────┬─────┘
    Données         │            │ Injection des variables
    et persistance  │            │
                    ▼            ▼
             ┌───────────┐  ┌───────────┐
             │  Models/  │  │  Views/   │
             └─────┬─────┘  └───────────┘
                   │
                   ▼
             ┌───────────┐
             │    PDO    │ ───► MySQL (Prod InfinityFree)
             │  Driver   │  ou  SQLite (Fallback Local autonome)
             └───────────┘
```

### 1. Contrôleur Frontal (`index.php`)
- Point d'entrée unique de toutes les requêtes HTTP.
- Démarre la session PHP de manière sécurisée.
- Charge les configurations globales (`App.php`) et la connexion à la base de données (`Database.php`).
- Implémente un **Autoloader PSR-4 natif** sans dépendance externe pour charger automatiquement toutes les classes sous le namespace `App\`.
- Détecte dynamiquement la route demandée via le paramètre d'URL `?page=...` ou via la réécriture d'URL Apache `REQUEST_URI`.
- Table de routage explicite via une structure `switch ($page)`.
- Gestion native des erreurs 404 avec affichage d'une vue d'erreur soignée.

### 2. Les Contrôleurs (`app/Controllers/`)
- `HomeController.php` : Agrège les données d'accueil (KPIs chiffrés, sélection de services, extraits de réalisations, avis clients).
- `AboutController.php` : Présente l'histoire, la vision, les 4 pôles organisationnels et les valeurs d'entreprise.
- `ServiceController.php` : Liste les 4 prestations majeures et les 3 packs tarifaires (Pack Starter, Pack Identité, Pack Studio Podcast).
- `PortfolioController.php` : Expose les réalisations filtrables par catégorie (`branding`, `community`, `podcast`, `startup`).
- `PodcastController.php` : Présente la cabine insonorisée, les équipements broadcast (Shure, Sony 4K) et des formats d'émissions suggérés aux PME.
- `ContactController.php` : Gère l'affichage du formulaire de contact, la génération du token CSRF, et le traitement POST avec validation et redirection flash.
- `DevisController.php` : Gère le formulaire de devis détaillé et le traitement de soumission en base de données.

### 3. Les Modèles (`app/Models/`)
- `ContactModel.php` : Persistance des messages de contact via PDO avec requêtes préparées (`INSERT INTO messages ...`) et méthode de consultation `getLatest()`.
- `DevisModel.php` : Persistance des demandes de devis (`INSERT INTO devis_requests ...`) et algorithme de calcul tarifaire indicatif `estimatePrice()`.
- `ServiceModel.php` : Fournit les données statiques structurées des offres, fonctionnalités et tarifs indicatifs.
- `PortfolioModel.php` : Fournit les études de cas détaillées avec métriques d'impact (KPIs réels) et filtrage par catégorie.

### 4. Les Vues (`app/Views/`)
- Découpage modulaire :
  - `layout/header.php` : Balises META SEO, Open Graph & Twitter Cards, préconnexions Google Fonts, liens CSS, et script anti-FOUC (Flash of Unstyled Content).
  - `layout/navbar.php` : Barre de navigation sticky, logo, liens, déclencheur de recherche, sélecteur de thème, et tiroir latéral responsive (menu mobile Aside).
  - `layout/footer.php` : Liens de navigation secondaire, coordonnées, mentions légales, crédit de soutenance BTS, modale de recherche Spotlight, et panneau de personnalisation d'accents graphiques.
  - `pages/*.php` : Contenu spécifique à chaque page (`home.php`, `about.php`, `services.php`, `portfolio.php`, `podcast.php`, `contact.php`, `devis.php`).

---

## 4. 💾 Base de Données & Gestionnaire PDO Intelligent

La classe `App\Config\Database` implémente un patron **Singleton** à double détente exceptionnellement robuste :

### Double Mode SGBD (Auto-détection & Fallback) :
1. **Mode MySQL (Production InfinityFree / WAMP / XAMPP) :**
   - Connecte à MySQL si les constantes `DB_HOST` et `DB_USER` sont renseignées.
   - Utilise l'encodage `utf8mb4` et le mode d'exception strict `PDO::ERRMODE_EXCEPTION`.
2. **Mode SQLite Fallback (Local & Démonstration sans configuration) :**
   - Si les identifiants MySQL par défaut sont détectés ou si la connexion MySQL échoue, l'application bascule **automatiquement et silencieusement** sur une base SQLite locale (`database.sqlite`).
   - Le site fonctionne ainsi **immédiatement à 100%**, même si MySQL n'est pas lancé, évitant tout crash lors d'une démonstration rapide.
   - Les tables sont créées automatiquement à la volée (`ensureTablesExist`) si le fichier SQLite vient d'être créé.

### Schéma des Tables Relationnelles (`database.sql`) :

#### Table 1 : `messages` (Formulaire de contact)
| Colonne | Type | Description |
| :--- | :--- | :--- |
| `id` | INT AUTO_INCREMENT PK | Identifiant unique du message |
| `name` | VARCHAR(120) | Nom complet du prospect |
| `email` | VARCHAR(150) | Adresse email de contact |
| `phone` | VARCHAR(50) | Numéro de téléphone (optionnel) |
| `service` | VARCHAR(100) | Service concerné |
| `subject` | VARCHAR(200) | Objet du message |
| `message` | TEXT | Contenu textuel de la demande |
| `created_at` | DATETIME | Date et heure de réception |

#### Table 2 : `devis_requests` (Simulateur et demandes de devis)
| Colonne | Type | Description |
| :--- | :--- | :--- |
| `id` | INT AUTO_INCREMENT PK | Identifiant unique de la demande |
| `company_name` | VARCHAR(150) | Nom de l'entreprise ou marque |
| `contact_name` | VARCHAR(120) | Nom du responsable ou contact |
| `email` | VARCHAR(150) | Adresse email professionnelle |
| `phone` | VARCHAR(50) | Numéro de téléphone / WhatsApp |
| `service_type` | VARCHAR(100) | Prestation souhaitée |
| `budget_range` | VARCHAR(50) | Tranche budgétaire estimée |
| `urgency` | VARCHAR(50) | Délai de réalisation exigé |
| `project_details`| TEXT | Description du projet |
| `created_at` | DATETIME | Date et heure de soumission |

---

## 5. 🛡️ Sécurité Applicative

Le code applique les standards de sécurité web recommandés par l'OWASP :
1. **Anti-Injections SQL :** 100% des opérations d'écriture et de lecture avec paramètres utilisent des requêtes préparées PDO avec liaison stricte (`execute([':cle' => $valeur])`).
2. **Anti-CSRF (Cross-Site Request Forgery) :** Chaque formulaire génère un jeton cryptographique aléatoire de 32 octets (`bin2hex(random_bytes(32))`) stocké en session et validé côté serveur via `hash_equals()`.
3. **Anti-XSS (Cross-Site Scripting) :** La fonction d'aide universelle `e(?string $str): string` encapsule `htmlspecialchars(..., ENT_QUOTES, 'UTF-8')` et sécurise tout affichage de données dynamiques dans les vues.
4. **Protection Serveur Apache (`.htaccess`) :**
   - Interdiction du listing des répertoires (`Options -Indexes`).
   - Masquage des versions serveur (`ServerSignature Off`).
   - Blocage strict de l'accès direct aux fichiers sensibles (`database.sql`, `database.sqlite`, `.git`, `.pdf`).
   - En-têtes de sécurité HTTP : `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, `X-XSS-Protection: 1; mode=block`.

---

## 6. 🎨 Système Frontend & UI/UX (Conforme aux 7 Disciplines d'Élite)

Le frontend est construit conformément au référentiel d'architecture d'élite présent dans `skill.txt` :

1. **Typographie de précision :**
   - Échelle typographique harmonique basée sur le ratio mathématique **Perfect Fourth (1.333)**.
   - Typographie fluide avec `clamp()` CSS pour adapter dynamiquement la taille du texte entre mobile et desktop sans ruptures brutales.
   - Limite de mesure de lecture fixée à 65 caractères (`max-width: 65ch`) pour un confort ergonomique optimal.
   - Polices Google Fonts : *Plus Jakarta Sans* pour les titres et *Inter* pour le corps de texte.

2. **Théorie des Couleurs & Design Tokens :**
   - Palette 60/30/10 : Neutres bleutés élégants (60%), Bleu Royal et Marine institutionnel (30%), et Accent Corail/Orange vif pour les boutons d'action et conversions (10%).
   - Aucun gris pur utilisé (uniquement des teintes chromatiques bleutées évitant l'effet terne).

3. **Moteur Dynamique de Thèmes & Accents :**
   - **3 modes de base :** Thème Clair (`light`), Thème Sombre (`dark`) et Thème Marine (`navy`).
   - **5 palettes d'accents prédéfinies :** Orange Flamme, Bleu Cyan, Émeraude, Violet Royal, Or/Jaune.
   - **Sélecteur de couleur personnalisé libre :** Permet à l'utilisateur de choisir n'importe quel code hexadécimal à la volée.
   - **Persistance :** Sauvegarde des préférences dans le `localStorage` du navigateur.
   - **Zéro FOUC :** Un micro-script inline dans le `<head>` applique les attributs `data-theme` et `data-accent` avant le rendu de la page.

4. **Composants d'Interaction (Vanilla JS pur) :**
   - **Spotlight Search (Recherche Instantanée) :** Déclenchée au clic ou via le raccourci universel `Ctrl + K` (ou `Cmd + K`), permettant de filtrer instantanément l'ensemble des pages et services du site.
   - **Simulateur de Devis en Temps Réel :** Calculateur dynamique instantané ajustant le coût estimé en FCFA selon le service, l'envergure (`starter`, `standard`, `premium`) et l'urgence.
   - **Filtrage Dynamique du Portfolio :** Filtrage instantané côté client avec micro-animations d'opacité.
   - **Header Sticky & Jauge Circulaire :** En-tête qui s'élève au scroll, couplé à un bouton flottant de retour en haut doté d'un indicateur de progression circulaire en SVG (`strokeDashoffset`).
   - **Menu Mobile Latéral (Aside Drawer) :** Panneau coulissant fluide avec fond flouté (`backdrop-filter: blur()`).

---

## 7. 🗂️ Arborescence Exhaustive du Projet

```
c:\wamp64\www\achelyrapport/
│
├── .htaccess                           # Règles Apache : sécurité, masquage des fichiers sensibles & rewriting
├── index.php                           # Contrôleur frontal (Front Controller) & Routeur principal
├── database.sql                        # Script SQL d'installation MySQL (tables messages & devis_requests)
├── database.sqlite                     # Base de données SQLite locale générée automatiquement (fallback)
├── README.md                           # Documentation d'installation et de déploiement
├── RAPPORT_ADAPTATION_TECHNIQUE.md     # Document justificatif pour le jury de soutenance BTS IDA
├── resume.md                           # La présente fiche de synthèse universelle pour IA et développeurs
├── skill.txt                           # Guide de référence des 7 disciplines de l'architecture Front-End
├── logo.jpg                            # Logo officiel de l'agence
├── RAPPORT_DE_STAGE_WIKY_HOLDING.pdf   # Rapport de stage complet prêt à imprimer (9.3 Mo)
├── RAPPORT DE SOUTENANCE-ACHLEY.pdf    # Deuxième copie du rapport de soutenance BTS (1.5 Mo)
│
├── app/                                # Cœur applicatif PHP (Architecture MVC / MVP)
│   ├── Config/
│   │   ├── App.php                     # Constantes de l'agence, helpers d'URL et fonction d'échappement e()
│   │   └── Database.php                # Singleton PDO avec détection automatique MySQL / SQLite
│   │
│   ├── Controllers/
│   │   ├── HomeController.php          # Page d'accueil : KPIs, services phares, témoignages
│   │   ├── AboutController.php         # Page À propos : histoire, valeurs et 4 pôles internes
│   │   ├── ServiceController.php       # Page Services : catalogue détaillé et packs tarifaires
│   │   ├── PortfolioController.php     # Page Réalisations : galerie filtrable par métier
│   │   ├── PodcastController.php       # Page Studio : régie 4K, micros Shure, cabine insonorisée
│   │   ├── ContactController.php       # Page Contact : formulaire, protection CSRF et sauvegarde PDO
│   │   └── DevisController.php         # Page Devis : calculateur en ligne et formulaire de soumission
│   │
│   ├── Models/
│   │   ├── ContactModel.php            # Persistance des messages (table `messages`)
│   │   ├── DevisModel.php              # Persistance et calcul des devis (table `devis_requests`)
│   │   ├── PortfolioModel.php          # Liste des projets et études de cas avec KPIs
│   │   └── ServiceModel.php            # Liste des offres, descriptions et livrables
│   │
│   └── Views/
│       ├── layout/
│       │   ├── header.php              # En-tête HTML, métas SEO, OG tags, Google Fonts, script anti-FOUC
│       │   ├── navbar.php              # Navigation principale, sélecteur de thème, recherche, menu aside
│       │   └── footer.php              # Pied de page, modale Spotlight search, tiroir de styles, crédits
│       │
│       └── pages/
│           ├── home.php                # Vue Accueil (Hero, KPIs, Services, Process, Avis)
│           ├── about.php               # Vue À propos (Histoire, Manifeste, 4 Pôles, Équipe)
│           ├── services.php            # Vue Services (Fiches métiers, Formules Packs)
│           ├── portfolio.php           # Vue Réalisations (Filtres par pills, Cartes projets)
│           ├── podcast.php             # Vue Studio Podcast (Équipements, Idées d'émissions)
│           ├── contact.php             # Vue Contact (Coordonnées Cocody, FAQ, Formulaire)
│           └── devis.php               # Vue Devis (Simulateur interactif temps réel + Formulaire)
│
├── assets/                             # Fichiers statiques publics
│   ├── css/
│   │   └── style.css                   # Feuille de styles globale (Design Tokens, Responsive, Thèmes)
│   ├── js/
│   │   └── main.js                     # Interactions frontend (Theme switcher, Devis live, Search, Aside)
│   └── images/                         # Photographies et illustrations optimisées du site
│
└── DeleteProd/                         # Dossier d'outillage éditorial & génération de rapport (hors prod)
    ├── captures/
    │   ├── capture_screens.py          # Script Playwright de captures d'écran Desktop & Mobile en local
    │   └── screens/                    # Captures d'écran PNG des différentes pages du site
    ├── gen_pdf.py                      # Script Playwright compilant `rapport.html` en PDF A4 officiel
    ├── rapport.html                    # Version HTML complète du rapport de stage formatée pour l'impression A4
    ├── promptdusite.txt                # Notes et instructions initiales de création du projet
    └── frontend.txt                    # Copie de référence des règles du design system
```

---

## 8. 🗺️ Table des Routes & Points d'Entrée HTTP

| URL / Route | Méthode | Contrôleur | Action | Rôle & Description |
| :--- | :---: | :--- | :--- | :--- |
| `/` ou `index.php?page=home` | GET | `HomeController` | `index()` | Page d'accueil : vitrine globale, statistiques clés et réassurance |
| `index.php?page=about` | GET | `AboutController` | `index()` | Page institutionnelle, présentation des 4 départements et de l'équipe |
| `index.php?page=services` | GET | `ServiceController` | `index()` | Présentation exhaustive des 4 offres et des 3 packs commerciaux |
| `index.php?page=portfolio` | GET | `PortfolioController` | `index()` | Galerie des réalisations avec filtrage dynamique par onglets |
| `index.php?page=podcast` | GET | `PodcastController` | `index()` | Focus sur le studio insonorisé à Abidjan et les formats audiovisuels |
| `index.php?page=contact` | GET | `ContactController` | `index()` | Affichage des coordonnées à Cocody, FAQ interactive et formulaire |
| `index.php?page=contact-submit`| POST | `ContactController` | `submit()` | Validation CSRF, sanitisation et insertion du message en base |
| `index.php?page=devis` | GET | `DevisController` | `index()` | Simulateur tarifaire indicatif temps réel et formulaire de projet |
| `index.php?page=devis-submit` | POST | `DevisController` | `submit()` | Validation CSRF, vérification des champs et enregistrement du devis |
| *(Toute autre route)* | ALL | *(Front Controller)* | *404* | Page d'erreur 404 soignée avec bouton de retour à l'accueil |

---

## 9. 🚀 Guide d'Installation, Exécution & Déploiement

### Option 1 : Exécution locale immédiate (Serveur interne PHP)
Puisque le projet dispose d'un fallback SQLite automatique, aucune configuration de base de données n'est obligatoire pour le tester en local :
```bash
# Se placer à la racine du projet
cd c:\wamp64\www\achelyrapport

# Démarrer le serveur interne de développement
php -S localhost:8000
```
Ouvrir votre navigateur à l'adresse : `http://localhost:8000`.

### Option 2 : Exécution sous WAMP / XAMPP / Laragon
1. Le projet se trouve déjà dans le répertoire web `c:\wamp64\www\achelyrapport`.
2. Démarrer WampServer (Apache + MySQL).
3. Créer une base de données MySQL nommée `wiky_db` dans phpMyAdmin et importer `database.sql`.
4. Dans `app/Config/Database.php`, configurer les accès locaux :
   ```php
   public const DB_HOST = 'localhost';
   public const DB_NAME = 'wiky_db';
   public const DB_USER = 'root';
   public const DB_PASS = '';
   ```
5. Accéder au site via `http://localhost/achelyrapport/`.

### Option 3 : Déploiement sur l'hébergement gratuit InfinityFree
1. Créer un compte d'hébergement sur [InfinityFree](https://app.infinityfree.com).
2. Créer une base de données MySQL dans le panneau de contrôle cPanel.
3. Importer le fichier `database.sql` via phpMyAdmin en ligne.
4. Renseigner les identifiants réels fournis par InfinityFree dans `app/Config/Database.php` :
   ```php
   public const DB_HOST = 'sqlxxx.infinityfree.com';
   public const DB_NAME = 'if0_xxxxxxx_wiky_db';
   public const DB_USER = 'if0_xxxxxxx';
   public const DB_PASS = 'VotreMotDePasseInfinityFree';
   ```
5. Téléverser l'ensemble des fichiers à la racine du dossier distant `htdocs/` via FileZilla (ou le Web File Manager).
6. Le site est opérationnel et sécurisé avec certificat SSL HTTPS gratuit.

---

## 10. 📝 Note pour les IA & Développeurs Ultérieurs

- **Fichiers orphelins / Hors périmètre dans `assets/images/` :**  
  Deux fichiers JSON (`WhatsApp auto-reply with Gemini.json` et `monbotrepondetelegram.json`) sont présents en local dans le dossier `assets/images/`. Il s'agit de workflows d'automatisation n8n provenant d'un travail tiers, déposés là par inadvertance. Ils ne font pas partie du site web de l'agence Wiky Holding et ne doivent **pas** être intégrés ou versionnés avec l'application web.
- **Rapports PDF :**  
  Le fichier `RAPPORT_DE_STAGE_WIKY_HOLDING.pdf` est le document final généré et prêt pour la soutenance. En cas de modification textuelle du rapport, il convient de modifier `DeleteProd/rapport.html` puis d'exécuter `python DeleteProd/gen_pdf.py` (nécessite la bibliothèque Python `playwright`).
