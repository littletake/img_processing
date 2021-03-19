# domain層
# ロジックの根幹
from typing import Any


class Exif(object):
    def __init__(
        self,
        name: str,
        gps: Any,  # gpsデータのない場合はNoneになるため
        path_original_img: str,
    ) -> None:
        self.name = name
        self.gps = gps
        self.path_original_img = path_original_img
