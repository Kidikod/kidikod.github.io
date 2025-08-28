#!/usr/bin/env python3
"""
Démonstrateur des capacités de contextualisation du script PDF2Markdown
"""

import os
import sys
sys.path.append('/workspaces/kidikod.github.io/scripts/pdf2md')

from pdf2markdown import PDF2Markdown

def demonstrate_context_extraction():
    """Démontre l'extraction du contexte textuel"""
    
    pdf_path = "/workspaces/kidikod.github.io/_scratch_tp/plantamagotchi/Plantamagotchi.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"PDF non trouvé : {pdf_path}")
        return
    
    print("=== Démonstration de l'extraction de contexte ===\n")
    
    # Créer le convertisseur (sans APIs Azure pour le test)
    converter = PDF2Markdown(pdf_path)
    
    # Extraire le contexte textuel
    print("1. Extraction du contexte textuel par page...")
    context_map = converter.extract_text_context_around_images()
    
    # Afficher un échantillon du contexte pour les premières pages
    print(f"\nContexte trouvé pour {len(context_map)} pages avec des images\n")
    
    for page_num in sorted(context_map.keys())[:3]:  # Afficher seulement les 3 premières pages
        context = context_map[page_num]
        # Afficher les 200 premiers caractères
        preview = context[:200] + "..." if len(context) > 200 else context
        print(f"Page {page_num}:")
        print(f"  Longueur du contexte: {len(context)} caractères")
        print(f"  Aperçu: {preview}")
        print()
    
    # Tester l'extraction de mots-clés
    print("2. Test d'extraction de mots-clés...")
    sample_context = """
    Dans Scratch, nous allons créer un programme avec des variables et des boucles.
    Cette étape montre comment utiliser les blocs de condition pour créer un algorithme.
    Le sprite va exécuter différentes actions selon les données reçues.
    """
    
    keywords = converter.extract_keywords_from_context(sample_context)
    print(f"Contexte d'exemple: {sample_context.strip()}")
    print(f"Mots-clés extraits: {keywords}")
    print()
    
    # Tester la création de description contextualisée
    print("3. Test de création de description contextualisée...")
    base_description = "Une capture d'écran d'interface utilisateur"
    enhanced = converter.create_contextual_description(base_description, sample_context)
    print(f"Description de base: {base_description}")
    print(f"Description enrichie: {enhanced}")
    print()
    
    print("=== Démonstration terminée ===")
    print("\nPour activer les descriptions complètes, configurez les APIs Azure:")
    print("- AZURE_VISION_ENDPOINT et AZURE_VISION_KEY pour Azure Computer Vision")
    print("- AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY et AZURE_TRANSLATOR_REGION pour la traduction")

if __name__ == '__main__':
    demonstrate_context_extraction()
