import pytesseract
from PIL import Image
import pandas as pd

# Load the image
image_path = "/mnt/data/IMG_6741.jpeg"
image = Image.open(image_path)

# Extract text from the image
extracted_text = pytesseract.image_to_string(image)

# Display extracted text for analysis
extracted_text