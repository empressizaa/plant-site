import os
import re

# Get all files in your root directory
files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    # Skip index.html if you don't want it to have individual canonical formatting
    if filename == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # Create the perfect clean link based on the actual filename
    slug = filename.replace('.html', '')
    perfect_canonical = f'<link rel="canonical" href="https://theplantmatrix.com{slug}">'

    # 1. FIX THE CANONICAL TAG: Strip out any existing broken or empty canonical tags completely
    content = re.sub(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']\s*/?>', '', content, flags=re.IGNORECASE)
    
    # Inject the perfect fresh canonical link directly right under the <head> tag
    if '<head>' in content:
        content = content.replace('<head>', f'<head>\n    {perfect_canonical}')

    # 2. INJECT PRIVACY POLICY FOOTER: Add the footer link right before the closing body tag
    footer_html = '\n<footer style="text-align: center; padding: 20px 0; margin-top: 40px; font-size: 14px;"><a href="/privacy-policy" style="color: #555; text-decoration: none;">Privacy Policy</a></footer>\n'
    if '</body>' in content and 'privacy-policy' not in content:
        content = content.replace('</body>', footer_html + '</body>')

    # Save the updated content back down safely
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully fixed canonical tags and injected privacy policies across all pages!")
