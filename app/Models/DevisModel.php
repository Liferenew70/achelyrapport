<?php
namespace App\Models;

use App\Config\Database;
use PDO;
use Exception;

class DevisModel
{
    /**
     * Enregistre une demande de devis dans la base de données
     */
    public static function save(array $data): bool
    {
        try {
            $pdo = Database::getConnection();
            $driver = $pdo->getAttribute(PDO::ATTR_DRIVER_NAME);

            $sql = $driver === 'mysql'
                ? "INSERT INTO devis_requests (company_name, contact_name, email, phone, service_type, budget_range, urgency, project_details, created_at)
                   VALUES (:company_name, :contact_name, :email, :phone, :service_type, :budget_range, :urgency, :project_details, NOW())"
                : "INSERT INTO devis_requests (company_name, contact_name, email, phone, service_type, budget_range, urgency, project_details, created_at)
                   VALUES (:company_name, :contact_name, :email, :phone, :service_type, :budget_range, :urgency, :project_details, datetime('now'))";

            $stmt = $pdo->prepare($sql);

            return $stmt->execute([
                ':company_name'    => $data['company_name'],
                ':contact_name'    => $data['contact_name'],
                ':email'           => $data['email'],
                ':phone'           => $data['phone'],
                ':service_type'    => $data['service_type'],
                ':budget_range'    => $data['budget_range'] ?? 'Non précisé',
                ':urgency'         => $data['urgency'] ?? 'Normal',
                ':project_details' => $data['project_details'],
            ]);
        } catch (Exception $e) {
            error_log("Erreur DevisModel: " . $e->getMessage());
            return false;
        }
    }

    /**
     * Estime un tarif indicatif pour le simulateur en temps réel (en FCFA)
     */
    public static function estimatePrice(string $service, string $scope, string $speed): array
    {
        $basePrices = [
            'community-management' => 150000,
            'branding-logos'       => 250000,
            'studio-podcast'       => 80000,
            'creation-entreprise'  => 450000,
        ];

        $scopeMultipliers = [
            'starter' => 1.0,
            'standard' => 1.6,
            'premium' => 2.4,
        ];

        $speedMultipliers = [
            'normal' => 1.0,
            'urgent' => 1.3,
        ];

        $base = $basePrices[$service] ?? 150000;
        $scopeMult = $scopeMultipliers[$scope] ?? 1.0;
        $speedMult = $speedMultipliers[$speed] ?? 1.0;

        $total = (int) round($base * $scopeMult * $speedMult);

        return [
            'total' => $total,
            'formatted' => number_format($total, 0, ',', ' ') . ' FCFA'
        ];
    }
}
