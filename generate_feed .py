import os
import xml.etree.ElementTree as ET

def generate_feed():
    sitemap_path = "sitemap.xml"
    feed_path = "feed.xml"
    
    # Referencing the file directly by its filename
    logo_file = "logo.png"
    
    # 1. Initialize the RSS structure
    rss_root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss_root, "channel")
    
    # 2. Add required Channel Metadata
    title = ET.SubElement(channel, "title")
    title.text = "The Plant Matrix Feed"
    
    link = ET.SubElement(channel, "link")
    link.text = "https://theplantmatrix.com"
    
    description = ET.SubElement(channel, "description")
    description.text = "Automated plant care updates"
    
    # 3. Parse Sitemap and Append Individual Post Items
    if os.path.exists(sitemap_path):
        tree = ET.parse(sitemap_path)
        sitemap_root = tree.getroot()
        
        # Namespace map handling for sitemaps
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        for url_tag in sitemap_root.findall('ns:url', ns):
            loc_tag = url_tag.find('ns:loc', ns)
            if loc_tag is not None and loc_tag.text:
                url_text = loc_tag.text
                
                # Filter out the homepage or non-guide URLs if necessary
                if url_text in ("https://theplantmatrix.com", "https://theplantmatrix.com/"):
                    continue
                
                # Generate clean presentation values from the URL path slug
                slug = url_text.replace("https://theplantmatrix.com/", "").replace(".html", "")
                clean_title = slug.replace("-", " ").title()
                
                # Append a dedicated item node block for each entry
                item = ET.SubElement(channel, "item")
                
                item_title = ET.SubElement(item, "title")
                item_title.text = clean_title
                
                item_link = ET.SubElement(item, "link")
                item_link.text = url_text
                
                item_desc = ET.SubElement(item, "description")
                item_desc.text = f"Read our latest guide on {clean_title}."
    
    # 4. Write the output file with the XML declaration header byte prefix
    feed_tree = ET.ElementTree(rss_root)
    with open(feed_path, "wb") as f:
        # Fixed: Combined the byte string declaration onto a single line using standard escape sequences (\n)
        f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
        feed_tree.write(f, encoding="utf-8", xml_declaration=False)

if __name__ == "__main__":
    generate_feed()
