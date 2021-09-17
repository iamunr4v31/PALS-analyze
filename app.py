from backend_app.image_from_pdf import ImgExtractor

def main():
    extractor = ImgExtractor("./PALS.pdf")
    extractor.extract_images()

if __name__ == "__main__":
    main()