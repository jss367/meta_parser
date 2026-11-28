from pathlib import Path

from libxmp import XMPMeta
from libxmp.utils import object_to_dict


def display_info(info):
    print("Image Metadata:")
    print("---------------")
    for key, value in info.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    xmp_file_path = Path(__file__).resolve().parent / "data" / "simple_sample.xmp"
    packet = XMPMeta(xmp_str=xmp_file_path.read_text(encoding="utf-8"))
    display_info(object_to_dict(packet))
