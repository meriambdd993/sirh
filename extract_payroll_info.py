import pdfplumber
import re
import sys
import json
from PIL import Image

def extract_payroll_info(pdf_path, output_folder):
    all_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            data = {}
            texte_paie = page.extract_text()
            # Extraire la date
            date_regex = re.compile(r"(Paye du\s*:)([^a-zA-Z]+)")
            date_match = date_regex.search(texte_paie)
            date_text = date_match.group(2).strip() if date_match else None
            date_text = date_text.replace(" ", "")
            day, month_number, year = date_text.split("/")
            
            month_names = {
                "01": "Janvier", "02": "Février", "03": "Mars",
                "04": "Avril", "05": "Mai", "06": "Juin",
                "07": "Juillet", "08": "Août", "09": "Septembre",
                "10": "Octobre", "11": "Novembre", "12": "Décembre"
            }
            month_name = month_names.get(month_number)
            data["Mois"] = f"{month_name}, {year}"
            
            # Extraire le titre, le nom et le prénom
            nom_prenom_regex = re.compile(r"(Mr|Mme|Mlle) ([A-Z]+) ([A-Za-z]+)")
            nom_prenom_match = nom_prenom_regex.search(texte_paie)
            data["Titre"] = nom_prenom_match.group(1) if nom_prenom_match else None
            data["Nom"] = nom_prenom_match.group(2) if nom_prenom_match else None
            data["Prénom"] = nom_prenom_match.group(3) if nom_prenom_match else None
            
            # Extraire le matricule
            matricule_regex = re.compile(r"Matricule (\d+)")
            matricule_match = matricule_regex.search(texte_paie)
            data["Matricule"] = matricule_match.group(1) if matricule_match else None

            # Enregistrement de la page actuelle en tant qu'image
            image = page.to_image()
            image.save(f'{output_folder}/page_{page_number}.png', 'PNG')
            page_link = f'{output_folder}/page_{page_number}.png'
            data["PageLink"] = page_link
            
            all_data.append(data)
            
    return all_data

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    output_folder = 'pages'  # Dossier où les images seront enregistrées
    results = extract_payroll_info(pdf_path, output_folder)
    print(json.dumps(results))
