from pyhwpx import Hwp
import re

def transform_equation(eq_str: str) -> str:
    eq_str = eq_str.strip("'\"")
    eq_str = re.sub(r"LEFT\s*\[\s*\{(\d+)\}\s*over\s*\{(\d+)\}\s*RIGHT\s*\]", 
                    r"\\frac{\1}{\2}", 
                    eq_str)
    eq_str = eq_str.replace("prime", "'")

    greek_letters = [
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta",
        "eta", "theta", "iota", "kappa", "lambda", "mu",
        "nu", "xi", "omicron", "pi", "rho", "sigma", "tau",
        "upsilon", "phi", "chi", "psi", "omega"
    ]
    for letter in greek_letters:
        eq_str = eq_str.replace(letter, "\\" + letter)

    return eq_str

# 이미 수식이 들어있는 문서를 열어놓은 상태라고 가정
hwp = Hwp()

eq_list = []
for ctrl in hwp.ctrl_list:
    if ctrl.UserDesc == "수식":
        eq_list.append(ctrl.Properties.Item("String"))

# 이제 eq_list에 들어있는 문자열을 변환하여 새 리스트 eq_list_converted 생성
eq_list_converted = [transform_equation(s) for s in eq_list]

print(eq_list)
print(eq_list_converted)
