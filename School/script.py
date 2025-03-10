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

def get_image_size(image_path):
    """Retourne la largeur et la hauteur de l'image."""
    img = fitz.open(image_path)
    return img[0].rect.width, img[0].rect.height

def generate_pdf_with_images():
    """ Génère un PDF avec des images spécifiées, classées selon leur taille. """

    doc = fitz.open()
    cover = doc.new_page(width=595, height=842)

    def center_text(page, text, y, fontsize, fontname="helv", color=(0, 0, 0)):
        text_width = fitz.get_text_length(text, fontname=fontname, fontsize=fontsize)
        x = (page.rect.width - text_width) / 2  # Centrer horizontalement
        page.insert_text((x, y), text, fontsize=fontsize, fontname=fontname, color=color)

    center_text(cover, "Titre du Document", 200, fontsize=20)
    center_text(cover, "Sous-titre ou Information", 250, fontsize=14)

    image_paths = [
        os.path.join(settings.BASE_DIR, "Math grade 3 - 2016 -question 33 CCSS.Math.Content.3.NF.A.3b.jpg"),
        os.path.join(settings.BASE_DIR, "Math grade 3 - 2017 - question 1 (CCSS.Math.Content.3.NF.A.1).jpg"),
        os.path.join(settings.BASE_DIR, "Math grade 3 - 2017 - question 2 (CCSS.Math.Content.3.OA.A.4 ).jpg"),
        os.path.join(settings.BASE_DIR, "Math grade 3 - 2017 - question 5 (CCSS.Math.Content.3.NBT.A.1 ).jpg"),

        os.path.join(settings.BASE_DIR, "Math grade 3 - 2017 - question 39 (CCSS.Math.Content.3.OA.D.8).jpg"),
        # Ajoutez d'autres chemins d'images ici
    ]

    images = []

    for img_path in image_paths:
        if os.path.exists(img_path):
            print(f"{img_path} existe.")
            width, height = get_image_size(img_path)
            images.append((img_path, width, height))
        else:
            print(f"{img_path} n'existe pas.")

    # Variables pour le positionnement
    margin_top = 54.7  # Marge supérieure
    spacing = 15.6  # Espacement entre les images
    question_number = 0  # Compteur pour les numéros de question

    # Insérer les images
    current_page = doc.new_page(width=595, height=842)
    y_position = margin_top  # Position Y pour l'insertion d'images

    for img_path, width, height in images:
        try:
            if height >= 600:  # Critère pour grande image
                # Créer une nouvelle page pour l'image grande
                current_page = doc.new_page(width=595, height=842)
                img_rect = fitz.Rect(0, margin_top, 595, margin_top + height)
                current_page.insert_image(img_rect, filename=img_path)

                # Numéro de question
                question_number += 1
                num_size = 16
                rect_width = 25  # Largeur du fond
                rect_height = 25  # Hauteur du fond
                rect_x = 20  # Ajustement de la position X pour le rectangle (décalé légèrement vers la gauche)
                rect_y = margin_top - 2  # Ajustement de la position Y

                # Dessiner le rectangle gris
                current_page.draw_rect(fitz.Rect(rect_x, rect_y, rect_x + rect_width, rect_y + rect_height),
                                        color=(0.8, 0.8, 0.8), fill=(0.8, 0.8, 0.8))  # Fond gris

                # Calculer la position centrale du texte dans le rectangle
                text_x = rect_x + (rect_width - fitz.get_text_length(str(question_number), fontname="Helvetica-Bold", fontsize=num_size)) / 2
                text_y = rect_y + (rect_height - num_size) / 2 + 14  # Ajustement pour centrer verticalement

                # Insérer le numéro de question sur l'image
                current_page.insert_text((text_x, text_y), str(question_number), fontsize=num_size, color=(0, 0, 0),
                                         fontname="Helvetica-Bold")

                y_position = margin_top + height + spacing  # Réinitialiser y_position pour la prochaine image

            elif height < 600 and height >= 300:  # Critère pour image moyenne
                if y_position + height > 842:  # Si la position dépasse la hauteur de la page
                    current_page = doc.new_page(width=595, height=842)
                    y_position = margin_top  # Réinitialiser la position Y

                img_rect = fitz.Rect(0, y_position, 595, y_position + height)
                current_page.insert_image(img_rect, filename=img_path)

                # Numéro de question
                question_number += 1
                num_size = 16
                rect_width = 25  # Largeur du fond
                rect_height = 25  # Hauteur du fond
                rect_x = 20  # Ajustement de la position X pour le rectangle (décalé légèrement vers la gauche)
                rect_y = y_position - 2  # Ajustement de la position Y

                # Dessiner le rectangle gris
                current_page.draw_rect(fitz.Rect(rect_x, rect_y, rect_x + rect_width, rect_y + rect_height),
                                        color=(0.8, 0.8, 0.8), fill=(0.8, 0.8, 0.8))  # Fond gris

                # Calculer la position centrale du texte dans le rectangle
                text_x = rect_x + (rect_width - fitz.get_text_length(str(question_number), fontname="Helvetica-Bold", fontsize=num_size)) / 2
                text_y = rect_y + (rect_height - num_size) / 2 + 14  # Ajustement pour centrer verticalement

                # Insérer le numéro de question sur l'image
                current_page.insert_text((text_x, text_y), str(question_number), fontsize=num_size, color=(0, 0, 0),
                                         fontname="Helvetica-Bold")

                y_position += height + spacing  # Mettre à jour la position Y pour la prochaine image

            else:  # Critère pour petite image
                if y_position + height > 842:  # Si la position dépasse la hauteur de la page
                    current_page = doc.new_page(width=595, height=842)
                    y_position = margin_top  # Réinitialiser la position Y

                img_rect = fitz.Rect(0, y_position, 595, y_position + height)
                current_page.insert_image(img_rect, filename=img_path)

                # Numéro de question
                question_number += 1
                num_size = 16
                rect_width = 25  # Largeur du fond
                rect_height = 25  # Hauteur du fond
                rect_x = 20  # Ajustement de la position X pour le rectangle (décalé légèrement vers la gauche)
                rect_y = y_position - 2 # Ajustement de la position Y

                # Dessiner le rectangle gris
                current_page.draw_rect(fitz.Rect(rect_x, rect_y, rect_x + rect_width, rect_y + rect_height),
                                        color=(0.8, 0.8, 0.8), fill=(0.8, 0.8, 0.8))  # Fond gris

                # Calculer la position centrale du texte dans le rectangle
                text_x = rect_x + (rect_width - fitz.get_text_length(str(question_number), fontname="Helvetica-Bold", fontsize=num_size)) / 2
                text_y = rect_y + (rect_height - num_size) / 2 + 14  # Ajustement pour centrer verticalement

                # Insérer le numéro de question sur l'image
                current_page.insert_text((text_x, text_y), str(question_number), fontsize=num_size, color=(0, 0, 0),
                                         fontname="Helvetica-Bold")

                y_position += height + spacing  # Mettre à jour la position Y pour la prochaine image

        except Exception as e:
            print(f"Erreur lors de l'insertion de l'image {img_path}: {e}")

    # Enregistrement du PDF
    doc.save("test.pdf")
    print("PDF généré : test.pdf")
    doc.close()

# Appel de la fonction pour générer le PDF
generate_pdf_with_images()