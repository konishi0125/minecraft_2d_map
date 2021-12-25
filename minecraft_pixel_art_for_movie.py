import time
import argparse
import numpy as np
import cv2
import mcpi.minecraft as minecraft
import mcpi.block as block
import pic2map


#実行時のparser設定
parser = argparse.ArgumentParser(description="画像をマイクラ内でピクセルアート化")
parser.add_argument("size", type=int, help="マイクラ内で生成するピクセルアートのサイズ size×sizeの正方形になる")
parser.add_argument("x", type=int, help="ピクセルアートの左上のx座標")
parser.add_argument("y", type=int, help="ピクセルアートの左上のy座標")
parser.add_argument("z", type=int, help="ピクセルアートの左上のz座標")
parser.add_argument("-c", "--color_convertor", default="srgbxyz", help="cie-xyzによる色相変換")
parser.add_argument("-b", "--brightness", type=float, default=1, help="輝度 デフォルトは1(変更なし)")

args = parser.parse_args()
map_size = args.size
corner = [args.x, args.y, args.z]
color_convertor = args.color_convertor
brightness = args.brightness

#位置の補正 なぜか指定した座標とマイクラ内座標がずれる
corner[0] -= 212
corner[1] -= 64
corner[2] -= 136

#マインクラフトとの接続
mc = minecraft.Minecraft()

#カメラ起動
camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()  # フレームを取得
    im = pic2map.resize_picture(frame, map_size, brightness)
    im_color = pic2map.to_color(im, color_convertor)
    patting_im_color = np.array(pic2map.patting(im_color))

    #ブロックの配置
    for i in range(map_size):
        for j in range(map_size):
            #余白は白のウール
            if im[i,j] == 255:
                mc.setBlock(corner[0] + j, corner[1], corner[2] + i, block.WOOL.id, 0)
            #ウールなどブロックidと種類idを持つブロックの設置
            elif im[i, j] > 1000:
                id1, id2 = divmod(im[i, j], 100)
                mc.setBlock(corner[0] + j, corner[1], corner[2] + i, int(id1), int(id2))
            #その他ブロックの設置
            else:
                mc.setBlock(corner[0] + j, corner[1], corner[2] + i, int(im[i, j]))

    # キー操作があればwhileループを抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(1)