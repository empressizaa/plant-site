import os
import re

# Get all HTML files in your root directory
files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    # Always skip the main homepage file
    if filename == 'index.html':
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Create the perfect clean link based on the actual filename
    slug = filename.replace('.html', '')
    perfect_canonical = f'<link rel="canonical" href="https://theplantmatrix.com{slug}">'
    
    # This regex catches ANY canonical tag, no matter what junk text is inside it
    # It will match href="#", href="example.com", or anything else!
    canonical_pattern = r'<link\s+rel=["\']canonical["\']\s+href=["\'][^"\']*["\']\s*/?>'
    
    if re.search(canonical_pattern, content):
        print(f"Replacing broken tag in: {filename}")
        # Overwrite the broken tag with your perfect live URL
        content = re.sub(canonical_pattern, perfect_canonical, content)
    else:
        print(f"No tag found. Injecting new tag in: {filename}")
        # If the tag is completely missing, inject it right under the <head>
        content = content.replace('<head>', f'<head>\n    {perfect_canonical}')
        
    # Save the polished file back to GitHub
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

print("All article files successfully sanitized and fixed!")
