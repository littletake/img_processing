# -*- coding: utf-8 -*-
import argparse
import os

from src.domain.repository.main import Repository
from src.usecase.main import Usecase_abs, Usecase
from src.interface.main import Interface_abs, Interface
from src.infra.main import SimplyPersistence, GPSPersistence

# ---
# args
# ---
parser = argparse.ArgumentParser()
parser.add_argument(
    "--img",
    type=str,
    help="画像ディレクトリの名称"
)
parser.add_argument(
    "--gps",
    type=str,
    help="GPSファイルの名称"
)
args = parser.parse_args()
dict_args = vars(args)

# path
DIR_PATH = os.path.dirname(__file__)

# ---
# object
# ---
if dict_args["gps"] is None:
    repo: Repository = SimplyPersistence()
else:
    repo: Repository = GPSPersistence()
usecase: Usecase_abs = Usecase(repo)
interface: Interface_abs = Interface(usecase)

# 実行
interface.create(
    DIR_PATH,
    dict_args
)
