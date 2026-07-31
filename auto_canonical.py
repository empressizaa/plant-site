import os
import re

# Get all HTML files in your root directory
files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    # Skip the main index page to preserve your custom grid formatting
    if filename == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Create the clean canonical link based on the true file slug
    slug = filename.replace('.html', '')
    perfect_canonical = f'<link rel="canonical" href="https://theplantmatrix.com{slug}">'

    # 1. FIX CANONICALS: Find and completely delete any existing messy, broken, or empty canonical links
    content = re.sub(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']\s*/?>', '', content, flags=re.IGNORECASE)
    
    # Inject the pristine, accurate canonical link directly under the opening <head> tag
    if '<head>' in content:
        content = content.replace('<head>', f'<head>\n    {perfect_canonical}')

    # 2. INJECT BOTH LINKS INTO FOOTER: Add About Us and Privacy Policy right before the closing body tag
    footer_html = '\n<footer style="text-align: center; padding: 20px 0; margin-top: 40px; font-size: 14px;"><a href="/about" style="color: #555; text-decoration: none; margin-right: 20px;">About Us</a> | <a href="/privacy-policy" style="color: #555; text-decoration: none; margin-left: 20px;">Privacy Policy</a></footer>\n'
    if '</body>' in content and 'privacy-policy' not in content:
        content = content.replace('</body>', footer_html + '</body>')

    # Save the polished content safely back down
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully fixed canonical tags and injected privacy policies across all pages!")
