import os
import re

# Get all HTML files in your root directory
files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    if filename == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. WHITESPACE COMPRESSION
    content = re.sub(r'(\n\s*){3,}', '\n\n', content)

    slug = filename.replace('.html', '')
    perfect_canonical = f'<link rel="canonical" href="https://theplantmatrix.com/{slug}">'

    # 2. CLEANUP OLD INJECTIONS: Clear existing canonical tags and schemas
    content = re.sub(r'<link\s+rel=["\']canonical["\'].*?>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<script\s+type=["\']application/ld\+json["\'].*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    # Case-insensitive check for the opening head tag
    head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
    if head_match:
        # Pull your clear H1 title
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
        
        # Pull the text inside your quick-answer box
        answer_match = re.search(r'class=["\']quick-answer["\'][^>]*>(.*?)</div>', content, re.DOTALL | re.IGNORECASE)
        
        schema_html = ""
        if title_match and answer_match:
            schema_title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            schema_desc = re.sub(r'<[^>]+>', '', answer_match.group(1)).replace('Quick Answer:', '').strip()
            
            # AGGRESSIVE SANITIZATION: Collapse all inner linebreaks, tabs, or multi-spaces into a single clean line space
            schema_title = re.sub(r'\s+', ' ', schema_title).replace('"', '\\"')
            schema_desc = re.sub(r'\s+', ' ', schema_desc).replace('"', '\\"')
            
            # Clean up trailing question marks
            schema_title = schema_title.rstrip('?')
            
            schema_html = f"""
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [{{
        "@type": "Question",
        "name": "{schema_title}?",
        "acceptedAnswer": {{
          "@type": "Answer",
          "text": "{schema_desc}"
        }}
      }}]
    }}
    </script>"""

        # Inject exactly ONE canonical tag and ONE clean schema tag right below <head>
        original_head_tag = head_match.group(0)
        content = content.replace(original_head_tag, f'{original_head_tag}\n    {perfect_canonical}{schema_html}')

    # 3. FOOTER SAFETY CHECK
    footer_html = '\n<footer style="text-align: center; padding: 20px 0; margin-top: 40px; font-size: 14px;"><a href="/about" style="color: #555; text-decoration: none; margin-right: 20px;">About Us</a> | <a href="/privacy-policy" style="color: #555; text-decoration: none; margin-left: 20px;">Privacy Policy</a></footer>\n'
    if '</body>' in content and 'privacy-policy' not in content:
        content = content.replace('</body>', footer_html + '</body>')

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully compressed whitespace and polished all 420 files!")
