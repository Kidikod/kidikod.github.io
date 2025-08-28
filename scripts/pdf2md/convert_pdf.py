import pymupdf4llm
import sys
from pathlib import Path

def convert_pdf_to_md(pdf_path, output_dir=None):
    """
    Convertit un fichier PDF en Markdown avec extraction des images
    
    Args:
        pdf_path (str): Chemin vers le fichier PDF source
        output_dir (str, optional): Dossier de sortie. Par défaut, utilise le même dossier que le PDF
    """
    if output_dir is None:
        output_dir = Path(pdf_path).parent
    
    # Créer le dossier assets s'il n'existe pas
    assets_dir = Path(output_dir) / 'assets'
    assets_dir.mkdir(exist_ok=True)
    
    print('Conversion du PDF...')
    md_text = pymupdf4llm.to_markdown(
        pdf_path,
        write_images=True,
        image_path=str(assets_dir)
    )
    
    # Créer le fichier Markdown
    output_file = Path(output_dir) / 'index.md'
    output_file.write_text(md_text, encoding='utf-8')
    print(f'Conversion terminée ! Fichier créé : {output_file}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python convert_pdf.py chemin/vers/fichier.pdf [dossier_sortie]")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    convert_pdf_to_md(pdf_path, output_dir)
