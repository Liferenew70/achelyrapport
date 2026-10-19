# Digital Agency Wiky (Wiky Holding) — Site Web Moderne en PHP MVP & PDO

Projet web d'entreprise réalisé pour la soutenance de **BTS Informatique Développeur d'Application (IDA)**.

---

## 🌟 Présentation de l'Entreprise & Métiers
**Digital Agency Wiky (Wiky Holding)** est une agence 360° basée à Abidjan (Côte d'Ivoire), spécialisée dans :
1. **Community Management & Modération :** Animation des réseaux, modération et réponses soignées aux commentaires 7j/7, rédaction publicitaire et Meta Ads.
2. **Identité Visuelle & Conception de Logos :** Logos vectoriels, chartes graphiques complètes, kits de lancement de marque.
3. **Studio Podcast & Production Audiovisuelle :** Studio insonorisé et équipé à Abidjan, captation 4K, micros broadcast, montage et capsules réseaux (Reels, TikTok, Shorts).
4. **Création d'Entreprise & Stratégie :** Naming, positionnement de marque et accompagnement des porteurs de projets.

---

## 🚀 Architecture Technique
- **Design Pattern :** Architecture MVP / MVC (Modèle - Vue - Présentateur / Contrôleur).
- **Backend :** PHP Vanilla moderne (compatible PHP 7.4 à 8.3).
- **Base de Données :** PDO (PHP Data Objects) avec requêtes préparées anti-injections SQL.
- **SGBD :** MySQL (pour InfinityFree, XAMPP, WAMP) + Fallback SQLite autonome sans configuration préalable.
- **Frontend d'Élite :** HTML5 sémantique + Vanilla CSS pur avec Design Tokens (échelle typographique harmonique, ratio 60/30/10, fluid clamp, animations GPU, `prefers-reduced-motion`) + Vanilla JavaScript ES6.

---

## 📁 Arborescence des Fichiers
```
├── app/
│   ├── Config/
│   │   ├── App.php             # Constantes et fonctions helpers
│   │   └── Database.php        # Connexion PDO MySQL (InfinityFree) & SQLite
│   ├── Controllers/            # Logique métier et routage des actions
│   │   ├── HomeController.php
│   │   ├── AboutController.php
│   │   ├── ServiceController.php
│   │   ├── PortfolioController.php
│   │   ├── PodcastController.php
│   │   ├── ContactController.php
│   │   └── DevisController.php
│   ├── Models/                 # Couche de données et requêtes SQL
│   │   ├── ContactModel.php
│   │   ├── DevisModel.php
│   │   ├── PortfolioModel.php
│   │   └── ServiceModel.php
│   └── Views/                  # Vues HTML et gabarits d'affichage
│       ├── layout/             # Header, Navbar responsive, Footer
│       └── pages/              # Accueil, À propos, Services, Portfolio, Podcast, Contact, Devis
├── assets/
│   ├── css/style.css           # Système de design complet
│   └── js/main.js              # Interactions, filtres & simulateur temps réel
├── database.sql                # Fichier SQL à importer dans phpMyAdmin
├── .htaccess                   # Sécurité et réécriture d'URL Apache
├── index.php                   # Contrôleur frontal (Front Controller)
├── README.md                   # Ce guide
└── RAPPORT_ADAPTATION_TECHNIQUE.md # Synthèse pour la soutenance BTS
```

---

## 💻 Test en Local

### Option A : Avec le serveur interne de PHP
Si PHP est installé sur votre ordinateur :
```bash
php -S localhost:8000
```
Ouvrez ensuite votre navigateur sur `http://localhost:8000`.

### Option B : Avec XAMPP / WampServer / Laragon
1. Déposez l'ensemble du dossier dans `C:\xampp\htdocs\bts-achley`.
2. Lancez Apache et MySQL.
3. Accédez à `http://localhost/bts-achley/`.

---

## 🌐 Déploiement sur InfinityFree (Hébergement Gratuit)

1. Connectez-vous sur votre compte [InfinityFree](https://app.infinityfree.com).
2. Créez une base de données dans le cPanel (**MySQL Databases**).
3. Ouvrez **phpMyAdmin** et importez le fichier `database.sql`.
4. Ouvrez le fichier `app/Config/Database.php` et renseignez les constantes :
   ```php
   public const DB_HOST = 'sqlxxx.infinityfree.com';
   public const DB_NAME = 'if0_xxxxxxx_wikydb';
   public const DB_USER = 'if0_xxxxxxx';
   public const DB_PASS = 'votre_mot_de_passe';
   ```
5. Téléversez tous les fichiers du projet dans le dossier `htdocs/` via FTP (FileZilla) ou le gestionnaire de fichiers en ligne.
6. Votre site est immédiatement en ligne et fonctionnel !
