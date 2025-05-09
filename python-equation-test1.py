import re

def transform_to_simple_list(input_text):
    results = []
    for line in input_text.strip().split('\n'):
        # 수식 ($...$) 추출
        formula_match = re.search(r'\$(.*?)\$', line)
        formula = formula_match.group(1).strip() if formula_match else ''

        # 식 번호 (괄호 안) 추출
        number_match = re.search(r'\(([\d\.\-]+)\)', line)
        formula_number = number_match.group(1).strip() if number_match else ''

        # 결과 포맷
        if formula and formula_number:
            result = f"- 공식 ({formula_number}) Latex: ${formula}$"
            results.append(result)

    return '\n'.join(results)

# 예제 입력 (여러 줄)
input_text = r"""
    $\rho _{rl}=\\frac{A_shl}{sb_{cs} }$ 	(4.1-14)
    $\rho _{rs}=\\frac{A_shs}{sb_{cl} }$ 	(4.1-15)
    $f_{c}=0.85f_{ck,c}\\left [1-\\left (1-\\frac{\\varepsilon _{c}}{\\varepsilon _{co,c} }\\right )^{n}\\right ]$ 	(4.1-6)
    $f_{c}=0.85f_{ck,c}$ 	(4.1-7)
    $f_{ck,c}=f_{ck}+3.7f_{c2}$ 	(4.1-8)
    $\\varepsilon _{co,c}=\\varepsilon _{co}\\left (f_{ck,c}overf_{ck}\\right )^{2}$ 	(4.1-9)
    $\\varepsilon _{cu,c}=\\varepsilon _{cu}+{0.2f_{c2}}overf_{ck}$ 	(4.1-10)
    $n=1.2+1.5\left (\frac{100-f_{ck}}{60} \right )^{4}\leq 2.0$ 	(4.1-3)
	    $\varepsilon _{co}=0.002+\left (\frac{f_{ck}-40}{100,000} \right )\geq 0.002$ 	(4.1-4)
	$\varepsilon _{cu}=0.0033-\left (\frac{f_{ck}-40}{100,000} \right )\leq 0.0033$ 	(4.1-5)
        $f_{c}=0.85f_{ck}\left [1-\left (1-\frac{\varepsilon _{c}}{\varepsilon _{co} }\right )^{n}\right ]$ 	(4.1-1)
	$f_{c}=0.85f_{ck}$ 	(4.1-2)
"""

# 실행
output = transform_to_simple_list(input_text)
print(output)
