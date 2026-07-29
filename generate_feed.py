import os
import re
from xml.sax.saxutils import escape

def extract_meta(html_content):
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
   title = title_match.group(1).strip() if title_match else "Untitled Article"
 
   # Extract description from meta tag
   desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html_content, re.IGNORECASE | re.DOTALL)
   if not desc_match:
        # Try variation with content first
        desc_match = re.search(r'<meta\s+content=["\'](.*?)["\']\s+name=["\']description["\']', html_content, re.IGNORECASE | re.DOTALL)
   description = desc_match.group(1).strip() if desc_match else "No description available."
 
   return escape(title), escape(description)

def main():
 base_url = "https://theplantmatrix.com"
 items_xml = []
 
 # Scan current directory for HTML files (excluding index, 404, etc.)
 files = sorted([f for f in os.listdir('.') if f.endswith('.html')])
 
 for filename in files:
     if filename in ['index.html', '404.html', 'feed.xml']:
        continue
 
    with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
         content = f.read()
 
    title, description = extract_meta(content)
    link = f"{base_url}{filename}"
 
    item = f""" <item>
   <title>{title}</title>
   <link>{link}</link>
   <description>{description}</description>
 </item>"""
   items_xml.append(item)
 
   # Combine into full RSS feed structure
   rss_feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
 <channel>
    <title>The Plant Matrix | Care Guides</title>
    <link>{base_url}</link>
    <description>Comprehensive plant watering and care schedules.</description>
\n""" + "\n".join(items_xml) + """
   </channel>
</rss>"""

    with open('feed.xml', 'w', encoding='utf-8') as f:
        f.write(rss_feed)
    print("Successfully updated feed.xml with all articles!")

if __name__ == "__main__":
   main()
