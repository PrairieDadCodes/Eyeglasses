import sys

from format_replay import load_replay
from pathlib import Path


def find_versions(base_directory: Path) -> None:
    """
    Search for and process files meeting specific criteria in their first four bytes.

    Args:
        base_directory: The root directory to start the search from.
    """
    last_dir = None

    for file_path in base_directory.rglob('*.bin'):
        if file_path.is_file():
            print(file_path)
            this_dir = file_path.relative_to(base_directory).parts[0]
            if this_dir != last_dir:
                if last_dir:
                    print()
                print(this_dir)
                print("-" * 80)

            last_dir = this_dir

            try:
                load_replay(file_path)
            except Exception as e:
                print(f"{type(e).__name__} processing '{file_path}':\n{e}")
                raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python version_checker.py <base_directory>")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    if not base_dir.is_dir():
        print(f"Error: {base_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    find_versions(base_dir)
