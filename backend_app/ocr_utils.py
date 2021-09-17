import sys
import os
from dotenv import load_dotenv
from numpy.lib.npyio import load
import pytesseract
from PIL import Image

load_dotenv()

class OCRImgToText:
    image: Image
    tesseract_path: str = os.environ.get("tesseract_path")

    def __init__(self, image):
        self.image = image
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
    
    def img_to_str(self, **kwargs):
        return pytesseract.image_to_string(self.image, **kwargs)
    
    list_languages = lambda config: pytesseract.get_languages(config=config)