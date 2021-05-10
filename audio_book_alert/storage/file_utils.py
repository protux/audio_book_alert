from pathlib import Path


def make_sure_file_exists(path_to_file: str):
    file_path = Path(path_to_file)
    directory_to_store_file = file_path.parent

    if not directory_to_store_file.is_dir():
        directory_to_store_file.mkdir(parents=True, exist_ok=True)
    if not file_path.is_file():
        file_path.touch()
        return True
    return False
