from pyhwpx import Hwp
import re

from pyparsing import nestedExpr, Word, alphanums, Literal, ParserElement

ParserElement.enablePackrat()

def parse_over_expression(text):
    # 중첩된 {}를 파싱하는 parser 정의
    brace_expr = nestedExpr('{', '}')

    # 전체 수식을 {} 단위로 파싱
    parsed = brace_expr.parseString('{' + text + '}').asList()[0]

    def process(parsed_list):
        result = ''
        i = 0
        while i < len(parsed_list):
            item = parsed_list[i]
            if isinstance(item, list) and i + 1 < len(parsed_list) and parsed_list[i + 1] == 'over' and i + 2 < len(parsed_list):
                # \frac 변환 처리
                left = process(item)
                right = process(parsed_list[i + 2])
                result += f"\\frac{{{left}}}{{{right}}}"
                i += 3  # skip over + right
            else:
                if isinstance(item, list):
                    result += '{' + process(item) + '}'
                else:
                    result += item
                i += 1
        return result

    return process(parsed)


def transform_equation(eq_str: str) -> str:
    # 0) 백틱(`) 제거
    eq_str = eq_str.replace("`", "")

    # 1) 앞뒤 따옴표(' 또는 ") 제거
    eq_str = eq_str.strip("'\"")

    # 2) \r, \n 등 개행문자 제거
    eq_str = eq_str.replace("\r\n", "").replace("\n", "").replace("\r", "")

    # 3) sqrt -> \sqrt, % -> \%
    eq_str = eq_str.replace("sqrt", r"\sqrt")
    eq_str = eq_str.replace("%", r"\%")

    # 5) prime -> '
    eq_str = eq_str.replace("prime", "'")




    # 6) 그리스 문자 처리
    greek_lower = [
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta",
        "eta", "theta", "iota", "kappa", "lambda", "mu",
        "nu", "xi", "omicron", "pi", "rho", "sigma", "tau",
        "upsilon", "phi", "chi", "psi", "omega", "varepsilon"
    ]
    greek_upper = [
        "ALPHA", "BETA", "GAMMA", "DELTA", "EPSILON", "ZETA",
        "ETA", "THETA", "IOTA", "KAPPA", "LAMBDA", "MU",
        "NU", "XI", "OMICRON", "PI", "RHO", "SIGMA", "TAU",
        "UPSILON", "PHI", "CHI", "PSI", "OMEGA"
    ]

    # (A) 대문자 그리스 문자 처리
    for letter in greek_upper:
        pattern = rf"\b{letter}(?=_|\^|\b)"
        replacement = rf"\\{letter.capitalize()} "
        eq_str = re.sub(pattern, replacement, eq_str)

    # (B) 소문자 그리스 문자 처리
    for letter in greek_lower:
        pattern = rf"\b{letter}(?=_|\^|\b)"
        replacement = rf"\\{letter} "
        eq_str = re.sub(pattern, replacement, eq_str)

    # 7) left / right -> \left / \right
    eq_str = re.sub(r"\bleft\b",  r"\\left ",  eq_str, flags=re.IGNORECASE)
    eq_str = re.sub(r"\bright\b", r"\\right ", eq_str, flags=re.IGNORECASE)

    # 8) leq / geq / times -> \leq / \geq / \times
    eq_str = re.sub(r"\bleq\b",   r"\\leq ",   eq_str, flags=re.IGNORECASE)
    eq_str = re.sub(r"\bgeq\b",   r"\\geq ",   eq_str, flags=re.IGNORECASE)
    eq_str = re.sub(r"\btimes\b", r"\\times ", eq_str, flags=re.IGNORECASE)

    # 모든공백제거
    eq_str = eq_str.replace(" ", "")  # 모든 공백 제거
    
    

    # 4) { ... }over{ ... } -> \frac{...}{...} (단, 중첩된 중괄호를 허용)
    eq_str = parse_over_expression(eq_str)
    
    return eq_str



# 이미 수식이 들어있는 문서를 열어놓은 상태라고 가정
hwp = Hwp()

eq_list = []
for ctrl in hwp.ctrl_list:
    if ctrl.UserDesc == "수식":
        prop = ctrl.Properties
        prop.SetItem("Color", hwp.RGBColor("Red"))
        ctrl.Properties = prop
        eq_list.append(ctrl.Properties.Item("String"))
        tem = transform_equation(ctrl.Properties.Item("String"))
        hwp.move_to_ctrl(ctrl)  # 수식으로 이동
        hwp.insert_text(f"${tem}$")  # 빈 줄에 수식문자열 삽입

# 변환
eq_list_converted = [transform_equation(s) for s in eq_list]

print(eq_list)
print(eq_list_converted)

with open("converted_equations.txt", "w", encoding="utf-8") as f:
    for item in eq_list_converted:
        # 앞뒤 공백 제거 후 $...$ 형태로 저장
        item = item.strip()
        f.write(f"\n${item}$\n")
