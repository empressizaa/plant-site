import os

# Get all HTML files in the main folder
files = [f for f in os.listdir('.') if f.endswith('.html')]

for filename in files:
    if filename == 'index.html':
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check if the placeholder example domain exists in the file
    if '://example.com' in content:
        print(f"Fixing domain in: {filename}")
        # Swap out example.com for your real, clean live domain
        content = content.replace('://example.com', 'theplantmatrix.com')
        
        # Save the updated file back to the repository
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

print("All files scanned and domains corrected successfully!")
