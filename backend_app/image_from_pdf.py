import fitz
from csv import DictWriter
from os.path import isfile
import io
from PIL import Image
from datetime import datetime
from backend_app.ocr_utils import OCRImgToText

class ImgExtractor:
    path: str

    def __init__(self, path):
        self.path = path
        self.file = self.path.split("/")[-1].split(".")[0]

    def extract_images(self):

        pdf_file = fitz.open(self.path)
        img_idx = 0 

        csv_writer = []
        for page_index in range(len(pdf_file)):
            
            page = pdf_file[page_index]
            image_list = page.getImageList() 
            if image_list:
                print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
            else:
                print("[!] No images found on page", page_index)
            for image_index, img in enumerate(image_list, start=1):
                print(img)
                xref = img[0]
                base_image = pdf_file.extractImage(xref)
                image_bytes = base_image["image"]
                image_ext = "jpeg"
                image = Image.open(io.BytesIO(image_bytes))
                ocr = OCRImgToText(image)
                text = ocr.img_to_str().strip()
                text = " ".join(text.split("\n"))
                dt = datetime.now().strftime("%d%m%Y")

                csv_writer.append({
                    "filename": self.file,
                    "date": dt,
                    "lineno": img_idx,
                    "text": text
                    })

                filenm = filename = f"images/{self.file}_{dt}_Image_running_{img_idx}"
                img_idx+=1
                iter = 1
                while True:
                    if isfile(f"{filename}.{image_ext}"):
                        print(filename)
                        filename = f"{filenm}_{iter}"
                        iter+=1
                    else:
                        image.save(open(f"{filename}.{image_ext}", "wb"))
                        print("img saved")
                        break
        with open(f"{self.file}.csv", 'w', newline="") as f:
            writer = DictWriter(f, fieldnames=["filename", "date", "lineno", "text"])
            # writer.writeheader()
            writer.writerows(csv_writer)
                # image.save(open(f"images/filename,{dt},{image_index},{text}.{image_ext}", "wb"))



