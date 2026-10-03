"""Headless-Chromium renderer: HTML/SVG files -> PNG (optionally transparent) and PDF."""
import os
import pathlib
from playwright.sync_api import sync_playwright


def file_url(p):
    return pathlib.Path(os.path.abspath(p)).as_uri()


class Renderer:
    def __enter__(self):
        self._pw = sync_playwright().start()
        self.browser = self._pw.chromium.launch()
        return self

    def __exit__(self, *a):
        self.browser.close()
        self._pw.stop()

    def png(self, src_path, out_png, w, h, transparent=False, scale=1.0, wait_ms=0):
        ctx = self.browser.new_context(viewport={'width': int(w), 'height': int(h)}, device_scale_factor=scale)
        page = ctx.new_page()
        page.goto(file_url(src_path))
        page.evaluate('document.fonts.ready')
        if wait_ms:
            page.wait_for_timeout(wait_ms)
        os.makedirs(os.path.dirname(os.path.abspath(out_png)), exist_ok=True)
        page.screenshot(path=out_png, omit_background=transparent, full_page=False,
                        clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        ctx.close()

    def png_bytes_from_html(self, html, w, h, transparent=True, base_dir=None):
        """Render an HTML string (written to a temp file next to base_dir) and return PNG bytes."""
        import tempfile
        d = base_dir or tempfile.gettempdir()
        p = os.path.join(d, '_tmp_render.html')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(html)
        ctx = self.browser.new_context(viewport={'width': int(w), 'height': int(h)})
        page = ctx.new_page()
        page.goto(file_url(p))
        page.evaluate('document.fonts.ready')
        b = page.screenshot(omit_background=transparent, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
        ctx.close()
        return b

    def pdf(self, src_path, out_pdf, width='8.5in', height='11in'):
        ctx = self.browser.new_context()
        page = ctx.new_page()
        page.goto(file_url(src_path))
        page.evaluate('document.fonts.ready')
        page.wait_for_timeout(300)
        page.pdf(path=out_pdf, width=width, height=height, print_background=True,
                 margin={'top': '0', 'right': '0', 'bottom': '0', 'left': '0'}, prefer_css_page_size=True)
        ctx.close()
