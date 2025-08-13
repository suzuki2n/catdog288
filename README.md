# 犬猫画像分類モデル（catdog288）
このリポジトリは、犬と猫の画像を分類するためのディープラーニングモデルを構築・実験した記録です。

## 使用技術
- Python 3.10
- CUDA 11.2 + cuDNN 8.1
- TensorFlow 2.10
- Keras（CNN / ResNet50 / VGG16 を使用した転移学習）
- Jupyter Notebook

## 構成
- `作成過程モデル/`：各種構築中のノートブック
- `perform_classification.py`：作成モデル実行用スクリプト
- `training_history.png`：学習曲線の可視化

## 備考
本リポジトリには、転移学習により精度99%を達成したモデルの構築過程（Jupyter Notebook）が含まれています。  
▶ [モデルの構築過程（Jupyter Notebook）](catdog_model_ResNet50_BATCH16_FT2_224.ipynb)

※ 練習用に作成したモデルであり、個人用途・ポートフォリオ閲覧用に限定しております。
