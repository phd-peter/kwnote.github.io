from pyhwpx import Hwp
import re

def transform_equation(eq_str: str) -> str:
    r"""
    0) 백틱(`) 제거
    1) 앞뒤 따옴표(' 또는 ") 제거
    2) \r, \n 등 개행문자 제거
    3) sqrt -> \sqrt
    4) { ... } over { ... } -> \frac{...}{...}
    5) prime -> '
    6) 그리스 문자 변환 (소문자/대문자 + _, ^, 또는 단독)
    7) left / right -> \left / \right (대소문자 무시)
    8) leq / geq / times -> \leq / \geq / \times (대소문자 무시)
    """

    # 0) 백틱(`) 제거
    eq_str = eq_str.replace("`", "")

    # 1) 앞뒤 따옴표(' 또는 ") 제거
    eq_str = eq_str.strip("'\"")

    # 2) \r, \n 등 개행문자 제거
    eq_str = eq_str.replace("\r\n", "").replace("\n", "").replace("\r", "")

    # 3) sqrt -> \sqrt
    eq_str = eq_str.replace("sqrt", r"\sqrt")

    # 4) { ... } over { ... } -> \frac{...}{...}
    eq_str = re.sub(
        r"\{\s*([^}]*)\}\s*over\s*\{\s*([^}]*)\}",
        r"\\frac{\1}{\2}",
        eq_str
    )

    # 5) prime -> '
    eq_str = eq_str.replace("prime", "'")

    # 6) 그리스 문자 처리

    # (A) 소문자 목록
    greek_lower = [
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta",
        "eta", "theta", "iota", "kappa", "lambda", "mu",
        "nu", "xi", "omicron", "pi", "rho", "sigma", "tau",
        "upsilon", "phi", "chi", "psi", "omega"
    ]
    # (B) 대문자 목록
    greek_upper = [
        "ALPHA", "BETA", "GAMMA", "DELTA", "EPSILON", "ZETA",
        "ETA", "THETA", "IOTA", "KAPPA", "LAMBDA", "MU",
        "NU", "XI", "OMICRON", "PI", "RHO", "SIGMA", "TAU",
        "UPSILON", "PHI", "CHI", "PSI", "OMEGA"
    ]

    # 길이가 긴 것부터 치환 (부분 문자열 충돌 방지)
    greek_lower.sort(key=len, reverse=True)
    greek_upper.sort(key=len, reverse=True)

    # 대문자 그리스 -> \Delta 등 (대소문자 무시를 원하면 flags=re.IGNORECASE)
    for letter in greek_upper:
        # 정규식 패턴
        pattern = rf"\b{letter}\b"
        # 치환 문자열 (e.g. "\\" + "Delta" => '\Delta')
        raw_replacement = "\\" + letter.capitalize()
        # re.escape()로 치환 문자열 이스케이프 처리
        replacement = re.escape(raw_replacement)
        # 치환
        eq_str = re.sub(pattern, replacement, eq_str, flags=re.IGNORECASE)

    # 소문자 그리스 -> \alpha 등
    for letter in greek_lower:
        pattern = rf"\b{letter}\b"
        raw_replacement = "\\" + letter
        replacement = re.escape(raw_replacement)
        eq_str = re.sub(pattern, replacement, eq_str, flags=re.IGNORECASE)

    # 7) left / right -> \left / \right (대소문자 무시)
    eq_str = re.sub(r"(?i)\bleft\b",  r"\\left",  eq_str)
    eq_str = re.sub(r"(?i)\bright\b", r"\\right", eq_str)

    # 8) leq / geq / times -> \leq / \geq / \times (대소문자 무시)
    eq_str = re.sub(r"(?i)\bleq\b",   r"\\leq",   eq_str)
    eq_str = re.sub(r"(?i)\bgeq\b",   r"\\geq",   eq_str)
    eq_str = re.sub(r"(?i)\btimes\b", r"\\times", eq_str)

    return eq_str


# 이미 수식이 들어있는 문서를 열어놓은 상태라고 가정
hwp = Hwp()

eq_list = []
for ctrl in hwp.ctrl_list:
    if ctrl.UserDesc == "수식":
        eq_list.append(ctrl.Properties.Item("String"))

# 변환
eq_list_converted = [transform_equation(s) for s in eq_list]

print(eq_list)
print(eq_list_converted)

with open("converted_equations.txt", "w", encoding="utf-8") as f:
    for item in eq_list_converted:
        # 앞뒤 공백 제거 후 $...$ 형태로 저장
        item = item.strip()
        f.write(f"${item}$\n")