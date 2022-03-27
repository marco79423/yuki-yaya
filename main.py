import sys

import PIL
import path
from PIL import Image


def run():
    current_folder = get_current_folder()
    target_folder = current_folder / '輸出'
    target_folder.makedirs_p()

    logo_path = current_folder / '.yuki-yaya' / 'logo.png'

    # 改名和轉格式順便移除層性
    for image_path in list_all_image_path_from_folder(current_folder):
        target_image_path = target_folder / f'{image_path.stem}.jpg'
        print(f'{image_path} to {target_image_path} ...', end=' ')

        with Image.open(image_path) as im:
            # 修改尺寸為一邊最大 1440
            width, height = im.size
            if max(width, height) > 1440:
                radio = 1440 / max(width, height)
                im.thumbnail((int(width * radio), int(height * radio)), Image.ANTIALIAS)

            # 因為 JPG 不支援透明，要存為 JPG 就必須所以要轉為 RGB
            if im.mode in ('RGBA', 'P'):
                im = im.convert("RGB")

            # 調整檔案大小
            save_image_smaller_than(im, target_image_path, 300)

        if logo_path.exists():
            with Image.open(target_image_path) as im:
                # 加上 logo 浮水印
                with Image.open(logo_path) as logo_im:
                    im = add_logo_image(im, logo_im)
                save_image_smaller_than(im, target_image_path, 300)

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


def save_image_smaller_than(image_im, target_path, image_size):
    """用小於指定的大小存圖片到指定路徑"""
    quality = 100
    while quality > 0:
        image_im.save(target_path, optimize=True, quality=quality)
        if target_path.stat().st_size / 1000 < image_size:
            break
        quality -= 5


def add_logo_image(image_im, logo_im):
    original_mode = image_im.mode

    # 確保圖片是 RGBA
    if original_mode != 'RGBA':
        image_im = image_im.convert('RGBA')
    logo_im = logo_im.convert('RGBA')

    image_x, image_y = image_im.size
    logo_x, logo_y = logo_im.size

    # 縮放圖片
    logo_size_ratio = min(image_x, image_y) / max(logo_x, logo_y) / 4
    new_logo_size = (int(logo_x * logo_size_ratio), int(logo_y * logo_size_ratio))
    logo_im = logo_im.resize(new_logo_size, resample=Image.ANTIALIAS)

    # 透明度
    logo_im.putalpha(150)

    logo_x, logo_y = logo_im.size

    # 水印位置
    margin = 30
    image_im.alpha_composite(logo_im, (image_x - logo_x - margin, image_y - logo_y - margin))  # 右下角

    # 轉回原來的模式
    if original_mode != 'RGBA':
        image_im = image_im.convert(original_mode)

    return image_im


if __name__ == '__main__':
    run()
