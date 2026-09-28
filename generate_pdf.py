import os
import sys
from playwright.sync_api import sync_playwright

def generate_pdf():
    html_path = os.path.abspath(r"C:\Users\admin\.gemini\antigravity\scratch\institutional_design\docs\ssrn_paper.html")
    pdf_path = os.path.abspath(r"C:\Users\admin\.gemini\antigravity\scratch\institutional_design\docs\a2a_institutional_dynamics_ssrn.pdf")
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    print(f"Loading HTML: {html_path}")
    print(f"Target PDF: {pdf_path}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=chrome_path, headless=True)
        page = browser.new_page()
        
        # Navigate to local HTML file
        page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
        
        # Wait for MathJax typesetting
        print("Waiting for MathJax typesetting...")
        try:
            page.wait_for_function("() => window.MathJax && window.MathJax.startup && window.MathJax.startup.promise", timeout=15000)
            page.evaluate("() => window.MathJax.startup.promise")
        except Exception as e:
            print(f"Warning on MathJax wait: {e}")
            
        page.wait_for_timeout(3000)
        
        # SSRN standard header and footer templates
        header_template = """
        <div style="font-size: 8pt; font-family: 'Times New Roman', Times, serif; color: #555555; width: 100%; text-align: right; padding-right: 0.95in;">
            Dyachkov &middot; Behavioral Institutionalism of the Agent-to-Agent (A2A) Economy
        </div>
        """
        
        footer_template = """
        <div style="font-size: 8pt; font-family: 'Times New Roman', Times, serif; color: #555555; width: 100%; display: flex; justify-content: space-between; padding: 0 0.95in;">
            <span>Electronic copy available at: https://ssrn.com/abstract=6742298</span>
            <span>Page <span class="pageNumber"></span> of <span class="totalPages"></span></span>
        </div>
        """
        
        print("Generating SSRN PDF...")
        page.pdf(
            path=pdf_path,
            format="Letter",
            print_background=True,
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            margin={
                "top": "0.95in",
                "bottom": "0.95in",
                "left": "0.95in",
                "right": "0.95in"
            }
        )
        
        browser.close()
        
    print(f"PDF generated successfully at: {pdf_path}")
    if os.path.exists(pdf_path):
        size_kb = os.path.getsize(pdf_path) / 1024
        print(f"File size: {size_kb:.2f} KB")

if __name__ == "__main__":
    generate_pdf()
