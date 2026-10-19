<?php
/**
 * Wiky Holding - Gestionnaire de Connexion PDO
 * Compatible hébergement mutualisé InfinityFree (MySQL) et mode local/démonstration (SQLite fallback)
 */

namespace App\Config;

use PDO;
use PDOException;

class Database
{
    private static ?PDO $instance = null;

    // Configuration MySQL pour InfinityFree ou environnement local (XAMPP / WAMP)
    // Remplacer ces constantes avec les identifiants fournis dans le panneau cPanel InfinityFree :
    public const DB_HOST = 'sqlxxx.infinityfree.com'; // ex: sql300.infinityfree.com ou localhost
    public const DB_NAME = 'if0_xxxxxxx_wiky_db';    // ex: if0_37000000_wiky_db
    public const DB_USER = 'if0_xxxxxxx';            // ex: if0_37000000
    public const DB_PASS = 'votre_mot_de_passe';     // Mot de passe compte InfinityFree
    public const DB_CHARSET = 'utf8mb4';

    /**
     * Récupère l'instance unique de connexion PDO (Singleton)
     */
    public static function getConnection(): PDO
    {
        if (self::$instance === null) {
            self::$instance = self::createConnection();
        }
        return self::$instance;
    }

    /**
     * Initialise la connexion : tente MySQL d'abord, sinon bascule sur SQLite pour garantir le fonctionnement immédiat
     */
    private static function createConnection(): PDO
    {
        // 1. Essai de connexion MySQL si les identifiants ne sont plus les valeurs par défaut
        if (self::DB_HOST !== 'sqlxxx.infinityfree.com' && self::DB_USER !== 'if0_xxxxxxx') {
            try {
                $dsn = "mysql:host=" . self::DB_HOST . ";dbname=" . self::DB_NAME . ";charset=" . self::DB_CHARSET;
                $options = [
                    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
                    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                    PDO::ATTR_EMULATE_PREPARES   => false,
                ];
                $pdo = new PDO($dsn, self::DB_USER, self::DB_PASS, $options);
                self::ensureTablesExist($pdo, 'mysql');
                return $pdo;
            } catch (PDOException $e) {
                // Si la connexion MySQL échoue, on continue vers le fallback pour éviter le crash du site
                error_log("Avertissement MySQL: " . $e->getMessage());
            }
        }

        // 2. Mode local / démonstration : SQLite portable
        // Ce mode garantit que le site s'exécute à 100% sans configuration préalable
        $sqlitePath = dirname(__DIR__, 2) . '/database.sqlite';
        $isNewDb = !file_exists($sqlitePath);
        
        $pdo = new PDO('sqlite:' . $sqlitePath);
        $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

        if ($isNewDb || filesize($sqlitePath) === 0) {
            self::ensureTablesExist($pdo, 'sqlite');
        }

        return $pdo;
    }

    /**
     * Auto-initialisation des tables nécessaires au site
     */
    private static function ensureTablesExist(PDO $pdo, string $driver): void
    {
        if ($driver === 'sqlite') {
            $pdo->exec("
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT,
                    service TEXT,
                    subject TEXT,
                    message TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS devis_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT NOT NULL,
                    contact_name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    service_type TEXT NOT NULL,
                    budget_range TEXT,
                    urgency TEXT,
                    project_details TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
            ");
        } else {
            $pdo->exec("
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(120) NOT NULL,
                    email VARCHAR(150) NOT NULL,
                    phone VARCHAR(50),
                    service VARCHAR(100),
                    subject VARCHAR(200),
                    message TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

                CREATE TABLE IF NOT EXISTS devis_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    company_name VARCHAR(150) NOT NULL,
                    contact_name VARCHAR(120) NOT NULL,
                    email VARCHAR(150) NOT NULL,
                    phone VARCHAR(50) NOT NULL,
                    service_type VARCHAR(100) NOT NULL,
                    budget_range VARCHAR(50),
                    urgency VARCHAR(50),
                    project_details TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            ");
        }
    }
}
