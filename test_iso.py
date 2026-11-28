import unittest

from main import parse_xmp


class IsoParsingTests(unittest.TestCase):
    def test_iso_formats(self):
        for attribute, elements, expected in [
            ('exif:ISOSpeedRatings="64"', "", "64"),
            ("", "<exif:ISOSpeedRatings><rdf:Seq><rdf:li>80</rdf:li>"
                 "<rdf:li>160</rdf:li></rdf:Seq></exif:ISOSpeedRatings>", "80"),
            ("", "", None),
        ]:
            with self.subTest(expected=expected):
                packet = f"""
                    <x:xmpmeta xmlns:x="adobe:ns:meta/">
                    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
                             xmlns:exif="http://ns.adobe.com/exif/1.0/">
                        <rdf:Description rdf:about="" {attribute}>
                            {elements}
                        </rdf:Description>
                    </rdf:RDF>
                    </x:xmpmeta>"""
                self.assertEqual(parse_xmp(packet)["ISO"], expected)
