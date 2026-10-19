<?php
namespace App\Models;

use App\Config\Database;
use PDO;
use Exception;

class ContactModel
{
    /**
     * Enregistre un message de contact dans la base de données
     */
    public static function save(array $data): bool
    {
        try {
            $pdo = Database::getConnection();
            $stmt = $pdo->prepare("
                INSERT INTO messages (name, email, phone, service, subject, message, created_at)
                VALUES (:name, :email, :phone, :service, :subject, :message, datetime('now'))
            ");

            // Adaptation syntaxique SQLite vs MySQL pour la date courante
            $driver = $pdo->getAttribute(PDO::ATTR_DRIVER_NAME);
            if ($driver === 'mysql') {
                $stmt = $pdo->prepare("
                    INSERT INTO messages (name, email, phone, service, subject, message, created_at)
                    VALUES (:name, :email, :phone, :service, :subject, :message, NOW())
                ");
            }

            return $stmt->execute([
                ':name'    => $data['name'],
                ':email'   => $data['email'],
                ':phone'   => $data['phone'] ?? null,
                ':service' => $data['service'] ?? 'Général',
                ':subject' => $data['subject'] ?? 'Demande de contact',
                ':message' => $data['message'],
            ]);
        } catch (Exception $e) {
            error_log("Erreur ContactModel: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Récupère les derniers messages reçus (pour le suivi administratif)
     */
    public static function getLatest(int $limit = 10): array
    {
        try {
            $pdo = Database::getConnection();
            $stmt = $pdo->prepare("SELECT * FROM messages ORDER BY id DESC LIMIT :limit");
            $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
            $stmt->execute();
            return $stmt->fetchAll();
        } catch (Exception $e) {
            return [];
        }
    }
}
