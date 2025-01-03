from py_asciimath.translator.translator import MathML2Tex
from pyhwpx import Hwp


tex_list = []


hwp = Hwp()
for ctrl in hwp.ctrl_list:
    if ctrl.UserDesc == "수식":
        mml_path = "eq.mml"
        hwp.select_ctrl(ctrl)
        hwp.export_mathml(mml_path)

        mathml2tex = MathML2Tex()
        with open(mml_path) as f:
            mml_eq = f.read()
        tex_eq = mathml2tex.translate(mml_eq, network=True, from_file=False)
        tex_list.append(tex_eq)
        
print(tex_list)