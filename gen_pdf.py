from playwright.sync_api import sync_playwright
import os

HTML_PATH = os.path.abspath("rapport.html")
PDF_PATH = os.path.abspath("RAPPORT_DE_STAGE_WIKY_HOLDING.pdf")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    # Charger le fichier HTML local
    page.goto("file:///" + HTML_PATH.replace("\\", "/"), wait_until="networkidle")
    # Attendre que les images/captures soient chargées
    page.wait_for_timeout(3000)
    page.pdf(
        path=PDF_PATH,
        format="A4",
        print_background=True,
        margin={"top": "22mm", "right": "18mm", "bottom": "20mm", "left": "18mm"},
        display_header_footer=False,  # géré par @page CSS
    )
    browser.close()
print("PDF genere :", PDF_PATH)
print("Taille :", os.path.getsize(PDF_PATH), "octets")
