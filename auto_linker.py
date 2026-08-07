import os
import re

# Get all HTML files in alphabetical order to lock in a permanent list sequence
files = sorted([f for f in os.listdir('.') if f.endswith('.html') and f != "index.html"])
all_pages = []

# Map out every page's URL and human-readable Title
for filename in files:
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()
    
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    if title_match:
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip().rstrip('?')
        slug = filename.replace('.html', '')
        all_pages.append({"slug": slug, "title": title, "filename": filename})

total_pages = len(all_pages)

# Process internal linking using a deterministic circular offset loop
for i, current_page in enumerate(all_pages):
    current_filename = current_page["filename"]
    
    # Select the next 5 pages in the list index sequence
    top_related = []
    for offset in range(1, 6):
        next_index = (i + offset) % total_pages
        if all_pages[next_index]["slug"] != current_page["slug"]:
            top_related.append(all_pages[next_index])
    
    if not top_related:
        continue

    # Construct a clean, stylized HTML related linking element with clear block margins
    linking_html = '\n<div class="related-guides" style="margin-top: 40px; padding: 15px; background-color: #f1f8e9; border-top: 2px solid #4CAF50; border-radius: 4px; clear: both; width: 100%; box-sizing: border-box;">\n'
    linking_html += '    <h3 style="margin-top: 0; color: #2e7d32;">Recommended Plant Guides</h3>\n    <ul style="padding-left: 20px; margin-bottom: 0;">\n'
    
    for item in top_related:
        linking_html += f'        <li><a href="/{item["slug"]}" style="color: #2e7d32; text-decoration: none; font-weight: bold;">{item["title"]}</a></li>\n'
    
    linking_html += '    </ul>\n</div>\n'

    # Re-open and apply the dynamic injection
    with open(current_filename, "r", encoding="utf-8") as f:
        file_content = f.read()

    # Strip out any old automated related blocks from prior runs to prevent accumulation loops
    file_content = re.sub(r'<div class=["\']related-guides["\'].*?</div>', '', file_content, flags=re.DOTALL)

    # FIX: Inject directly inside the closing </article> tag so it stays inside your main text layout bounds
    if '</article>' in file_content:
        file_content = file_content.replace('</article>', f'{linking_html}</article>')
    elif '<footer' in file_content:
        file_content = file_content.replace('<footer', f'{linking_html}<footer')
    elif '</body>' in file_content:
        file_content = file_content.replace('</body>', f'{linking_html}</body>')

    with open(current_filename, "w", encoding="utf-8") as f:
        f.write(file_content)

print(f"Successfully established a layout-safe circular link mesh across all {total_pages} pages!")
