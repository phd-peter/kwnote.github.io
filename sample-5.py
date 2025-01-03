import re

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
        replacement = rf"\\{letter.capitalize()}"
        eq_str = re.sub(pattern, replacement, eq_str)

    # (B) 소문자 그리스 문자 처리
    for letter in greek_lower:
        pattern = rf"\b{letter}(?=_|\^|\b)"
        replacement = rf"\\{letter}"
        eq_str = re.sub(pattern, replacement, eq_str)

    # 7) left / right -> \left / \right
    eq_str = re.sub(r"\bleft\b",  r"\\left",  eq_str, flags=re.IGNORECASE)
    eq_str = re.sub(r"\bright\b", r"\\right", eq_str, flags=re.IGNORECASE)

    # 8) leq / geq / times -> \leq / \geq / \times
    eq_str = re.sub(r"\bleq\b",   r"\\leq",   eq_str, flags=re.IGNORECASE)
    eq_str = re.sub(r"\bgeq\b",   r"\\geq",   eq_str, flags=re.IGNORECASE)
    eq_str = re.sub(r"\btimes\b", r"\\times", eq_str, flags=re.IGNORECASE)

    # 모든공백제거
    eq_str = eq_str.replace(" ", "")  # 모든 공백 제거
    
    # 4) { ... }over{ ... } -> \frac{...}{...} (단, 중첩된 중괄호를 허용)
    eq_str = re.sub(
        r"\{(.*?)\}over\{(.*?)\}",
        r"\\frac{\1}{\2}",
        eq_str
    )



    return eq_str

# 간단 테스트 예시
if __name__ == "__main__":
    sample_list = [
        "$l_{hb}={0.24betad_{b}f_{y}}over{\lambda\sqrt{f_{ck}}}$",
        "LEFT ( － {4,000} over {273＋T( DELTA `t  _{i} )} ＋13.65 RIGHT )",
        "LEFT [ {9} over {2} RIGHT ]",  
        "{alpha}over{beta}prime",
    ]
    converted_list = [transform_equation(s) for s in sample_list]
    for before, after in zip(sample_list, converted_list):
        print(f"입력 :  {repr(before)}")
        print(f"출력 :  {repr(after)}")
        print("-"*60)
