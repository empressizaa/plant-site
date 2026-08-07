import os
import re
import random

# -------------------------------------------------
# Find all article pages (.html except index.html)
# -------------------------------------------------
pages = []

for filename in os.listdir("."):
    if not filename.endswith(".html"):
        continue

    if filename.lower() == "index.html":
        continue

    with open(filename, "r", encoding="utf-8") as f:
        html = f.read()

    match = re.search(
        r"<h1[^>]*>(.*?)</h1>",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )

    if not match:
        print(f"Skipping {filename} (no H1)")
        continue

    title = re.sub(r"<[^>]+>", "", match.group(1)).strip()

    pages.append({
        "filename": filename,
        "slug": filename[:-5],
        "title": title
    })

total = len(pages)

if total < 2:
    print("Not enough pages to create links.")
    exit()

print(f"Found {total} articles.")

# -------------------------------------------------
# Shuffle once
# -------------------------------------------------
random.shuffle(pages)

# -------------------------------------------------
# Process every article
# -------------------------------------------------
for i, page in enumerate(pages):

    with open(page["filename"], "r", encoding="utf-8") as f:
        html = f.read()

    # 1. CLEANUP NEW BLOCKS: Safely handle updates using target comment markers
    html = re.sub(
        r'<!-- RELATED GUIDES START -->.*?<!-- RELATED GUIDES END -->',
        '',
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 2. CLEANUP OLD BLOCKS: Flexible class-based sweeping without brittle <h3> dependencies
    html = re.sub(
        r'<div\s+class="related-guides"[\s\S]*?(?=<footer|</body>)',
        '',
        html,
        flags=re.IGNORECASE
    )

    # Number of links
    link_count = min(5, total - 1)

    related = []

    for n in range(1, link_count + 1):
        related.append(
            pages[(i + n) % total]
        )

    links = ""

    for item in related:
        links += f'''
<li style="margin-bottom:8px;">
<a href="/{item["slug"]}.html"
style="color:#2e7d32;text-decoration:none;font-weight:bold;">
{item["title"]}
</a>
</li>
'''

    related_html = f"""

<!-- RELATED GUIDES START -->

<div class="related-guides" style="
clear:both;
display:block;
width:100%;
margin-top:40px;
padding:20px;
background:#f1f8e9;
border-top:2px solid #4CAF50;
border-radius:6px;
box-sizing:border-box;
">

<h3 style="
margin-top:0;
color:#2e7d32;
">
Recommended Plant Guides
</h3>

<ul style="
padding-left:20px;
margin-bottom:0;
">

{links}

</ul>

</div>

<!-- RELATED GUIDES END -->

"""

    inserted = False

    # Preferred location: Cleanly capture the footer and prepend the block
    if re.search(r"<footer\s*[^>]*>", html, re.IGNORECASE):
        html = re.sub(
            r"(<footer\s*[^>]*>)",
            related_html + r"\1",
            html,
            count=1,
            flags=re.IGNORECASE
        )
        inserted = True

    # Second choice: Inside the closing article wrapper container
    elif re.search(r"</article\s*>", html, re.IGNORECASE):
        html = re.sub(
            r"</article\s*>",
            related_html + "</article>",
            html,
            count=1,
            flags=re.IGNORECASE
        )
        inserted = True

    # Third choice: Right above closing body element
    elif re.search(r"</body\s*>", html, re.IGNORECASE):
        html = re.sub(
            r"</body\s*>",
            related_html + "</body>",
            html,
            count=1,
            flags=re.IGNORECASE
        )
        inserted = True

    # Fallback
    if not inserted:
        html += related_html

    with open(page["filename"], "w", encoding="utf-8") as f:
        f.write(html)

print(f"✅ Successfully linked all {total} articles with a standardized layout.")
