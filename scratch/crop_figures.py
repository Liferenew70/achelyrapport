from PIL import Image
import os

os.makedirs('scratch/docx_assets/fig', exist_ok=True)
screens_dir = 'DeleteProd/captures/screens'

# Load desktop images
im_home = Image.open(f'{screens_dir}/accueil-desktop.png')
im_about = Image.open(f'{screens_dir}/a-propos-desktop.png')
im_services = Image.open(f'{screens_dir}/services-desktop.png')
im_portfolio = Image.open(f'{screens_dir}/portfolio-desktop.png')
im_podcast = Image.open(f'{screens_dir}/podcast-desktop.png')
im_contact = Image.open(f'{screens_dir}/contact-desktop.png')
im_devis = Image.open(f'{screens_dir}/devis-desktop.png')

# Load mobile images
im_mob_home = Image.open(f'{screens_dir}/accueil-mobile.png')
im_mob_devis = Image.open(f'{screens_dir}/devis-mobile.png')

W = 1366

# 1. home_hero: (0, 0, W, 850)
im_home.crop((0, 0, W, 850)).save('scratch/docx_assets/fig/home_hero.png')

# 2. home_services: approx (0, 1150, W, 2300)
im_home.crop((0, 1150, W, 2250)).save('scratch/docx_assets/fig/home_services.png')

# 3. home_real: approx (0, 2250, W, 3350)
im_home.crop((0, 2250, W, 3350)).save('scratch/docx_assets/fig/home_real.png')

# 4. home_method: approx (0, 3350, W, 4250)
im_home.crop((0, 3350, W, 4250)).save('scratch/docx_assets/fig/home_method.png')

# 5. about_top: (0, 0, W, 1100)
im_about.crop((0, 0, W, 1100)).save('scratch/docx_assets/fig/about_top.png')

# 6. about_poles: approx (0, 1100, W, 2300)
im_about.crop((0, 1100, W, 2300)).save('scratch/docx_assets/fig/about_poles.png')

# 7. about_values: approx (0, 2300, W, 3300)
im_about.crop((0, 2300, W, 3250)).save('scratch/docx_assets/fig/about_values.png')

# 8. serv_top: (0, 0, W, 1300)
im_services.crop((0, 0, W, 1300)).save('scratch/docx_assets/fig/serv_top.png')

# 9. serv_packs: approx (0, 3400, W, 4450)
im_services.crop((0, 3400, W, 4500)).save('scratch/docx_assets/fig/serv_packs.png')

# 10. port_top: (0, 0, W, 700)
im_portfolio.crop((0, 0, W, 700)).save('scratch/docx_assets/fig/port_top.png')

# 11. port_cards: approx (0, 700, W, 2200)
im_portfolio.crop((0, 700, W, 2200)).save('scratch/docx_assets/fig/port_cards.png')

# 12. pod_top: (0, 0, W, 1100)
im_podcast.crop((0, 0, W, 1100)).save('scratch/docx_assets/fig/pod_top.png')

# 13. pod_equip: approx (0, 1100, W, 2300)
im_podcast.crop((0, 1100, W, 2300)).save('scratch/docx_assets/fig/pod_equip.png')

# 14. cont_form: (0, 0, W, 1300)
im_contact.crop((0, 0, W, 1300)).save('scratch/docx_assets/fig/cont_form.png')

# 15. cont_faq: approx (0, 1300, W, 2450)
im_contact.crop((0, 1300, W, 2450)).save('scratch/docx_assets/fig/cont_faq.png')

# 16. devis: (0, 0, W, 1350)
im_devis.crop((0, 0, W, 1350)).save('scratch/docx_assets/fig/devis.png')

# 17 & 18. mob_a & mob_b: mobile home & devis (top 1000px)
im_mob_home.crop((0, 0, 375, 950)).save('scratch/docx_assets/fig/mob_a.png')
im_mob_devis.crop((0, 0, 375, 950)).save('scratch/docx_assets/fig/mob_b.png')

print("All figures cropped and saved successfully!")
print("Figures count:", len(os.listdir('scratch/docx_assets/fig')))
