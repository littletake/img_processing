import piexif
from PIL import Image

from src.domain.repository.main import Repository


class SimplyPersistence(Repository):
    def save(self, path_original_img, path_new_img):
        """
        名称を日時に変更した画像の保存
        """
        # 改名作業と新規写真の作成
        img = Image.open(path_original_img)
        with Image.new(img.mode, img.size) as dst:
            dst.putdata(img.getdata())
            dst.save(path_new_img, quality=95)

        # exif情報のコピー
        piexif.transplant(path_original_img, path_new_img)


class GPSPersistence(Repository):
    def save(self, path_original_img, path_new_img, exif_bytes):
        """
        名称を日時に変更しジオタグを付与した画像の保存
        """
        # 改名作業と新規写真の作成
        img = Image.open(path_original_img)
        with Image.new(img.mode, img.size) as dst:
            dst.putdata(img.getdata())
            dst.save(path_new_img, quality=95)

        # ジオタグの追加
        piexif.insert(exif_bytes, path_new_img)
