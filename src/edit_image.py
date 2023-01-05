"""
1. モノクロならガンマ調整して色を濃くする（表紙などカラーならそのまま or 軽くガンマ）
2. サイズ調整する
"""

from pathlib import Path
import numpy as np
import cv2


def gamma_correction(img: np.ndarray, gamma: float = 1.5) -> np.ndarray:
    """ガンマ補正 (gamma correction)

    次のような変換を行う
        y = (x / 255)^gamma * 255
    """
    # 非線形関数（look up table）を作る
    look_up_table = np.empty((1,256), np.uint8)
    for i in range(256):
        look_up_table[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    # 補正をかける
    return cv2.LUT(img, look_up_table)


def edit_image(input_path: Path, save_dir: Path):
    # read
    # cv2.imread()は日本語があると文字化けしてエラーになるためnpを通す
    buf = np.fromfile(str(input_path), np.uint8)
    img = cv2.imdecode(buf, cv2.IMREAD_UNCHANGED)

    is_gray_scale = True
    if img.ndim == 3:
        channel_diff = (img[:, :, 0] - img[:, :, -1])
        is_gray_scale = channel_diff.sum() == 0

    # gamma correction
    if is_gray_scale:
        # gamma=1.5くらいがIrfanviewで0.6にしたときに近い（IrfanViewは逆数(1/0.6=1.66)にしてる?）
        img = gamma_correction(img, gamma=1.6)

    # resize
    height, width = img.shape[0:2]
    new_width = 1080
    new_height = round((height / width) * new_width)
    img = cv2.resize(src=img, dsize=(new_width, new_height))

    # save
    save_path = str(save_dir / input_path.name)
    cv2.imwrite(save_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    print(f"success: {input_path} -> {save_path}")
