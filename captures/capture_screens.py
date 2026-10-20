"""
Script de capture d'écran du site Wiky Holding (localhost:8000)
Génère des captures desktop et mobile de chaque page pour le rapport de stage.
"""
from playwright.sync_api import sync_playwright
import os
import time

BASE_URL = "http://localhost:8000"
OUT_DIR = os.path.join(os.path.dirname(__file__), "screens")
os.makedirs(OUT_DIR, exist_ok=True)

PAGES = [
    ("accueil", "/"),
    ("a-propos", "/index.php?page=about"),
    ("services", "/index.php?page=services"),
    ("portfolio", "/index.php?page=portfolio"),
    ("podcast", "/index.php?page=podcast"),
    ("contact", "/index.php?page=contact"),
    ("devis", "/index.php?page=devis"),
]

DESKTOP = {"width": 1366, "height": 900}
MOBILE = {"width": 375, "height": 812}

def wait_ready(page):
    """Attend que la page soit complètement chargée (réseau inactif + images)."""
    page.wait_for_load_state("networkidle")
    time.sleep(1.5)  # laisse le temps aux images CSS/JS de se positionner

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport=DESKTOP)

        for slug, path in PAGES:
            page = context.new_page()
            page.goto(BASE_URL + path, wait_until="networkidle")
            wait_ready(page)
            out = os.path.join(OUT_DIR, f"{slug}-desktop.png")
            page.screenshot(full_page=True, path=out)
            print(f"[OK] desktop -> {out}")
            page.close()

        # Vues mobiles (accueil + contact + devis pour montrer le responsive & menu hamburger)
        context.close()
        context = browser.new_context(viewport=MOBILE)
        mobile_pages = [("accueil", "/"), ("contact", "/index.php?page=contact"), ("devis", "/index.php?page=devis"), ("portfolio", "/index.php?page=portfolio")]
        for slug, path in mobile_pages:
            page = context.new_page()
            page.goto(BASE_URL + path, wait_until="networkidle")
            wait_ready(page)
            out = os.path.join(OUT_DIR, f"{slug}-mobile.png")
            page.screenshot(full_page=True, path=out)
            print(f"[OK] mobile  -> {out}")
            page.close()

        browser.close()
    print("Toutes les captures sont terminees.")

if __name__ == "__main__":
    main()
