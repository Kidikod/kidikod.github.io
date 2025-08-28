# Convertisseur PDF vers Markdown avec Descriptions Contextualisées

Ce script Python convertit des fichiers PDF en Markdown avec des descriptions d'images intelligentes et contextualisées.

## 🚀 Nouvelles Fonctionnalités

### Descriptions Contextualisées
- **Extraction du contexte textuel** : Le script analyse le texte autour de chaque image
- **Positionnement intelligent** : Utilise la position des images pour trouver le texte le plus pertinent
- **Enrichissement des descriptions** : Combine la description Azure Vision avec le contexte local
- **Mots-clés techniques** : Détecte automatiquement les termes techniques pertinents

### Améliorations de l'Analyse d'Images
- **Tags et objets** : Utilise plus de fonctionnalités d'Azure Vision (tags, objets)
- **Filtrage par confiance** : Ne garde que les tags avec un niveau de confiance élevé
- **Descriptions enrichies** : Combine plusieurs sources d'information

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🔧 Configuration

### Variables d'Environnement (Recommandé)

```bash
export AZURE_VISION_ENDPOINT="https://votre-region.cognitiveservices.azure.com/"
export AZURE_VISION_KEY="votre_clé_azure_vision"
export AZURE_TRANSLATOR_ENDPOINT="https://api.cognitive.microsofttranslator.com/"
export AZURE_TRANSLATOR_KEY="votre_clé_azure_translator"
export AZURE_TRANSLATOR_REGION="votre_région"
```

### Utilisation en Ligne de Commande

```bash
# Conversion de base (sans descriptions d'images)
python pdf2markdown.py document.pdf

# Avec descriptions contextualisées
python pdf2markdown.py document.pdf --vision-endpoint "https://..." --vision-key "..."

# Pages spécifiques
python pdf2markdown.py document.pdf --pages 0 1 2

# Attendre si quota atteint (au lieu d'échouer)
python pdf2markdown.py document.pdf --wait-if-quota-reached
```

## 🧠 Comment Ça Marche

### 1. Extraction du Contexte
Le script :
1. Analyse chaque page du PDF avec PyMuPDF
2. Extrait les positions exactes des images
3. Identifie les blocs de texte proches de chaque image
4. Calcule la distance euclidienne pour trouver le texte le plus pertinent

### 2. Analyse Contextualisée
Pour chaque image :
1. **Description de base** via Azure Computer Vision (description, tags, objets)
2. **Extraction de mots-clés** du contexte textuel environnant
3. **Enrichissement** de la description avec le contexte pertinent
4. **Traduction** en français via Azure Translator

### 3. Génération du Markdown
- Remplacement des références d'images par des descriptions enrichies
- Organisation des images dans un dossier `assets/`
- Préservation de la structure du document original

## 📊 Exemple de Résultat

### Avant (description générique) :
```markdown
![a screenshot of a computer screen](assets/image_001.png)
```

### Après (description contextualisée) :
```markdown
![capture d'écran montrant une interface de programmation Scratch (en relation avec : algorithme, boucle, condition)](assets/image_001.png)
```

## 🔄 Gestion des Quotas

Le script inclut une gestion intelligente des quotas Azure :
- **Suivi automatique** des limites mensuelles et par minute
- **Persistance** : sauvegarde l'état entre les exécutions
- **Mode d'attente** : peut attendre que les quotas se renouvellent
- **Limites par défaut** :
  - Azure Vision : 5000 req/mois, 20 req/minute
  - Azure Translator : 2M caractères/mois, 5 req/seconde

## 🛠️ Utilisation Programmatique

```python
from pdf2markdown import PDF2Markdown

# Conversion avec contexte
converter = PDF2Markdown(
    "document.pdf",
    vision_endpoint="https://...",
    vision_key="...",
    translator_endpoint="https://...",
    translator_key="...",
    translator_region="...",
    wait_if_quota_reached=True
)

markdown_content = converter.convert_to_markdown()

# Sauvegarder
with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)
```

## 🎯 Cas d'Usage Optimaux

Ce convertisseur est particulièrement efficace pour :
- **Documents techniques** avec diagrammes et schémas
- **Tutoriels de programmation** avec captures d'écran
- **Manuels éducatifs** avec illustrations contextuelles
- **Documentation** mêlant texte et images explicatives

## 🔍 Débogage

Le script fournit des messages détaillés pour suivre le processus :
```
Extraction du contexte textuel des images...
Conversion du PDF en Markdown...
Traitement de 5 images...
Analyse de l'image image_001.png avec contexte...
Conversion terminée !
```

## ⚠️ Limitations

- Nécessite des APIs Azure pour les meilleures descriptions
- La qualité dépend de la clarté du texte dans le PDF
- Les quotas Azure peuvent limiter le traitement de gros documents
- La reconnaissance du contexte fonctionne mieux avec du texte structuré

## 🤝 Contribution

N'hésitez pas à proposer des améliorations pour :
- Nouveaux algorithmes de contextualisation
- Support d'autres APIs de vision
- Optimisations de performance
- Nouveaux formats de sortie
