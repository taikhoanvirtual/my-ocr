import ocrmypdf
from ocrmypdf.hocrtransform import HocrTransform
def convert_hocr_to_pdf(hocr_file, img_file, output_pdf, do_strip=False):

    hocr = HocrTransform(hocr_filename=hocr_file, dpi=300, do_strip=do_strip)
    hocr.to_pdf(out_filename=output_pdf,
                 image_filename=img_file, 
                )
    print(f"Converted {hocr_file} and {img_file} to {output_pdf}")

"""
def __init__(
        self,
        *,
        hocr_filename: str | Path,
        dpi: float,
        debug: bool = False,
        fontname: Name = Name("/f-0-0"),
        font: Font = GlyphlessFont(),
        debug_render_options: DebugRenderOptions | None = None,
        do_strip: bool = True,
    ):

self.do_strip = do_strip

def _do_line_word(
        self,
        canvas: Canvas,
        line_matrix: Matrix,
        text: Text,
        fontsize: float,
        elem: Element | None,
        next_elem: Element | None,
        text_direction: TextDirection,
        inject_word_breaks: bool,
    ):
        Render the text for a single word.
        if elem is None:
            return
        if self.do_normalize:
            elemtxt = self.normalize_text(self._get_element_text(elem).strip())
"""

if __name__ == "__main__":
    hocr_file = "./temp/a/page0.hocr"
    img_file = "./output_pages/a/page1.png"
    output_pdf = "page1.pdf"
    convert_hocr_to_pdf(hocr_file, img_file, output_pdf)


