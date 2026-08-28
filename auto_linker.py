import os
import re
# ============================================================
# PLANT MATRIX AUTO LINKER
# ============================================================
# Behavior:
# 1. Only links to HTML files that actually exist.
# 2. index.html is never processed.
# 3. Calculator pages are kept but do NOT receive article
#    recommendation blocks.
# 4. Calculator pages are NOT used as recommended guides.
# 5. Existing related-guide blocks are completely removed first.
# 6. Deleted/old article URLs cannot be recreated by this script.
# ============================================================
# ------------------------------------------------------------
# CALCULATORS TO KEEP
# ------------------------------------------------------------
CALCULATOR_FILES = {
    "lawn-fertilizer-calculator.html",
    "plant-population-density-calculator.html",
    "plant-spacing-calculator.html",
    "rainwater-collection-calculator.html",
    "raised-bed-garden-soil-calculator.html",
}
# ------------------------------------------------------------
# STOP WORDS
# ------------------------------------------------------------
STOP_WORDS = {
    "how",
    "often",
    "to",
    "for",
    "in",
    "after",
    "the",
    "a",
    "an",
    "and",
    "of",
    "on",
    "with",
    "at",
    "is",
    "are",
    "was",
    "were",
    "zone",
    "water",
    "watering",
    "when",
    "should",
    "you",
    "your",
    "frequently",
    "can",
    "do",
    "does",
    "doesnt",
    "what",
    "why",
    "which",
    "this",
    "that",
    "these",
    "those",
    "plant",
    "plants",
}
SIMILARITY_THRESHOLD = 0.50
# ------------------------------------------------------------
# FIND ARTICLE PAGES
# ------------------------------------------------------------
pages = []
print("Scanning existing HTML files...")
for filename in os.listdir("."):
    if not filename.lower().endswith(".html"):
        continue
    if filename.lower() == "index.html":
        continue
    # --------------------------------------------------------
    # IMPORTANT:
    # Calculators are NOT included in recommendation targets.
    # They remain on the site but are not treated as guides.
    # --------------------------------------------------------
    if filename in CALCULATOR_FILES:
        continue
    try:
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"SKIP: Could not read {filename}: {e}")
        continue
    # --------------------------------------------------------
    # FIND H1
    # --------------------------------------------------------
    match = re.search(
        r"<h1[^>]*>(.*?)</h1>",
        html,
        flags=re.IGNORECASE | re.DOTALL
    )
    if not match:
        print(f"SKIP: No H1 found in {filename}")
        continue
    title = re.sub(
        r"<[^>]+>",
        "",
        match.group(1)
    ).strip()
    # --------------------------------------------------------
    # CREATE KEYWORDS
    # --------------------------------------------------------
    words = re.findall(
        r"\b\w+\b",
        title.lower()
    )
    keywords = {
        word
        for word in words
        if (
            word not in STOP_WORDS
            and not word.isdigit()
            and len(word) > 2
        )
    }
    pages.append({
        "filename": filename,
        "slug": filename[:-5],
        "title": title,
        "keywords": keywords
    })
