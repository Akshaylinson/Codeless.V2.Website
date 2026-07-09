import re

BASE = r"E:\Templates for webpage\aivora-ai-agency-technology-html-template-2025-10-24-13-16-46-utc\aivora-html-package\Aivora"

desktop_nav = """                            <ul>
                                <li class="menu-item-has-children"><a href="index.html"><span>Home</span></a></li>
                                <li class=""><a href="about.html"><span>About Us</span></a></li>
                                <li class=""><a href="service.html"><span>Services</span></a></li>
                                <li class=""><a href="contact.html"><span>Contact Us</span></a></li>
                            </ul>"""

mobile_nav = """                                <ul class="xb-menu-primary clearfix">
                                    <li class="menu-item"><a href="index.html"><span>Home</span></a></li>
                                    <li class=""><a href="about.html"><span>about us</span></a></li>
                                    <li class=""><a href="service.html"><span>services</span></a></li>
                                    <li class=""><a href="contact.html"><span>Contact Us</span></a></li>
                                </ul>"""

files = ['service-details.html', 'career.html', 'project.html', 'project-details.html', 'blog.html', 'blog-details.html']

for filename in files:
    path = BASE + '\\' + filename
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(
        r'(<nav class="main-menu collapse navbar-collapse">\s*)<ul>.*?</ul>(\s*</nav>)',
        lambda m: m.group(1) + desktop_nav + m.group(2),
        content, flags=re.DOTALL
    )
    new_content = re.sub(
        r'<ul class="xb-menu-primary clearfix">.*?</ul>(\s*</nav>)',
        mobile_nav + r'\1',
        new_content, flags=re.DOTALL
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Updated:', filename)

print('Done!')
