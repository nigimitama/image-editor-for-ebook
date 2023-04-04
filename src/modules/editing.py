"""
1. モノクロならガンマ調整して色を濃くする（表紙などカラーならそのまま or 軽くガンマ）
2. サイズ調整する
"""

from pathlib import Path
import numpy as np
import cv2
from PIL import Image


def contrast_adjustments(img, contrast=1.0, brightness=0.0):
    dst = contrast * img.astype(np.uint16) + brightness
    # [0, 255] でクリップし、uint8 型にする。
    return np.clip(dst, 0, 255).astype(np.uint8)


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


def edit_image(input_path: Path, save_dir: Path, brightness: int = 20,
               gamma: float = 1.6, gamma_target: str = "gray",
               new_width: int = 1080, quality: int = 75):
    # read
    # cv2.imread()/cv2.imwrite()はパスが日本語を含むとき文字化けしてエラーになるためPILを使う
    img = np.array([])
    with Image.open(input_path) as pil_img:
        img = np.array(pil_img)

    is_color = img.ndim == 3
    if is_color:  # カラー画像のときは、RGBからBGRへ変換する
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # MEMO: gamma=1.5くらいがIrfanviewで0.6にしたときに近い（IrfanViewは逆数(1/0.6=1.66)にしてる?）
    if gamma_target == "all" or ((gamma_target == "gray") and (not is_color)):
        # ガンマ補正
        img = gamma_correction(img, gamma=gamma)
        # コントラスト補正
        img = contrast_adjustments(img, contrast=1, brightness=brightness)

    # resize
    height, width = img.shape[0:2]
    new_height = round((height / width) * new_width)
    img = cv2.resize(src=img, dsize=(new_width, new_height))

    # save
    save_path = str(save_dir / input_path.name)

    if is_color:  # カラー画像のときは、BGRからRGBへ変換する
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    Image.fromarray(img).save(save_path, quality=quality, optimize=True)
    print(f"success: {input_path} -> {save_path}")
