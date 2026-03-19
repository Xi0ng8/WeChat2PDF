import os
import argparse
import re
import sys
from playwright.sync_api import sync_playwright

def sanitize_filename(name):
    # Remove invalid characters and limit length
    sanitized = re.sub(r'[\\/*?:"<>|]', "", name).strip()
    return sanitized[:100] if sanitized else "X_Post"

def process_x_post(url, output_dir="."):
    print(f"Processing X Post: {url}")
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        # Use a desktop UA to get the full layout
        context = browser.new_context(
            viewport={'width': 1280, 'height': 1600},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        
        print("Navigating to page...")
        try:
            # X can be slow, especially with networkidle. Using domcontentloaded + timeout.
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print(f"Navigation warning: {e}")

        # Wait for the main tweet to render
        try:
            # Standard tweet article selector
            page.wait_for_selector('article[data-testid="tweet"]', timeout=30000)
            print("Detected tweet content.")
        except Exception:
            print("Warning: Could not detect standard tweet element, attempting best-effort capture.")

        # Let lazy-loaded content or images load
        page.wait_for_timeout(5000)

        # Extract title/text for filename
        try:
            title_text = page.title()
            # Remove "X | " or similar prefix if present
            title_text = re.sub(r'^.*?on X: ', '', title_text)
            title_text = re.sub(r'^X \/ ', '', title_text)
        except:
            title_text = "X_Post_" + url.split('/')[-1]
        
        safe_title = sanitize_filename(title_text)
        pdf_filename = f"{safe_title}.pdf"
        pdf_path = os.path.join(output_dir, pdf_filename)

        print(f"Title: {title_text}")

        # Inject CSS to hide sidebars, login bars, and other distractions
        page.evaluate("""() => {
            const selectorsToHide = [
                '[data-testid="sidebarColumn"]',
                '[data-testid="BottomBar"]',
                'nav[aria-label="Primary"]',
                '#layers', // This handles many overlays including login wall
                'div[role="progressbar"]',
                '[data-testid="SideNav_AccountSwitcher_Button"]',
                'header[role="banner"]'
            ];
            
            selectorsToHide.forEach(selector => {
                const elements = document.querySelectorAll(selector);
                elements.forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                });
            });

            // Adjust main column to take center stage
            const main = document.querySelector('main');
            if (main) {
                main.style.width = '100%';
                main.style.maxWidth = '100%';
                main.style.display = 'flex';
                main.style.justifyContent = 'center';
            }
            
            // Try to find the inner column and make it wider for the PDF
            const primaryColumn = document.querySelector('[data-testid="primaryColumn"]');
            if (primaryColumn) {
                primaryColumn.style.width = '100%';
                primaryColumn.style.maxWidth = '700px';
                primaryColumn.style.margin = '0 auto';
            }
        }""")

        # Add a bit of padding for the PDF
        page.add_style_tag(content="""
            @media print {
                body {
                    padding: 20px;
                }
            }
        """)

        print("Generating PDF...")
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"}
        )
        
        print(f"=> Saved PDF to: {pdf_path}")
        browser.close()
        return pdf_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert X (Twitter) post to PDF.")
    parser.add_argument("url", help="Target X post URL")
    parser.add_argument("-o", "--output", default=".", help="Output directory")
    args = parser.parse_args()
    
    try:
        process_x_post(args.url, args.output)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
