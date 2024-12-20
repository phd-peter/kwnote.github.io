# 블루스택의 창 제목을 확인하기 위한 사전 파일
import pygetwindow as gw
print([w.title for w in gw.getAllWindows()])
