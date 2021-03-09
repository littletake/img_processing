class Exif(object):
    def __init__(self, gps: str) -> None:
        self.gps = gps


class Img(Exif):
    def __init__(
        self,
        name: str,
        gps: str
    ) -> None:
        self.name: str = name
        self.exif: Exif = (gps)
