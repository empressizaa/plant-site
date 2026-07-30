import os
import xml.etree.ElementTree as ET

# CONFIGURATION
DEFAULT_IMAGE = "https://theplantmatrix.com/logo.png" 

rss_root = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss_root, "channel")

ET.SubElement(channel, "title").text = "The Plant Matrix Feed"
ET.SubElement(channel, "link").text = "https://theplantmatrix.com"
ET.SubElement(channel, "description").text = "Automated plant care updates"

sitemap_path = "sitemap.xml"

if os.path.exists(sitemap_path):
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url_tag in root.findall('ns:url', ns):
            loc = url_tag.find('ns:loc', ns)
            if loc is not None and loc.text:
                page_url = loc.text
                
                if page_url.strip('/') == "https://theplantmatrix.com":
                    continue
                
                slug = page_url.rstrip('/').split('/')[-1]
                clean_title = slug.replace(".html", "").replace("-", " ").title()
                
                item = ET.SubElement(channel, "item")
                ET.SubElement(item, "title").text = clean_title
                ET.SubElement(item, "link").text = page_url
                ET.SubElement(item, "description").text = f"Read our latest guide on {clean_title}."
                
                ET.SubElement(item, "enclosure", url=DEFAULT_IMAGE, type="image/png", length="0")
                
    except Exception as e:
        print(f"Error parsing sitemap: {e}")

output_tree = ET.ElementTree(rss_root)
ET.indent(output_tree, space="    ")
output_tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
