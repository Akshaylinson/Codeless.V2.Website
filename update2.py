import glob, os

REPLACEMENTS = [
    # Footer address
    ('>India</span>', '>Thrissur, India</span>'),
    # Footer phone icon link
    ('href="callto:+918921403821"', 'href="callto:+917034607887"'),
    # Footer phone text link (old href still had original value)
    ('href="callto:+(1)12304528597">+91 89214 03821', 'href="callto:+917034607887">+91 7034607887'),
    # Any remaining old phone display text
    ('+91 89214 03821', '+91 7034607887'),
    # Contact page office phones
    ('+91 89214 03821', '+91 7034607887'),
]

for fn in glob.glob('*.html'):
    with open(fn, encoding='utf-8') as f:
        c = f.read()
    orig = c
    for old, new in REPLACEMENTS:
        c = c.replace(old, new)
    if c != orig:
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(c)
        print('Updated:', fn)
    else:
        print('No change:', fn)
