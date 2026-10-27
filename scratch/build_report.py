# -*- coding: utf-8 -*-
import sys, json, os, subprocess
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import pymupdf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
ASSETS_DIR = os.path.join(SCRIPT_DIR, "docx_assets")
FIG_DIR = os.path.join(ASSETS_DIR, "fig") + "/"
LOGO_DIR = os.path.join(ASSETS_DIR, "logos") + "/"

FINAL_DOCX = os.path.join(PROJECT_DIR, "RAPPORT_DE_STAGE_WIKY_HOLDING.docx")
FINAL_PDF = os.path.join(PROJECT_DIR, "RAPPORT_DE_STAGE_WIKY_HOLDING.pdf")
TEMP_DOCX = os.path.join(SCRIPT_DIR, "temp_report.docx")
TEMP_PDF = os.path.join(SCRIPT_DIR, "temp_report.pdf")
PAGES_JSON = os.path.join(SCRIPT_DIR, "pages.json")
TOC_JSON = os.path.join(SCRIPT_DIR, "toc_entries.json")

def generate_document(out_path, pages_dict):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.5)
    sec.top_margin = Cm(2.3); sec.bottom_margin = Cm(2.3)
    sec.different_first_page_header_footer = True

    BLACK = RGBColor(0, 0, 0)

    def setfont(style, size, bold=False, italic=False):
        style.font.name = "Times New Roman"
        style.element.rPr.rFonts.set(qn("w:eastAsia"), "Times New Roman")
        style.font.size = Pt(size); style.font.bold = bold; style.font.italic = italic
        style.font.color.rgb = BLACK

    st = doc.styles
    setfont(st["Normal"], 12)
    st["Normal"].paragraph_format.space_after = Pt(6)
    st["Normal"].paragraph_format.line_spacing = 1.3
    for name, size, align, before, after in (("Heading 1", 16, WD_ALIGN_PARAGRAPH.CENTER, 0, 14),
                                             ("Heading 2", 14, WD_ALIGN_PARAGRAPH.LEFT, 14, 8),
                                             ("Heading 3", 12.5, WD_ALIGN_PARAGRAPH.LEFT, 12, 6),
                                             ("Heading 4", 12, WD_ALIGN_PARAGRAPH.LEFT, 8, 4)):
        s = st[name]; setfont(s, size, bold=True)
        s.paragraph_format.alignment = align
        s.paragraph_format.space_before = Pt(before); s.paragraph_format.space_after = Pt(after)
        s.paragraph_format.keep_with_next = True
        s.paragraph_format.line_spacing = 1.1

    toc_entries = []  # (level, text)

    def P(text="", bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=None, after=None, keep=False, indent=None):
        p = doc.add_paragraph()
        p.alignment = align
        if after is not None: p.paragraph_format.space_after = Pt(after)
        if indent: p.paragraph_format.left_indent = Cm(indent)
        if keep: p.paragraph_format.keep_with_next = True
        parts = text.split("**")
        for i, t in enumerate(parts):
            if not t: continue
            r = p.add_run(t); r.bold = bold or (i % 2 == 1); r.italic = italic
            r.font.name = "Times New Roman"
            if size: r.font.size = Pt(size)
        return p

    def H(level, text, toc=True, page_break=False):
        h = doc.add_heading(text, level=level)
        if page_break: h.paragraph_format.page_break_before = True
        if toc: toc_entries.append((level, text))
        return h

    def BL(items, indent=0.6):
        for it in items:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.left_indent = Cm(indent + 0.6)
            p.paragraph_format.first_line_indent = Cm(-0.6)
            p.paragraph_format.space_after = Pt(3)
            parts = ("-\t" + it).split("**")
            p.paragraph_format.tab_stops.add_tab_stop(Cm(indent + 0.6))
            for i, t in enumerate(parts):
                if t:
                    r = p.add_run(t); r.bold = (i % 2 == 1)
                    r.font.name = "Times New Roman"
        if doc.paragraphs:
            doc.paragraphs[-1].paragraph_format.space_after = Pt(8)

    def set_cell_border(cell, sz=4):
        tcPr = cell._tc.get_or_add_tcPr()
        b = OxmlElement("w:tcBorders")
        for e in ("top", "left", "bottom", "right"):
            x = OxmlElement("w:" + e); x.set(qn("w:val"), "single"); x.set(qn("w:sz"), str(sz)); x.set(qn("w:color"), "000000")
            b.append(x)
        tcPr.append(b)

    def TABLE(header, rows, widths, size=10.5):
        t = doc.add_table(rows=1, cols=len(header))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        for i, h in enumerate(header):
            c = t.rows[0].cells[i]; c.width = Cm(widths[i]); c.text = ""
            r = c.paragraphs[0].add_run(h); r.bold = True; r.font.size = Pt(size)
            r.font.name = "Times New Roman"
            c.paragraphs[0].paragraph_format.space_after = Pt(2); c.paragraphs[0].paragraph_format.line_spacing = 1.1
            set_cell_border(c)
        for row in rows:
            cells = t.add_row().cells
            for i, v in enumerate(row):
                cells[i].width = Cm(widths[i]); cells[i].text = ""
                par = cells[i].paragraphs[0]
                par.paragraph_format.space_after = Pt(2); par.paragraph_format.line_spacing = 1.1
                r = par.add_run(v); r.font.size = Pt(size)
                r.font.name = "Times New Roman"
                set_cell_border(cells[i])
        trPr = t.rows[0]._tr.get_or_add_trPr(); th = OxmlElement("w:tblHeader"); th.set(qn("w:val"), "true"); trPr.append(th)
        for row in t.rows:
            trPr = row._tr.get_or_add_trPr(); cs = OxmlElement("w:cantSplit"); trPr.append(cs)
        sp = doc.add_paragraph(); sp.paragraph_format.space_after = Pt(4)
        return t

    def CODE(lines, size=9.5):
        t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
        c = t.rows[0].cells[0]; c.width = Cm(15.5); set_cell_border(c)
        c.text = ""
        for i, ln in enumerate(lines):
            par = c.paragraphs[0] if i == 0 else c.add_paragraph()
            par.paragraph_format.space_after = Pt(0); par.paragraph_format.line_spacing = 1.0
            par.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = par.add_run(ln if ln else " "); r.font.name = "Courier New"; r.font.size = Pt(size)
            r._element.rPr.rFonts.set(qn("w:eastAsia"), "Courier New")
        sp = doc.add_paragraph(); sp.paragraph_format.space_after = Pt(4)

    fig_n = [0]
    def FIG(files, caption, width=14.5):
        if isinstance(files, str): files = [files]
        fig_n[0] += 1
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.keep_with_next = True; p.paragraph_format.space_after = Pt(3); p.paragraph_format.line_spacing = 1.0
        p.paragraph_format.space_before = Pt(6)
        for i, f in enumerate(files):
            r = p.add_run()
            pic = r.add_picture(FIG_DIR + f + ".png", width=Cm(width if len(files) == 1 else width / len(files) - 0.3))
            sp = pic._inline.graphic.graphicData.pic.spPr
            ln = OxmlElement("a:ln"); ln.set("w", "6350")
            sf = OxmlElement("a:solidFill"); clr = OxmlElement("a:srgbClr"); clr.set("val", "000000"); sf.append(clr); ln.append(sf); sp.append(ln)
            if i < len(files) - 1: p.add_run("   ")
        c = P("Figure %d : %s" % (fig_n[0], caption), italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, size=11, after=10)
        c.paragraph_format.line_spacing = 1.0

    def field(run, instr):
        for t, txt in (("begin", None), (None, instr), ("end", None)):
            if t:
                e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), t); run._r.append(e)
            else:
                e = OxmlElement("w:instrText"); e.set(qn("xml:space"), "preserve"); e.text = txt; run._r.append(e)

    # ---------- footer ----------
    fp = sec.footer.paragraphs[0]
    fp.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT)
    r = fp.add_run("RÉALISÉ PAR : KOUAME ACHLEY\t"); r.font.size = Pt(10)
    r.font.name = "Times New Roman"
    r2 = fp.add_run(); r2.font.size = Pt(10); field(r2, "PAGE")
    r2.font.name = "Times New Roman"

    def page_border(section):
        sp = section._sectPr
        pb = OxmlElement("w:pgBorders"); pb.set(qn("w:offsetFrom"), "page")
        pb.set(qn("w:display"), "firstPage")
        for e in ("top", "left", "bottom", "right"):
            x = OxmlElement("w:" + e); x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "12"); x.set(qn("w:space"), "24"); x.set(qn("w:color"), "000000")
            pb.append(x)
        sp.append(pb)

    # ================= COUVERTURE =================
    def C(text, size=12, bold=False, after=6, italic=False):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(after); p.paragraph_format.line_spacing = 1.15
        r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size)
        r.font.name = "Times New Roman"
        return p

    t = doc.add_table(rows=1, cols=3); t.autofit = False
    heads = ["MINISTÈRE DE L’ENSEIGNEMENT SUPÉRIEUR\nET DE LA RECHERCHE SCIENTIFIQUE", None, "RÉPUBLIQUE DE CÔTE D’IVOIRE\nUnion - Discipline - Travail"]
    w = [5.6, 4.8, 5.6]
    for i in range(3):
        c = t.rows[0].cells[i]; c.width = Cm(w[i]); c.text = ""
        par = c.paragraphs[0]; par.alignment = WD_ALIGN_PARAGRAPH.CENTER; par.paragraph_format.line_spacing = 1.1
        if heads[i]:
            rr = par.add_run(heads[i]); rr.font.size = Pt(10); rr.font.name = "Times New Roman"
        else:
            rr = par.add_run(); rr.add_picture(LOGO_DIR + "l-002.png", height=Cm(2.6))
    t2 = doc.add_table(rows=1, cols=2); t2.autofit = False
    for i, (f, h) in enumerate((("l-137.png", 2.6), ("l-000.png", 2.2))):
        c = t2.rows[0].cells[i]; c.width = Cm(8); c.text = ""
        par = c.paragraphs[0]; par.alignment = WD_ALIGN_PARAGRAPH.CENTER
        par.add_run().add_picture(LOGO_DIR + f, height=Cm(h))
    C("", after=4)
    C("", after=0).add_run().add_picture(LOGO_DIR + "l-001.png", height=Cm(2.6))
    C("", after=10)
    C("RAPPORT DE STAGE", 18, True, 4)
    C("BREVET DE TECHNICIEN SUPÉRIEUR", 15, True, 4)
    C("Option : Informatique Développeur d’Application", 13, False, 18)
    C("THÈME :", 14, True, 8)
    bt = doc.add_table(rows=1, cols=1); bt.alignment = WD_TABLE_ALIGNMENT.CENTER
    bc = bt.rows[0].cells[0]; bc.width = Cm(14); set_cell_border(bc, 12); bc.text = ""
    bp = bc.paragraphs[0]; bp.alignment = WD_ALIGN_PARAGRAPH.CENTER; bp.paragraph_format.space_before = Pt(8); bp.paragraph_format.space_after = Pt(8)
    rr = bp.add_run("CONCEPTION ET RÉALISATION DU SITE WEB D’UNE ENTREPRISE : CAS DE WIKY HOLDING"); rr.bold = True; rr.font.size = Pt(15); rr.font.name = "Times New Roman"
    C("", after=14)
    C("PRÉSENTÉ PAR :", 12, False, 4)
    C("KOUAME AFFOUE CYNTICHE ACHLEY DELMAS", 13, True, 30)
    t3 = doc.add_table(rows=2, cols=2); t3.autofit = False
    vals = [("MAÎTRE DE STAGE", "ENCADRANT"), ("M. AKE WILLY DONALD", "M. AKE WILLY")]
    for ri in range(2):
        for ci in range(2):
            c = t3.rows[ri].cells[ci]; c.width = Cm(8); c.text = ""
            par = c.paragraphs[0]; par.alignment = WD_ALIGN_PARAGRAPH.CENTER
            rr = par.add_run(vals[ri][ci]); rr.bold = (ri == 0); rr.font.size = Pt(12); rr.font.name = "Times New Roman"
    C("", after=24)
    C("Année académique : 2025 - 2026", 12, False, 0)
    page_border(sec)

    # ================= SOMMAIRE (rempli à la fin) =================
    sommaire_h = doc.add_heading("SOMMAIRE", level=1); sommaire_h.paragraph_format.page_break_before = True
    sommaire_anchor = doc.add_paragraph()

    # ================= PAGES LIMINAIRES =================
    H(1, "DÉDICACE", toc=True, page_break=True)
    P("Je dédie ce travail à ma famille pour son soutien constant, ses encouragements et ses conseils qui m’ont permis de mener à bien mes études.")

    H(1, "REMERCIEMENTS", page_break=True)
    P("Je tiens à exprimer ma profonde gratitude à toutes les personnes qui ont contribué à la réalisation de ce rapport de stage.")
    P("Mes remerciements s’adressent en premier lieu à la direction de **Digital Agency Wiky** pour m’avoir offert l’opportunité d’effectuer mon stage au sein de leur structure.")
    P("Je remercie particulièrement mon maître de stage, Monsieur **AKE WILLY**, pour son encadrement, sa disponibilité et ses précieux conseils tout au long de cette expérience professionnelle.")
    P("Mes remerciements vont également à l’ensemble du personnel de l’entreprise pour leur accueil chaleureux et leur esprit de collaboration.")
    P("Enfin, j’exprime ma profonde gratitude à l’**ES2I Plateau** ainsi qu’à l’ensemble de mes enseignants pour la qualité de la formation que j’y ai reçue. Leur engagement, leur rigueur et leur disponibilité ont largement contribué à mon évolution académique et personnelle, et resteront pour moi une référence précieuse dans mon parcours.")

    H(1, "AVANT-PROPOS", page_break=True)
    P("Ce stage professionnel s’inscrit dans le cadre de la préparation du Brevet de Technicien Supérieur (BTS), une formation en deux années qui associe enseignements théoriques et expériences pratiques.")
    P("Ce rapport est le résultat de la période d’immersion professionnelle effectuée au sein de l’entreprise **Digital Agency Wiky**. Il constitue une étape importante pour relier ce que j’ai appris à l’ES2I Plateau aux réalités du terrain.")
    P("Le thème de ce rapport est : **Conception et réalisation du site web d’une entreprise : cas de Wiky Holding**.")
    P("Ce thème a été choisi parce que toute entreprise d’aujourd’hui a besoin d’une présence efficace sur Internet. Réaliser le site de Wiky Holding était pour moi l’occasion d’appliquer mes connaissances en développement d’applications sur un projet réel, utile à la structure qui m’a accueillie.")
    P("Ce rapport présente aussi un changement important dans mon travail : le premier site avait été réalisé avec WordPress, mais il n’est plus disponible. J’ai donc refait le site entièrement, en programmant moi-même, avec le langage PHP. C’est ce nouveau site qui est décrit dans les pages qui suivent.")

    H(1, "INTRODUCTION", page_break=True)
    P("Le monde professionnel demande aujourd’hui de savoir appliquer concrètement les connaissances reçues en cours. Ce stage, réalisé dans le cadre de ma formation à l’ES2I Plateau en vue du Brevet de Technicien Supérieur (BTS), a été pour moi l’occasion de le faire.")
    P("J’ai effectué mon stage au sein de l’entreprise **Digital Agency Wiky**, située à Cocody Riviera Faya, à Abidjan. Ma mission était de réaliser le site web de Wiky Holding.")
    P("Au départ, j’avais réalisé ce site avec le système de gestion de contenu WordPress. Ce site n’est malheureusement plus en ligne. De plus, ma filière est celle des développeurs d’applications : il était plus logique de montrer ce que je sais programmer plutôt que d’utiliser un outil déjà tout fait. J’ai donc décidé de recommencer le site depuis zéro, avec du code écrit par moi, en PHP, avec une base de données et une organisation claire des fichiers.")
    P("Ce rapport explique comment le site a été pensé et construit. Il est divisé en deux grandes parties :")
    BL(["la première partie présente l’entreprise d’accueil et le projet (contexte, objectifs, besoins) ;",
        "la deuxième partie décrit la réalisation du site : son organisation, ses dossiers, sa base de données, ses pages, ses fonctionnalités, sa sécurité, les tests et la mise en ligne."])
    P("Le rapport se termine par une conclusion, qui résume ce que ce projet m’a apporté, et par quelques annexes.")

    # ================= PREMIERE PARTIE =================
    H(1, "PREMIÈRE PARTIE : GÉNÉRALITÉS", page_break=True)
    H(2, "CHAPITRE I : PRÉSENTATION DE DIGITAL AGENCY WIKY")
    H(3, "I. Présentation de Digital Agency Wiky")
    H(4, "1. Historique")
    P("Digital Agency Wiky, aussi appelée Wiky Holding, est une agence de communication 360°. Elle accompagne les entreprises, les marques et les entrepreneurs dans leur communication, surtout sur Internet : réseaux sociaux, identité visuelle, vidéo et podcast.")
    P("L’agence aide les marques à se faire connaître et à se faire remarquer dans le monde numérique, en proposant des stratégies adaptées aux besoins de chaque client.")
    H(4, "2. Situation géographique")
    P("L’agence est située à Abidjan, dans la commune de Cocody, au quartier Riviera Faya (Côte d’Ivoire). Ses coordonnées sont les suivantes :")
    TABLE(["Rubrique", "Information"],
          [["Adresse", "Abidjan, Cocody Riviera Faya, Côte d’Ivoire"],
           ["Téléphones", "+225 07 88 83 70 24 / +225 27 24 42 42 00"],
           ["Email", "Wikytechnologieci@gmail.com"],
           ["Horaires", "Lundi au vendredi : 08h30 - 18h30 ; samedi : 09h00 - 14h00"]],
          [4, 11.5])
    H(4, "3. Domaine d’activité")
    P("Digital Agency Wiky travaille dans le domaine de la communication. Elle propose des services sur mesure, entre autres :")
    BL(["la communication digitale et la couverture médiatique ;",
        "la confection d’affiches ;",
        "le branding de produit et la création de sites web ;",
        "le branding d’entreprise et le personal branding ;",
        "la production de podcasts et de vidéos dans son studio."])

    H(3, "II. Organigramme du groupe Wiky")
    P("À la tête de l’agence se trouve le Directeur Général. Autour de lui, le travail est réparti en plusieurs pôles qui collaborent entre eux.")
    H(4, "1. Direction")
    P("Le Directeur Général supervise l’ensemble des pôles et la stratégie de développement. Il valide les projets, fixe les grandes orientations créatives et commerciales et veille à la bonne entente des équipes. Il est aidé par une assistante, qui gère l’agenda, les documents administratifs et les échanges internes, et qui réalise aussi les voix off des vidéos et des podcasts.")
    H(4, "2. Gestion des projets et relations clients")
    P("Le chargé de projets (ou responsable relation client) est le premier contact des clients. Il reçoit les commandes, prend les rendez-vous, transmet les demandes aux équipes (community managers, graphistes, vidéastes) et suit l’avancement des projets jusqu’à la livraison. On peut le comparer à un chef d’orchestre entre les clients et l’équipe de production.")
    H(4, "3. Pôle communication digitale")
    P("Ce pôle est composé de deux community managers. Ils rédigent les textes des visuels, des publications et des campagnes, écrivent les scripts des vidéos et gèrent les pages des clients ainsi que celles du groupe Wiky (animation, planification, publicité). Ils travaillent en lien étroit avec les pôles graphisme et audiovisuel.")
    H(4, "4. Pôle graphique et création visuelle")
    P("Un infographe titulaire et un infographe assistant créent les affiches, les identités visuelles et les visuels pour les réseaux sociaux. Ils transforment les textes des community managers en images attrayantes. Le titulaire valide le travail de l’assistant avant toute diffusion.")
    H(4, "5. Pôle audiovisuel et shooting photo")
    P("Un vidéaste-photographe titulaire et un assistant réalisent et montent les vidéos, les séances photo, les capsules et les interviews. Ils mettent en images les scripts écrits par les community managers et assurent la direction artistique des tournages.")
    H(4, "6. Pôle studio podcast")
    P("Le studio podcast est supervisé par le Directeur Général, qui vérifie la qualité du travail à chaque étape. Les vidéastes préparent le décor avant chaque enregistrement, assurent le tournage, la prise de son et le montage. Le chargé de projets reçoit les commandes et planifie les séances, et l’assistante du directeur intervient pour les voix off.")

    H(3, "III. Services de l’entreprise")
    P("Comme la plupart des entreprises de communication, l’agence offre plusieurs services pour accompagner ses clients, qu’ils soient grands ou petits.")
    H(4, "1. Community management")
    P("Le community manager s’occupe de toute la communication digitale des clients de Wiky Holding. Il définit les objectifs (faire connaître la marque, créer de l’échange, obtenir des ventes), choisit les réseaux adaptés (Facebook, Instagram, TikTok, LinkedIn), publie les contenus, répond aux commentaires et aux messages, rédige les textes publicitaires, gère les campagnes sponsorisées et prépare des rapports de résultats pour les clients.")
    H(4, "2. Graphisme et identité visuelle")
    P("Le pôle graphisme crée tous les visuels dont les clients ont besoin : logos, chartes graphiques, affiches, publications pour les réseaux sociaux, bannières web et éléments pour les vidéos. Il respecte toujours la charte du client (couleurs, polices, logo) et prépare les fichiers dans les formats adaptés à chaque support.")
    H(4, "3. Audiovisuel et studio podcast")
    P("Ce pôle produit les contenus vidéo et audio. Le studio est insonorisé et équipé de micros de type broadcast, de caméras Sony 4K et d’un éclairage professionnel. Après l’enregistrement, l’équipe réalise le montage et peut découper l’émission en courtes vidéos pour TikTok, Reels et Shorts.")
    H(4, "4. Chargé de projets")
    P("Il reçoit les demandes des clients, analyse leurs besoins, crée la fiche du projet, répartit les tâches entre les pôles, suit les délais, vérifie les livrables avant la validation finale du Directeur Général et s’assure que le client est satisfait.")

    H(2, "CHAPITRE II : PRÉSENTATION DU PROJET")
    H(3, "2.1 Contexte du projet")
    P("De nos jours, la présence d’une entreprise sur Internet est devenue essentielle. Un site web est une vitrine ouverte à tout moment : il présente les activités, les services et les valeurs de l’entreprise, et il rassure les clients et les partenaires.")
    P("Wiky Holding avait besoin d’un site moderne pour présenter son agence. Mon stage au sein de Digital Agency Wiky avait pour but de concevoir et réaliser ce site.")
    P("Une première version avait été faite avec WordPress et l’extension Elementor. Cette version n’est plus disponible en ligne. Par ailleurs, WordPress permet de créer un site sans vraiment programmer, alors que ma formation (BTS Informatique Développeur d’Application) est une formation de développeur. J’ai donc choisi de refaire le site entièrement, avec du code écrit à la main, pour montrer concrètement mes compétences en programmation, en organisation d’un projet logiciel et en sécurité des données.")
    H(3, "2.2 Problématique")
    P("La question qui a guidé tout mon travail est la suivante :")
    P("**Comment concevoir un site web professionnel, rapide et sécurisé pour Wiky Holding, en le programmant soi-même, de façon à ce qu’il puisse fonctionner même sur un hébergement gratuit ?**", align=WD_ALIGN_PARAGRAPH.CENTER)
    H(3, "2.3 Objectifs du projet")
    H(4, "Objectif général")
    P("Réaliser et mettre en ligne un site web de présentation pour Wiky Holding, afin d’améliorer sa visibilité et de faciliter le contact avec ses clients.")
    H(4, "Objectifs spécifiques")
    BL(["analyser les besoins de l’entreprise ;",
        "organiser le site en pages claires (accueil, à propos, services, réalisations, studio podcast, contact, devis) ;",
        "programmer le site en PHP avec une organisation en modèles, vues et contrôleurs (MVC) ;",
        "enregistrer les messages et les demandes de devis dans une base de données ;",
        "proposer un simulateur de devis qui donne un prix estimé tout de suite ;",
        "rendre le site agréable sur ordinateur, tablette et téléphone ;",
        "protéger les formulaires contre les attaques courantes ;",
        "préparer le site pour qu’il soit installé facilement sur un hébergement gratuit."])
    H(3, "2.4 Cahier des charges")
    H(4, "Besoins fonctionnels")
    BL(["présenter l’entreprise, ses quatre pôles et ses valeurs ;",
        "afficher les services, les tarifs indicatifs et les packs ;",
        "montrer les réalisations avec un filtre par catégorie ;",
        "présenter le studio podcast et son matériel ;",
        "donner les coordonnées de l’agence et permettre d’envoyer un message ;",
        "permettre de demander un devis et d’en voir une estimation en direct ;",
        "permettre de rechercher rapidement une page ou un service."])
    H(4, "Besoins non fonctionnels")
    BL(["un site rapide à charger ;",
        "un site sécurisé (formulaires protégés, fichiers sensibles cachés) ;",
        "un affichage adapté à tous les écrans (responsive) ;",
        "un design moderne et lisible ;",
        "un code organisé, facile à comprendre et à modifier ;",
        "un fonctionnement possible sur un hébergement mutualisé gratuit (InfinityFree) et en local (WAMP, XAMPP)."])
    H(3, "2.5 Méthodologie de travail")
    P("J’ai travaillé par étapes, dans un ordre logique :")
    BL(["**Recueil des besoins** : discussion avec mon maître de stage pour savoir ce que le site devait contenir ;",
        "**Analyse** : liste des pages et des fonctionnalités, choix des technologies ;",
        "**Conception** : choix de l’organisation des dossiers, de la base de données et de la charte graphique ;",
        "**Développement** : programmation du site page par page, puis des fonctionnalités (formulaires, simulateur, recherche) ;",
        "**Tests** : vérification de chaque page et de chaque formulaire, sur ordinateur et sur mobile ;",
        "**Mise en ligne** : préparation du site pour l’hébergement InfinityFree."])
    H(3, "2.6 Pourquoi ne pas utiliser un framework")
    P("Il existe des frameworks PHP très connus comme Laravel ou Symfony. Je n’en ai pas utilisé, pour deux raisons. D’abord, un hébergement gratuit comme InfinityFree n’offre ni accès en ligne de commande, ni Composer, et limite beaucoup la mémoire : un framework lourd y poserait des problèmes. Ensuite, programmer sans framework m’a obligé à écrire moi-même les éléments importants (routage, chargement des classes, protection des formulaires), ce qui m’a permis de bien comprendre comment ils fonctionnent.")

    # ================= DEUXIEME PARTIE =================
    H(1, "DEUXIÈME PARTIE : RÉALISATION DU SITE WEB", page_break=True)
    H(2, "CHAPITRE I : ANALYSE ET CONCEPTION")
    H(3, "3.1 Analyse des besoins")
    P("Les échanges avec mon maître de stage ont montré que le site devait d’abord servir de vitrine : présenter l’agence, ses services et ses réalisations. Il devait aussi inciter les visiteurs à contacter l’agence, par un formulaire de contact ou par une demande de devis.")
    P("J’ai aussi tenu compte de contraintes techniques : le site devait être léger, fonctionner sur un hébergement gratuit et pouvoir être testé facilement sur n’importe quel ordinateur. C’est pour cela que le site peut utiliser une base MySQL en ligne, mais aussi une petite base SQLite qui ne demande aucune installation (voir chapitre IV).")
    H(3, "3.2 Arborescence du site")
    P("Le site comporte sept pages principales, plus une page d’erreur 404 :")
    TABLE(["Page", "Contenu"],
          [["Accueil", "Présentation générale, chiffres clés, services principaux, réalisations, méthode de travail, avis de clients"],
           ["À propos", "Histoire de l’agence, vision, quatre pôles, valeurs"],
           ["Services", "Quatre services détaillés et trois packs tarifaires"],
           ["Réalisations", "Projets classés par catégorie, avec filtre"],
           ["Studio podcast", "Matériel du studio, idées d’émissions pour les entreprises"],
           ["Contact", "Coordonnées, questions fréquentes, formulaire de contact"],
           ["Devis", "Simulateur de prix et formulaire de demande de devis"],
           ["Erreur 404", "Page affichée quand l’adresse demandée n’existe pas"]],
          [3.5, 12])
    H(3, "3.3 Charte graphique")
    H(4, "Les couleurs")
    P("Le site utilise surtout des bleus (bleu marine et bleu royal) et des fonds clairs légèrement bleutés. Une couleur vive, le orange corail, est réservée aux boutons importants (demander un devis, envoyer un message) pour que le visiteur les repère tout de suite. J’ai évité le gris pur, qui donne un aspect triste, en choisissant des gris légèrement bleutés.")
    H(4, "Les polices")
    P("Deux polices Google Fonts sont utilisées : Plus Jakarta Sans pour les titres et Inter pour les textes. La taille du texte s’adapte à la largeur de l’écran grâce à la fonction CSS clamp(), et les lignes de texte sont limitées à environ 65 caractères pour que la lecture reste confortable.")
    H(4, "Les thèmes")
    P("Le visiteur peut choisir entre trois thèmes (clair, sombre et bleu marine) et changer la couleur d’accentuation (orange, bleu cyan, émeraude, violet, or, ou une couleur de son choix). Son choix est gardé dans le navigateur pour sa prochaine visite.")

    H(2, "CHAPITRE II : ENVIRONNEMENT TECHNIQUE")
    H(3, "4.1 Langages utilisés")
    TABLE(["Langage", "Utilisation dans le projet"],
          [["PHP (orienté objet)", "Partie serveur : routage, contrôleurs, modèles, traitement des formulaires"],
           ["HTML5", "Structure des pages"],
           ["CSS3", "Mise en forme, couleurs, thèmes, affichage adaptatif"],
           ["JavaScript (sans bibliothèque)", "Interactions : recherche, simulateur de devis, filtre, menu mobile, thèmes"],
           ["SQL", "Création des tables et requêtes vers la base de données"]],
          [5, 10.5])
    H(3, "4.2 Base de données")
    P("Le site utilise **PDO** (PHP Data Objects) pour communiquer avec la base de données. PDO permet d’écrire des requêtes préparées, qui protègent contre les injections SQL. Deux systèmes de base de données sont possibles : **MySQL** pour la mise en ligne, et **SQLite** comme solution de secours en local.")
    H(3, "4.3 Outils de développement")
    BL(["**WAMP** : serveur local (Apache, PHP, MySQL) installé sur mon ordinateur ;",
        "**phpMyAdmin** : gestion de la base MySQL et import du fichier database.sql ;",
        "**serveur interne de PHP** : lancé avec la commande php -S localhost:8000 pour tester rapidement ;",
        "**un éditeur de code** pour écrire les fichiers ;",
        "**un navigateur web** pour tester l’affichage et les fonctionnalités ;",
        "**FileZilla** : transfert des fichiers vers l’hébergeur."])
    H(3, "4.4 Hébergement")
    P("Le site est prévu pour l’hébergement gratuit **InfinityFree**, qui fournit un serveur Apache, PHP et MySQL, un panneau de contrôle, phpMyAdmin et un certificat SSL gratuit pour avoir une adresse en HTTPS. Comme cet hébergement est limité (pas de terminal SSH, pas de Composer, mémoire réduite), le site a été écrit pour rester léger et simple.")

    H(2, "CHAPITRE III : ARCHITECTURE DU SITE")
    H(3, "5.1 Le modèle MVC")
    P("Le site est organisé selon le modèle **MVC** (Modèle - Vue - Contrôleur), qui sépare le code en trois rôles :")
    BL(["le **modèle** s’occupe des données (base de données, listes de services, de projets) ;",
        "la **vue** s’occupe de l’affichage (le code HTML des pages) ;",
        "le **contrôleur** fait le lien : il reçoit la demande du visiteur, demande les données au modèle, puis envoie le résultat à la vue."])
    P("Cette séparation évite de mélanger le HTML, les requêtes SQL et la logique du site dans un même fichier. Le code est ainsi plus facile à lire, à corriger et à faire évoluer. Un fichier unique, index.php, reçoit toutes les demandes et les dirige vers le bon contrôleur.")
    P("Le schéma suivant résume le trajet d’une demande :")
    CODE(["Navigateur",
          "    |   demande (ex. index.php?page=contact)",
          "    v",
          "index.php  (routeur)",
          "    |   choisit le contrôleur",
          "    v",
          "Controller  ----->  Model  ----->  PDO  ----->  MySQL ou SQLite",
          "    |",
          "    v",
          "View  (page HTML envoyée au visiteur)"])
    H(3, "5.2 Les dossiers du projet")
    P("Voici l’organisation des fichiers du site :")
    CODE(["achelyrapport/",
          "|-- index.php",
          "|-- .htaccess",
          "|-- database.sql",
          "|-- database.sqlite",
          "|-- README.md",
          "|-- logo.jpg",
          "|-- app/",
          "|   |-- Config/",
          "|   |   |-- App.php",
          "|   |   `-- Database.php",
          "|   |-- Controllers/",
          "|   |   |-- HomeController.php",
          "|   |   |-- AboutController.php",
          "|   |   |-- ServiceController.php",
          "|   |   |-- PortfolioController.php",
          "|   |   |-- PodcastController.php",
          "|   |   |-- ContactController.php",
          "|   |   `-- DevisController.php",
          "|   |-- Models/",
          "|   |   |-- ContactModel.php",
          "|   |   |-- DevisModel.php",
          "|   |   |-- PortfolioModel.php",
          "|   |   `-- ServiceModel.php",
          "|   `-- Views/",
          "|       |-- layout/",
          "|       |   |-- header.php",
          "|       |   |-- navbar.php",
          "|       |   `-- footer.php",
          "|       `-- pages/",
          "|           |-- home.php, about.php, services.php",
          "|           |-- portfolio.php, podcast.php",
          "|           `-- contact.php, devis.php",
          "`-- assets/",
          "    |-- css/style.css",
          "    |-- js/main.js",
          "    `-- images/"], size=9)
    P("Les paragraphes suivants expliquent le rôle de chaque élément.")
    H(3, "5.3 Le fichier index.php")
    P("C’est le point d’entrée unique du site : toutes les demandes passent par lui. Il fait les opérations suivantes :")
    BL(["démarrer la session PHP, qui sert à garder certaines informations (jeton de sécurité, messages) ;",
        "charger la configuration (App.php) et la connexion à la base de données (Database.php) ;",
        "charger automatiquement les classes grâce à un chargeur écrit en PHP, sans bibliothèque externe, pour les fichiers du namespace App ;",
        "lire la page demandée, soit avec le paramètre ?page=..., soit avec l’adresse réécrite par Apache ;",
        "appeler le bon contrôleur grâce à une structure switch ;",
        "afficher une page 404 si la page n’existe pas."])
    H(3, "5.4 Le dossier app/Config")
    BL(["**App.php** : contient les informations générales de l’agence (nom, adresse, téléphone), les fonctions utiles comme url() pour fabriquer les liens, et e() qui sécurise l’affichage des textes ;",
        "**Database.php** : gère la connexion à la base de données (voir chapitre IV)."])
    H(3, "5.5 Le dossier app/Controllers")
    P("Chaque page a son contrôleur :")
    TABLE(["Contrôleur", "Rôle"],
          [["HomeController", "Prépare les données de l’accueil : chiffres clés, services, réalisations, avis"],
           ["AboutController", "Présente l’histoire, la vision, les quatre pôles et les valeurs"],
           ["ServiceController", "Envoie la liste des services et des trois packs"],
           ["PortfolioController", "Envoie les réalisations, filtrables par catégorie"],
           ["PodcastController", "Présente le studio, le matériel et des idées d’émissions"],
           ["ContactController", "Affiche le formulaire, crée le jeton de sécurité, traite l’envoi du message"],
           ["DevisController", "Affiche le simulateur et traite l’envoi de la demande de devis"]],
          [4.5, 11])
    H(3, "5.6 Le dossier app/Models")
    TABLE(["Modèle", "Rôle"],
          [["ContactModel", "Enregistre les messages dans la table messages ; contient aussi getLatest() pour lire les derniers messages"],
           ["DevisModel", "Enregistre les demandes dans la table devis_requests ; contient estimatePrice() qui calcule une estimation de prix"],
           ["ServiceModel", "Fournit la liste des services, leurs contenus et leurs tarifs indicatifs"],
           ["PortfolioModel", "Fournit les projets avec leurs résultats et le filtre par catégorie"]],
          [4, 11.5])
    H(3, "5.7 Le dossier app/Views")
    P("Les vues contiennent le code HTML. Elles sont divisées en deux sous-dossiers.")
    P("Le dossier **layout** contient les parties communes à toutes les pages :", after=3)
    BL(["header.php : balises d’en-tête, référencement (SEO), partage sur les réseaux, polices, fichiers CSS ;",
        "navbar.php : barre de navigation, logo, recherche, choix du thème et menu mobile ;",
        "footer.php : pied de page, coordonnées, fenêtre de recherche et panneau de personnalisation des couleurs."])
    P("Le dossier **pages** contient le contenu propre à chaque page : home.php, about.php, services.php, portfolio.php, podcast.php, contact.php et devis.php. Grâce à ce découpage, le menu et le pied de page sont écrits une seule fois pour tout le site.")
    H(3, "5.8 Le dossier assets")
    BL(["**css/style.css** : la feuille de style du site (couleurs, tailles, thèmes, affichage mobile) ;",
        "**js/main.js** : le JavaScript du site (changement de thème, recherche, simulateur de devis, filtre, menu mobile) ;",
        "**images/** : les images utilisées sur les pages."])
    H(3, "5.9 Les fichiers à la racine")
    BL(["**.htaccess** : règles Apache pour la sécurité et la réécriture des adresses ;",
        "**database.sql** : script qui crée les deux tables dans MySQL ;",
        "**database.sqlite** : base SQLite créée automatiquement quand MySQL n’est pas disponible ;",
        "**README.md** : explications pour installer et lancer le site ;",
        "**logo.jpg** : le logo de l’agence."])
    H(3, "5.10 Les routes du site")
    TABLE(["Adresse", "Méthode", "Contrôleur", "Rôle"],
          [["index.php (ou page=home)", "GET", "HomeController", "Accueil"],
           ["?page=about", "GET", "AboutController", "À propos"],
           ["?page=services", "GET", "ServiceController", "Services et packs"],
           ["?page=portfolio", "GET", "PortfolioController", "Réalisations"],
           ["?page=podcast", "GET", "PodcastController", "Studio podcast"],
           ["?page=contact", "GET", "ContactController", "Formulaire de contact"],
           ["?page=contact-submit", "POST", "ContactController", "Enregistre le message"],
           ["?page=devis", "GET", "DevisController", "Simulateur et formulaire"],
           ["?page=devis-submit", "POST", "DevisController", "Enregistre la demande"],
           ["Autre adresse", "-", "index.php", "Page 404"]],
          [4.6, 1.9, 4.3, 4.7], size=10)
    H(3, "5.11 Exemple : l’envoi d’un message de contact")
    P("Pour mieux comprendre le fonctionnement, voici ce qui se passe quand un visiteur envoie un message :")
    BL(["le visiteur ouvre la page contact ; le contrôleur crée un jeton de sécurité et affiche le formulaire ;",
        "il remplit le formulaire et clique sur envoyer ; la demande arrive sur ?page=contact-submit ;",
        "index.php appelle la méthode submit() de ContactController ;",
        "le contrôleur vérifie le jeton de sécurité, puis contrôle les champs (champs obligatoires, format de l’email, longueur) ;",
        "si tout est correct, ContactModel enregistre le message dans la table messages avec une requête préparée ;",
        "le visiteur est redirigé vers la page contact avec un message de confirmation (message « flash »). En cas d’erreur, un message d’erreur s’affiche à la place."])

    # ================= CHAPITRE IV : BASE DE DONNÉES =================
    H(2, "CHAPITRE IV : BASE DE DONNÉES")
    H(3, "6.1 La classe Database")
    P("La classe Database (dans app/Config) gère la connexion avec la base de données. Elle fonctionne en « singleton » : la connexion est créée une seule fois puis réutilisée partout dans le site, ce qui évite d’ouvrir plusieurs connexions inutiles.")
    P("Elle peut utiliser deux types de base de données :")
    BL(["**MySQL** : utilisée si les informations de connexion (hôte, utilisateur) ont été renseignées. La connexion se fait en utf8mb4, et PDO est réglé pour signaler les erreurs par des exceptions ;",
        "**SQLite** : si les identifiants par défaut sont détectés ou si la connexion MySQL échoue, le site bascule automatiquement sur un fichier local database.sqlite. Les tables y sont créées automatiquement."])
    P("Grâce à cela, le site fonctionne tout de suite, même si MySQL n’est pas lancé. C’est très pratique pour une démonstration ou pour tester le site sur un autre ordinateur.")
    H(3, "6.2 Les tables")
    H(4, "Table messages (formulaire de contact)")
    TABLE(["Colonne", "Type", "Description"],
          [["id", "INT, clé primaire, auto-incrémenté", "Identifiant du message"],
           ["name", "VARCHAR(120)", "Nom complet de la personne"],
           ["email", "VARCHAR(150)", "Adresse email"],
           ["phone", "VARCHAR(50)", "Téléphone (facultatif)"],
           ["service", "VARCHAR(100)", "Service concerné"],
           ["subject", "VARCHAR(200)", "Objet du message"],
           ["message", "TEXT", "Contenu du message"],
           ["created_at", "DATETIME", "Date et heure de réception"]],
          [3, 5.5, 7])
    H(4, "Table devis_requests (demandes de devis)")
    TABLE(["Colonne", "Type", "Description"],
          [["id", "INT, clé primaire, auto-incrémenté", "Identifiant de la demande"],
           ["company_name", "VARCHAR(150)", "Nom de l’entreprise ou de la marque"],
           ["contact_name", "VARCHAR(120)", "Nom du responsable"],
           ["email", "VARCHAR(150)", "Adresse email professionnelle"],
           ["phone", "VARCHAR(50)", "Téléphone ou WhatsApp"],
           ["service_type", "VARCHAR(100)", "Prestation souhaitée"],
           ["budget_range", "VARCHAR(50)", "Tranche de budget estimée"],
           ["urgency", "VARCHAR(50)", "Délai de réalisation souhaité"],
           ["project_details", "TEXT", "Description du projet"],
           ["created_at", "DATETIME", "Date et heure de la demande"]],
          [3.6, 5.2, 6.7])
    P("Les deux tables sont indépendantes : il n’y a pas de lien entre elles, car chacune enregistre un type d’information différent.")

    # ================= CHAPITRE V : PRÉSENTATION DES PAGES DU SITE =================
    H(2, "CHAPITRE V : PRÉSENTATION DES PAGES DU SITE")
    P("Ce chapitre présente les pages du site avec des captures d’écran réalisées sur le site en fonctionnement. Les captures montrent seulement les parties importantes de chaque page.")
    H(3, "7.1 La page d’accueil")
    P("C’est la première page que le visiteur voit. En haut, on trouve la barre de navigation puis un grand titre qui présente l’agence, avec deux boutons : « Estimer mon projet » et « Explorer nos services ».")
    FIG("home_hero", "Page d’accueil : en-tête et titre principal")
    P("Sous le titre, la page affiche des chiffres clés puis un résumé des quatre services principaux (community management, identité visuelle, studio podcast et branding d’entreprise), chacun avec un prix de départ.")
    FIG("home_services", "Page d’accueil : présentation des services")
    P("L’accueil montre ensuite quelques réalisations récentes, puis la méthode de travail en quatre étapes (diagnostic et brief, création et direction, production et répétition, validation et reporting), des avis de clients et un bouton final invitant à demander un devis.")
    FIG("home_real", "Page d’accueil : réalisations récentes")
    FIG("home_method", "Page d’accueil : méthode de travail", width=14.5)
    H(3, "7.2 La page À propos")
    P("Cette page raconte qui est Wiky Holding : sa vision, son équipe et sa façon de travailler. Elle présente les quatre pôles de l’agence (direction et gestion de projets, communication digitale, graphisme et identité visuelle, audiovisuel et studio podcast), puis les valeurs de l’entreprise : excellence et créativité, réactivité chirurgicale, transparence et rigueur, impact mesurable.")
    FIG("about_top", "Page À propos : présentation de l’agence")
    FIG("about_poles", "Page À propos : les quatre pôles")
    FIG("about_values", "Page À propos : les valeurs de l’agence")
    H(3, "7.3 La page Services")
    P("La page Services détaille chaque prestation : une description, ce qui est inclus dans l’offre, et un prix de départ en FCFA. Les données viennent du modèle ServiceModel.")
    FIG("serv_top", "Page Services : détail d’un service")
    P("En bas de page, trois packs sont proposés : Pack Starter Visibilité, Pack Identité et Autorité de Marque, et Pack Studio Podcast et Vidéo 360°. Chaque pack a son prix et la liste de ce qu’il contient. Le pack du milieu est mis en valeur comme étant le plus recommandé.")
    FIG("serv_packs", "Page Services : les trois packs d’accompagnement")
    H(3, "7.4 La page Réalisations")
    P("Cette page présente les projets réalisés pour des clients. Les projets sont affichés sous forme de cartes, avec une image, un titre, une courte description, les résultats obtenus et les services concernés. Des boutons en haut de la page permettent de filtrer par catégorie (branding, community management, podcast, création d’entreprise). Le filtrage se fait directement dans le navigateur, sans recharger la page.")
    FIG("port_top", "Page Réalisations : titre et filtres par catégorie")
    FIG("port_cards", "Page Réalisations : cartes des projets")
    H(3, "7.5 La page Studio podcast")
    P("Cette page présente le studio d’enregistrement de l’agence à Abidjan. Elle explique le format proposé (enregistrement audio et vidéo en 4K, montage, découpage en courtes vidéos), présente le matériel (micros broadcast Shure SM7B, caméras Sony 4K, éclairage Godox, traitement acoustique) et propose des idées d’émissions aux entreprises, avec un bouton pour réserver une session.")
    FIG("pod_top", "Page Studio podcast : présentation du studio")
    FIG("pod_equip", "Page Studio podcast : équipements")
    H(3, "7.6 La page Contact")
    P("La page Contact réunit les informations pratiques (adresse à Cocody, téléphones, email, horaires, bouton WhatsApp), une série de questions fréquentes qui s’ouvrent au clic, et le formulaire de contact. Le formulaire demande le nom, l’email, le téléphone, le service concerné, l’objet et le message. Il est protégé par un jeton de sécurité et vérifié côté serveur avant l’enregistrement.")
    FIG("cont_form", "Page Contact : formulaire et coordonnées")
    FIG("cont_faq", "Page Contact : questions fréquentes")
    H(3, "7.7 La page Devis")
    P("Cette page permet de décrire son projet et d’obtenir une estimation de prix. À droite, un encadré affiche l’estimation en FCFA, qui change dès que le visiteur modifie le type de prestation, l’envergure du projet (starter, standard ou premium) ou le délai souhaité. Le visiteur peut ensuite remplir ses coordonnées et envoyer sa demande, qui est enregistrée dans la table devis_requests.")
    FIG("devis", "Page Devis : simulateur et formulaire de demande")
    P("L’estimation affichée est seulement indicative : elle donne une idée du budget, mais le prix final est confirmé par l’agence après l’étude du projet.")

    # ================= CHAPITRE VI : FONCTIONNALITÉS DU SITE =================
    H(2, "CHAPITRE VI : FONCTIONNALITÉS DU SITE")
    H(3, "8.1 Le simulateur de devis")
    P("Le simulateur est écrit en JavaScript. Quand le visiteur change un choix (service, envergure, urgence), le script recalcule le prix et l’affiche immédiatement, sans recharger la page. Côté serveur, la méthode estimatePrice() de DevisModel fait aussi un calcul indicatif lors de l’enregistrement de la demande.")
    H(3, "8.2 La recherche instantanée")
    P("Un bouton de recherche dans la barre de navigation, ou le raccourci Ctrl + K (Cmd + K sur Mac), ouvre une fenêtre dans laquelle on peut taper un mot. La liste des pages et des services se filtre pendant la frappe, ce qui permet d’aller directement à la page voulue.")
    H(3, "8.3 Les thèmes et les couleurs")
    P("Le visiteur peut passer du thème clair au thème sombre ou au thème bleu marine, et choisir une couleur d’accentuation. Le choix est enregistré dans le localStorage du navigateur. Un petit script placé dans l’en-tête de la page applique ce choix avant l’affichage, pour éviter un éclair de la mauvaise couleur au chargement.")
    H(3, "8.4 Le filtre des réalisations")
    P("Sur la page Réalisations, un clic sur une catégorie masque les projets qui ne correspondent pas. Le changement se fait avec une petite animation de transparence.")
    H(3, "8.5 La barre de navigation et le bouton de retour en haut")
    P("La barre de navigation reste visible quand on descend dans la page et prend une légère ombre. Un bouton flottant permet de remonter en haut ; il est entouré d’un cercle qui se remplit au fur et à mesure du défilement, pour indiquer où l’on se trouve dans la page.")
    H(3, "8.6 L’affichage sur mobile")
    P("Le site est conçu pour s’adapter à la taille de l’écran. Sur téléphone, la navigation devient un menu latéral qui glisse depuis le bord de l’écran, les blocs s’empilent les uns sous les autres et les formulaires prennent toute la largeur.")
    FIG(["mob_a", "mob_b"], "Version mobile : accueil (à gauche) et page Devis (à droite)", width=12)

    # ================= CHAPITRE VII : SÉCURITÉ DU SITE =================
    H(2, "CHAPITRE VII : SÉCURITÉ DU SITE")
    P("Comme le site contient des formulaires qui enregistrent des informations de visiteurs, j’ai appliqué les principales protections recommandées pour le web.")
    H(3, "9.1 Protection contre les injections SQL")
    P("Toutes les requêtes qui utilisent des données venant des visiteurs sont des requêtes préparées PDO. Les valeurs ne sont jamais collées dans le texte de la requête : elles sont transmises séparément, ce qui empêche un visiteur d’injecter du code SQL.")
    H(3, "9.2 Protection contre les attaques CSRF")
    P("Chaque formulaire contient un jeton aléatoire de 32 octets, créé avec random_bytes() et gardé dans la session. Au moment de l’envoi, le serveur compare le jeton reçu avec celui de la session grâce à la fonction hash_equals(). Si les jetons ne correspondent pas, la demande est refusée. Cela empêche un autre site d’envoyer un formulaire à la place de l’utilisateur.")
    H(3, "9.3 Protection contre les attaques XSS")
    P("Tout texte venant d’un utilisateur ou de la base de données est affiché avec la fonction e(), qui utilise htmlspecialchars() avec ENT_QUOTES et l’encodage UTF-8. Ainsi, du code HTML ou JavaScript saisi dans un formulaire est affiché comme du simple texte et ne s’exécute pas.")
    H(3, "9.4 Validation des données")
    P("Le serveur vérifie les champs obligatoires, le format de l’adresse email et la longueur des textes avant d’enregistrer quoi que ce soit. La vérification côté serveur est indispensable, car celle du navigateur peut être contournée.")
    H(3, "9.5 Protection du serveur avec .htaccess")
    BL(["interdiction d’afficher la liste des fichiers d’un dossier (Options -Indexes) ;",
        "masquage de la version du serveur (ServerSignature Off) ;",
        "blocage de l’accès direct aux fichiers sensibles : database.sql, database.sqlite, le dossier .git et les fichiers PDF ;",
        "ajout d’en-têtes de sécurité : X-Content-Type-Options, X-Frame-Options et X-XSS-Protection ;",
        "réécriture des adresses pour avoir des liens propres."])

    # ================= CHAPITRE VIII : TESTS ET DÉBOGAGE =================
    H(2, "CHAPITRE VIII : TESTS ET DÉBOGAGE")
    H(3, "10.1 Les tests effectués")
    P("Avant la mise en ligne, j’ai testé le site en local avec WAMP et avec le serveur interne de PHP. Le tableau suivant résume les principaux tests :")
    TABLE(["Élément testé", "Test effectué", "Résultat"],
          [["Chargement des pages", "Ouverture des sept pages", "Aucune erreur PHP"],
           ["Routage", "Changement de page avec ?page= et avec les adresses réécrites", "Le bon contrôleur est appelé"],
           ["Base de données", "Création automatique des tables (MySQL et SQLite)", "Tables créées, connexion PDO fonctionnelle"],
           ["Formulaire de contact", "Envoi avec des données valides, puis invalides", "Validation correcte, message enregistré, confirmation affichée"],
           ["Formulaire de devis", "Envoi complet, puis avec des champs manquants", "Demande enregistrée ou erreur affichée"],
           ["Simulateur", "Changement du service, de l’envergure et de l’urgence", "Prix recalculé en direct en FCFA"],
           ["Sécurité CSRF", "Envoi sans jeton ou avec un faux jeton", "Demande refusée avec un message d’erreur"],
           ["Affichage adaptatif", "Ordinateur (1366 px) et mobile (375 px)", "Mise en page correcte, menu mobile fonctionnel"],
           ["Page 404", "Ouverture d’une adresse qui n’existe pas", "Page d’erreur personnalisée"]],
          [3.6, 6.4, 5.5], size=10)
    H(3, "10.2 Problèmes rencontrés et corrections")
    BL(["**Chemins des fichiers (CSS, JS, images)** : certains chemins ne marchaient pas selon que le site était dans un sous-dossier ou à la racine. J’ai créé une constante ASSETS_URL pour construire les chemins de façon uniforme ;",
        "**Date dans les requêtes SQL** : MySQL utilise NOW() et SQLite utilise datetime('now'). J’ai adapté la requête selon la base utilisée ;",
        "**Jeton CSRF** : le jeton n’existait pas toujours au moment d’afficher le formulaire. Il est maintenant créé avant l’affichage ;",
        "**Base de données indisponible** : pour éviter que le site plante quand MySQL n’est pas lancé, j’ai ajouté le mode de secours SQLite."])

    # ================= CHAPITRE IX : MISE EN LIGNE ET COÛT =================
    H(2, "CHAPITRE IX : MISE EN LIGNE ET COÛT")
    H(3, "11.1 Test en local avec WAMP")
    BL(["placer le dossier du projet dans le dossier www de WAMP ;",
        "lancer Apache et MySQL depuis WAMP ;",
        "importer database.sql dans phpMyAdmin (ou laisser le mode SQLite créer la base automatiquement) ;",
        "ouvrir http://localhost/achelyrapport/ dans le navigateur."])
    P("Une autre possibilité, sans WAMP, consiste à ouvrir un terminal dans le dossier du projet et à lancer la commande suivante, puis à ouvrir http://localhost:8000 :")
    CODE(["php -S localhost:8000"])
    H(3, "11.2 Mise en ligne sur InfinityFree")
    BL(["créer un compte sur InfinityFree et un sous-domaine ;",
        "créer une base de données MySQL dans le panneau de contrôle et noter l’hôte, le nom de la base, l’utilisateur et le mot de passe ;",
        "ouvrir phpMyAdmin et importer le fichier database.sql ;",
        "renseigner les informations de connexion dans app/Config/Database.php (DB_HOST, DB_NAME, DB_USER, DB_PASS) ;",
        "envoyer tous les fichiers dans le dossier htdocs de l’hébergeur avec FileZilla ou le gestionnaire de fichiers en ligne ;",
        "ouvrir l’adresse du site : il est accessible en HTTPS grâce au certificat gratuit."])
    H(3, "11.3 Coût de réalisation")
    P("Ce projet n’a demandé aucun achat : PHP, MySQL, WAMP, phpMyAdmin, FileZilla et l’hébergement InfinityFree sont gratuits. Les polices viennent de Google Fonts, également gratuites. Le principal coût du projet est donc le temps de travail passé à l’analyse, à la programmation, aux tests et à la rédaction. Si le site doit un jour être hébergé sur un serveur payant avec un nom de domaine personnalisé, un budget annuel d’hébergement et de nom de domaine devra être prévu par l’entreprise.")

    # ================= APPORTS, DIFFICULTÉS ET PERSPECTIVES =================
    H(2, "APPORTS, DIFFICULTÉS ET PERSPECTIVES")
    H(3, "12.1 Ce que ce stage m’a apporté")
    BL(["j’ai appris à organiser un vrai projet web avec le modèle MVC ;",
        "j’ai mieux compris la communication entre PHP et une base de données avec PDO ;",
        "j’ai appris à sécuriser des formulaires (CSRF, XSS, requêtes préparées) ;",
        "j’ai amélioré mes compétences en HTML, CSS et JavaScript, notamment pour l’affichage adaptatif ;",
        "j’ai découvert le fonctionnement d’une agence de communication et le travail de ses différents pôles ;",
        "j’ai appris à tester mon travail, à corriger les erreurs et à mettre un site en ligne."])
    H(3, "12.2 Les difficultés")
    P("La principale difficulté a été de devoir refaire le site depuis le début après la perte du site WordPress, tout en respectant le temps du stage. J’ai aussi dû chercher comment faire fonctionner le même code avec MySQL et avec SQLite, et comment rendre le site léger pour un hébergement gratuit.")
    H(3, "12.3 Perspectives d’amélioration")
    BL(["créer un espace d’administration protégé par mot de passe pour lire les messages et les demandes de devis directement depuis le site ;",
        "envoyer un email à l’agence à chaque nouveau message ou nouvelle demande de devis ;",
        "stocker les services et les réalisations dans la base de données pour pouvoir les modifier sans toucher au code ;",
        "ajouter une version du site en anglais ;",
        "ajouter un suivi des visites pour mesurer l’audience du site."])

    # ================= CONCLUSION =================
    H(1, "CONCLUSION", page_break=True)
    P("Ce stage au sein de Digital Agency Wiky m’a permis de mettre en pratique ce que j’ai appris pendant ma formation de BTS Informatique Développeur d’Application : analyser un besoin, concevoir l’organisation d’un logiciel, programmer, tester et mettre en ligne.")
    P("Le site réalisé pour Wiky Holding présente l’agence, ses quatre pôles, ses services, ses réalisations et son studio podcast. Il permet aux visiteurs d’envoyer un message, de demander un devis et d’obtenir une estimation de prix en direct. Il est organisé selon le modèle MVC, utilise PDO pour la base de données, et peut fonctionner avec MySQL ou avec SQLite. Il est protégé contre les principales attaques et peut être installé facilement sur un hébergement gratuit.")
    P("Ce projet remplace le site WordPress qui n’est plus disponible. Le refaire entièrement en PHP m’a demandé plus de travail, mais m’a surtout permis de mieux comprendre comment fonctionne un site web de l’intérieur.")
    P("Le site peut encore être amélioré, par exemple avec un espace d’administration ou l’envoi d’emails automatiques, mais il constitue déjà une base solide pour la présence de Wiky Holding sur Internet. Pour moi, ce stage a été une première expérience professionnelle très utile et une bonne préparation à mon futur métier de développeur.")
    P("")
    P("Fait à Abidjan, le ………………………", align=WD_ALIGN_PARAGRAPH.LEFT)
    P("")
    t = doc.add_table(rows=2, cols=2)
    for i, tx in enumerate(["L’étudiante", "Visa du maître de stage"]):
        c = t.rows[0].cells[i]; c.text = ""; r = c.paragraphs[0].add_run(tx); r.bold = True
        r.font.name = "Times New Roman"
        c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    for i, tx in enumerate(["KOUAME AFFOUE CYNTICHE ACHLEY DELMAS", "\n\n………………………………………"]):
        c = t.rows[1].cells[i]; c.text = ""; c.paragraphs[0].add_run(tx); c.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        c.paragraphs[0].runs[0].font.name = "Times New Roman"

    # ================= ANNEXES =================
    H(1, "ANNEXES", page_break=True)
    H(3, "Annexe 1 : Exemple de requête préparée (principe)")
    P("Les valeurs sont transmises séparément de la requête, ce qui empêche l’injection SQL :")
    CODE(["$stmt = $pdo->prepare(",
          "  \"INSERT INTO messages (name, email, subject, message)",
          "   VALUES (:name, :email, :subject, :message)\"",
          ");",
          "$stmt->execute([",
          "  ':name'    => $name,",
          "  ':email'   => $email,",
          "  ':subject' => $subject,",
          "  ':message' => $message",
          "]);"])
    H(3, "Annexe 2 : Jeton CSRF (principe)")
    CODE(["// création du jeton avant d'afficher le formulaire",
          "$_SESSION['csrf_token'] = bin2hex(random_bytes(32));",
          "",
          "// vérification à l'envoi du formulaire",
          "if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {",
          "    // demande refusée",
          "}"])
    H(3, "Annexe 3 : Configuration de la base MySQL")
    P("Les valeurs ci-dessous sont à remplacer par celles de l’hébergeur (ici en local avec WAMP) dans le fichier app/Config/Database.php :")
    CODE(["public const DB_HOST = 'localhost';",
          "public const DB_NAME = 'wiky_db';",
          "public const DB_USER = 'root';",
          "public const DB_PASS = '';"])
    H(3, "Annexe 4 : Technologies utilisées")
    TABLE(["Domaine", "Technologie"],
          [["Langage serveur", "PHP 7.4 à 8.3, programmation orientée objet"],
           ["Organisation du code", "MVC, chargement automatique des classes (PSR-4)"],
           ["Base de données", "MySQL ou SQLite, via PDO"],
           ["Interface", "HTML5, CSS3, JavaScript ES6"],
           ["Polices", "Plus Jakarta Sans et Inter (Google Fonts)"],
           ["Serveur", "Apache avec .htaccess"],
           ["Hébergement", "InfinityFree"],
           ["Outils", "WAMP, phpMyAdmin, FileZilla"]],
          [5, 10.5])

    # ================= remplir le SOMMAIRE =================
    def toc_line(level, text, page):
        p = sommaire_anchor.insert_paragraph_before()
        p.paragraph_format.tab_stops.add_tab_stop(Cm(16), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p.paragraph_format.space_after = Pt(3 if level >= 3 else 5)
        p.paragraph_format.line_spacing = 1.1
        indent_val = {1: 0, 2: 0, 3: 0.6, 4: 1.2}.get(level, 0)
        p.paragraph_format.left_indent = Cm(indent_val)
        r = p.add_run(text + "\t" + str(page))
        r.bold = (level <= 2)
        r.font.size = Pt(10.5 if level == 4 else 11)
        r.font.name = "Times New Roman"
        if level == 1: p.paragraph_format.space_before = Pt(4)

    for level, text in toc_entries:
        if level == 4 and False: continue
        # Page fallback
        page_val = pages_dict.get(text, pages_dict.get(text.strip(), "1"))
        toc_line(level, text, page_val)

    sommaire_anchor._element.getparent().remove(sommaire_anchor._element)

    doc.save(out_path)
    print(f"Generated {out_path} with {len(toc_entries)} TOC entries, {fig_n[0]} figures.")
    return toc_entries


def extract_pages_from_pdf(pdf_path, toc_entries):
    """Scan the generated PDF to find the exact page number of each heading."""
    doc = pymupdf.open(pdf_path)
    pages_map = {}
    print(f"Scanning PDF ({len(doc)} pages) for heading locations...")

    for level, heading in toc_entries:
        # Search starting from page 2 (index 1) to ignore the Sommaire itself
        clean_heading = heading.strip().replace("\xa0", " ")
        # Short anchor if long heading
        search_terms = [clean_heading]
        if ":" in clean_heading:
            search_terms.append(clean_heading.split(":", 1)[1].strip())
        if "." in clean_heading and len(clean_heading) > 10:
            search_terms.append(clean_heading.split(".", 1)[1].strip())

        found_page = None
        for pno in range(2, len(doc)):
            page_text = doc[pno].get_text().replace("\xa0", " ")
            for term in search_terms:
                if term in page_text:
                    found_page = pno + 1  # 1-indexed
                    break
            if found_page:
                break
        
        if found_page:
            pages_map[heading] = found_page
        else:
            # Fallback estimation
            pages_map[heading] = pages_map.get(heading, 1)

    print(f"Mapped {len(pages_map)} heading pages.")
    return pages_map


def main():
    print("=== PASS 1: Generate initial DOCX ===")
    toc_entries = generate_document(TEMP_DOCX, {})
    with open(TOC_JSON, "w", encoding="utf-8") as f:
        json.dump(toc_entries, f, ensure_ascii=False, indent=2)

    print("=== Convert PASS 1 to PDF to determine exact pagination ===")
    ps_cmd = [
        "powershell", "-ExecutionPolicy", "Bypass", "-File",
        os.path.join(SCRIPT_DIR, "convert_to_pdf.ps1"),
        "-docxPath", TEMP_DOCX,
        "-pdfPath", TEMP_PDF
    ]
    res = subprocess.run(ps_cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)

    if not os.path.exists(TEMP_PDF):
        print("ERROR: PDF was not generated in pass 1!")
        sys.exit(1)

    print("=== Extract exact page numbers from PDF ===")
    pages_map = extract_pages_from_pdf(TEMP_PDF, toc_entries)
    with open(PAGES_JSON, "w", encoding="utf-8") as f:
        json.dump(pages_map, f, ensure_ascii=False, indent=2)

    print("=== PASS 2: Generate final DOCX with exact Table of Contents ===")
    generate_document(FINAL_DOCX, pages_map)

    print("=== Convert final DOCX to final PDF ===")
    ps_cmd_final = [
        "powershell", "-ExecutionPolicy", "Bypass", "-File",
        os.path.join(SCRIPT_DIR, "convert_to_pdf.ps1"),
        "-docxPath", FINAL_DOCX,
        "-pdfPath", FINAL_PDF
    ]
    res_final = subprocess.run(ps_cmd_final, capture_output=True, text=True)
    print(res_final.stdout)
    if res_final.stderr:
        print("STDERR:", res_final.stderr)

    print("=== ALL DONE SUCCESSFULLY ===")
    print(f"Final DOCX: {FINAL_DOCX} ({os.path.getsize(FINAL_DOCX)} bytes)")
    if os.path.exists(FINAL_PDF):
        print(f"Final PDF: {FINAL_PDF} ({os.path.getsize(FINAL_PDF)} bytes)")

if __name__ == "__main__":
    main()
