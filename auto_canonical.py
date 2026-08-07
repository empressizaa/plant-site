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
        # Flexible match that handles case-sensitivity and internal tag attributes (like classes)
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
        p_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.DOTALL | re.IGNORECASE)
        
        schema_html = ""
        if title_match and p_match:
            schema_title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            schema_desc = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
            
            schema_html = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [{{
        "@type": "Question",
        "name": "{schema_title}",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{schema_desc}"
        }}
      }}]
    }}
    </script>"""

        # Inject both your canonical tag AND the schema tag right below <head>
        content = content.replace('<head>', f'<head>\n    {perfect_canonical}{schema_html}')

    # 3. FOOTER SAFETY CHECK
    footer_html = '\n<footer style="text-align: center; padding: 20px 0; margin-top: 40px; font-size: 14px;"><a href="/about" style="color: #555; text-decoration: none; margin-right: 20px;">About Us</a> | <a href="/privacy-policy" style="color: #555; text-decoration: none; margin-left: 20px;">Privacy Policy</a></footer>\n'
    if '</body>' in content and 'privacy-policy' not in content:
        content = content.replace('</body>', footer_html + '</body>')

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully compressed whitespace and polished all 420 files!")
