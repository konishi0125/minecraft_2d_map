# minecraft_pixel_art
Make pixel art in minecraft from .jpg file  
マイクラで.jpgファイルからピクセルアートを作る\
_black_and_white.py:白黒2色\
_color.py:色付き\
_color.pyで使われるブロックは羊毛16色、砂岩、金ブロック、オークの木材、土

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
他にmcpiが必要

## プログラム修正
black_and_white.py:25-27行\
color.py:29-31行\
プログラム側から座標を入力するときなぜか座標がずれるため修正\
修正値はワールドによって違う

## 実行

```
.\venv\Scripts\python.exe minecraft_pixel_art_for_color.py path size x y z --color_convertor --brightness
```
path:画像のパス\
size:ピクセルアートのサイズ size×sizeになる\
x, y, z:ピクセルアートの左上の座標\
--color_convertor:色相変換指定 デフォルトはsrgbxyz 他にciexyz,srgbcxyz,adobexyzがある\
--brightness:画像の輝度調整 デフォルトは1