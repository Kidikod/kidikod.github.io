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
    import argparse
    
    parser = argparse.ArgumentParser(description='Applique les descriptions aux images dans un fichier Markdown')
    parser.add_argument('file', nargs='?', default='index.md', help='Fichier Markdown à traiter')
    parser.add_argument('--list-missing', action='store_true', help='Liste les images sans description')
    
    args = parser.parse_args()
    
    updated, missing = apply_descriptions(args.file)
    print(f"{updated} descriptions appliquées")
    
    if args.list_missing and missing:
        print("\nImages sans description :")
        for img in missing:
            print(f"- {img}")
