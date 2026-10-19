-- ==============================================================
-- BASE DE DONNÉES : DIGITAL AGENCY WIKY / WIKY HOLDING
-- Compatibilité : MySQL 5.7+ / MariaDB 10+ (InfinityFree / XAMPP)
-- ==============================================================

SET NAMES utf8mb4;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

-- --------------------------------------------------------------
-- Table 1: Messages du formulaire de contact
-- --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `messages` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(120) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `phone` VARCHAR(50) DEFAULT NULL,
  `service` VARCHAR(100) DEFAULT 'Général',
  `subject` VARCHAR(200) DEFAULT NULL,
  `message` TEXT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------------
-- Table 2: Demandes de devis détaillées
-- --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `devis_requests` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `company_name` VARCHAR(150) NOT NULL,
  `contact_name` VARCHAR(120) NOT NULL,
  `email` VARCHAR(150) NOT NULL,
  `phone` VARCHAR(50) NOT NULL,
  `service_type` VARCHAR(100) NOT NULL,
  `budget_range` VARCHAR(50) DEFAULT 'Non précisé',
  `urgency` VARCHAR(50) DEFAULT 'Normal (2-3 semaines)',
  `project_details` TEXT NOT NULL,
  `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------------
-- Données d'exemple pour tester la réception
-- --------------------------------------------------------------
INSERT INTO `messages` (`name`, `email`, `phone`, `service`, `subject`, `message`, `created_at`) VALUES
('Jean-Marc Koffi', 'koffi.jm@example.ci', '+225 07 12 34 56', 'Community Management', 'Accompagnement marque cosmétique', 'Bonjour, nous souhaitons déléguer la gestion de nos réseaux sociaux Instagram et Facebook avec modération de commentaires 7j/7.', NOW());

INSERT INTO `devis_requests` (`company_name`, `contact_name`, `email`, `phone`, `service_type`, `budget_range`, `urgency`, `project_details`, `created_at`) VALUES
('Ivoire Tech Solutions', 'Aïssata Traoré', 'aissata@ivoiretech.ci', '+225 05 98 76 54', 'Branding & Identité Visuelle', '500.000 - 1.000.000 FCFA', 'Urgent (< 1 semaine)', 'Création complète de la charte graphique, du logo vectoriel et des déclinaisons pour lancement officiel de notre fintech.', NOW());
