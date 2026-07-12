import os, re, glob

# Remove the Project details col block from the megamenu
PROJECT_DETAILS_BLOCK = re.compile(
    r'\s*<div class="col-xl-4 col-lg-4">\s*'
    r'<a class="iconbox_block_2" href="project-details\.html">.*?</a>\s*'
    r'</div>',
    re.DOTALL
)

html_files = glob.glob('*.html')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = PROJECT_DETAILS_BLOCK.sub('', content)
    if new_content != content:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated: {fname}')
    else:
        print(f'No match: {fname}')
