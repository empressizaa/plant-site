import os
import xml.etree.ElementTree as ET
from datetime import datetime

# CONFIGURATION
DOMAIN = "https://theplantmatrix.com"
DEFAULT_IMAGE = "https://theplantmatrix.com/images/default-share-graphic.png" 

rss_root = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss_root, "channel")

ET.SubElement(channel, "title").text = "The Plant Matrix Feed"
ET.SubElement(channel, "link").text = DOMAIN
ET.SubElement(channel, "description").text = "Automated plant care updates"

# Scan current directory for your article files automatically
for file in os.listdir("."):
    if file.endswith(".html") and file != "index.html":
        # Formulate clean title from the filename
        clean_title = file.replace(".html", "").replace("-", " ").title()
        page_link = f"{DOMAIN}/{file.replace('.html', '')}"
        
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = clean_title
        ET.SubElement(item, "link").text = page_link
        ET.SubElement(item, "description").text = f"Read our latest guide on {clean_title}."
        
        # Injects the mandatory image data Pinterest requires
        ET.SubElement(item, "enclosure", url=DEFAULT_IMAGE, type="image/png", length="0")

# Write out the new compiled feed.xml
tree = ET.ElementTree(rss_root)
ET.indent(tree, space="    ")
tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
print("feed.xml generated successfully via script configuration.")
