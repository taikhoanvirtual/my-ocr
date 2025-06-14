import os
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image
import numpy as np

def pdf_to_images(pdf_path):
    # Create output directory based on PDF filename
    pdf_name = Path(pdf_path).stem
    output_dir = Path('./output_pages') / pdf_name
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Convert PDF to images with higher DPI for better quality
        pages = convert_from_path(pdf_path, dpi= 300, fmt='png', use_cropbox=True)
        
        # Save each page as PNG
        for i, page in enumerate(pages, start=1):
            
            image_path = output_dir / f'page{i}.png'
            page.save(str(image_path), 'PNG')
            print(f'Saved page {i} to {image_path}')
            
        return len(pages)
    
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return 0

if __name__ == "__main__":
    # Example usage with the PDF files in the current directory
    pdf_files = ["a.pdf", "b.pdf"]
    
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            print(f"\nProcessing {pdf_file}...")
            num_pages = pdf_to_images(pdf_file)
            print(f"Successfully converted {num_pages} pages from {pdf_file}")
        else:
            print(f"File {pdf_file} not found")