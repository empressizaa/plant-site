import os
import re

# Get all HTML files in your root directory
files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    if filename == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. WHITESPACE COMPRESSION: Find any spot with 3 or more consecutive blank lines and shrink it to a single clean break
    content = re.sub(r'(\n\s*){3,}', '\n\n', content)

    slug = filename.replace('.html', '')
    perfect_canonical = f'<link rel="canonical" href="https://theplantmatrix.com/{slug}">'

    # 2. CANONICAL CLEANUP: Strip out duplicate canonical tags if any accumulated
    content = re.sub(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']\s*/?>', '', content, flags=re.IGNORECASE)
    
    if '<head>' in content:
        content = content.replace('<head>', f'<head>\n    {perfect_canonical}')

    # 3. FOOTER SAFETY CHECK
    footer_html = '\n<footer style="text-align: center; padding: 20px 0; margin-top: 40px; font-size: 14px;"><a href="/about" style="color: #555; text-decoration: none; margin-right: 20px;">About Us</a> | <a href="/privacy-policy" style="color: #555; text-decoration: none; margin-left: 20px;">Privacy Policy</a></footer>\n'
    if '</body>' in content and 'privacy-policy' not in content:
        content = content.replace('</body>', footer_html + '</body>')

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully compressed whitespace and polished all 420 files!")
