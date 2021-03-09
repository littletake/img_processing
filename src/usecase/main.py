from src.domain.repository.main import Repository


class Usecase():
    def __init__(
        self,
        path_original_img: str,
        repo: Repository
    ) -> None:
        self.repo = repo

# TODO: どう書けばいいかわからない
