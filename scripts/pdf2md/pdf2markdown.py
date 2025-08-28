#!/usr/bin/env python3
import os
import glob
import json
import time
import re
from datetime import datetime
from typing import Optional, Dict, List, Tuple
import pymupdf4llm
import fitz  # PyMuPDF
import requests
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

class AzureQuota:
    """Gère le quota d'utilisation des APIs Azure"""
    def __init__(self, quota_file: str, monthly_limit: int, rate_limit: int, time_unit: str = 'minute',
                 wait_if_quota_reached: bool = False):
        """
        Initialise le gestionnaire de quota
        Args:
            quota_file: Chemin vers le fichier de sauvegarde du quota
            monthly_limit: Limite mensuelle de requêtes
            rate_limit: Nombre maximum de requêtes par unité de temps
            time_unit: Unité de temps pour le rate limit ('second' ou 'minute')
            wait_if_quota_reached: Si True, attend que le quota soit à nouveau disponible au lieu de retourner False
        """
        self.quota_file = quota_file
        self.monthly_limit = monthly_limit
        self.rate_limit = rate_limit
        self.time_unit = time_unit
        self.wait_if_quota_reached = wait_if_quota_reached
        self.load_quota()
    
    def load_quota(self):
        """Charge l'état du quota depuis le fichier"""
        if os.path.exists(self.quota_file):
            with open(self.quota_file, 'r') as f:
                data = json.load(f)
                self.monthly_count = data.get('monthly_count', 0)
                self.last_reset = datetime.fromisoformat(data.get('last_reset', datetime.now().isoformat()))
                self.time_counts = data.get('time_counts', [])
        else:
            self.monthly_count = 0
            self.last_reset = datetime.now()
            self.time_counts = []
    
    def save_quota(self):
        """Sauvegarde l'état du quota dans le fichier"""
        data = {
            'monthly_count': self.monthly_count,
            'last_reset': self.last_reset.isoformat(),
            'time_counts': self.time_counts
        }
        with open(self.quota_file, 'w') as f:
            json.dump(data, f)
    
    def can_make_request(self) -> bool:
        """Vérifie si une nouvelle requête est possible"""
        while True:
            now = datetime.now()
            
            # Réinitialisation mensuelle
            if now.month != self.last_reset.month or now.year != self.last_reset.year:
                self.monthly_count = 0
                self.last_reset = now
                self.time_counts = []
            
            # Vérification du quota mensuel
            if self.monthly_count >= self.monthly_limit:
                if not self.wait_if_quota_reached:
                    return False
                # Attendre jusqu'au début du mois prochain
                time_to_next_month = (datetime(now.year + (now.month == 12), 
                                             (now.month % 12) + 1, 1) - now).total_seconds()
                time.sleep(time_to_next_month)
                continue
            
            # Format du timestamp selon l'unité de temps
            if self.time_unit == 'second':
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            else:  # minute
                current_time = now.strftime("%Y-%m-%d %H:%M")
            
            # Mise à jour des compteurs
            self.time_counts = [count for count in self.time_counts 
                            if count['time'] == current_time]
            
            if not self.time_counts:
                self.time_counts.append({'time': current_time, 'count': 0})
                return True
            
            # Vérification de la limite par unité de temps
            if self.time_counts[0]['count'] >= self.rate_limit:
                if not self.wait_if_quota_reached:
                    return False
                # Attendre jusqu'à la prochaine unité de temps
                if self.time_unit == 'second':
                    time.sleep(1)
                else:  # minute
                    time.sleep(60 - now.second)
                continue
            
            return True
    
    def increment(self, count: int = 1):
        """Incrémente les compteurs après une requête réussie"""
        self.monthly_count += count
        if self.time_counts:
            self.time_counts[0]['count'] += count
        self.save_quota()

