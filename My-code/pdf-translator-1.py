import pytesseract
from pdf2image import convert_from_path
import json
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

# Tesseract 실행 파일 경로 지정 (필요 시)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler 경로 지정 (Windows)
poppler_path = r"C:\poppler-24.08.0\Library\bin"

def process_page(page_image, page_number, tolerance=10):
    """페이지별 OCR 처리 및 라인별 텍스트 그룹화."""
    ocr_data = pytesseract.image_to_data(page_image, lang='jpn', output_type=pytesseract.Output.DICT)
    lines = defaultdict(list)

    # OCR 데이터 그룹화
    for i in range(len(ocr_data['text'])):
        if ocr_data['text'][i].strip():  # 텍스트가 비어 있지 않은 경우
            y = int(ocr_data['top'][i])
            x = int(ocr_data['left'][i])
            text = ocr_data['text'][i]

            # 기존 라인과 y 좌표가 비슷하면 해당 라인에 추가
            for line_y in lines:
                if abs(line_y - y) <= tolerance:
                    lines[line_y].append({"x": x, "text": text})
                    break
            else:
                # 새로운 라인 추가
                lines[y].append({"x": x, "text": text})

    # 정렬 및 라인별 텍스트 결합
    page_result = []
    for line_y in sorted(lines.keys()):
        # 각 라인의 단어와 x 좌표를 포함한 데이터를 저장
        line_data = sorted(lines[line_y], key=lambda t: t["x"])
        line_text = " ".join(item["text"] for item in line_data)
        first_x = line_data[0]["x"] if line_data else 0  # 가장 첫 번째 x 좌표

        page_result.append({
            "page": page_number,
            "y": line_y,
            "text": line_text,
            "x": first_x  # 첫 번째 x 좌표를 저장
        })

    return page_result

def pdf_to_json(pdf_path, output_json_path, dpi=200, max_workers=4):
    """PDF를 JSON으로 변환."""
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    result = []

    # 병렬 처리
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_page, image, page_number): page_number
                   for page_number, image in enumerate(images, start=1)}
        for future in futures:
            result.extend(future.result())

    # JSON 저장
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file, ensure_ascii=False, indent=4)
    print(f"OCR 데이터가 {output_json_path}에 저장되었습니다.")

# 사용 예시
pdf_path = r"C:\Users\Alpha\OneDrive\SEN\1-Projects\OSC-stair\Company-introduction.pdf"  # PDF 파일 경로
output_json_path = r"C:\Users\Alpha\OneDrive\SEN\1-Projects\OSC-stair\output.json"      # 저장할 JSON 파일 경로

pdf_to_json(pdf_path, output_json_path, dpi=200, max_workers=8)
