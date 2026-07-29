import os
import re
from xml.sax.saxutils import escape

def extract_meta(html_content):
  # Extract title
  title_match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE | re.DOTALL)
  title = title_match.group(1).strip() if title_match else "Untitled Article"

# Extract description from meta tag (handles any attribute order)
desc_match = re.search(r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']', html_content, re.IGNORECASE | re.DOTALL)
if not desc_match:
    desc_match = re.search(r'<meta\s+[^>]*content=["\'](.*?)["\'][^>]*name=["\']description["\']', html_content, re.IGNORECASE | re.DOTALL)

 description = desc_match.group(1).strip() if desc_match else "No description available."

 return escape(title), escape(description)

def main():
base_url = "https://theplantmatrix.com"

 # Start building the XML string
 xml_output = '<?xml version="1.0" encoding="UTF-8" ?>\n'
 xml_output += '<rss version="2.0">\n'
 xml_output += '<channel>\n'
 xml_output += ' <title>The Plant Matrix | Care Guides</title>\n'
 xml_output += f' <link>{base_url}</link>\n'
 xml_output += ' <description>Comprehensive plant watering and care schedules.</description>\n\n'

# Scan current directory for HTML files (excluding index, 404, etc.)
files = sorted([f for f in os.listdir('.') if f.endswith('.html')])

for filename in files:
   if filename in ['index.html', '404.html', 'feed.html']:
   continue

try:
   with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
   content = f.read()

   title, description = extract_meta(content)

   # Combines base URL with filename for a unique link (e.g., https://theplantmatrix.comhow-to-water.html)
  article_link = f"{base_url}{filename}"

  # Append item to XML block
  xml_output += ' <item>\n'
  xml_output += f' <title>{title}</title>\n'
  xml_output += f' <link>{article_link}</link>\n'
  xml_output += f' <description>{description}</description>\n'
  xml_output += ' </item>\n\n'
except Exception as e:
  print(f"Error processing {filename}: {e}")

# Properly close out the XML tags
xml_output += '</channel>\n'
xml_output += '</rss>'

# Save the generated content directly to feed.xml
with open('feed.xml', 'w', encoding='utf-8') as f:
f.write(xml_output)

print("Successfully generated feed.xml!")

if __name__ == "__main__":
main()
