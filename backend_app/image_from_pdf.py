import fitz
import io
from PIL import Image
from datetime import datetime
from backend_app.ocr_utils import OCRImgToText

class ImgExtractor:
    path: str

    def __init__(self, path):
        self.path = path

    def extract_images(self):

        pdf_file = fitz.open(self.path)
        for page_index in range(len(pdf_file)):
            
            page = pdf_file[page_index]
            image_list = page.getImageList()  
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print("[!] No images found on page", page_index)
            for image_index, img in enumerate(page.getImageList(), start=1):
                xref = img[0]
                base_image = pdf_file.extractImage(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image = Image.open(io.BytesIO(image_bytes))
                ocr = OCRImgToText(image)
                text = ocr.img_to_str()
                ## OCR utils
                image.save(open(f"./images/filename,{datetime.now()},{image_index},{text}.{image_ext}", "wb"))


