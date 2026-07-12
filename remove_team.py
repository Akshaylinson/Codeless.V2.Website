import os, re, glob

# The exact "Our team" col block to remove from the megamenu
TEAM_BLOCK = re.compile(
    r'\s*<div class="col-xl-4 col-lg-4">\s*'
    r'<a class="iconbox_block_2" href="team\.html">.*?</a>\s*'
    r'</div>',
    re.DOTALL
)

html_files = glob.glob('*.html')
for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'team.html' in content and 'iconbox_title' in content:
        new_content = TEAM_BLOCK.sub('', content)
        if new_content != content:
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated: {fname}')
        else:
            print(f'No match found: {fname}')
    else:
        print(f'Skipped: {fname}')
