#!/bin/bash
# Script de configuration des APIs Azure
# REMPLACEZ LES VALEURS CI-DESSOUS PAR VOS VRAIES CLÉS AZURE

echo "=== Configuration des APIs Azure pour le convertisseur PDF ==="
echo ""

# Azure Computer Vision
echo "Configuration Azure Computer Vision..."
export AZURE_VISION_ENDPOINT="https://VOTRE-REGION.cognitiveservices.azure.com/"
export AZURE_VISION_KEY="VOTRE_CLE_AZURE_VISION"

# Azure Translator
echo "Configuration Azure Translator..."
export AZURE_TRANSLATOR_ENDPOINT="https://api.cognitive.microsofttranslator.com/"
export AZURE_TRANSLATOR_KEY="VOTRE_CLE_AZURE_TRANSLATOR"
export AZURE_TRANSLATOR_REGION="VOTRE_REGION"

echo ""
echo "Variables configurées :"
echo "AZURE_VISION_ENDPOINT=${AZURE_VISION_ENDPOINT}"
echo "AZURE_VISION_KEY=***${AZURE_VISION_KEY: -4}"
echo "AZURE_TRANSLATOR_ENDPOINT=${AZURE_TRANSLATOR_ENDPOINT}"
echo "AZURE_TRANSLATOR_KEY=***${AZURE_TRANSLATOR_KEY: -4}"
echo "AZURE_TRANSLATOR_REGION=${AZURE_TRANSLATOR_REGION}"
echo ""
echo "Pour tester, exécutez :"
echo "source configure_azure.sh"
echo "python pdf2markdown.py /path/to/pdf --pages 0 1 2"
