from py_asciimath.translator.translator import MathML2Tex

# MathML to TeX 변환 객체 생성
mathml2tex = MathML2Tex()

# 입력 파일 경로
mml_path = r"test-1.mml"

# 파일에서 MathML 읽기
with open(mml_path, "r", encoding="utf-8") as f:
    mml_eq = f.read()

# MathML을 TeX 형식으로 변환
tex_eq = mathml2tex.translate(mml_eq, network=False, from_file=False)

# 결과 출력
print(tex_eq)
