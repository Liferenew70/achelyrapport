import pymupdf

doc = pymupdf.open('RAPPORT DE SOUTENANCE-ACHLEY.pdf')
page = doc[0]
for idx, info in enumerate(page.get_image_info()):
    if info['width'] > 40 and info['height'] > 40:
        print(idx, "bbox:", info['bbox'], "size:", info['width'], "x", info['height'], "bytes:", info['size'])
