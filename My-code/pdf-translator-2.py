import os
from openai import OpenAI
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


# Load the API key from environment variables
api_key = os.getenv('OPENAI_API_KEY')

# Validate API key
if not api_key:
    raise ValueError("API key not found. Please set 'OPENAI_API_KEY' as an environment variable.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

# Chat model and system setup
model = "gpt-3.5-turbo"



def preprocess_text(text):
    """텍스트 전처리: 공백 제거."""
    return text.replace(" ", "").strip()

def translate_text(text, source_lang='ja', target_lang='en'):
    """텍스트를 번역하는 함수."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                    {"role": "system", "content": f"You are a translator that translates {source_lang} to {target_lang}."},
                    {"role": "user", "content": text}
            ],
            max_tokens=1500,  # 출력 크기 조정
            temperature=0.3  # Use 0 for deterministic results
        )

        # Extract and display the translated text
        translated_text = response.choices[0].message.content
        return translated_text

    except Exception as e:
        print(f"번역 실패: {text} - {e}")
        return None


def translate_json(input_json_path, output_json_path, source_lang='ja', target_lang='en'):
    """JSON 파일의 텍스트를 번역하여 새로운 JSON 파일로 저장."""
    # JSON 파일 읽기
    with open(input_json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # 번역 작업을 위한 ThreadPoolExecutor 사용
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_entry = {}
        for entry in data:
            # 전처리 및 번역 작업 준비
            entry["text"] = preprocess_text(entry["text"])
            future = executor.submit(translate_text, entry["text"], source_lang, target_lang)
            future_to_entry[future] = entry

        # tqdm을 사용하여 진행 상황 표시
        for future in tqdm(as_completed(future_to_entry), total=len(future_to_entry), desc="Translating"):
            entry = future_to_entry[future]
            try:
                translated_text = future.result()
                entry["translated_text"] = translated_text
            except Exception as e:
                print(f"번역 중 에러 발생: {e}")
                entry["translated_text"] = None

    # 번역된 데이터 저장
    with open(output_json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f"번역된 JSON 데이터가 {output_json_path}에 저장되었습니다.")

# 사용 예시
if __name__ == "__main__":
    input_json_path = r"C:\Users\Alpha\OneDrive\SEN\1-Projects\OSC-stair\output.json"  # OCR로 생성된 JSON 파일 경로
    output_json_path = r"C:\Users\Alpha\OneDrive\SEN\1-Projects\OSC-stair\translated_output.json"  # 번역 결과를 저장할 JSON 파일 경로

    translate_json(input_json_path, output_json_path)
