import os
import re

print("Starting global sweep to remove all recommendation structures...")
count = 0

for filename in os.listdir("."):
    if not filename.endswith(".html") or filename.lower() == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    # Capture original state to check if changes occurred
    original_html = html

    # 1. Wipe comment-bounded blocks completely
    html = re.sub(r'<!-- RELATED GUIDES START -->.*?<!-- RELATED GUIDES END -->', '', html, flags=re.DOTALL | re.IGNORECASE)
    
    # 2. Wipe any loose/orphan raw division layouts
    html = re.sub(r'<div class="related-guides"[\s\S]*?</div>', '', html, flags=re.DOTALL | re.IGNORECASE)

    # 3. Double-check for nested duplicates that might have leaked outside comments
    html = re.sub(r'<div class="related-guides"[\s\S]*?(?=<footer\b|</body>)', '', html, flags=re.DOTALL | re.IGNORECASE)

    # Only save if the layout actually contained messy blocks
    if html != original_html:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1

print(f"Sweep complete! Successfully stripped messy structures out of {count} files.")
