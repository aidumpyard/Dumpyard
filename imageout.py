from PIL import Image
import pytesseract

def extract_text_lines(image_path, output_txt_path):
    # Load image
    img = Image.open(image_path)

    # Use Tesseract to extract text
    full_text = pytesseract.image_to_string(img)

    # Split by lines
    lines = full_text.strip().split('\n')

    # Write each line to the output file
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        for line in lines:
            if line.strip():  # Skip empty lines
                f.write(line.strip() + '\n')

# Example usage
extract_text_lines("text_image.jpg", "output_text.txt")