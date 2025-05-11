from pathlib import Path
import shutil
import tkinter as tk
from tkinter import filedialog

# ======= 設定 =======
split_size = 75  # 分割する枚数（例：500枚ずつ）
valid_exts = ['.jpg', '.jpeg', '.png']  # 対象とする画像の拡張子
# ====================

# 🎯 フォルダ選択ダイアログ
root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="画像フォルダを選択してニャ")

if not folder_path:
    print("❌ フォルダが選択されていませんにゃ…")
    exit()

src_folder = Path(folder_path)
all_files = sorted([f for f in src_folder.iterdir() if f.suffix.lower() in valid_exts])

# 🔄 分割処理
for i in range(0, len(all_files), split_size):
    split_folder = src_folder / f"split_{i // split_size + 1:03}"
    split_folder.mkdir(exist_ok=True)
    
    for file in all_files[i:i + split_size]:
        shutil.copy2(file, split_folder / file.name)

print(f"✅ {len(all_files)} 枚の画像を {split_size} 枚ずつフォルダに分けたにゃ！")
