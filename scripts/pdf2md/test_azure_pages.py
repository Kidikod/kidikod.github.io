#!/usr/bin/env python3
"""
Test du convertisseur avec les 3 premières pages de Plantamagotchi
et simulation des APIs Azure pour démonstration
"""

import os
import sys
sys.path.append('/workspaces/kidikod.github.io/scripts/pdf2md')

from pdf2markdown import PDF2Markdown

def test_with_simulated_azure():
    """Test avec APIs Azure simulées pour démonstration"""
    
    pdf_path = "/workspaces/kidikod.github.io/_scratch_tp/plantamagotchi/Plantamagotchi.pdf"
    output_path = "/workspaces/kidikod.github.io/_scratch_tp/plantamagotchi/test_azure.md"
    
    print("=== Test des 3 premières pages avec APIs Azure ===\n")
    
    # Pour cette démonstration, on va simuler la configuration Azure
    # En production, vous configureriez vos vraies clés Azure
    
    # Configuration simulée (remplacez par vos vraies valeurs)
    azure_config = {
        'vision_endpoint': os.getenv('AZURE_VISION_ENDPOINT', 'https://demo.cognitiveservices.azure.com/'),
        'vision_key': os.getenv('AZURE_VISION_KEY', 'demo_key_vision'),
        'translator_endpoint': os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com/'),
        'translator_key': os.getenv('AZURE_TRANSLATOR_KEY', 'demo_key_translator'),
        'translator_region': os.getenv('AZURE_TRANSLATOR_REGION', 'westeurope')
    }
    
    print("Configuration Azure détectée :")
    for key, value in azure_config.items():
        masked_value = "***" + value[-4:] if len(value) > 4 else "***"
        print(f"  {key}: {masked_value}")
    print()
    
    # Test d'abord sans Azure pour voir la différence
    print("1. Test SANS Azure (pour comparaison)...")
    converter_basic = PDF2Markdown(pdf_path, pages=[0, 1, 2])
    
    # Extraction du contexte pour démonstration
    context_map = converter_basic.extract_text_context_around_images()
    print(f"   Contexte extrait pour {len(context_map)} pages")
    
    # Afficher un échantillon du contexte
    for page_num in sorted(context_map.keys())[:3]:
        context = context_map[page_num]
        keywords = converter_basic.extract_keywords_from_context(context)
        preview = context[:100] + "..." if len(context) > 100 else context
        print(f"   Page {page_num}: {len(keywords)} mots-clés trouvés: {keywords[:3]}")
        print(f"   Contexte: {preview}")
        print()
    
    # Conversion sans Azure
    print("   Conversion en cours...")
    markdown_basic = converter_basic.convert_to_markdown()
    
    # Sauvegarder la version sans Azure
    basic_output = output_path.replace('.md', '_sans_azure.md')
    with open(basic_output, 'w', encoding='utf-8') as f:
        f.write(markdown_basic)
    print(f"   Résultat sauvé : {basic_output}")
    print()
    
    # Test avec Azure si configuré
    if all(azure_config.values()) and not any('demo' in str(v) for v in azure_config.values()):
        print("2. Test AVEC Azure...")
        converter_azure = PDF2Markdown(
            pdf_path,
            pages=[0, 1, 2],
            vision_endpoint=azure_config['vision_endpoint'],
            vision_key=azure_config['vision_key'],
            translator_endpoint=azure_config['translator_endpoint'],
            translator_key=azure_config['translator_key'],
            translator_region=azure_config['translator_region'],
            wait_if_quota_reached=True
        )
        
        print("   Conversion avec descriptions Azure en cours...")
        markdown_azure = converter_azure.convert_to_markdown()
        
        # Sauvegarder la version avec Azure
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_azure)
        print(f"   Résultat avec Azure sauvé : {output_path}")
        
        # Comparer les résultats
        print("\n3. Comparaison des résultats...")
        basic_images = markdown_basic.count('![')
        azure_images = markdown_azure.count('![')
        
        print(f"   Images trouvées (sans Azure): {basic_images}")
        print(f"   Images trouvées (avec Azure): {azure_images}")
        
        # Chercher des exemples de descriptions améliorées
        basic_lines = markdown_basic.split('\n')
        azure_lines = markdown_azure.split('\n')
        
        for i, (basic_line, azure_line) in enumerate(zip(basic_lines, azure_lines)):
            if basic_line.startswith('![') and azure_line.startswith('!['):
                if basic_line != azure_line:
                    print(f"\n   Exemple de différence (ligne {i+1}):")
                    print(f"   Sans Azure: {basic_line}")
                    print(f"   Avec Azure: {azure_line}")
                    break
    else:
        print("2. APIs Azure non configurées avec de vraies clés.")
        print("   Pour tester avec Azure, configurez les variables d'environnement :")
        print("   - AZURE_VISION_ENDPOINT et AZURE_VISION_KEY")
        print("   - AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY et AZURE_TRANSLATOR_REGION")
        print()
        print("   Exemple de configuration :")
        print("   export AZURE_VISION_ENDPOINT='https://votre-region.cognitiveservices.azure.com/'")
        print("   export AZURE_VISION_KEY='votre_clé_vision'")
        print("   # ... etc")
    
    print("\n=== Test terminé ===")
    print(f"Vérifiez les fichiers générés dans : {os.path.dirname(output_path)}")

if __name__ == '__main__':
    test_with_simulated_azure()
