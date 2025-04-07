from PIL import Image

def image_to_text(image_path, output_txt_path):
    # Open the image
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Ensure it's in RGB mode

        width, height = img.size

        with open(output_txt_path, 'w') as f:
            for y in range(height):
                line = []
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    line.append(f"({r},{g},{b})")
                f.write(' '.join(line) + '\n')

# Example usage
image_to_text("example.jpg", "image_data.txt")