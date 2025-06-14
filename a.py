from ollama_ocr import OCRProcessor

# Initialize OCR processor
ocr = OCRProcessor(model_name='llama3.2-vision:11b-instruct-fp16')  # You can use any vision model available on Ollama
# you can pass your custom ollama api

# Process an image
result = ocr.process_image(
    image_path="./a.pdf", # path to your pdf files "path/to/your/file.pdf"
    format_type="markdown",  # Options: markdown, text, json, structured, key_value
    custom_prompt="Extract all text", # Optional custom prompt
    language="Vietnamese" # Specify the language of the text (New! 🆕)
)
print(result)

with open("result.md", "w", encoding="utf-8") as f:
    f.write(result)