total = len(pages)
print(
    f"Found {total} article pages available for recommendations."
)
# ------------------------------------------------------------
# PROCESS EACH ARTICLE
# ------------------------------------------------------------
for page in pages:
    filename = page["filename"]
    try:
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"ERROR reading {filename}: {e}")
        continue
    # --------------------------------------------------------
    # REMOVE OLD AUTO-GENERATED RELATED BLOCK
    # --------------------------------------------------------
    html = re.sub(
        r'<!-- RELATED GUIDES START -->.*?<!-- RELATED GUIDES END -->',
        '',
        html,
        flags=re.DOTALL | re.IGNORECASE
    )
    # --------------------------------------------------------
    # REMOVE OLD RELATED-GUIDES DIVS
    # --------------------------------------------------------
    html = re.sub(
        r'<div[^>]*class=["\']related-guides["\'][^>]*>.*?</div>',
        '',
        html,
        flags=re.DOTALL | re.IGNORECASE
    )
    # --------------------------------------------------------
    # FIND POSSIBLE RECOMMENDATIONS
    # --------------------------------------------------------
    candidates = []
    for other in pages:
        if other["filename"] == page["filename"]:
            continue
        overlap = len(
            page["keywords"].intersection(
                other["keywords"]
            )
        )
        candidates.append(
            (overlap, other)
        )
    # --------------------------------------------------------
    # SORT BY RELEVANCE
    # --------------------------------------------------------
    candidates.sort(
        key=lambda x: (
            -x[0],
            x[1]["title"].lower()
        )
    )
    # --------------------------------------------------------
    # SELECT UP TO 5 DIVERSE GUIDES
    # --------------------------------------------------------
    selected_guides = []
    for score, item in candidates:
        if len(selected_guides) >= min(5, len(candidates)):
            break
        is_duplicate_idea = False
        for selected_item in selected_guides:
            if (
                not item["keywords"]
                or not selected_item["keywords"]
            ):
                continue
            shared_words = (
                item["keywords"]
                .intersection(
                    selected_item["keywords"]
                )
            )
            smaller_set_size = min(
                len(item["keywords"]),
                len(selected_item["keywords"])
            )
            if smaller_set_size == 0:
                continue
            similarity = (
                len(shared_words)
                / smaller_set_size
            )
            if similarity >= SIMILARITY_THRESHOLD:
                is_duplicate_idea = True
                break
        if not is_duplicate_idea:
            selected_guides.append(item)
    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------
    if len(selected_guides) < min(5, len(candidates)):
        for score, item in candidates:
            if len(selected_guides) >= min(5, len(candidates)):
                break
            if item not in selected_guides:
                selected_guides.append(item)
    # --------------------------------------------------------
    # BUILD LINKS
    # --------------------------------------------------------
    links_html = ""
    for target in selected_guides:
        # Extra safety:
        # Only link to a file that still exists.
        if not os.path.isfile(target["filename"]):
            continue
        links_html += (
            '\n        <li style="margin-bottom:12px;">'
            f'<a href="/{target["slug"]}" '
            'style="color:#2e7d32;'
            'text-decoration:none;'
            'font-weight:bold;">'
            f'{target["title"]}'
            '</a></li>'
        )
    # --------------------------------------------------------
    # IF NO VALID TARGETS EXIST
    # DON'T CREATE AN EMPTY RECOMMENDATION BOX
    # --------------------------------------------------------
    if not links_html:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(
            f"CLEANED: {filename} "
            "(no recommendation targets)"
        )
        continue
    # --------------------------------------------------------
    # CREATE RELATED GUIDES BLOCK
    # --------------------------------------------------------
    related_block = f"""
<!-- RELATED GUIDES START -->
<div class="related-guides" style="clear:both;display:block;width:100%;margin-top:40px;margin-bottom:40px;padding:25px;background:#f1f8e9;border-top:3px solid #4CAF50;border-radius:8px;box-sizing:border-box;font-family:sans-serif;">
    <h3 style="margin-top:0;margin-bottom:18px;color:#2e7d32;font-size:20px;">
        Recommended Plant Guides
    </h3>
    <ul style="padding-left:20px;margin-bottom:0;line-height:1.5;">
        {links_html}
    </ul>
</div>
<!-- RELATED GUIDES END -->
"""
    # --------------------------------------------------------
    # INSERT BEFORE FOOTER
    # --------------------------------------------------------
    if re.search(
        r'(<footer\b[^>]*>)',
        html,
        flags=re.IGNORECASE
    ):
        html = re.sub(
            r'(<footer\b[^>]*>)',
            related_block + r'\1',
            html,
            count=1,
            flags=re.IGNORECASE
        )
    # --------------------------------------------------------
    # OTHERWISE INSERT BEFORE BODY
    # --------------------------------------------------------
    else:
        html = re.sub(
            r'(</body>)',
            related_block + r'\1',
            html,
            count=1,
            flags=re.IGNORECASE
        )
    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(
        f"UPDATED: {filename} "
        f"→ {len(selected_guides)} recommendations"
    )
# ------------------------------------------------------------
# FINAL SAFETY CHECK
# ------------------------------------------------------------
print("")
print("==============================================")
print("AUTO LINKER COMPLETE")
print("==============================================")
print(f"Article pages processed: {total}")
print("Calculators excluded from recommendation system:")
for calculator in sorted(CALCULATOR_FILES):
    print(f"  KEEP: {calculator}")
print("==============================================")
