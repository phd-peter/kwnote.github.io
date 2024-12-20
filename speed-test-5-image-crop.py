import pytesseract
from PIL import Image, ImageFilter
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert("L")  # 흑백 변환
        img = img.filter(ImageFilter.SHARPEN)  # 선명하게
        
        return img

def extract_text_with_config(image_path, region, lang="kor"):
    with preprocess_image(image_path) as img:
        cropped = img.crop(region)
        cropped.show()  # Crop된 이미지 확인
        custom_config = r'--psm 6 --oem 1'
        text = pytesseract.image_to_string(cropped, lang=lang, config=custom_config)
        return text.strip()

# 테스트 실행
if __name__ == "__main__":
    region = (50, 314, 712, 343)  # 예시 좌표
    image_path = "screenshots/bluestacks_set_1.png"
    text = extract_text_with_config(image_path, region)
    print("OCR Result:")
    print(text)
