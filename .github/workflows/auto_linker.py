import os
import re

# 1. Define your category clusters based on your URL naming patterns
CATEGORIES = {
    "grass": ["grass", "sod", "lawn"],
    "trees": ["tree", "aspen", "calamansi", "fig", "bay-tree", "blossom"],
    "veggies": ["veggies", "vegetable", "tomato", "pepper", "garden"],
    "succulents": ["succulent", "cactus", "adenium", "zz-plant", "indoor"]
}

# Get all HTML files
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

# Process internal linking loops
for current_page in all_pages:
    current_slug = current_page["slug"].lower()
    current_filename = current_page["filename"]
    
    # Identify the matching category group
    matched_category = None
    for cat_name, keywords in CATEGORIES.items():
        if any(keyword in current_slug for keyword in keywords):
            matched_category = cat_name
            break
    
    if not matched_category:
        continue # Skip if it doesn't align with a core category cluster

    # Find relevant internal peers within the same group (excluding itself)
    related_links = [
        p for p in all_pages 
        if p["slug"] != current_page["slug"] and any(k in p["slug"].lower() for k in CATEGORIES[matched_category])
    ]
    
    # Grab the top 3 contextual recommendations
    top_related = related_links[:3]
    if not top_related:
        continue

    # Construct a clean, stylized HTML related linking element
    linking_html = '\n<div class="related-guides" style="margin-top: 40px; padding: 15px; background-color: #f1f8e9; border-top: 2px solid #4CAF50; border-radius: 4px;">\n'
    linking_html += '    <h3 style="margin-top: 0; color: #2e7d32;">Recommended Plant Guides</h3>\n    <ul style="padding-left: 20px; margin-bottom: 0;">\n'
    
    for item in top_related:
        linking_html += f'        <li><a href="/{item["slug"]}" style="color: #2e7d32; text-decoration: none; font-weight: bold;">{item["title"]}</a></li>\n'
    
    linking_html += '    </ul>\n</div>\n'

    # Re-open and apply the dynamic injection
    with open(current_filename, "r", encoding="utf-8") as f:
        file_content = f.read()

    # Strip out any old automated related blocks from prior runs to prevent accumulation loops
    file_content = re.sub(r'<div class=["\']related-guides["\'].*?</div>', '', file_content, flags=re.DOTALL)

    # Inject right above the opening footer tag element safely
    if '<footer' in file_content:
        file_content = file_content.replace('<footer', f'{linking_html}<footer')
    elif '</body>' in file_content:
        file_content = file_content.replace('</body>', f'{linking_html}</body>')

    with open(current_filename, "w", encoding="utf-8") as f:
        f.write(file_content)

print(f"Successfully contextualized links across {len(all_pages)} site pages!")
