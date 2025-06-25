from io import BufferedReader
from pathlib import Path
import sys


def is_tgm4_replay(magic_bytes: bytes) -> bool:
    return magic_bytes == b'TGRP'


def read_version(file_path: Path, file: BufferedReader) -> int:
    return 1337


def find_versions(base_directory: Path) -> None:
    """
    Search for and process files meeting specific criteria in their first four bytes.

    Args:
        base_directory: The root directory to start the search from.
    """
    last_dir = None
    for file_path in base_directory.rglob('*.bin'):
        if file_path.is_file():
            this_dir = file_path.relative_to(base_directory).parts[0]
            if this_dir != last_dir:
                if last_dir:
                    print()
                print(this_dir)
                print("-" * 80)

            last_dir = this_dir

            try:
                new_name = None
                with open(file_path, 'rb') as f:
                    magic_bytes = f.read(4)
                    if is_tgm4_replay(magic_bytes):
                        version = f.read(4)
                        mode = file_path.relative_to(base_directory).parts[-2]
                        type = file_path.relative_to(base_directory).parts[-3]
                        if mode != 'versus':
                            f.seek(0x28)
                            tgm_mode = int.from_bytes(f.read(1))
                            tgm_suffix = "tgm" if tgm_mode else "std"
                            type_suffix = None
                            suffix = "_" + tgm_suffix
                            if mode == "konoha":
                                type_suffix = "easy" if type == "exhibition" else "hard"

                            if type_suffix:
                                suffix = "_" + type_suffix + suffix

                            if not file_path.stem.endswith(suffix):
                                # rename
                                new_name = file_path.stem + suffix + file_path.suffix

                        version = int.from_bytes(version, 'little')
                        file_name = file_path.relative_to(base_directory)
                        if new_name:
                            file_name = file_name.with_name(new_name)

                        print(f"0x{version:08X}", file_name)

                if RENAME_FILES and new_name:
                    file_path.rename(file_path.with_name(new_name))
            except Exception as e:
                print(f"Error processing {file_path}: {e}")


if __name__ == "__main__":
    RENAME_FILES = False

    if len(sys.argv) != 2:
        print("Usage: python version_checker.py <base_directory>")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    if not base_dir.is_dir():
        print(f"Error: {base_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    find_versions(base_dir)