class PDF2Markdown:
    def __init__(self, pdf_path: str, pages: Optional[list] = None, 
                 vision_endpoint: Optional[str] = None, vision_key: Optional[str] = None,
                 translator_endpoint: Optional[str] = None, translator_key: Optional[str] = None, 
                 translator_region: Optional[str] = None, wait_if_quota_reached: bool = False):
        """
        Initialise le convertisseur PDF vers Markdown
        Args:
            pdf_path: Chemin vers le fichier PDF à convertir
            pages: Liste des numéros de pages à convertir (0-based, optionnel)
            vision_endpoint: Point d'entrée de l'API Azure Vision (optionnel)
            vision_key: Clé API Azure Vision (optionnel)
            translator_endpoint: Point d'entrée de l'API Azure Translator (optionnel)
            translator_key: Clé API Azure Translator (optionnel)
            translator_region: Région Azure Translator (optionnel)
            wait_if_quota_reached: Si True, attend que le quota soit à nouveau disponible au lieu d'échouer
        """
        self.pdf_path = pdf_path
        self.output_dir = os.path.dirname(pdf_path)
        self.assets_dir = os.path.join(self.output_dir, "assets")
        self.ensure_dirs()
        
        # Initialiser la liste des pages
        self.pages = pages
        
        # Configuration Azure Vision
        self.vision_endpoint = vision_endpoint
        self.vision_key = vision_key
        
        # Configuration Azure Translator
        self.translator_endpoint = translator_endpoint
        self.translator_key = translator_key
        self.translator_region = translator_region
        
        # Initialiser le client Azure Vision s'il est configuré
        if self.vision_endpoint and self.vision_key:
            self.vision_client = ComputerVisionClient(
                self.vision_endpoint,
                CognitiveServicesCredentials(self.vision_key)
            )
            # Initialiser le quota pour Vision (5000 requêtes/mois, 20 requêtes/minute)
            self.vision_quota = AzureQuota(".azure_vision_quota.json", 5000, 20, 'minute', 
                                         wait_if_quota_reached=wait_if_quota_reached)
        else:
            self.vision_client = None
            self.vision_quota = None
            print("ATTENTION: Azure Vision non configuré. Les images n'auront pas de descriptions.")
            print("Pour activer les descriptions, définissez AZURE_VISION_ENDPOINT et AZURE_VISION_KEY")
        
        # Vérifier la configuration du Translator
        if not all([self.translator_endpoint, self.translator_key, self.translator_region]):
            print("ATTENTION: Azure Translator non configuré. Les descriptions ne seront pas traduites.")
            print("Pour activer la traduction, définissez AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY et AZURE_TRANSLATOR_REGION")
            self.translator_quota = None
        else:
            # Initialiser le quota pour Translator (2M caractères/mois, 5 requêtes/seconde)
            self.translator_quota = AzureQuota(".azure_translator_quota.json", 2000000, 5, 'second',
                                             wait_if_quota_reached=wait_if_quota_reached)
        
    def ensure_dirs(self):
        """Crée le dossier assets s'il n'existe pas"""
        if not os.path.exists(self.assets_dir):
            os.makedirs(self.assets_dir)

    def extract_text_context_around_images(self) -> Dict[int, str]:
        """
        Extrait le contexte textuel autour de chaque image dans le PDF
        Returns:
            Dictionnaire {page_num: context_text} pour chaque page contenant des images
        """
        context_map = {}
        
        try:
            # Ouvrir le PDF avec PyMuPDF
            doc = fitz.open(self.pdf_path)
            
            for page_num in range(len(doc)):
                # Filtrer par pages si spécifié
                if self.pages is not None and page_num not in self.pages:
                    continue
                    
                page = doc[page_num]
                
                # Vérifier s'il y a des images sur cette page
                image_list = page.get_images()
                if not image_list:
                    continue
                
                # Extraire tout le texte de la page
                page_text = page.get_text()
                
                # Nettoyer et normaliser le texte
                cleaned_text = re.sub(r'\s+', ' ', page_text).strip()
                
                # Stocker le contexte pour cette page
                if cleaned_text:
                    context_map[page_num] = cleaned_text
                    
            doc.close()
            
        except Exception as e:
            print(f"Erreur lors de l'extraction du contexte textuel : {e}")
            
        return context_map

    def get_image_context_from_position(self, page_num: int, image_bbox: Tuple[float, float, float, float], 
                                      page_text_blocks: List[Dict]) -> str:
        """
        Extrait le texte contextuellement proche d'une image basé sur sa position
        Args:
            page_num: Numéro de la page
            image_bbox: Boîte englobante de l'image (x0, y0, x1, y1)
            page_text_blocks: Liste des blocs de texte avec leurs positions
        Returns:
            Texte contextuellement proche de l'image
        """
        if not page_text_blocks:
            return ""
            
        x0, y0, x1, y1 = image_bbox
        image_center_x = (x0 + x1) / 2
        image_center_y = (y0 + y1) / 2
        
        # Calculer la distance de chaque bloc de texte par rapport à l'image
        nearby_texts = []
        
        for block in page_text_blocks:
            if block.get('type') == 0:  # Type 0 = bloc de texte
                bbox = block['bbox']
                block_center_x = (bbox[0] + bbox[2]) / 2
                block_center_y = (bbox[1] + bbox[3]) / 2
                
                # Calculer la distance euclidienne
                distance = ((image_center_x - block_center_x) ** 2 + 
                           (image_center_y - block_center_y) ** 2) ** 0.5
                
                text_content = block.get('text', '').strip()
                if text_content:
                    nearby_texts.append((distance, text_content))
        
        # Trier par distance et prendre les 3 blocs les plus proches
        nearby_texts.sort(key=lambda x: x[0])
        context_texts = [text for _, text in nearby_texts[:3]]
        
    def get_detailed_image_context(self) -> Dict[str, str]:
        """
        Extrait un contexte détaillé pour chaque image basé sur sa position exacte
        Returns:
            Dictionnaire {image_identifier: context_text}
        """
        context_map = {}
        
        try:
            doc = fitz.open(self.pdf_path)
            
            for page_num in range(len(doc)):
                # Filtrer par pages si spécifié
                if self.pages is not None and page_num not in self.pages:
                    continue
                    
                page = doc[page_num]
                
                # Obtenir les images et leurs positions
                image_list = page.get_images(full=True)
                if not image_list:
                    continue
                
                # Obtenir les blocs de texte avec leurs positions
                text_blocks = page.get_text("dict")["blocks"]
                
                for img_index, img in enumerate(image_list):
                    # Obtenir la position de l'image
                    img_rects = page.get_image_rects(img[0])
                    if img_rects:
                        img_rect = img_rects[0]
                        
                        # Identifier l'image
                        img_identifier = f"page_{page_num}_img_{img_index}"
                        
                        # Extraire le contexte proche
                        context = self.get_image_context_from_position(
                            page_num, 
                            (img_rect.x0, img_rect.y0, img_rect.x1, img_rect.y1),
                            text_blocks
                        )
                        
                        if context:
                            context_map[img_identifier] = context
                            
            doc.close()
            
        except Exception as e:
            print(f"Erreur lors de l'extraction du contexte détaillé : {e}")
            
        return context_map

    def create_contextual_description(self, base_description: str, context_text: str) -> str:
        """
        Crée une description plus contextualisée en combinant la description de base
        et le contexte textuel
        Args:
            base_description: Description de base de l'image
            context_text: Contexte textuel autour de l'image
        Returns:
            Description contextualisée améliorée
        """
        if not context_text or not base_description:
            return base_description
        
        # Analyser le contexte pour extraire des mots-clés pertinents
        context_keywords = self.extract_keywords_from_context(context_text)
        
        # Si on trouve des mots-clés pertinents, enrichir la description
        if context_keywords:
            keywords_str = ", ".join(context_keywords[:3])  # Limiter à 3 mots-clés
            enhanced_description = f"{base_description} (en relation avec : {keywords_str})"
            return enhanced_description
        
        return base_description

    def extract_keywords_from_context(self, context_text: str) -> List[str]:
        """
        Extrait des mots-clés pertinents du contexte textuel
        Args:
            context_text: Texte du contexte
        Returns:
            Liste des mots-clés pertinents
        """
        if not context_text:
            return []
        
        # Mots-clés techniques et éducatifs courants
        technical_keywords = [
            'algorithme', 'programme', 'code', 'fonction', 'variable', 'boucle',
            'condition', 'scratch', 'python', 'javascript', 'html', 'css',
            'données', 'tableau', 'liste', 'graphique', 'diagramme', 'schéma',
            'étape', 'processus', 'méthode', 'résultat', 'exemple', 'exercice',
            'problème', 'solution', 'calcul', 'formule', 'équation'
        ]
        
        # Convertir en minuscules pour la recherche
        context_lower = context_text.lower()
        
        # Rechercher les mots-clés présents
        found_keywords = []
        for keyword in technical_keywords:
            if keyword in context_lower:
                found_keywords.append(keyword)
        
        # Également extraire des mots qui semblent importants (commencent par une majuscule)
        words = context_text.split()
        important_words = [word.strip('.,!?;:') for word in words 
                          if len(word) > 3 and word[0].isupper() and word.isalpha()]
        
        # Combiner et limiter
        all_keywords = found_keywords + important_words[:2]
        return list(set(all_keywords))  # Supprimer les doublons

    def translate_text(self, text: str) -> str:
        """
        Traduit un texte de l'anglais vers le français en utilisant Azure Translator
        Args:
            text: Texte à traduire
        Returns:
            Texte traduit en français
        """
        if not self.translator_quota or not text:
            return text
            
        # Vérifier le quota
        if not self.translator_quota.can_make_request():
            print(f"Quota Azure Translator atteint. Texte non traduit : {text}")
            return text
            
        try:
            # Préparer la requête
            url = f"{self.translator_endpoint}/translate"
            params = {
                'api-version': '3.0',
                'from': 'en',
                'to': 'fr'
            }
            headers = {
                'Ocp-Apim-Subscription-Key': self.translator_key,
                'Ocp-Apim-Subscription-Region': self.translator_region,
                'Content-type': 'application/json'
            }
            body = [{'text': text}]
            
            # Faire la requête
            response = requests.post(url, params=params, headers=headers, json=body)
            response.raise_for_status()
            
            # Incrémenter le quota (nombre de caractères)
            self.translator_quota.increment(len(text))
            
            # Extraire la traduction
            translations = response.json()
            if translations and len(translations) > 0:
                return translations[0]['translations'][0]['text']
            
            return text
            
        except Exception as e:
            print(f"Erreur lors de la traduction : {e}")
            return text
            
    def analyze_image(self, image_path: str, context_text: str = "") -> str:
        """
        Analyse une image en utilisant Azure Computer Vision avec contexte textuel
        Args:
            image_path: Chemin vers l'image à analyser
            context_text: Texte du contexte autour de l'image pour améliorer la description
        Returns:
            Description de l'image en français, contextualisée
        """
        # Si Azure Vision n'est pas configuré, retourner une chaîne vide
        if not self.vision_client:
            return ""
            
        try:
            # Vérifier le quota Vision
            if not self.vision_quota.can_make_request():
                print(f"Quota Azure Vision atteint pour {image_path}. Description ignorée.")
                return ""
            
            # Ouvrir l'image en mode binaire
            with open(image_path, "rb") as image_file:
                # Analyser l'image avec le client
                features = [VisualFeatureTypes.description, VisualFeatureTypes.tags, VisualFeatureTypes.objects]
                results = self.vision_client.analyze_image_in_stream(
                    image_file,
                    features,
                    language="en"  # Utiliser l'anglais pour de meilleurs résultats
                )
                
                # Incrémenter le quota Vision
                self.vision_quota.increment()
                
                # Construire une description contextualisée
                description_parts = []
                
                # Description principale
                if len(results.description.captions) > 0:
                    main_description = results.description.captions[0].text
                    description_parts.append(main_description)
                
                # Ajouter les tags pertinents si disponibles
                if results.tags:
                    relevant_tags = [tag.name for tag in results.tags[:5] if tag.confidence > 0.7]
                    if relevant_tags:
                        tags_text = ", ".join(relevant_tags)
                        description_parts.append(f"Tags: {tags_text}")
                
                # Créer la description finale
                if description_parts:
                    base_description = ". ".join(description_parts)
                    
                    # Créer une description contextualisée
                    if context_text:
                        enhanced_description = self.create_contextual_description(base_description, context_text)
                        # Traduire la description améliorée en français
                        return self.translate_text(enhanced_description)
                    else:
                        # Traduire la description de base en français
                        return self.translate_text(base_description)
                
                return ""
                
        except Exception as e:
            print(f"Erreur lors de l'analyse de l'image {image_path}: {e}")
            return ""
            
    def convert_to_markdown(self) -> str:
        """
        Convertit le PDF en Markdown en utilisant pymupdf4llm
        avec extraction automatique des images et contexte textuel
        Returns:
            Contenu Markdown
        """
        # Extraire le contexte textuel autour des images
        print("Extraction du contexte textuel des images...")
        context_map = self.extract_text_context_around_images()
        
        # Obtenir le nom du fichier PDF sans le chemin
        pdf_basename = os.path.basename(self.pdf_path)
        
        # Préparer les paramètres de conversion
        conversion_params = {
            'write_images': True
        }
        
        # Ajouter la liste des pages si spécifiée
        if self.pages is not None:
            conversion_params['pages'] = self.pages
            
        # Convertir le PDF en markdown avec extraction des images
        print("Conversion du PDF en Markdown...")
        markdown_text = pymupdf4llm.to_markdown(
            self.pdf_path,
            **conversion_params
        )
        
        # Traiter les images générées et leurs descriptions
        current_dir = os.getcwd()
        image_files = glob.glob(f"{pdf_basename}-*.png")
        
        print(f"Traitement de {len(image_files)} images...")
        
        for img_path in image_files:
            # Extraire le numéro de page à partir du nom de fichier
            # Format attendu : filename-page_num-img_num.png
            match = re.search(r'-(\d+)-\d+\.png$', img_path)
            page_num = int(match.group(1)) if match else 0
            
            new_name = img_path.replace(f"{pdf_basename}-", "image_")
            new_path = os.path.join(self.assets_dir, new_name)
            os.rename(os.path.join(current_dir, img_path), new_path)
            
            # Obtenir le contexte textuel pour cette page
            context_text = context_map.get(page_num, "")
            
            # Analyser l'image avec le contexte et obtenir une description
            print(f"Analyse de l'image {new_name} avec contexte...")
            description = self.analyze_image(new_path, context_text)
            
            # Mettre à jour le chemin dans le markdown
            base_dir = os.path.dirname(self.pdf_path)
            relative_assets = os.path.relpath(self.assets_dir, base_dir)
            
            # Mettre à jour le chemin dans le markdown et ajouter la description
            markdown_text = markdown_text.replace(
                f"![]({img_path})",
                f"![{description}]({os.path.join(relative_assets, new_name)})"
            )
        
        print("Conversion terminée !")
        return markdown_text

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Convertit un PDF en Markdown')
    parser.add_argument('pdf_path', help='Chemin vers le fichier PDF')
    parser.add_argument('--output', '-o', help='Chemin du fichier markdown de sortie')
    parser.add_argument('--vision-endpoint', 
                       help='Point d\'entrée Azure Vision (ou utilisez AZURE_VISION_ENDPOINT)')
    parser.add_argument('--vision-key', 
                       help='Clé API Azure Vision (ou utilisez AZURE_VISION_KEY)')
    parser.add_argument('--translator-endpoint',
                       help='Point d\'entrée Azure Translator (ou utilisez AZURE_TRANSLATOR_ENDPOINT)')
    parser.add_argument('--translator-key',
                       help='Clé API Azure Translator (ou utilisez AZURE_TRANSLATOR_KEY)')
    parser.add_argument('--translator-region',
                       help='Région Azure Translator (ou utilisez AZURE_TRANSLATOR_REGION)')
    parser.add_argument('--pages', '-p', type=int, nargs='+',
                       help='Liste des numéros de pages à convertir (commence à 0)')
    parser.add_argument('--wait-if-quota-reached', action='store_true',
                       help='Attendre au lieu d\'échouer quand les quotas sont atteints')
    
    args = parser.parse_args()
    
    # Créer le chemin de sortie s'il n'est pas spécifié
    if not args.output:
        args.output = os.path.splitext(args.pdf_path)[0] + '.md'
    
    # Récupérer les paramètres Azure Vision (arguments ou variables d'environnement)
    vision_endpoint = args.vision_endpoint or os.getenv('AZURE_VISION_ENDPOINT')
    vision_key = args.vision_key or os.getenv('AZURE_VISION_KEY')
    
    # Récupérer les paramètres Azure Translator (arguments ou variables d'environnement)
    translator_endpoint = args.translator_endpoint or os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    translator_key = args.translator_key or os.getenv('AZURE_TRANSLATOR_KEY')
    translator_region = args.translator_region or os.getenv('AZURE_TRANSLATOR_REGION')
    
    # Convertir le PDF
    converter = PDF2Markdown(
        args.pdf_path,
        pages=args.pages,
        vision_endpoint=vision_endpoint,
        vision_key=vision_key,
        translator_endpoint=translator_endpoint,
        translator_key=translator_key,
        translator_region=translator_region,
        wait_if_quota_reached=args.wait_if_quota_reached
    )
    markdown_content = converter.convert_to_markdown()
    
    # Sauvegarder le résultat
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"Conversion terminée. Fichier markdown créé : {args.output}")
    print(f"Les images ont été extraites dans : {converter.assets_dir}")

if __name__ == '__main__':
    main()
