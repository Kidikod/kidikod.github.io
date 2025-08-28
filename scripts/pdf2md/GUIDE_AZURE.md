# 🚀 Guide d'Utilisation avec Azure - Descriptions Contextualisées

## 📊 Résultats du Test sur Plantamagotchi

### Performance Mesurée
- **12 images** traitées sur les 3 premières pages
- **100% de taux de description** avec Azure
- **9 mots-clés techniques** détectés automatiquement
- **Taille augmentée de 2.2KB à 3.8KB** (descriptions riches)

### Exemples de Descriptions Générées

#### Sans Azure :
```markdown
![](assets/image_0-0.png)
```

#### Avec Azure + Contexte :
```markdown
![motif de fond. Tags : fleur, dessin, pédicelle, art enfant (en relation avec : étape, Plantagotchi, Introduction)](assets/image_0-0.png)
```

## 🔧 Configuration Azure

### 1. Prérequis Azure
- Compte Azure actif
- Ressource Computer Vision créée
- Ressource Translator créée (optionnel mais recommandé)

### 2. Configuration Rapide
```bash
# Variables d'environnement
export AZURE_VISION_ENDPOINT="https://votre-region.cognitiveservices.azure.com/"
export AZURE_VISION_KEY="votre_clé_vision"
export AZURE_TRANSLATOR_ENDPOINT="https://api.cognitive.microsofttranslator.com/"
export AZURE_TRANSLATOR_KEY="votre_clé_translator"
export AZURE_TRANSLATOR_REGION="votre_région"
```

### 3. Test de Configuration
```bash
# Vérifier que tout fonctionne
python test_azure_pages.py
```

## 🎯 Utilisation Recommandée

### Conversion de Pages Spécifiques
```bash
# Les 3 premières pages avec descriptions contextualisées
python pdf2markdown.py document.pdf --pages 0 1 2 --wait-if-quota-reached
```

### Conversion Complète
```bash
# Document entier avec gestion intelligente des quotas
python pdf2markdown.py document.pdf --wait-if-quota-reached
```

### Mode Développement (sans Azure)
```bash
# Extraction de contexte sans descriptions d'images
python pdf2markdown.py document.pdf
```

## 📈 Fonctionnalités Avancées

### 1. Gestion Intelligente des Quotas
- **Suivi automatique** des limites Azure
- **Attente automatique** si quota atteint
- **Persistance** entre les exécutions

### 2. Contextualisation Multi-niveau
- **Position géographique** : Distance euclidienne texte-image
- **Mots-clés techniques** : Détection automatique (Scratch, algorithme, etc.)
- **Enrichissement sémantique** : Combinaison description + contexte

### 3. Descriptions Riches
- **Description principale** via Computer Vision
- **Tags pertinents** avec filtrage par confiance
- **Objets détectés** dans l'image
- **Traduction française** automatique

## 🏆 Cas d'Usage Optimaux

### Documents Techniques
```markdown
![interface de programmation Scratch montrant des blocs de condition et de boucle (en relation avec : algorithme, variable, programme)](assets/screenshot.png)
```

### Tutoriels Éducatifs
```markdown
![diagramme illustrant les étapes de croissance d'une plante virtuelle (en relation avec : Plantagotchi, costume, sprite)](assets/diagram.png)
```

### Manuels avec Schémas
```markdown
![capture d'écran de l'interface utilisateur montrant les outils de dessin (en relation avec : canvas, graphique, costume)](assets/interface.png)
```

## 💰 Coûts et Optimisation

### Estimation des Coûts
- **Computer Vision** : 5000 images gratuites/mois, puis ~1€/1000 images
- **Translator** : 2M caractères gratuits/mois, puis ~10€/1M caractères

### Optimisation
```bash
# Traiter seulement les pages importantes
python pdf2markdown.py doc.pdf --pages 1 3 5 7

# Mode batch pour plusieurs documents
for pdf in *.pdf; do
    python pdf2markdown.py "$pdf" --wait-if-quota-reached
done
```

## 🔍 Débogage et Monitoring

### Logs Détaillés
```
Extraction du contexte textuel des images...
Conversion du PDF en Markdown...
Traitement de 12 images...
Analyse de l'image image_0-0.png avec contexte...
Conversion terminée !
```

### Vérification des Quotas
```bash
# Les fichiers de quota sont automatiquement créés
ls -la .azure_*_quota.json
```

### Analyse des Résultats
```bash
# Script d'analyse automatique
python analyze_results.py
```

## 📁 Structure des Fichiers Générés

```
document/
├── document.md                     # Markdown avec descriptions contextualisées
├── assets/                         # Images extraites
│   ├── image_0-0.png              # Image page 0, index 0
│   ├── image_1-1.png              # Image page 1, index 1
│   └── ...
├── .azure_vision_quota.json       # Suivi quota Computer Vision
└── .azure_translator_quota.json   # Suivi quota Translator
```

## 🚨 Bonnes Pratiques

### Sécurité
```bash
# Ne jamais commiter les clés
echo ".azure_*_quota.json" >> .gitignore
echo "configure_azure.sh" >> .gitignore
```

### Performance
```bash
# Traitement par lots pour gros documents
python pdf2markdown.py huge_doc.pdf --pages 0 1 2 3 4
# Puis continuer avec les pages suivantes
```

### Qualité
- **Documents structurés** donnent de meilleurs résultats
- **Texte clair** améliore la détection de contexte
- **Images de qualité** produisent de meilleures descriptions

## 🎯 Résumé des Améliorations

| Fonctionnalité | Avant | Après |
|----------------|-------|-------|
| **Descriptions** | ❌ Aucune | ✅ 100% contextualisées |
| **Contexte** | ❌ Ignoré | ✅ Texte environnant |
| **Mots-clés** | ❌ Aucun | ✅ 9 détectés automatiquement |
| **Pertinence** | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Utilité** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

**🎉 Félicitations !** Votre convertisseur PDF vers Markdown génère maintenant des descriptions d'images intelligentes et contextualisées !
