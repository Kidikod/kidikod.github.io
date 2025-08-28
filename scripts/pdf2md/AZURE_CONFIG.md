# Configuration Azure - Instructions

## 🔑 Obtenir vos clés Azure

### 1. Azure Computer Vision
1. Connectez-vous au [portail Azure](https://portal.azure.com)
2. Créez une ressource "Computer Vision" ou utilisez une existante
3. Dans les paramètres de la ressource :
   - **Endpoint** : Copiez l'URL (ex: `https://votre-region.cognitiveservices.azure.com/`)
   - **Key** : Copiez une des clés d'accès

### 2. Azure Translator
1. Créez une ressource "Translator" dans le portail Azure
2. Dans les paramètres de la ressource :
   - **Endpoint** : Généralement `https://api.cognitive.microsofttranslator.com/`
   - **Key** : Copiez une des clés d'accès
   - **Region** : La région de votre ressource (ex: `westeurope`, `eastus`)

## 🚀 Configuration Rapide

### Option 1: Variables d'environnement (Recommandé)
```bash
# Dans votre terminal
export AZURE_VISION_ENDPOINT="https://VOTRE-REGION.cognitiveservices.azure.com/"
export AZURE_VISION_KEY="VOTRE_CLE_AZURE_VISION"
export AZURE_TRANSLATOR_ENDPOINT="https://api.cognitive.microsofttranslator.com/"
export AZURE_TRANSLATOR_KEY="VOTRE_CLE_AZURE_TRANSLATOR"
export AZURE_TRANSLATOR_REGION="VOTRE_REGION"
```

### Option 2: Script de configuration
```bash
# Éditez le fichier configure_azure.sh avec vos vraies clés
nano configure_azure.sh

# Puis exécutez
source configure_azure.sh
```

### Option 3: Fichier .env (pour développement)
Créez un fichier `.env` :
```
AZURE_VISION_ENDPOINT=https://votre-region.cognitiveservices.azure.com/
AZURE_VISION_KEY=votre_clé_vision
AZURE_TRANSLATOR_ENDPOINT=https://api.cognitive.microsofttranslator.com/
AZURE_TRANSLATOR_KEY=votre_clé_translator
AZURE_TRANSLATOR_REGION=votre_région
```

## ✅ Vérification de la configuration
```bash
# Testez la configuration
python test_azure_pages.py
```

## 💰 Coûts et Quotas

### Azure Computer Vision
- **Gratuit** : 5 000 transactions/mois
- **Payant** : À partir de 1€ pour 1 000 transactions

### Azure Translator
- **Gratuit** : 2M caractères/mois
- **Payant** : ~10€ par million de caractères

## 🔒 Sécurité

⚠️ **IMPORTANT** : Ne commitez jamais vos clés dans Git !

```bash
# Ajoutez à votre .gitignore
echo "configure_azure.sh" >> .gitignore
echo ".env" >> .gitignore
echo ".azure_*_quota.json" >> .gitignore
```
