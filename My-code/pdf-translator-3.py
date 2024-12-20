import fitz  # PyMuPDF
import json

def add_translated_text_to_pdf(input_pdf_path, translated_json_path, output_pdf_path):
    """
    원본 PDF에 번역된 텍스트를 삽입하여 새 PDF 파일을 생성합니다.
    
    Args:
        input_pdf_path (str): 입력 PDF 파일 경로
        translated_json_path (str): 번역된 텍스트가 포함된 JSON 파일 경로
        output_pdf_path (str): 출력 PDF 파일 경로
    """
    # PDF 열기
    pdf_document = fitz.open(input_pdf_path)

    # JSON 파일 읽기
    with open(translated_json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 번역된 텍스트 삽입
    for entry in data:
        page_number = entry["page"] - 1  # PyMuPDF는 0부터 시작하는 페이지 인덱스를 사용
        if page_number < 0 or page_number >= len(pdf_document):
            print(f"페이지 번호 {entry['page']}는 유효하지 않습니다.")
            continue
        page = pdf_document[page_number]
        
        # 위치 및 텍스트 정보 가져오기
        translated_text = entry.get("translated_text", "")
        x = entry["x"]
        y = entry["y"]
        
        # 폰트 크기 설정
        fontsize = 10
        # 텍스트 길이에 따라 배경 사각형의 너비 계산 (간단한 예시)
        text_width = fitz.get_text_length(translated_text, fontsize=fontsize)
        text_height = fontsize * 1.2  # 약간의 여백을 추가
        
        # 배경 사각형 좌표 계산
        rect = fitz.Rect(x, y - text_height, x + text_width, y)
        
        # 하얀색 배경 그리기
        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
        
        # 텍스트 추가 (검은색)
        page.insert_text((x, y - text_height * 0.2), translated_text, fontsize=fontsize, color=(0, 0, 0))  # 약간의 여백을 조정

    # 변경된 PDF 저장
    pdf_document.save(output_pdf_path)
    pdf_document.close()

    print(f"번역된 텍스트가 삽입된 PDF가 {output_pdf_path}에 저장되었습니다.")

# 사용 예시
input_pdf_path = r"C:\Users\Alpha\OneDrive\SEN\1-Projects\OSC-stair\Company-introduction.pdf"  # 원본 PDF 파일 경로
translated_json_path = r"C:\Users\Alpha\OneDrive\SEN\1-Projects\OSC-stair\translated_output.json"  # 번역된 JSON 파일 경로
output_pdf_path = r"C:\Users\Alpha\OneDrive\SEN\1-Projects\OSC-stair\Company-introduction_tranlated.pdf"  # 저장할 출력 PDF 파일 경로

add_translated_text_to_pdf(input_pdf_path, translated_json_path, output_pdf_path)
