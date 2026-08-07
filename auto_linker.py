import os
import re
import random

# Get all HTML files in your root directory
files = [f for f in os.listdir('.') if f.endswith('.html') and f != "index.html"]
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

# Process internal linking loops
for current_page in all_pages:
    current_filename = current_page["filename"]
    
    # Create a link pool excluding the current page so it never links to itself
    pool = [p for p in all_pages if p["slug"] != current_page["slug"]]
    
    # Secure exactly 5 random pages from the entire database pool
    sample_size = min(5, len(pool))
    top_related = random.sample(pool, sample_size) if sample_size > 0 else []
    
    if not top_related:
        continue

    # Construct a clean, stylized HTML related linking element with strict layout constraints
    linking_html = '\n<div class="related-guides" style="margin-top: 40px; padding: 15px; background-color: #f1f8e9; border-top: 2px solid #4CAF50; border-radius: 4px; display: block; clear: both; width: 100%; box-sizing: border-box;">\n'
    linking_html += '    <h3 style="margin-top: 0; color: #2e7d32;">Recommended Plant Guides</h3>\n    <ul style="padding-left: 20px; margin-bottom: 0;">\n'
    
    for item in top_related:
        linking_html += f'        <li><a href="/{item["slug"]}" style="color: #2e7d32; text-decoration: none; font-weight: bold;">{item["title"]}</a></li>\n'
    
    linking_html += '    </ul>\n</div>\n'

    # Re-open and apply the dynamic injection
    with open(current_filename, "r", encoding="utf-8") as f:
        file_content = f.read()

    # Clean up any old structural links or related-guides blocks left over from earlier test runs
    file_content = re.sub(r'<div class=["\']related-guides["\'].*?</div>', '', file_content, flags=re.DOTALL)

    # CRITICAL POSITION FIX: Drop the box inside the main container element right before it closes
    if '</article>' in file_content:
        file_content = file_content.replace('</article>', f'{linking_html}</article>')
    elif '</div>\n\n<footer' in file_content:
        file_content = file_content.replace('</div>\n\n<footer', f'{linking_html}</div>\n\n<footer')
    elif '</div>\n<footer' in file_content:
        file_content = file_content.replace('</div>\n<footer', f'{linking_html}</div>\n<footer')
    elif '</body>' in file_content:
        file_content = file_content.replace('</body>', f'{linking_html}</body>')

    with open(current_filename, "w", encoding="utf-8") as f:
        f.write(file_content)

print(f"Successfully random-linked exactly 5 pages across all {total_pages} site URLs!")
