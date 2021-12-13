import sys
import argparse
import numpy as np
import mcpi.minecraft as minecraft
import mcpi.block as block
import pic2map

#実行時のparser設定
parser = argparse.ArgumentParser(description="画像をマイクラ内でピクセルアート化")
parser.add_argument("path", help="画像ファイルのパス")
parser.add_argument("size", type=int, help="マイクラ内で生成するピクセルアートのサイズ size×sizeの正方形になる")
parser.add_argument("x", type=int, help="ピクセルアートの左上のx座標")
parser.add_argument("y", type=int, help="ピクセルアートの左上のy座標")
parser.add_argument("z", type=int, help="ピクセルアートの左上のz座標")

args = parser.parse_args()
path = args.path
map_size = args.size
corner = [args.x, args.y, args.z]

#画像をマイクラ内block idに変換
im = pic2map.pic2map_black_and_white(path, map_size)

#位置の補正 なぜか指定した座標とマイクラ内座標がずれる
corner[0] -= 212
corner[1] -= 64
corner[2] -= 136

#マインクラフトとの接続
mc = minecraft.Minecraft()

#ブロックの配置
for i in range(map_size):
    for j in range(map_size):
        if im[i,j] == 0:
            mc.setBlock(corner[0]+j,corner[1],corner[2]+i,block.WOOL.id, 15)
        elif im[i,j] == 255:
            mc.setBlock(corner[0]+j,corner[1],corner[2]+i, block.WOOL.id, 0)