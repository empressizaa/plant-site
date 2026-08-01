import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    if filename == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # SAFETY CHECK: If the file is corrupted, completely empty, or has less than 5 lines, 
    # DO NOT let the script overwrite it with blank data. Skip it entirely.
    if len(content.strip()) < 50 or '<body' not in content.lower():
        print(f"⚠️ Skipping corrupted or empty file to prevent data loss: {filename}")
        continue

    slug = filename.replace('.html', '')
    perfect_canonical = f'<link rel="canonical" href="https://theplantmatrix.com/{slug}">'

    # Clean out old canonicals safely
    content = re.sub(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']*)["\']\s*/?>', '', content, flags=re.IGNORECASE)
    
    if '<head>' in content:
        content = content.replace('<head>', f'<head>\n    {perfect_canonical}')

    footer_html = '\n<footer style="text-align: center; padding: 20px 0; margin-top: 40px; font-size: 14px;"><a href="/about" style="color: #555; text-decoration: none; margin-right: 20px;">About Us</a> | <a href="/privacy-policy" style="color: #555; text-decoration: none; margin-left: 20px;">Privacy Policy</a></footer>\n'
    if '</body>' in content and 'privacy-policy' not in content:
        content = content.replace('</body>', footer_html + '</body>')

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Finished processing canonical tags safely!")
