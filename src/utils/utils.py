import shutil
from typing import Union
from pathlib import Path
import pandas as pd


def subdirectories(path: Union[str, Path]):
    return [p for p in Path(path).iterdir() if p.is_dir()]


def file_paths(folder: Union[str, Path]):
    return [p for p in Path(folder).iterdir() if p.is_file()]


def delete_folder(path: Union[str, Path]):
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def time_now():
    return pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
