"""
1. モノクロならガンマ調整して色を濃くする（表紙などカラーならそのまま or 軽くガンマ）
2. サイズ調整する
"""

from pathlib import Path
import numpy as np
import cv2
from PIL import Image


def gamma_correction(img: np.ndarray, gamma: float) -> np.ndarray:
    """ガンマ補正 (gamma correction)

    次のような変換を行う
        y = (x / 255)^gamma * 255
    """
    # 非線形関数（look up table）を作る
    look_up_table = np.empty((1, 256), np.uint8)
    for i in range(256):
        look_up_table[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    # 補正をかける
    return cv2.LUT(img, look_up_table)


def edit_image(input_path: Path, save_dir: Path, gamma: float = 1.6, new_width: int = 1080):
    # read
    # cv2.imread()/cv2.imwrite()はパスが日本語を含むとき文字化けしてエラーになるためPILを使う
    img = np.array([])
    with Image.open(input_path) as pil_img:
        img = np.array(pil_img)

    is_color = img.ndim == 3
    if is_color:  # カラー画像のときは、RGBからBGRへ変換する
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # gamma correction
    if not is_color:
        # gamma=1.5くらいがIrfanviewで0.6にしたときに近い（IrfanViewは逆数(1/0.6=1.66)にしてる?）
        img = gamma_correction(img, gamma=gamma)

    # resize
    height, width = img.shape[0:2]
    new_height = round((height / width) * new_width)
    img = cv2.resize(src=img, dsize=(new_width, new_height))

    # save
    save_path = str(save_dir / input_path.name)

    if is_color:  # カラー画像のときは、BGRからRGBへ変換する
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    Image.fromarray(img).save(save_path)
    print(f"success: {input_path} -> {save_path}")
