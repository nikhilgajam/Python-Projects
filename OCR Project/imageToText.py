import pytesseract as tess
# To download tesseract ocr https://github.com/UB-Mannheim/tesseract/wiki and locate exe
tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from PIL import Image

img = Image.open('text.png')
text = tess.image_to_string(img)

print(text)
