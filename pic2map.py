import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from PIL import ImageEnhance

#リサイズ #輝度の変換
def resize_picture(im, map_size, brightness):
    con = ImageEnhance.Brightness(im)
    im = con.enhance(brightness)
    if im.size[0] > im.size[1]:
        resize_rate = map_size / im.size[0]
    else:
        resize_rate = map_size / im.size[1]
    im = im.resize((round(resize_rate*im.size[0]), round(resize_rate*im.size[1])))
    return im

#画像の読み込み、リサイズ
def load_picture(file_path, map_size, brightness):
    im = Image.open(file_path)
    con = ImageEnhance.Brightness(im)
    im = con.enhance(brightness)
    if im.size[0] > im.size[1]:
        resize_rate = map_size / im.size[0]
    else:
        resize_rate = map_size / im.size[1]
    im = im.resize((round(resize_rate*im.size[0]), round(resize_rate*im.size[1])))
    return im

#numpy.arrayの長さと平均を算出
def calculate_length_mean(im_array):
    length = len(im_array)
    myu = im_array.mean()
    return length, myu

#大津の2値化で白黒画像に変更
def otsu_method(im):
    im_array = np.array(im.convert("L"))
    S = 0
    threshold = 0
    for i in range(1, 256, 1):
        class1 = im_array[im_array<i]
        class2 = im_array[im_array>=i]
        if len(class1) == 0 or len(class2) == 0:
            continue
        length1, myu1 = calculate_length_mean(class1)
        length2, myu2 = calculate_length_mean(class2)
        S_ = length1*length2*(myu1-myu2)**2
        if S < S_:
            threshold = i
            S = S_
    im_array_otsu = np.where(im_array<threshold, 0, 255)
    im_otsu = Image.fromarray(im_array_otsu)
    return im_otsu

#色相空間の変換
def color_conversion(key):
    if key == "ciexyz":
        rgb2xyz = (
            0.4898, 0.3101, 0.2001, 0,
            0.1769, 0.8124, 0.0107, 0,
            0.0000, 0.0100, 0.9903, 0
        )
        return rgb2xyz
    elif key == "srgbxyz":
        rgb2xyz = (
            0.4124, 0.3576, 0.1805, 0,
            0.2126, 0.7152, 0.0722, 0,
            0.0193, 0.1192, 0.9505, 0
        )
        return rgb2xyz
    elif key == "srgbcxyz":
        rgb2xyz = (
            0.6069, 0.1735, 0.2003, 0,
            0.2989, 0.5866, 0.1144, 0,
            0.0000, 0.0661, 1.1157, 0
        )
        return rgb2xyz
    elif key == "adobexyz":
        rgb2xyz = (
            0.5778, 0.1825, 0.1902, 0,
            0.3070, 0.617, 0.0761, 0,
            0.0181, 0.0695, 1.0015, 0
        )
        return rgb2xyz


#CIE-XYZで各ピクセルの色に対応するblock_idに変更
def to_color(im, color_convertor):
    block_list = np.loadtxt(f"color_list/color_{color_convertor}.csv", delimiter=",", skiprows=1)
    rgb2xyz = color_conversion(color_convertor)
    im_array = np.array(im.convert("RGB", rgb2xyz))
    out = np.zeros(im.size, dtype=int).T
    for i in range(im.size[1]):
        for j in range(im.size[0]):
            dist = 100000
            for k in range(len(block_list)):
                dist_ = np.linalg.norm(im_array[i,j]-block_list[k,1:])
                if dist_ < dist:
                    out[i,j] = block_list[k,0]
                    dist = dist_
    out = Image.fromarray(out)
    return out


#正方形になるよう余白を白で埋める
def patting(im):
    width, height = im.size
    if width == height:
        return im
    if width > height:
        result = Image.new(im.mode, (width, width), 255)
        result.paste(im, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(im.mode, (height, height), 255)
        result.paste(im, ((height - width) // 2, 0))
        return result

#画像を白黒の2値に変換する
def pic2map_black_and_white(path, map_size):
    im = load_picture(path, map_size, 1)
    im_otsu = otsu_method(im)
    patting_im_otsu = patting(im_otsu)
    return np.array(patting_im_otsu)


#画像を羊毛16色+alphaのidに変換する
def pic2map_color(path, map_size, color_convertor, brightness):
    im = load_picture(path, map_size, brightness)
    im_color = to_color(im, color_convertor)
    patting_im_color = patting(im_color)
    return np.array(patting_im_color)

if __name__ == "__main__":
    path = "./picture/1.jpg"
    map_size = 128
    im_array = pic2map_color(path, map_size, "srgbxyz", 1)
    print(im_array)
    im = Image.fromarray(im_array)
    im.show()
