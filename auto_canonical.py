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
    
    # Case-insensitive check for the opening head tag
    head_match = re.search(r'<head[^>]*>', content, re.IGNORECASE)
    if head_match:
        # Flexible match for any H1 header variant
        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
        
        schema_html = ""
        if title_match:
            schema_title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
            
            # Look for the next block of actual text content following the H1 tag
            post_h1_content = content.split(title_match.group(0))[1]
            
            # Extract the first paragraph tag or text container block it can find
            any_text_match = re.search(r'<(p|div|span)[^>]*>(.*?)</\1>', post_h1_content, re.DOTALL | re.IGNORECASE)
            
            if any_text_match:
                schema_desc = re.sub(r'<[^>]+>', '', any_text_match.group(2)).strip()
            else:
                # Absolute fall-back if text container parsing completely fails
                schema_desc = f"Learn how often to water and care for {schema_title} properly."

            # Strip out any newline breaks inside the text content strings to keep JSON parsing happy
            schema_title = schema_title.replace('\n', ' ').replace('"', '\\"')
            schema_desc = schema_desc.replace('\n', ' ').replace('"', '\\"')

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

        # Inject both your canonical tag AND the schema tag right below the head tag variation found
        original_head_tag = head_match.group(0)
        content = content.replace(original_head_tag, f'{original_head_tag}\n    {perfect_canonical}{schema_html}')

    # 3. FOOTER SAFETY CHECK
    footer_html = '\n<footer style="text-align: center; padding: 20px 0; margin-top: 40px; font-size: 14px;"><a href="/about" style="color: #555; text-decoration: none; margin-right: 20px;">About Us</a> | <a href="/privacy-policy" style="color: #555; text-decoration: none; margin-left: 20px;">Privacy Policy</a></footer>\n'
    if '</body>' in content and 'privacy-policy' not in content:
        content = content.replace('</body>', footer_html + '</body>')

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

print("Successfully compressed whitespace and polished all 420 files!")
