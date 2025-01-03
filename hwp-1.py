from pyhwpx import Hwp

# 수식이 든 문서를 열어놓은 상태로
hwp = Hwp()

for ctrl in hwp.ctrl_list:
    if ctrl.UserDesc == "수식":
        prop = ctrl.Properties
        prop.SetItem("Color", hwp.RGBColor("Red"))
        ctrl.Properties = prop


eq_list = []

for ctrl in hwp.ctrl_list:
    if ctrl.UserDesc == "수식":
        eq_list.append(ctrl.Properties.Item("String"))
print(eq_list)


# from pyhwpx import Hwp

# # hwp = Hwp()
# # hwp.SelectCtrlFront()  # 수식컨트롤을 선택한 상태여야 추출 가능함.
# path = r"./output/sample.mml"
# hwp.export_mathml(path)

# # for ctrl in hwp.ctrl_list:
# #     if ctrl.UserDesc == "수식":
#         string = ctrl.Properties.Item("String")
#         hwp.move_to_ctrl(ctrl)
#         hwp.MoveParaEnd()
#         hwp.BreakPara()
#         hwp.set_font(Height=20)  # <--------
#         hwp.insert_text(string)

