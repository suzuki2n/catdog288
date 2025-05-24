# perform_classification.py
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input


# ---------- ダイアログ関数 ----------
def select_model() -> str:
    """学習済みモデル(.h5)を選択するダイアログ"""
    messagebox.showinfo("モデル選択", "学習済みモデル（.h5）を選択してくださいにゃ！")
    return filedialog.askopenfilename(
        title="モデルファイルを選択してください",
        filetypes=[("Keras model", "*.h5"), ("All files", "*.*")],
    )


def select_dir() -> str:
    """画像が入ったフォルダを選択するダイアログ"""
    messagebox.showinfo("フォルダ選択", "画像が入ったフォルダを選択してくださいにゃ！")
    return filedialog.askdirectory(title="画像が入ったフォルダを選択してください")


# ---------- メイン処理 ----------
def classify_images(model, folder_path: str):
    """
    選択フォルダ内の画像を猫/犬に分類し移動。
    さらに「確信度が低い（0.4〜0.6）」画像は review フォルダにまとめて移動。
    """
    if not folder_path:
        messagebox.showwarning("中止", "フォルダが選択されませんでしたにゃ…")
        return

    selected_folder = Path(folder_path)
    parent_folder = selected_folder.parent

    # 結果フォルダ
    result_cats_dir = parent_folder / "result_cats"
    result_dogs_dir = parent_folder / "result_dogs"
    review_uncertain = parent_folder / "review_uncertain"
    result_cats_dir.mkdir(exist_ok=True)
    result_dogs_dir.mkdir(exist_ok=True)
    review_uncertain.mkdir(exist_ok=True)

    image_extensions = {".jpg", ".jpeg", ".png"}

    for image_path in selected_folder.iterdir():
        if image_path.suffix.lower() not in image_extensions:
            continue

        print(f"処理中: {image_path}")

        # 前処理（学習時と同じ 224×224 & 0‑1 正規化）
        img = load_img(image_path, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = preprocess_input(img_array)  # ResNet50 用の前処理
        img_array = np.expand_dims(img_array, axis=0)

        # 予測
        prediction = model.predict(img_array, verbose=0)
        pred_prob = float(prediction[0][0])  # 0〜1 のスカラー
        print(f"予測確率 (dog): {pred_prob:.4f}")

        # 1) 確信度が低い画像を review フォルダへ
        if 0.4 <= pred_prob <= 0.6:
            shutil.move(image_path, review_uncertain / image_path.name)
            print(f"{image_path.name} を {review_uncertain} に移動（確信度低）")
            continue  # 分類フォルダへは入れない

        # 2) 通常の 0.5 しきい値で cat / dog 分類
        if pred_prob >= 0.5:  # 犬
            shutil.move(image_path, result_dogs_dir / image_path.name)
            print(f"{image_path.name} を {result_dogs_dir} に移動しましたにゃ！")
        else:  # 猫
            shutil.move(image_path, result_cats_dir / image_path.name)
            print(f"{image_path.name} を {result_cats_dir} に移動しましたにゃ！")

    messagebox.showinfo("完了", "分類とレビュー抽出が完了しましたにゃ！")


# ---------- スクリプト実行 ----------
if __name__ == "__main__":
    # Tk のメインウィンドウを 1 回だけ生成して非表示
    root = tk.Tk()
    root.withdraw()

    # 1) モデルファイルを選択
    model_path = select_model()
    if not model_path:
        messagebox.showwarning("中止", "モデルが選択されませんでしたにゃ…")
        exit()

    model = load_model(model_path)
    print(f"モデル {model_path} を読み込みましたにゃ！")

    # 2) 画像フォルダを選択
    folder_path = select_dir()
    classify_images(model, folder_path)
