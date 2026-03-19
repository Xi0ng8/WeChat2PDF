import sys
import argparse
from wx_converter import process_article as process_wechat
from x_converter import process_x_post as process_x

def main():
    parser = argparse.ArgumentParser(description="Convert WeChat articles or X posts to PDF.")
    parser.add_argument("url", help="Target URL (WeChat article or X post)")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    args = parser.parse_args()

    url = args.url
    if "mp.weixin.qq.com" in url:
        print("Detected WeChat URL. Processing...")
        process_wechat(url, args.output)
    elif "x.com" in url or "twitter.com" in url:
        print("Detected X/Twitter URL. Processing...")
        process_x(url, args.output)
    else:
        print("Unknown URL type. Attempting generic processing with X converter (Playwright)...")
        # X converter is more generic for JS-heavy sites
        process_x(url, args.output)

if __name__ == "__main__":
    main()
