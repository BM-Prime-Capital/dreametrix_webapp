import os
import sys
import django
import fitz

# Ajouter le dossier parent au sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Définir le module de paramètres
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolManagementSystem.settings')
django.setup()

from django.conf import settings

def generate_pdf_with_images():
    """ Génère un PDF avec deux images spécifiées sur la même page, avec la numérotation des questions. """

    doc = fitz.open()
    cover = doc.new_page(width=595, height=842)

    def center_text(page, text, y, fontsize, fontname="helv", color=(0, 0, 0)):
        text_width = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
        x = (page.rect.width - text_width) / 2  # Centrer horizontalement
        page.insert_text((x, y), text, fontsize=fontsize, fontname=fontname, color=color)

    center_text(cover, "Titre du Document", 200, fontsize=20)
    center_text(cover, "Sous-titre ou Information", 250, fontsize=14)

    page = doc.new_page(width=595, height=842)

    image_1_path = os.path.join(settings.BASE_DIR, "image_1.jpeg")
    image_2_path = os.path.join(settings.BASE_DIR, "image_2.jpeg")

    print(f"Image 1 path: {image_1_path}")
    print(f"Image 2 path: {image_2_path}")

    # Vérifiez si les images existent
    if os.path.exists(image_1_path):
        print(f"{image_1_path} existe.")
    else:
        print(f"{image_1_path} n'existe pas.")

    if os.path.exists(image_2_path):
        print(f"{image_2_path} existe.")
    else:
        print(f"{image_2_path} n'existe pas.")

    images = [image_1_path, image_2_path]
    margin = 10  # Définir la marge
    img_width = 575  # Largeur totale de l'image
    img_height = (842 - margin * 3) / 2  # Hauteur de l'image (50% de la page moins les marges)

    # Position Y du numéro de question
    question_position_offset = 79  # Ajustez cette valeur pour déplacer le numéro vers le bas

    # Décalage à droite
    offset_right = 5  # Ajustez cette valeur pour déplacer le rectangle et le numéro vers la droite

    # Ajustement pour faire monter le numéro et le rectangle
    vertical_offset = 10  # Valeur pour monter le rectangle et le numéro

    for i, image_path in enumerate(images):
        try:
            # Calculer la position Y pour chaque image en tenant compte de la marge
            y_position = margin + i * (img_height + margin)  # Position Y avec marge
            img_rect = fitz.Rect(margin, y_position, margin + img_width, y_position + img_height)
            page.insert_image(img_rect, filename=image_path)

            # Définir le numéro de question
            question_number = i + 17
            num_size = 16

            # Dessiner le fond gris pour le numéro
            rect_width = 25  # Largeur du fond
            rect_height = 25  # Hauteur du fond
            rect_x = margin + 5 + offset_right  # Ajustement de la position X pour le rectangle
            rect_y = y_position + question_position_offset - 18 - vertical_offset  # Ajustement de la position Y pour le rectangle (monter le box)

            # Dessiner le rectangle gris
            page.draw_rect(fitz.Rect(rect_x, rect_y, rect_x + rect_width, rect_y + rect_height),
                           color=(0.8, 0.8, 0.8), fill=(0.8, 0.8, 0.8))  # Fond gris

            # Calculer la position centrale du texte dans le rectangle
            text_x = rect_x + (rect_width - fitz.get_text_length(str(question_number), fontname="Helvetica-Bold", fontsize=num_size)) / 2
            text_y = rect_y + (rect_height - num_size) / 2 + 12  # Ajustement pour centrer verticalement

            # Insérer le numéro de question sur l'image
            page.insert_text((text_x, text_y), str(question_number), fontsize=num_size, color=(0, 0, 0),
                             fontname="Helvetica-Bold")

        except Exception as e:
            print(f"Erreur lors de l'insertion de l'image {image_path}: {e}")

    # Enregistrement du PDF
    doc.save("test.pdf")
    print("PDF généré : test.pdf")
    doc.close()

# Appel de la fonction pour générer le PDF
generate_pdf_with_images()