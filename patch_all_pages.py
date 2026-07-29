import os

# Define our clean layout slots
TOP_SLOT = '<div id="ad-top-slot" style="text-align:center; margin:20px 0;"></div>\n'
BOT_SLOT = '<div id="ad-bottom-slot" style="text-align:center; margin:20px 0;"></div>\n'
SCRIPT_LINK = '<script src="/monetization.js"></script>\n'

for filename in os.listdir('.'):
if filename.endswith('.html') and filename != 'index.html':
with open(filename, 'r', encoding='utf-8') as f:
content = f.read()

modified = False

# 1. CLEAN UP PREVIOUS LAYOUTS: Prevents stacking double targets
if '<div id="ad-bottom-slot"></div>' in content:
content = content.replace('<div id="ad-bottom-slot"></div>', '')
modified = True
if '<div id="ad-bottom-slot" style="text-align:center; margin:20px 0;"></div>' in content:
content = content.replace('<div id="ad-bottom-slot" style="text-align:center; margin:20px 0;"></div>', '')
modified = True
if '<script src="/monetization.js"></script>' in content:
content = content.replace('<script src="/monetization.js"></script>', '')
modified = True

# 2. INJECT TOP SLOT: Right below the main page title header
if '</h1>' in content and 'ad-top-slot' not in content:
content = content.replace('</h1>', f'</h1>\n{TOP_SLOT}')
modified = True

# 3. INJECT BOTTOM SLOT: Safely right above the closing body layout tag
if '</body>' in content and 'ad-bottom-slot' not in content:
content = content.replace('</body>', f'{BOT_SLOT}{SCRIPT_LINK}</body>')
modified = True

# Save files cleanly back to your project directory
if modified:
with open(filename, 'w', encoding='utf-8') as f:
f.write(content)
print(f"Patched slots into: {filename}")

print("\nSuccess! All plant pages successfully configured for Top and Bottom monetization layout!")
