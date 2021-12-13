# minecraft_3d_plot
Make structure in minecraft from .obj file  
マイクラで.objファイルから形状を作る

# 必要なもの
minecraft JE (Raspberry Jam Modが適用されているもの)

# Windowsで動かす
Run these command by sudo in PowerShell  
下記のコマンドをPowerShellで管理者で実行

## 仮想環境作成

```
python -m venv venv
.\venv\Scripts\python.exe -m pip install -U pip setuptools wheel
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 実行

```
.\venv\Scripts\python.exe make_3d.py model_file_path

```