import sys

import PIL
import path
from PIL import Image


def run():
    current_folder = get_current_folder()
    target_folder = current_folder / '輸出'
    target_folder.makedirs_p()

    # 改名和轉格式順便移除層性
    for image_path in list_all_image_path_from_folder(current_folder):
        target_image_path = target_folder / f'{image_path.stem}.jpg'
        print(f'{image_path} to {target_image_path} ...', end=' ')

        with Image.open(image_path) as im:
            # JPG 不支援透明，所以要轉為 RGB
            if im.mode in ('RGBA', 'P'):
                im = im.convert("RGB")

            # 修改尺寸為一邊最大 1440
            width, height = im.size
            if max(width, height) > 1440:
                radio = 1440 / max(width, height)
                im.thumbnail((int(width * radio), int(height * radio)), Image.ANTIALIAS)

            # 調整檔案大小
            quality = 100
            while quality > 0:
                im.save(target_image_path, optimize=True, quality=quality)
                if target_image_path.stat().st_size / 1000 <= 300:
                    break
                quality -= 5

            print('ok')
    print('Ya Ya！')


def get_current_folder() -> path.Path:
    """取得檔案當前目錄 (需支援 Nuitka)"""
    if '__compiled__' in globals():
        current_folder = path.Path(sys.argv[0]).dirname().abspath()
    else:
        current_folder = path.Path(__file__).dirname().abspath()
    return current_folder


def list_all_image_path_from_folder(folder: path.Path) -> [path.Path]:
    """列出資料夾裡所有支援的圖片"""
    for image_path in folder.files():
        try:
            with Image.open(image_path):
                yield image_path
        except PIL.UnidentifiedImageError:
            continue


if __name__ == '__main__':
    run()
