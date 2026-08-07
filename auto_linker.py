import os
import re

STOP_WORDS = {"how", "often", "to", "for", "in", "after", "the", "a", "and", "of", "on", "with", "at", "is", "zone"}
SIMILARITY_THRESHOLD = 0.70

pages = []

print("Scanning files...")
for filename in os.listdir("."):
    if not filename.endswith(".html") or filename.lower() == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

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
print(f"Found {total} files. Beginning automatic sweep and clean...")

for page in pages:
    with open(page["filename"], "r", encoding="utf-8") as f:
        html = f.read()

    # MASS CLEANUP: Strips out ALL old comment blocks and double layout classes automatically
    html = re.sub(r'<!-- RELATED GUIDES START -->.*?<!-- RELATED GUIDES END -->', '', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<div class="related-guides"[\s\S]*?</div>', '', html, flags=re.DOTALL | re.IGNORECASE)

    candidates = []
    for other in pages:
        if other["filename"] == page["filename"]:
            continue
        overlap = len(page["keywords"].intersection(other["keywords"]))
        candidates.append((overlap, other))

    candidates.sort(key=lambda x: (-x, x["title"]))

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
            
            if (len(shared_words) / smaller_set_size) >= SIMILARITY_THRESHOLD:
                is_duplicate_idea = True
                break
                
        if not is_duplicate_idea:
            selected_guides.append(item)
            
    if len(selected_guides) < min(5, len(candidates)):
        for score, item in candidates:
            if len(selected_guides) >= min(5, len(candidates)):
                break
            if item not in selected_guides:
                selected_guides.append(item)

    links_html = ""
    for target in selected_guides:
        links_html += f'\n        <li style="margin-bottom:8px;"><a href="/{target["slug"]}.html" style="color:#2e7d32;text-decoration:none;font-weight:bold;">{target["title"]}</a></li>'

    related_block = f"""\n<!-- RELATED GUIDES START -->
<div class="related-guides" style="clear:both;display:block;width:100%;margin-top:40px;padding:20px;background:#f1f8e9;border-top:2px solid #4CAF50;border-radius:6px;box-sizing:border-box;">
    <h3 style="margin-top:0;color:#2e7d32;">Recommended Plant Guides</h3>
    <ul style="padding-left:20px;margin-bottom:0;">{links_html}
    </ul>
</div>
<!-- RELATED GUIDES END -->\n"""

    if re.search(r'<footer\b', html, flags=re.IGNORECASE):
        html = re.sub(r'(<footer\b[^>]*>)', related_block + r'\1', html, count=1, flags=re.IGNORECASE)
    else:
        html = re.sub(r'(</body>)', related_block + r'\1', html, count=1, flags=re.IGNORECASE)

    with open(page["filename"], "w", encoding="utf-8") as f:
        f.write(html)

print("Finished automatic cleanup and linking.")
