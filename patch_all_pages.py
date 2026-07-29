name: Patch Monetization Slots

on:
  push:
    branches:
      - main
  workflow_dispatch:

permissions:
  contents: write

jobs:
  patch-html:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Patch HTML files
        run: |
          python <<'PY'
          import os

          TOP_SLOT = '<div id="ad-top-slot" style="text-align:center; margin:20px 0;"></div>\n'
          BOT_SLOT = '<div id="ad-bottom-slot" style="text-align:center; margin:20px 0;"></div>\n'
          SCRIPT_LINK = '<script src="/monetization.js"></script>\n'

          for filename in os.listdir('.'):
              if filename.endswith('.html') and filename != 'index.html':
                  with open(filename, 'r', encoding='utf-8') as f:
                      content = f.read()

                  modified = False

                  if '<div id="ad-bottom-slot"></div>' in content:
                      content = content.replace('<div id="ad-bottom-slot"></div>', '')
                      modified = True

                  if '<div id="ad-bottom-slot" style="text-align:center; margin:20px 0;"></div>' in content:
                      content = content.replace('<div id="ad-bottom-slot" style="text-align:center; margin:20px 0;"></div>', '')
                      modified = True

                  if '<script src="/monetization.js"></script>' in content:
                      content = content.replace('<script src="/monetization.js"></script>', '')
                      modified = True

                  if '</h1>' in content and 'ad-top-slot' not in content:
                      content = content.replace('</h1>', f'</h1>\n{TOP_SLOT}')
                      modified = True

                  if '</body>' in content and 'ad-bottom-slot' not in content:
                      content = content.replace('</body>', f'{BOT_SLOT}{SCRIPT_LINK}</body>')
                      modified = True

                  if modified:
                      with open(filename, 'w', encoding='utf-8') as f:
                          f.write(content)
                      print(f"Patched slots into: {filename}")

          print("Success! All plant pages successfully configured for Top and Bottom monetization layout!")
          PY

      - name: Commit changes
        run: |
          if git diff --quiet; then
            echo "No changes detected."
            exit 0
          fi

          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

          git add *.html
          git commit -m "Automatically patch monetization slots"
          git push
