# ディープラーニングを使うフォルダ構成にするためのスクリプト

import os, shutil
import random

base_path = os.path.dirname(os.path.abspath(__file__))  # このスクリプトがあるフォルダ
# 元データ
cat_dir = os.path.join(base_path, "train_cats")
# cat_dir = "C:/Users/User/Desktop/catdog/train_cats"
print("猫の画像ファイル数：", len(os.listdir(cat_dir)))
dog_dir = os.path.join(base_path, "train_dogs")
# dog_dir = "C:/Users/User/Desktop/catdog/train_dogs"
print("犬の画像ファイル数：", len(os.listdir(dog_dir)))

# 新しいデータセットフォルダ
# base_path = "C:/Users/User/Desktop/catdog"  # このスクリプトがあるフォルダ
base_dir = os.path.join(base_path, "dataset")  # base_pathの下に"dataset"フォルダを作る
os.makedirs(base_dir, exist_ok=True)

# train / validationを作成

for category in ["train", "validation"]:
    for label in ["cats", "dogs"]:
        path = os.path.join(base_dir, category, label)
        os.makedirs(path, exist_ok=True)
        
# 画像を分類して移動（80%をtrain、20%をvalidationにする）
def split_and_move(src_dir, dst_train, dst_val, split_ratio=0.8):
    files = os.listdir(src_dir)
    random.shuffle(files)
    split = int(len(files) * split_ratio)
    for i, fname in enumerate(files):
        src_path = os.path.join(src_dir, fname)
        if i < split:
            dst_path = os.path.join(dst_train, fname)
        else:
            dst_path = os.path.join(dst_val, fname)
        shutil.copy2(src_path, dst_path)
    
# 実行
split_and_move(cat_dir,
               os.path.join(base_dir, "train", "cats"),
               os.path.join(base_dir, "validation", "cats"))

split_and_move(dog_dir,
               os.path.join(base_dir, "train", "dogs"),
               os.path.join(base_dir, "validation", "dogs"))
print("データセットの作成が完了しました！")
# このスクリプトを実行すると、元データのtrain_cats, train_dogsフォルダから、datasetフォルダにtrainとvalidationのフォルダが作成され、その中にcatとdogのフォルダが作成されます。
# そして、元データの画像が80%をtrain、20%をvalidationに分けられて移動されます。               
        
