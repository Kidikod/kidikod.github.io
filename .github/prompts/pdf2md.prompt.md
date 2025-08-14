---
mode: 'agent'
model: Claude Sonnet 3.5
tools: ['codebase', 'usages', 'vscodeAPI', 'changes', 'terminalSelection', 'terminalLastCommand', 'fetch', 'searchResults', 'githubRepo', 'runCommands', 'runTasks', 'editFiles', 'search']
description: 'Convertir un fichier PDF en Markdown, en extrayant les images et en nettoyant le contenu pour une meilleure lisibilité et structure.'
---
Ton travail consiste à convertir un fichier PDF en Markdown, en extrayant les images et en nettoyant le contenu pour une meilleure lisibilité et structure. 

Commence par demander quel fichier PDF est à convertir.

Suis les étapes ci-dessous pour réaliser cette tâche efficacement.

# Instructions pour la conversion PDF vers Markdown

## Procédure de conversion PDF vers Markdown

1. Première conversion avec `pdftohtml` :
   ```bash
   pdftohtml -s -i fichier.pdf
   ```
   Options importantes :
   - `-s` : génère une seule page HTML
   - `-i` : ignore les images (nous les traiterons séparément)

2. Nettoyage initial du HTML :
   - Supprimer les balises de style et de mise en page
   - Conserver uniquement la structure du contenu
   - Vérifier l'encodage des caractères

3. Conversion HTML vers Markdown avec `pandoc` :
   ```bash
   pandoc -f html -t markdown fichier.html -o fichier.md
   ```

4. Post-traitement du Markdown :
   - Créer un fichier tampon `clean_fichier.md` pour le post-traitement
   - Ne jamais modifier directement le fichier de sortie de pandoc
   - Effectuer les modifications progressivement dans le fichier tampon :
     - Corriger la hiérarchie des titres
     - Uniformiser les listes
     - Vérifier les sauts de ligne
     - Nettoyer les espaces superflus
     - Standardiser la ponctuation
   - Garder le fichier original comme référence pendant le nettoyage

5. Structure du document :
   - Ajouter le front matter si nécessaire
   - Vérifier la cohérence des niveaux de titres
   - Ajouter les métadonnées pertinentes
   - Organiser le contenu en sections logiques

6. Validation :
   - Vérifier le rendu final
   - S'assurer que la structure est préservée
   - Contrôler la lisibilité du code source
   - Valider les liens et références

## Extraction des images

1. Utiliser `pdfimages` plutôt que `pdftohtml` pour extraire les images individuelles :
   ```bash
   pdfimages -all input.pdf output_directory/prefix
   ```

2. Options importantes de `pdfimages` :
   - `-f` : spécifier la première page à extraire
   - `-l` : spécifier la dernière page à extraire
   - `-all` : extraire tous les types d'images

## Traitement des images

1. Examiner chaque image extraite pour comprendre son contenu et son contexte
2. Renommer les images avec des noms descriptifs qui reflètent leur contenu
3. Pour les images composites (contenant plusieurs sous-images) :
   - Utiliser CSS `clip-path: inset()` pour rogner les parties spécifiques
   - Conserver l'image source complète et l'utiliser plusieurs fois avec différents rognages

## Structure HTML/CSS pour les images

1. Pour aligner horizontalement des images :
```html
<div style="display: flex; justify-content: space-around; align-items: center; margin: 20px 0;">
    <img src="..." alt="..." style="...">
</div>
```

2. Pour afficher une partie spécifique d'une image (technique des sprites CSS) :
```html
<div style="width: W; height: H; background: url('image.png') no-repeat; background-position: X Y; background-size: W auto;" title="Description"></div>
```
Où :
- W : largeur fixe du conteneur
- H : hauteur fixe du conteneur
- X : position horizontale du sprite (généralement 0)
- Y : position verticale du sprite (ex: 0, -H, -2H, etc.)

Exemple avec une image verticale contenant 5 sprites de même taille :
```html
<div style="display: flex; justify-content: space-around; align-items: center;">
    <!-- Premier sprite (haut de l'image) -->
    <div style="width: 100px; height: 115px; background: url('sprite.png') no-repeat; background-position: 0 0; background-size: 100px auto;" title="Sprite 1"></div>
    <!-- Deuxième sprite (20% plus bas) -->
    <div style="width: 100px; height: 115px; background: url('sprite.png') no-repeat; background-position: 0 -115px; background-size: 100px auto;" title="Sprite 2"></div>
    <!-- Troisième sprite (40% plus bas) -->
    <div style="width: 100px; height: 115px; background: url('sprite.png') no-repeat; background-position: 0 -230px; background-size: 100px auto;" title="Sprite 3"></div>
</div>
```

Avantages de la technique des sprites CSS :
- Une seule requête HTTP pour charger l'image
- Meilleure performance que clip-path
- Positionnement précis des éléments
- Maintien des proportions
- Facilité de maintenance

## Organisation des fichiers

1. Créer une structure de dossiers cohérente :
   ```
   assets/
     └── sous-dossier-thematique/
         └── images-specifiques.png
   ```

2. Préférer des noms de fichiers :
   - En minuscules
   - Utilisant des tirets pour les espaces
   - Descriptifs du contenu
   - Sans caractères spéciaux

## Bonnes pratiques

1. Toujours ajouter des attributs `alt` descriptifs aux images
2. Maintenir une cohérence dans les dimensions des images
3. Éviter de dupliquer les images quand elles peuvent être réutilisées
4. Préférer le HTML/CSS pour la mise en page plutôt que des espaces dans le Markdown
5. Retirer les textes redondants quand ils sont déjà présents dans le contenu principal

## Nettoyage des fichiers temporaires

1. Fichiers générés par pdftohtml :
   ```bash
   rm fichier.html         # Fichier HTML principal
   rm fichier-*.html       # Pages HTML individuelles
   rm fichier_ind.html     # Fichier d'index
   ```

2. Dossiers d'images temporaires :
   ```bash
   rm -r extracted_*/      # Dossiers d'extraction temporaire
   ```

3. Fichiers intermédiaires :
   ```bash
   rm fichier_original.md  # Version markdown initiale
   ```

4. Vérifications avant suppression :
   - S'assurer que toutes les images nécessaires ont été copiées dans le dossier `assets`
   - Vérifier que le fichier `clean_fichier.md` est complet et validé
   - Sauvegarder tout fichier intermédiaire qui pourrait être utile plus tard

5. Garder une trace du processus :
   - Documenter les commandes utilisées
   - Noter les modifications spécifiques effectuées
   - Conserver les paramètres de conversion importants
