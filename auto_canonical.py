import os
import re

# Scan the directory for all HTML files
files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    # Skip the homepage
    if filename == 'index.html':
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Generate the clean canonical link using the filename slug
    slug = filename.replace('.html', '')
    canonical_link = f'<link rel="canonical" href="https://theplantmatrix.com{slug}" />'
    
    # If a canonical tag exists, update it; otherwise, insert it in the <head>
    if 'rel="canonical"' in content:
        content = re.sub(r'<link rel="canonical" href="[^"]+" */?>', canonical_link, content)
    else:
        content = content.replace('<head>', f'<head>\n    {canonical_link}')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Successfully processed {len(files) - 1} article pages!")
