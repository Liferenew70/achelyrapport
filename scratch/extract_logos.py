import pymupdf
import os

doc = pymupdf.open('RAPPORT DE SOUTENANCE-ACHLEY.pdf')
os.makedirs('scratch/logos', exist_ok=True)
count = 0
for page_num in range(len(doc)):
    for img in doc.get_page_images(page_num):
        xref = img[0]
        base_img = doc.extract_image(xref)
        w, h = base_img['width'], base_img['height']
        ext = base_img['ext']
        if w > 40 and h > 40:
            filename = f"scratch/logos/img_p{page_num}_{xref}_{w}x{h}.{ext}"
            with open(filename, 'wb') as f:
                f.write(base_img['image'])
            print(filename, len(base_img['image']))
            count += 1
print('total images > 40px:', count)
