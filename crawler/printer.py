from typing import List

import os


def create_directory(directory: str) -> None:
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print(f"Error: Creating directory {directory}")


def print(directory: str, contents: List[str]) -> None:
    create_directory(directory)
    with open(f"{directory}/result.txt", mode="w", encoding="utf8") as f:
        f.write("\n\n".join(contents))
