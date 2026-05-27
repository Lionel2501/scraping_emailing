from bs4 import BeautifulSoup
import re

# Fichier contenant le HTML copié
INPUT_FILE = "input.txt"

# Fichier de sortie
OUTPUT_FILE = "hrefs2.txt"

# Lire le contenu du fichier
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    html = f.read()

# Parser HTML
soup = BeautifulSoup(html, "html.parser")

# Récupérer tous les href
hrefs = []

for tag in soup.find_all(href=True):
    href = tag.get("href")

    # Nettoyage optionnel
    href = href.strip()

    # Ignorer les href vides
    if href:
        hrefs.append(href)

# Supprimer doublons tout en gardant l'ordre
hrefs = list(dict.fromkeys(hrefs))

# Sauvegarder
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for href in hrefs:
        f.write(href + "\n")

print(f"{len(hrefs)} href trouvés.")
print(f"Résultat sauvegardé dans : {OUTPUT_FILE}")