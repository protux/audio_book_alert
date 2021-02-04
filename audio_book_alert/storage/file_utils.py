from pathlib import Path


def make_sure_file_exists(path_to_file: str):
    path_to_file = Path(path_to_file)
    directory_to_store_file = path_to_file.parent

    if not directory_to_store_file.is_dir():
        directory_to_store_file.mkdir(parents=True, exist_ok=True)
    if not path_to_file.is_file():
        path_to_file.touch()
        return True
    return False
