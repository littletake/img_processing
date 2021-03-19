# infra層
# 画像の出力
# Exifクラスをexifに、名前を日付にして新規の画像を作成
import piexif
from PIL import Image

from src.domain.model.main import Exif
from src.domain.repository.main import Repository
from utils.add_gps import add_gpsinfo


# 名称を日時に変更した画像の保存
class SimplyPersistence(Repository):
    def save_img(
        self,
        exif
    ) -> None:
        # 改名作業と新規写真の作成
        img = Image.open(exif.path_original_img)
        with Image.new(img.mode, img.size) as dst:
            dst.putdata(img.getdata())
            dst.save(exif.name, quality=95)

    def add_gps(
        self,
        exif,
    ) -> None:
        # exif情報のコピー
        piexif.transplant(exif.path_original_img, exif.name)


# 名称を日時に変更しジオタグを付与した画像の保存
class GPSPersistence(Repository):
    def save_img(
        self,
        exif
    ) -> None:
        # 改名作業と新規写真の作成
        img = Image.open(exif.path_original_img)
        with Image.new(img.mode, img.size) as dst:
            dst.putdata(img.getdata())
            dst.save(exif.name, quality=95)

    def add_gps(
        self,
        exif,
    ) -> None:
        # 新規写真にジオタグを付与
        exif_dict = piexif.load(exif.path_original_img)
        exif_bytes = add_gpsinfo(
            exif.path_original_img,
            exif.gps,
            exif_dict
        )
        piexif.insert(exif_bytes, exif.name)
