import os
import re

print("Starting aggressive targeted sweep to force remove all duplicate blocks...")
count = 0

for filename in os.listdir("."):
    if not filename.endswith(".html") or filename.lower() == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    original_html = html

    # 1. Wipe comment-bounded recommendation boxes
    html = re.sub(r'<!-- RELATED GUIDES START -->.*?<!-- RELATED GUIDES END -->', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # 2. Wipe class-based green containers
    html = re.sub(r'<div class="related-guides"[\s\S]*?</div>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # 3. Targeted Fix: Strip any duplicate blocks leaking out around the navigation links
    # This targets anything matching your exact plant guides design text
    html = re.sub(r'<div[^>]*>\s*<h3[^>]*>\s*Recommended Plant Guides\s*</h3>[\s\S]*?</ul>\s*</div>', '', html, flags=re.IGNORECASE | re.DOTALL)
    html = re.sub(r'<h3[^>]*>\s*Recommended Plant Guides\s*</h3>[\s\S]*?</ul>', '', html, flags=re.IGNORECASE | re.DOTALL)

    # Save only if a broken layout block was successfully discovered and deleted
    if html != original_html:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1

print(f"Sweep complete! Successfully stripped out duplicate boxes from {count} files.")
