---
mode: 'agent'
model: Claude Sonnet 4
tools: ['codebase', 'usages', 'changes', 'runCommands', 'runTasks', 'editFiles', 'search']
description: 'Convertir un PDF en Markdown avec gestion des images et de leurs descriptions'
---
Ton travail consiste à convertir un fichier PDF en Markdown en assurant une documentation détaillée des images.

Commence par demander quel fichier PDF est à convertir.

**IMPORTANT : Utilise les scripts existants dans `scripts/pdf2md/` pour effectuer la conversion :**
- `scripts/pdf2md/convert_pdf.py` : Conversion automatique PDF vers Markdown
- `scripts/pdf2md/apply_descriptions.py` : Application des descriptions d'images  
- `scripts/pdf2md/requirements.txt` : Dépendances Python nécessaires

Cette approche de conversion offre :
- Séparation des préoccupations : descriptions dans un fichier dédié
- Réutilisabilité : scripts applicables à d'autres PDFs
- Maintenance facile : modifications des descriptions sans toucher au Markdown
- Qualité : descriptions manuelles précises et contextuelles
- Traçabilité : rapport détaillé des modifications

# Instructions de conversion PDF vers Markdown

## Configuration initiale

1. Installer les dépendances Python :
   ```bash
   pip install pymupdf4llm pillow
   ```

2. **Utiliser les scripts existants** :
   Le projet contient déjà des scripts prêts à l'emploi dans `scripts/pdf2md/` :
   - `convert_pdf.py` : Script de conversion PDF vers Markdown
   - `apply_descriptions.py` : Script d'application des descriptions
   - `requirements.txt` : Dépendances Python

3. Structure recommandée du projet :
   ```
   /chemin/vers/projet/
   ├── source.pdf             # Fichier PDF source
   ├── index.md              # Fichier Markdown final
   ├── index_old.md         # Version originale avant modifications
   ├── assets/              # Dossier contenant les images extraites
   ├── image_descriptions.py # Base de données des descriptions
   └── apply_descriptions.py # Script d'application des descriptions (copié depuis scripts/pdf2md/)
   ```

## Procédure de conversion

1. **Conversion initiale avec le script existant** :
   ```bash
   python scripts/pdf2md/convert_pdf.py chemin/vers/source.pdf [dossier_destination]
   ```
   
   Ou manuellement :
   ```python
   import pymupdf4llm
   
   # Convertir le PDF avec extraction automatique des images
   md_text = pymupdf4llm.to_markdown(
       'source.pdf',
       write_images=True,
       image_path='assets'
   )
   
   # Sauvegarder le résultat
   with open('index.md', 'w', encoding='utf-8') as f:
       f.write(md_text)
   ```

2. **Copier les scripts dans le dossier de travail** :
   ```bash
   cp scripts/pdf2md/apply_descriptions.py chemin/vers/projet/
   ```

3. **Gestion des descriptions (image_descriptions.py)** :
   Créer un fichier `image_descriptions.py` dans le dossier du projet :
   ```python
   # Base de données des descriptions d'images
   IMAGE_DESCRIPTIONS = {
       'assets/image_1.png': {
           'description': 'Description détaillée de l\'image',
           'context': 'Rôle de cette image dans le document',
           'type': 'interface/sprite/capture/etc'
       },
       # ... autres images
   }
   ```

4. **Application des descriptions** :
   Le script `apply_descriptions.py` (copié depuis `scripts/pdf2md/`) contient déjà la logique :
   ```python
   import re
   from pathlib import Path
   from image_descriptions import IMAGE_DESCRIPTIONS

   def apply_descriptions(markdown_file='index.md'):
       content = Path(markdown_file).read_text(encoding='utf-8')
       updated = 0
       missing = []
       
       # Chercher toutes les images
       for match in re.finditer(r'!\[(.*?)\]\(([^)]+)\)', content):
           img_path = match.group(2)
           if img_path in IMAGE_DESCRIPTIONS:
               desc = IMAGE_DESCRIPTIONS[img_path]
               new_image = f'![{desc["description"]}]({img_path})'
               content = content.replace(match.group(0), new_image)
               updated += 1
           else:
               missing.append(img_path)
       
       # Sauvegarder avec backup
       if updated > 0:
           Path(f"{markdown_file[:-3]}_old.md").write_text(
               Path(markdown_file).read_text(encoding='utf-8'),
               encoding='utf-8'
           )
           Path(markdown_file).write_text(content, encoding='utf-8')
       
       return updated, missing

   if __name__ == '__main__':
       import sys
       file = sys.argv[1] if len(sys.argv) > 1 else 'index.md'
       updated, missing = apply_descriptions(file)
       print(f"{updated} descriptions appliquées")
       if missing:
           print("Images sans description :")
           for img in missing:
               print(f"- {img}")
   ```
    
    ## Utilisation

1. **Conversion du PDF avec le script existant** :
   ```bash
   # Utiliser le script de conversion automatique
   python scripts/pdf2md/convert_pdf.py chemin/vers/source.pdf [dossier_destination]
   ```
   
   Ou manuellement :
   ```bash
   python -c "
   import pymupdf4llm
   print('Conversion du PDF...')
   md_text = pymupdf4llm.to_markdown('source.pdf', write_images=True, image_path='assets')
   with open('index.md', 'w', encoding='utf-8') as f:
       f.write(md_text)
   print('Conversion terminée !')
   "
   ```

2. **Copier et configurer les scripts** :
   ```bash
   # Copier le script d'application des descriptions
   cp scripts/pdf2md/apply_descriptions.py ./
   
   # Créer le fichier image_descriptions.py avec les descriptions personnalisées
   ```

3. **Application des descriptions** :
   ```bash
   # Appliquer les descriptions au fichier par défaut
   python apply_descriptions.py

   # Appliquer à un fichier spécifique
   python apply_descriptions.py mon_fichier.md

   # Lister les images sans description
   python apply_descriptions.py --list-missing
   ```

## Validation

1. **Vérifications** :
   - Toutes les images sont extraites dans assets/
   - Les liens d'images dans le Markdown sont corrects
   - Chaque image a une description appropriée
   - La structure du document est préservée

2. **Qualité des descriptions** :
   - Descriptions contextuelles et précises
   - Informations pertinentes pour chaque image
   - Cohérence dans le style des descriptions

## Bonnes pratiques

1. **Organisation** :
   - Garder les descriptions séparées du contenu
   - Faire des sauvegardes avant modifications (fichiers _old)
   - Utiliser des chemins relatifs pour les images

2. **Descriptions** :
   - Être précis et concis
   - Inclure le contexte nécessaire
   - Penser à l'accessibilité

3. **Maintenance** :
   - Documenter le processus
   - Conserver les fichiers originaux
   - Garder une trace des modifications
