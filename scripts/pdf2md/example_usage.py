#!/usr/bin/env python3
"""
Exemple d'utilisation du convertisseur PDF vers Markdown avec descriptions contextualisées
"""

import os
from pdf2markdown import PDF2Markdown

def example_basic_conversion():
    """Exemple de conversion de base sans API Azure"""
    pdf_path = "example.pdf"  # Remplacez par votre fichier PDF
    
    if not os.path.exists(pdf_path):
        print(f"Fichier {pdf_path} non trouvé. Créez un PDF de test ou modifiez le chemin.")
        return
    
    # Conversion sans description d'images (pas d'API Azure configurée)
    converter = PDF2Markdown(pdf_path)
    markdown_content = converter.convert_to_markdown()
    
    # Sauvegarder le résultat
    output_path = pdf_path.replace('.pdf', '_basic.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Conversion de base terminée : {output_path}")

def example_with_azure_apis():
    """Exemple avec APIs Azure pour descriptions contextualisées"""
    pdf_path = "example.pdf"  # Remplacez par votre fichier PDF
    
    if not os.path.exists(pdf_path):
        print(f"Fichier {pdf_path} non trouvé. Créez un PDF de test ou modifiez le chemin.")
        return
    
    # Configuration Azure (remplacez par vos vraies clés)
    vision_endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    vision_key = os.getenv('AZURE_VISION_KEY')
    translator_endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    translator_key = os.getenv('AZURE_TRANSLATOR_KEY')
    translator_region = os.getenv('AZURE_TRANSLATOR_REGION')
    
    if not all([vision_endpoint, vision_key]):
        print("Variables d'environnement Azure Vision non configurées.")
        print("Configurez AZURE_VISION_ENDPOINT et AZURE_VISION_KEY pour activer les descriptions.")
        return
    
    # Conversion avec descriptions contextualisées
    converter = PDF2Markdown(
        pdf_path,
        vision_endpoint=vision_endpoint,
        vision_key=vision_key,
        translator_endpoint=translator_endpoint,
        translator_key=translator_key,
        translator_region=translator_region,
        wait_if_quota_reached=True  # Attendre si quota atteint
    )
    
    markdown_content = converter.convert_to_markdown()
    
    # Sauvegarder le résultat
    output_path = pdf_path.replace('.pdf', '_contextual.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Conversion avec contexte terminée : {output_path}")
    print(f"Images sauvegardées dans : {converter.assets_dir}")

def example_specific_pages():
    """Exemple de conversion de pages spécifiques"""
    pdf_path = "example.pdf"  # Remplacez par votre fichier PDF
    
    if not os.path.exists(pdf_path):
        print(f"Fichier {pdf_path} non trouvé. Créez un PDF de test ou modifiez le chemin.")
        return
    
    # Convertir seulement les pages 0, 1 et 2 (première, deuxième et troisième pages)
    converter = PDF2Markdown(pdf_path, pages=[0, 1, 2])
    markdown_content = converter.convert_to_markdown()
    
    # Sauvegarder le résultat
    output_path = pdf_path.replace('.pdf', '_pages_0_1_2.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Conversion des pages 0-2 terminée : {output_path}")

if __name__ == '__main__':
    print("=== Exemples d'utilisation du convertisseur PDF vers Markdown ===\n")
    
    print("1. Conversion de base (sans APIs Azure)")
    example_basic_conversion()
    
    print("\n2. Conversion avec descriptions contextualisées (APIs Azure)")
    example_with_azure_apis()
    
    print("\n3. Conversion de pages spécifiques")
    example_specific_pages()
    
    print("\n=== Terminé ===")
