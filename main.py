import os
from pathlib import Path
import subprocess
from pdf2image import convert_from_path
import PyPDF2
from pdf_to_pages import pdf_to_images
from converter_surya_hocr import convert_surya_result_to_hocr
from hocr_to_pdf import convert_hocr_to_pdf
import argparse

def ensure_directory(path):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def run_surya_ocr(pdf_name, surya_path="surya_ocr"):
    """Run Surya OCR on the PDF file"""
    try:
        # Run surya command
        result = subprocess.run(
            ["RECOGNITION_BATCH_SIZE=16", surya_path, pdf_name],
            check=True,
        )
        print(f"Surya OCR completed successfully for {pdf_name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running Surya OCR: {str(e)}")
        return False
    except FileNotFoundError:
        print(f"Error: Surya command not found at {surya_path}")
        return False

def combine_pdfs(input_folder, output_path):
    """Combine multiple PDFs into a single PDF"""
    merger = PyPDF2.PdfMerger()
    
    # Get all PDF files and sort them by page number
    pdf_files = sorted(
        [f for f in os.listdir(input_folder) if f.endswith('.pdf')],
        key=lambda x: int(x.split('page')[1].split('.')[0])
    )
    
    # Add each PDF to the merger
    for pdf_file in pdf_files:
        file_path = os.path.join(input_folder, pdf_file)
        merger.append(file_path)
    
    # Write the combined PDF
    merger.write(output_path)
    merger.close()
    print(f"Combined PDF saved to {output_path}")

def process_pdf(pdf_path):
    """Process a PDF file through OCR pipeline"""
    # Get PDF name without extension
    pdf_name = Path(pdf_path).stem
    
    # Create necessary directories
    output_dir = Path('./output_pages') / pdf_name
    temp_dir = Path('./temp') / pdf_name
    output_pdf_dir = Path('./output_pdf_pages') / pdf_name
    ensure_directory(output_dir)
    ensure_directory(temp_dir)
    ensure_directory(output_pdf_dir)
    
    # Step 1: Convert PDF to images
    print(f"Converting PDF to images...")
    num_pages = pdf_to_images(pdf_path)
    if num_pages == 0:
        print("Failed to convert PDF to images")
        return
    
    # Step 2: Run Surya OCR
    print(f"Running Surya OCR...")
    if not run_surya_ocr(pdf_path):
        print("Surya OCR processing failed")
        return
    
    # Step 3: Convert Surya results to HOCR
    print(f"Converting Surya results to HOCR...")
    surya_result_file = f"results/surya/{pdf_name}/results.json"
    target_bbox = [0, 0, 2480, 3360]  # Standard dimensions
    convert_surya_result_to_hocr(surya_result_file, pdf_name, target_bbox, str(temp_dir))
    
    # Step 4: Convert each page's HOCR to PDF
    print(f"Converting HOCR to PDF for each page...")
    for i in range(num_pages):
        hocr_file = temp_dir / f"page{i}.hocr"
        img_file = output_dir / f"page{i+1}.png"
        output_pdf = output_pdf_dir / f"page{i+1}.pdf"
        
        if hocr_file.exists() and img_file.exists():
            convert_hocr_to_pdf(str(hocr_file), str(img_file), str(output_pdf))
    
    # Step 5: Combine all PDFs
    print(f"Combining PDFs...")
    final_pdf = Path('./output_pdf_pages') / f"{pdf_name}_final.pdf"
    combine_pdfs(str(output_pdf_dir), str(final_pdf))
    
    print(f"Processing complete! Final PDF saved as: {final_pdf}")

def main():
    parser = argparse.ArgumentParser(description='Process PDF through OCR pipeline')
    parser.add_argument('pdf_path', help='Path to the PDF file to process')
    args = parser.parse_args()
    
    if not os.path.exists(args.pdf_path):
        print(f"Error: PDF file '{args.pdf_path}' not found")
        return
    
    process_pdf(args.pdf_path)

if __name__ == "__main__":
    import os
    os.environ["RECOGNITION_BATCH_SIZE"] = "16"
    from time import time
    start_time = time()
    print("Starting PDF processing...")
    main()
    end_time = time()
    print(f"Total processing time: {end_time - start_time:.2f} seconds")
    print("PDF processing completed.")
