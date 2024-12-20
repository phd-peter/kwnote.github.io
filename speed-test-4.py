import pytesseract
from PIL import Image
import os

# Tesseract 실행 경로 (환경에 맞게 수정)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 필요한 영역의 좌표 정의 (x1, y1, x2, y2)
REGION_COORDS = {
    "title": (303, 188, 450, 210),          # 제목 영역
    "table1_title": (50, 150, 400, 200),   # 표1 제목 영역
    "table1": (50, 250, 500, 400),         # 표1 (3열 2행)
    "table2_title": (50, 450, 400, 500),   # 표2 제목 영역
    "table2": (50, 550, 300, 600),         # 표2 (2열 1행)
}

# 이미지 파일 경로 설정
SCREENSHOTS_DIR = "screenshots"
IMAGE_PATTERN = "bluestacks_set_{}.png"  # 이미지 이름 패턴 (1~5)

def extract_text_from_region(image_path, region, save_cropped=False, cropped_output_dir="cropped"):
    """특정 영역에서 OCR로 텍스트를 추출하고, 필요 시 crop된 이미지를 저장."""
    with Image.open(image_path) as img:
        cropped = img.crop(region)  # 해당 영역 잘라내기
        
        # crop된 이미지 저장
        if save_cropped:
            if not os.path.exists(cropped_output_dir):
                os.makedirs(cropped_output_dir)
            cropped_filename = os.path.join(cropped_output_dir, f"cropped_{os.path.basename(image_path)}_{region}.png")
            cropped.save(cropped_filename)
            print(f"Cropped image saved: {cropped_filename}")
        
        # OCR 처리
        text = pytesseract.image_to_string(cropped, lang="eng+kor")
        return text.strip()


def extract_data_from_image(image_path):
    """전체 이미지에서 필요한 데이터를 추출."""
    data = {}
    for key, coords in REGION_COORDS.items():
        data[key] = extract_text_from_region(image_path, coords)
    return data

def process_all_images():
    """screenshots 폴더에 있는 모든 이미지를 처리."""
    extracted_results = {}
    for i in range(1, 6):  # 1부터 5까지 처리
        image_path = os.path.join(SCREENSHOTS_DIR, IMAGE_PATTERN.format(i))
        if os.path.exists(image_path):
            print(f"Processing: {image_path}")
            extracted_results[f"Image_{i}"] = {}
            for key, coords in REGION_COORDS.items():
                text = extract_text_from_region(image_path, coords, save_cropped=True)  # crop 저장 활성화
                extracted_results[f"Image_{i}"][key] = text
        else:
            print(f"Image not found: {image_path}")
    return extracted_results


if __name__ == "__main__":
    # 모든 이미지 처리
    results = process_all_images()

    # 결과 출력
    print("Extracted Results:")
    for image_key, data in results.items():
        print(f"\n{image_key}:")
        for region, text in data.items():
            print(f"  {region}: {text}")
