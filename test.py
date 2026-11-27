from pathlib import Path

from main import display_info, parse_xmp_file


if __name__ == "__main__":
    xmp_file_path = Path(__file__).resolve().parent / "data" / "simple_sample.xmp"
    display_info(parse_xmp_file(xmp_file_path))
