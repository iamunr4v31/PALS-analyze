import sys
import os
from dotenv import load_dotenv
from numpy.lib.npyio import load
import pytesseract
from PIL import Image

load_dotenv()

class OCRImgToText:
    path: str
    tesseract_path: str = os.environ.get("tesseract_path")

    def __init__(self, path):
        self.path = path
    
    def img_to_pdf(self, **kwargs):
        return pytesseract.image_to_string(Image.open(self.path), **kwargs)
    
    list_languages = lambda config: pytesseract.get_languages(config=config)