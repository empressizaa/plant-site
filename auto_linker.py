import os
import re

# Stop words to ignore when calculating keyword relevance
STOP_WORDS = {"how", "often", "to", "for", "in", "after", "the", "a", "and", "of", "on", "with", "at", "is", "zone"}
SIMILARITY_THRESHOLD = 0.70  # Prevents repetitive topics from stacking up together

pages = []

print("Scanning clean files...")
for filename in os.listdir("."):
    if not filename.endswith(".html") or filename.lower() == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    # Extract the H1 title to determine the topic
    match = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        continue

    title = re.sub(r"<[^>]+>", "", match.group(1)).strip()
    words = re.findall(r"\b\w+\b", title.lower())
    keywords = {word for word in words if word not in STOP_WORDS and not word.isdigit()}

    pages.append({
        "filename": filename,
        "slug": filename[:-5],
        "title": title,
        "keywords": keywords
    })

total = len(pages)
print(f"Found {total} clean articles. Generating smart recommendations...")

for page in pages:
    with open(page["filename"], "r", encoding="utf-8") as f:
        html = f.read()

    # Calculate match scores based on overlapping title words
    candidates = []
    for other in pages:
        if other["filename"] == page["filename"]:
            continue
        overlap = len(page["keywords"].intersection(other["keywords"]))
        candidates.append((overlap, other))

    # Sort: highest keyword match first, then alphabetically by title for stability
    candidates.sort(key=lambda x: (-x[0], x[1]["title"]))

    # Pick up to 5 unique guides while aggressively filtering out repetitive topics
    selected_guides = []
    for score, item in candidates:
        if len(selected_guides) >= min(5, len(candidates)):
            break
            
        is_duplicate_idea = False
        for selected_item in selected_guides:
            if not item["keywords"] or not selected_item["keywords"]:
                continue
            shared_words = item["keywords"].intersection(selected_item["keywords"])
            smaller_set_size = min(len(item["keywords"]), len(selected_item["keywords"]))
            
            # Skip if titles share more than 70% of the same words
            if (len(shared_words) / smaller_set_size) >= SIMILARITY_THRESHOLD:
                is_duplicate_idea = True
                break
                
        if not is_duplicate_idea:
            selected_guides.append(item)
            
    # Fallback padding to make sure we hit the target link count if filtering was tight
    if len(selected_guides) < min(5, len(candidates)):
        for score, item in candidates:
            if len(selected_guides) >= min(5, len(candidates)):
                break
            if item not in selected_guides:
                selected_guides.append(item)

    # Build the clean HTML link block markup
    links_html = ""
    for target in selected_guides:
        links_html += f'\n        <li style="margin-bottom:12px;"><a href="/{target["slug"]}.html" style="color:#2e7d32;text-decoration:none;font-weight:bold;">{target["title"]}</a></li>'

    related_block = f"""\n<!-- RELATED GUIDES START -->
<div class="related-guides" style="clear:both;display:block;width:100%;margin-top:40px;margin-bottom:40px;padding:25px;background:#f1f8e9;border-top:3px solid #4CAF50;border-radius:8px;box-sizing:border-box;font-family:sans-serif;">
    <h3 style="margin-top:0;margin-bottom:18px;color:#2e7d32;font-size:20px;">Recommended Plant Guides</h3>
    <ul style="padding-left:20px;margin-bottom:0;line-height:1.5;">{links_html}
    </ul>
</div>
<!-- RELATED GUIDES END -->\n"""

    # TARGETED POSITIONING: Drop the block cleanly right above your text footer links
    if re.search(r'About Us\s*\|\s*Privacy Policy', html, flags=re.IGNORECASE):
        # Insert perfectly directly above the line that contains your About Us link container
        html = re.sub(r'(<div[^>]*>\s*<a[^>]*>About Us)', lambda m: related_block + m.group(1), html, count=1, flags=re.IGNORECASE)
    elif re.search(r'<footer\b', html, flags=re.IGNORECASE):
        html = re.sub(r'(<footer\b[^>]*>)', related_block + r'\1', html, count=1, flags=re.IGNORECASE)
    else:
        html = re.sub(r'(</body>)', related_block + r'\1', html, count=1, flags=re.IGNORECASE)

    with open(page["filename"], "w", encoding="utf-8") as f:
        f.write(html)

print("Successfully injected all smart contextual blocks.")
