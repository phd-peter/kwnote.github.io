import os

def list_folders(start_path):
    with open("folder_structure.txt", "w", encoding="utf-8") as f:
        for root, dirs, _ in os.walk(start_path):
            level = root.replace(start_path, "").count(os.sep)
            indent = " " * 4 * level
            f.write(f"{indent}{os.path.basename(root)}\n")
            sub_indent = " " * 4 * (level + 1)
            for d in dirs:
                f.write(f"{sub_indent}{d}\n")

# 폴더 경로 설정
start_path = r"C:\Users\Alpha\OneDrive\SEN"
list_folders(start_path)
