import os

from libxmp import XMPMeta


def parse_xmp(xmp_string):
    xmp = XMPMeta(xmp_str=xmp_string)

    # Define namespaces
    ns_xmp = "http://ns.adobe.com/xap/1.0/"
    ns_tiff = "http://ns.adobe.com/tiff/1.0/"
    ns_exif = "http://ns.adobe.com/exif/1.0/"
    ns_exif_ex = "http://cipa.jp/exif/1.0/"
    ns_dc = "http://purl.org/dc/elements/1.1/"
    ns_crs = "http://ns.adobe.com/camera-raw-settings/1.0/"
    ns_lr = "http://ns.adobe.com/lightroom/1.0/"

    def property_value(namespace, name):
        if xmp.does_property_exist(namespace, name):
            return xmp.get_property(namespace, name)
        return None

    def array_values(namespace, name):
        count = xmp.count_array_items(namespace, name)
        return [xmp.get_array_item(namespace, name, index) for index in range(1, count + 1)]

    iso = property_value(ns_exif, "ISOSpeedRatings")
    if iso == "" and xmp.does_property_exist(ns_exif, "ISOSpeedRatings[1]"):
        iso = xmp.get_array_item(ns_exif, "ISOSpeedRatings", 1)

    # Extract relevant information
    info = {
        "Creator Tool": property_value(ns_xmp, 'CreatorTool'),
        "Create Date": property_value(ns_xmp, 'CreateDate'),
        "Camera Make": property_value(ns_tiff, 'Make'),
        "Camera Model": property_value(ns_tiff, 'Model'),
        "Lens": property_value(ns_exif_ex, 'LensModel'),
        "ISO": iso,
        "Exposure Time": property_value(ns_exif, 'ExposureTime'),
        "Aperture": property_value(ns_exif, 'FNumber'),
        "Focal Length": property_value(ns_exif, 'FocalLength'),
        "Subject": array_values(ns_dc, 'subject'),
        "Keywords": array_values(ns_lr, 'hierarchicalSubject'),
        "White Balance": property_value(ns_crs, 'WhiteBalance'),
        "Temperature": property_value(ns_crs, 'Temperature'),
        "Tint": property_value(ns_crs, 'Tint'),
        "Exposure": property_value(ns_crs, 'Exposure2012'),
        "Contrast": property_value(ns_crs, 'Contrast2012'),
        "Highlights": property_value(ns_crs, 'Highlights2012'),
        "Shadows": property_value(ns_crs, 'Shadows2012'),
        "Clarity": property_value(ns_crs, 'Clarity2012'),
        "Vibrance": property_value(ns_crs, 'Vibrance'),
        "Saturation": property_value(ns_crs, 'Saturation'),
        "Sharpness": property_value(ns_crs, 'Sharpness'),
        "Noise Reduction": property_value(ns_crs, 'ColorNoiseReduction'),
        "Preset": property_value(ns_crs, 'Look/crs:Name'),
    }

    return info


def display_info(info):
    print("Image Metadata:")
    print("---------------")
    for key, value in info.items():
        print(f"{key}: {value}")


def parse_xmp_file(file_path):
    """
    Reads an XMP file from the given path and parses its contents.

    :param file_path: str, path to the XMP file
    :return: dict, parsed XMP information
    """
    file_path = os.fspath(file_path)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    if not file_path.lower().endswith('.xmp'):
        raise ValueError(f"The file {file_path} is not an XMP file.")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            xmp_string = file.read()

        return parse_xmp(xmp_string)
    except Exception as e:
        print(f"An error occurred while parsing the XMP file: {str(e)}")
        return None
