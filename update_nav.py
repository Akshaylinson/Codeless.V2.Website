import re

BASE = r"E:\Templates for webpage\aivora-ai-agency-technology-html-template-2025-10-24-13-16-46-utc\aivora-html-package\Aivora"

# Each file has a different "active" class on one of the 4 nav items
# We'll define the nav per file

def make_desktop_nav(active):
    items = {
        'home': '<li class="menu-item-has-children{a}"><a href="index.html"><span>Home</span></a></li>'.format(
            a=' active' if active == 'home' else ''),
        'about': '<li class="{a}"><a href="about.html"><span>About Us</span></a></li>'.format(
            a='active' if active == 'about' else ''),
        'services': '<li class="{a}"><a href="service.html"><span>Services</span></a></li>'.format(
            a='active' if active == 'services' else ''),
        'contact': '<li class="{a}"><a href="contact.html"><span>Contact Us</span></a></li>'.format(
            a='active' if active == 'contact' else ''),
    }
    return """                            <ul>
                                {home}
                                {about}
                                {services}
                                {contact}
                            </ul>""".format(**items)

def make_mobile_nav(active):
    items = {
        'home': '<li class="menu-item{a}"><a href="index.html"><span>Home</span></a></li>'.format(
            a=' active' if active == 'home' else ''),
        'about': '<li class="{a}"><a href="about.html"><span>about us</span></a></li>'.format(
            a='active' if active == 'about' else ''),
        'services': '<li class="{a}"><a href="service.html"><span>services</span></a></li>'.format(
            a='active' if active == 'services' else ''),
        'contact': '<li class="{a}"><a href="contact.html"><span>Contact Us</span></a></li>'.format(
            a='active' if active == 'contact' else ''),
    }
    return """                                <ul class="xb-menu-primary clearfix">
                                    {home}
                                    {about}
                                    {services}
                                    {contact}
                                </ul>""".format(**items)

files = {
    'index.html': 'home',
    'about.html': 'about',
    'service.html': 'services',
    'contact.html': 'contact',
}

for filename, active in files.items():
    path = BASE + '\\' + filename
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace desktop nav <ul>...</ul> inside main-menu
    # Pattern: the <ul> inside <nav class="main-menu collapse navbar-collapse">
    desktop_pattern = r'(<nav class="main-menu collapse navbar-collapse">\s*)<ul>.*?</ul>(\s*</nav>)'
    desktop_replacement = r'\g<1>' + make_desktop_nav(active) + r'\2'
    new_content = re.sub(desktop_pattern, desktop_replacement, content, flags=re.DOTALL)

    # Replace mobile nav <ul class="xb-menu-primary clearfix">...</ul>
    mobile_pattern = r'<ul class="xb-menu-primary clearfix">.*?</ul>(\s*</nav>)'
    mobile_replacement = make_mobile_nav(active) + r'\1'
    new_content = re.sub(mobile_pattern, mobile_replacement, new_content, flags=re.DOTALL)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Updated: {filename}")

print("Done!")
