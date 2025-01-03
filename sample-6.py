import re

def replace_over_with_frac(latex_str):
    """
    LaTeX 문자열에서 {분자}over{분모} 패턴을 \frac{분자}{분모}로 변환합니다.

    Args:
        latex_str (str): 변환할 LaTeX 문자열.

    Returns:
        str: 변환된 LaTeX 문자열.
    """
    # (.*?)로 변경하여 내부에 중괄호 등이 있어도 매칭하도록 함
    pattern = r'\{(.*?)\}over\{(.*?)\}'
    replacement = r'\\frac{\1}{\2}'

    transformed_str = re.sub(pattern, replacement, latex_str)
    return transformed_str


if __name__ == "__main__":
    input_str1 = "$\\left({f_{y}-245}over{f_{y}}\\right)$"
    output_str1 = replace_over_with_frac(input_str1)
    print(output_str1)  # 기대: $\left(\frac{f_{y}-245}{f_{y}}\right)$

    input_str2 = "$\\left({5d_{b}}over{s_{w}}\\right)$"
    output_str2 = replace_over_with_frac(input_str2)
    print(output_str2)  # 기대: $\left(\frac{5d_{b}}{s_{w}}\right)$

    input_str3 = "$\\left({a_{b+c}}over{d_{e+f}}\\right)$"
    output_str3 = replace_over_with_frac(input_str3)
    print(output_str3)  # 기대: $\left(\frac{a_{b+c}}{d_{e+f}}\right)$
