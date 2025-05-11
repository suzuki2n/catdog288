# 画像を用意したら、リサイズとパディングを行うスクリプト
# 画像のサイズ224×224にリサイズし、黒背景でパディングする
# これが終わったらmkdir_learning.pyでディープラーニング用のフォルダ構成にする

import cv2
import os
import numpy as np
import glob
import tkinter as tk
from tkinter import filedialog


def resize_and_pad(img, size=(224, 224), pad_color=(0, 0, 0)):
    h, w = img.shape[:2]
    # img.shape[0] → 画像の「高さ (height)
    # img.shape[1] → 画像の「幅 (width)
    # img.shape[2] → 画像の「チャンネル数 (channel)

    # スケールを計算して、短辺を基準にリサイズ
    scale = min(size[0] / w, size[1] / h)
    # size[0] = 224  # 出力画像の幅（width）, size[0] / w → 出力画像の幅 / 元画像の幅（横のスケール）
    # size[1] = 224  # 出力画像の高さ（height）, size[1] / h → 出力画像の高さ / 元画像の高さ（縦のスケール）
    # （例）256×512を224×224にするには横を0.5倍、縦を0.25にする。minなので0.25の（縦に合わせる）

    new_w, new_h = int(w * scale), int(h * scale)
    img_resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    # パディングのサイズ計算
    top = (size[1] - new_h) // 2
    bottom = size[1] - new_h - top
    left = (size[0] - new_w) // 2
    right = size[0] - new_w - left

    # パディングを追加（黒背景 or 白背景）
    img_padded = cv2.copyMakeBorder(
        img_resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=pad_color
    )

    return img_padded


def main():
    # tkinterのルートウィンドウ作成（表示はしない）
    root = tk.Tk()
    root.withdraw()

    # フォルダ選択ダイアログを表示
    print("リサイズしたい画像が含まれているフォルダを選択してください。")
    input_folder = filedialog.askdirectory(title="リサイズする画像のフォルダを選択")

    # ユーザーがキャンセルした場合や無効なパスの場合
    if not input_folder:
        print("フォルダが選択されませんでした。処理を終了します。")
        return

    # 出力フォルダの設定
    base_path = os.path.dirname(input_folder)
    folder_name = os.path.basename(input_folder)
    output_folder = os.path.join(base_path, folder_name + "_resized")

    os.makedirs(output_folder, exist_ok=True)

    # 画像ファイルの検索パターンを定義
    image_patterns = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]
    image_paths = []

    # 複数の拡張子に対応
    for pattern in image_patterns:
        image_paths.extend(glob.glob(os.path.join(input_folder, pattern)))

    if not image_paths:
        print(f"選択されたフォルダ '{input_folder}' には画像が見つかりませんでした。")
        return

    print("画像数:", len(image_paths))  # 取得した画像の数を表示
    print(f"リサイズ処理を開始します。出力先: {output_folder}")

    for path in image_paths:
        img = cv2.imread(path)
        if img is None:
            print(f"警告: '{path}' を読み込めませんでした。スキップします。")
            continue

        img_padded = resize_and_pad(img, size=(224, 224), pad_color=(0, 0, 0))  # 黒背景
        filename = os.path.basename(path)
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, img_padded)

    print("リサイズとパディング処理が完了しました！")
    print(f"出力フォルダ: {output_folder}")


if __name__ == "__main__":
    main()
