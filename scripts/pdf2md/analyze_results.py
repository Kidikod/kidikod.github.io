#!/usr/bin/env python3
"""
Script d'analyse des résultats de conversion avec et sans Azure
"""

import os
import re

def analyze_conversion_results():
    """Analyse et compare les résultats de conversion"""
    
    base_dir = "/workspaces/kidikod.github.io/_scratch_tp/plantamagotchi"
    
    files_to_analyze = {
        "Sans Azure": f"{base_dir}/test_pages_0_1_2_azure_sans_azure.md",
        "Avec Azure": f"{base_dir}/test_pages_0_1_2_azure.md",
        "Direct Azure": f"{base_dir}/test_direct_azure.md"
    }
    
    print("=== Analyse des Résultats de Conversion ===\n")
    
    results = {}
    
    for version, file_path in files_to_analyze.items():
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Analyser le contenu
            results[version] = analyze_markdown_content(content)
            
        else:
            print(f"❌ Fichier non trouvé : {file_path}")
    
    # Afficher les résultats
    print("📊 Statistiques de Conversion :\n")
    
    headers = ["Version", "Images", "Descriptions", "Contexte", "Mots-clés", "Taille"]
    print(f"{'Version':<15} {'Images':<8} {'Descriptions':<12} {'Contexte':<10} {'Mots-clés':<10} {'Taille (KB)':<12}")
    print("-" * 75)
    
    for version, data in results.items():
        size_kb = data['size'] / 1024
        print(f"{version:<15} {data['images']:<8} {data['described']:<12} {data['with_context']:<10} {data['keywords']:<10} {size_kb:<12.1f}")
    
    # Exemples de descriptions
    print("\n🎯 Exemples de Descriptions :\n")
    
    for version, file_path in files_to_analyze.items():
        if os.path.exists(file_path):
            print(f"**{version}** :")
            show_image_examples(file_path)
            print()
    
    # Analyse de la qualité
    print("📈 Analyse de la Qualité :\n")
    
    if "Sans Azure" in results and "Avec Azure" in results:
        sans_azure = results["Sans Azure"]
        avec_azure = results["Avec Azure"]
        
        improvement = {
            'descriptions': avec_azure['described'] - sans_azure['described'],
            'contexte': avec_azure['with_context'] - sans_azure['with_context'],
            'mots_cles': avec_azure['keywords'] - sans_azure['keywords']
        }
        
        print(f"✅ Améliorations avec Azure :")
        print(f"   - Descriptions ajoutées : +{improvement['descriptions']}")
        print(f"   - Images avec contexte : +{improvement['contexte']}")
        print(f"   - Mots-clés détectés : +{improvement['mots_cles']}")
        
        if improvement['descriptions'] > 0:
            print(f"   - Taux de description : {avec_azure['described']/avec_azure['images']*100:.1f}%")

def analyze_markdown_content(content):
    """Analyse le contenu markdown et retourne des statistiques"""
    
    # Compter les images
    image_pattern = r'!\[([^\]]*)\]\([^)]+\)'
    images = re.findall(image_pattern, content)
    total_images = len(images)
    
    # Compter les descriptions non vides
    described_images = len([desc for desc in images if desc.strip()])
    
    # Compter les images avec contexte (contiennent "en relation avec")
    with_context = len([desc for desc in images if "en relation avec" in desc])
    
    # Compter les mots-clés uniques mentionnés
    keywords_pattern = r'en relation avec : ([^)]+)'
    all_keywords = re.findall(keywords_pattern, content)
    unique_keywords = set()
    for keyword_list in all_keywords:
        keywords = [k.strip() for k in keyword_list.split(',')]
        unique_keywords.update(keywords)
    
    return {
        'images': total_images,
        'described': described_images,
        'with_context': with_context,
        'keywords': len(unique_keywords),
        'size': len(content.encode('utf-8'))
    }

def show_image_examples(file_path, max_examples=2):
    """Affiche des exemples d'images du fichier"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    image_pattern = r'!\[([^\]]*)\]\([^)]+\)'
    images = re.findall(image_pattern, content)
    
    count = 0
    for desc in images:
        if count >= max_examples:
            break
        
        if desc.strip():
            # Limiter la longueur de l'affichage
            display_desc = desc[:100] + "..." if len(desc) > 100 else desc
            print(f"   • {display_desc}")
        else:
            print(f"   • (pas de description)")
        
        count += 1

if __name__ == '__main__':
    analyze_conversion_results()
