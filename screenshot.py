import argparse
from playwright.sync_api import sync_playwright

def take_screenshot(url, output, width=1280, height=720, zoom=1.0, wait=0, scroll=False):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=zoom
        )
        page.goto(url, wait_until="networkidle")

        if scroll:
            # Scroll to bottom to trigger lazy-loaded content
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(500)
            # Scroll back to top
            page.evaluate("window.scrollTo(0, 0)")

        if wait > 0:
            page.wait_for_timeout(wait)

        page.screenshot(path=output, full_page=True)
        browser.close()
    print(f"Screenshot saved: {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take a full-page screenshot")
    parser.add_argument("url", nargs="?", default="http://localhost:5000", help="URL to screenshot")
    parser.add_argument("-o", "--output", default="screenshot.png", help="Output filename")
    parser.add_argument("-w", "--width", type=int, default=1280, help="Viewport width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Viewport height (default: 720)")
    parser.add_argument("-z", "--zoom", type=float, default=1.0, help="Zoom/scale factor (default: 1.0)")
    parser.add_argument("--wait", type=int, default=0, help="Extra wait time in ms after page load")
    parser.add_argument("--scroll", action="store_true", help="Scroll to bottom first (triggers lazy content)")
    args = parser.parse_args()

    take_screenshot(args.url, args.output, args.width, args.height, args.zoom, args.wait, args.scroll)
