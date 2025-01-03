from py_asciimath.translator.translator import MathML2Tex
from pyhwpx import Hwp

hwp = Hwp()
hwp.SelectCtrlFront()
mml_path = "eq.mml"
hwp.export_mathml(mml_path)
mathml2tex = MathML2Tex()
with open(mml_path) as f:
    mml_eq = f.read()
tex_eq = mathml2tex.translate(mml_eq, network=False, from_file=False)
print(tex_eq)